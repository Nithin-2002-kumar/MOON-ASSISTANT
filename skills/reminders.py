import threading
import time
import logging
from datetime import datetime, timedelta

log = logging.getLogger("moon.skills.reminders")


class ReminderManager:
    """Schedule reminders in background threads."""

    def __init__(self, speaker=None):
        self.reminders = []
        self.speaker = speaker

    def add_reminder(self, text: str, delay_seconds: int):
        t = threading.Thread(target=self._reminder_worker, args=(text, delay_seconds), daemon=True)
        t.start()
        self.reminders.append((text, datetime.now() + timedelta(seconds=delay_seconds)))
        log.info("Reminder set: %s (in %s seconds)", text, delay_seconds)
        return f"Reminder set for {delay_seconds} seconds from now."

    def _reminder_worker(self, text: str, delay: int):
        time.sleep(delay)
        msg = f"Reminder: {text}"
        log.info(msg)
        if self.speaker:
            self.speaker.say(msg)
