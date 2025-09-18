import logging
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

log = logging.getLogger("moon.nlp")
log.setLevel(logging.INFO)


class IntentProcessor:
    """
    Lightweight intent processor using TF-IDF + linear SVC trained on a small
    command list. Returns simple responses for time/date queries.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = SVC(kernel="linear", probability=True)
        self._train_basic_intents()

    def _train_basic_intents(self):
        commands = [
            "open notepad", "open browser", "search web", "set reminder", "tell time", "tell date",
            "take screenshot", "send email", "check weather", "scan room", "detect objects",
            "recognize face", "analyze sentiment", "detect emotion", "close notepad", "type in notepad",
            "navigate browser", "detect gender", "ask llm", "who am i", "classify entities", "detect colors"
        ]
        labels = [
            "open", "open", "search", "reminder", "time", "date", "screenshot", "email", "weather", "scan",
            "object_detection", "face_recognition", "sentiment", "emotion", "close", "type", "navigate", "gender",
            "grok", "identify", "classify", "color_detection"
        ]
        X = self.vectorizer.fit_transform(commands)
        self.classifier.fit(X, labels)
        log.info("NLP: basic intent classifier trained on %d examples", len(commands))

    def predict_intent(self, text: str):
        """Return (intent_label, confidence). If model unsure, returns (None, 0.0)."""
        if not text:
            return None, 0.0
        X = self.vectorizer.transform([text])
        probs = self.classifier.predict_proba(X)[0]
        intent = self.classifier.predict(X)[0]
        confidence = float(max(probs))
        log.debug("NLP predict: %s -> %s (%.2f)", text, intent, confidence)
        return intent, confidence

    def get_time_date(self) -> str:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return f"The time is {time_str}. Today is {date_str}."
