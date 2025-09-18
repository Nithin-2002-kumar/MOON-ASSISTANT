import webbrowser
import logging

log = logging.getLogger("moon.skills.browser")


class BrowserManager:
    """Handle simple web browsing and searches."""

    def open_url(self, url: str):
        try:
            webbrowser.open(url)
            log.info("Opened URL: %s", url)
            return f"Opening {url}"
        except Exception:
            log.exception("Failed to open URL: %s", url)
            return "Couldn't open browser."

    def search(self, query: str):
        try:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            log.info("Searching: %s", query)
            return f"Searching Google for {query}"
        except Exception:
            log.exception("Search failed: %s", query)
            return "Couldn't perform search."
