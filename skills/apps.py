import os
import subprocess
import logging

log = logging.getLogger("moon.skills.apps")


class AppManager:
    """Open, close, and type into apps (basic OS-level)."""

    def open_app(self, app_name: str):
        try:
            if app_name.lower() == "notepad":
                subprocess.Popen(["notepad.exe"])
            elif app_name.lower() == "calculator":
                subprocess.Popen(["calc.exe"])
            else:
                os.system(f"start {app_name}")
            log.info("Opened app: %s", app_name)
            return f"Opening {app_name}."
        except Exception:
            log.exception("Failed to open app: %s", app_name)
            return f"Couldn't open {app_name}."

    def close_app(self, app_name: str):
        try:
            os.system(f"taskkill /f /im {app_name}.exe")
            log.info("Closed app: %s", app_name)
            return f"Closed {app_name}."
        except Exception:
            log.exception("Failed to close app: %s", app_name)
            return f"Couldn't close {app_name}."
