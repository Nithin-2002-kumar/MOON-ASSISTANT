import logging
from core import config
from core.speech import SpeechEngine
from core.nlp import IntentProcessor
from core.vision import VisionSystem
from core.memory import Memory
from ui.hud import MoonHUD

# skills
from skills.apps import AppManager
from skills.browser import BrowserManager
from skills.emailer import Emailer
from skills.reminders import ReminderManager
from skills.weather import Weather
from skills.grok import ask_grok

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("moon.main")


class MoonAssistant:
    """Main orchestrator that glues NLP, speech, vision, skills, and UI."""

    def __init__(self):
        # core
        self.speech = SpeechEngine()
        self.nlp = IntentProcessor()
        self.vision = VisionSystem()
        self.memory = Memory()
        self.wake_word = "hey moon"

        # skills
        self.apps = AppManager()
        self.browser = BrowserManager()
        self.emailer = Emailer()
        self.reminders = ReminderManager(speaker=self.speech)
        self.weather = Weather()

        # UI
        self.hud = MoonHUD(self)

    # ------------------ main logic ------------------ #
    def process_command(self, text: str):
        """Take raw command text, classify intent, and execute skill."""
        if not text:
            self._respond("I didn't catch that.")
            return

        intent, confidence = self.nlp.predict_intent(text)
        if not intent or confidence < 0.4:
            reply = self.chatgpt.ask(text)
            self._respond(reply)
            return

        log.info("Intent: %s (conf %.2f)", intent, confidence)

        if intent == "time" or intent == "date":
            reply = self.nlp.get_time_date()

        elif intent == "open":
            app_name = text.replace("open", "").strip()
            reply = self.apps.open_app(app_name)

        elif intent == "close":
            app_name = text.replace("close", "").strip()
            reply = self.apps.close_app(app_name)

        elif intent == "search":
            reply = self.browser.search(text.replace("search", "").strip())

        elif intent == "reminder":
            reply = self.reminders.add_reminder("Reminder from command", 10)

        elif intent == "screenshot":
            reply = "Screenshot feature not yet implemented."

        elif intent == "email":
            reply = self.emailer.send_email("test@example.com", "Test Subject", "This is a test email.")

        elif intent == "weather":
            reply = self.weather.get_weather("London")

        elif intent == "scan" or intent == "object_detection":
            frame = self._dummy_frame()
            objs = self.vision.detect_objects(frame)
            reply = f"Detected objects: {objs}" if objs else "No objects found."

        elif intent == "face_recognition":
            frame = self._dummy_frame()
            faces = self.vision.recognize_faces(frame)
            reply = f"Detected faces: {faces}" if faces else "No faces found."

        elif intent == "color_detection":
            frame = self._dummy_frame()
            reply = self.vision.detect_colors(frame, 50, 50)

        elif intent == "llm":
            reply = ask_grok(text)

        else:
            reply = f"I understood intent '{intent}', but no action is linked."

        self._respond(reply)

    # ------------------ helpers ------------------ #

    def _respond(self, text: str):
        if not text:
            log.warning("No reply generated for command.")
            text = "I couldn’t figure out a response."
        log.info("Assistant reply: %s", text)
        self.speech.say(text)
        self.hud.update_status(text)
        self.hud.log(f"Assistant: {text}")


    def _dummy_frame(self):
        """Generate blank frame for placeholder vision tests."""
        import numpy as np
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def run(self):
        self.hud.run()


if __name__ == "__main__":
    assistant = MoonAssistant()
    assistant.run()
