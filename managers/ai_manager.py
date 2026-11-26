"""AI narrator: asks Gemini to write short event stories."""

import os
import json
import logging
import urllib.error
import urllib.request

AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = "gemini-flash-lite-latest"
DEFAULT_TIMEOUT = 5
MAX_LINES = 3
PROMPT = ("You are the narrator of a dark sci-fi terminal RPG set in 'the terminal void'. "
        "Write 2 short sentences (max 15 words each), one per line, for this moment: {moment}. "
        "No numbers, no markdown, no quotes.")

class AiManager:
    """Writes event stories with an AI, or returns the default story if it fails."""

    def __init__(self):
        """Reads the AI key, model and timeout from the environment (.env)."""
        self._api_key = os.getenv("AI_API_KEY", "")
        self._model = os.getenv("AI_MODEL", DEFAULT_MODEL)
        try:
            self._timeout = float(os.getenv("AI_TIMEOUT", DEFAULT_TIMEOUT))
        except ValueError:
            logging.warning("AI_TIMEOUT is not a number, using default")
            self._timeout = DEFAULT_TIMEOUT

    def narrate(self, moment, fallback):
        """Returns the AI story lines for the moment as a tuple, or the fallback story."""
        if not self._api_key:
            return fallback
        try:
            text = self._ask(PROMPT.format(moment=moment))
        except urllib.error.URLError:
            # no internet, wrong key (HTTP 400/403) or too many requests (HTTP 429)
            logging.warning("AI not reachable, using default story")
            return fallback
        except TimeoutError:
            logging.warning("AI timed out, using default story")
            return fallback
        except (json.JSONDecodeError, KeyError, IndexError):
            logging.warning("AI answered something unexpected, using default story")
            return fallback
        lines = tuple(line.strip() for line in text.splitlines() if line.strip())
        return lines[:MAX_LINES] or fallback

    def _ask(self, prompt):
        """Sends the prompt to Gemini and returns the answer text."""
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
        request = urllib.request.Request(
            AI_URL.format(model=self._model), data=body, method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": self._api_key})
        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"]