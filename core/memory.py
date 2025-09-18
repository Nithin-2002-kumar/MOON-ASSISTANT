import json
import os
from core import config


class Memory:
    def __init__(self):
        self.file = config.MEMORY_FILE
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                return json.load(f)
        return {"reminders": [], "preferences": {}}

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_reminder(self, reminder):
        self.data["reminders"].append(reminder)
        self.save()

    def get_reminders(self):
        return self.data.get("reminders", [])

    def set_preference(self, user, key, value):
        if user not in self.data["preferences"]:
            self.data["preferences"][user] = {}
        self.data["preferences"][user][key] = value
        self.save()

    def get_preferences(self, user):
        return self.data["preferences"].get(user, {})
