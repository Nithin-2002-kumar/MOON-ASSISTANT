import logging
import threading
import time
import queue
import speech_recognition as sr
import pyttsx3

from core import config

log = logging.getLogger("moon.speech")
log.setLevel(logging.INFO)


class SpeechEngine:
    """
    Wrapper around pyttsx3 (TTS) and SpeechRecognition (STT).
    - listen() blocks for a single utterance and returns lowercase text (or '' on failure).
    - say() speaks asynchronously (non-blocking).
    """

    def __init__(self, tts_rate: int = 170, voice_index: int = 0):
        # TTS
        self.engine = pyttsx3.init()
        try:
            voices = self.engine.getProperty("voices")
            if voices and len(voices) > voice_index:
                self.engine.setProperty("voice", voices[voice_index].id)
        except Exception:
            log.exception("Failed to set voice (continuing).")
        self.engine.setProperty("rate", tts_rate)

        # STT
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True

        # Non-blocking TTS queue
        self._speak_queue = queue.Queue()
        self._speaker_thread = threading.Thread(target=self._speaker_loop, daemon=True)
        self._speaker_thread.start()

    def _speaker_loop(self):
        while True:
            text = self._speak_queue.get()
            if text is None:
                break
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                log.exception("TTS failed for text: %s", text)
            time.sleep(0.05)

    def say(self, text: str):
        """Queue text to speak (non-blocking)."""
        if not text:
            return
        log.info("TTS queue: %s", text)
        self._speak_queue.put(text)

    def listen(self, timeout: float = 6.0, phrase_time_limit: float = 10.0) -> str:
        """
        Listen once and return recognized text (lowercased). Returns '' on failure.
        """
        try:
            with sr.Microphone() as src:   # fresh microphone context
                self.recognizer.adjust_for_ambient_noise(src, duration=0.8)
                audio = self.recognizer.listen(src, timeout=timeout, phrase_time_limit=phrase_time_limit)

            try:
                text = self.recognizer.recognize_google(audio)
                log.info("STT recognized: %s", text)
                return text.lower()
            except sr.UnknownValueError:
                log.debug("STT unknown value")
                return ""
            except sr.RequestError:
                log.warning("STT request error (service may be down)")
                return ""
        except sr.WaitTimeoutError:
            log.debug("STT wait timeout")
            return ""
        except Exception:
            log.exception("Unexpected STT error")
            return ""

    def stop(self):
        """Shut down speaker thread."""
        self._speak_queue.put(None)
        self._speaker_thread.join(timeout=1.0)
