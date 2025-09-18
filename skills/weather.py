import requests
import logging
from core import config

log = logging.getLogger("moon.skills.weather")


class Weather:
    """Fetch current weather (OpenWeatherMap placeholder)."""

    def get_weather(self, city: str) -> str:
        if not config.OPENWEATHER_API_KEY:
            return "Weather API key missing."
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.OPENWEATHER_API_KEY}&units=metric"
            r = requests.get(url, timeout=5)
            data = r.json()
            if r.status_code == 200 and "main" in data:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                return f"The weather in {city} is {desc} with {temp}°C."
            else:
                return "Couldn't fetch weather right now."
        except Exception:
            log.exception("Weather fetch failed for city: %s", city)
            return "Weather service error."
