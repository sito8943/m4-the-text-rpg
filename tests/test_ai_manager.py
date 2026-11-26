import os
import unittest
import urllib.error
from unittest.mock import patch

from managers.ai_manager import AiManager

FALLBACK = ("Default line one.", "Default line two.")


class TestAiManager(unittest.TestCase):

    # clear=True removes the real environment, so the tests don't use your real key
    @patch.dict(os.environ, {}, clear=True)
    def test_without_key_returns_fallback_without_calling_ai(self):
        ai = AiManager()
        with patch.object(ai, "_ask") as ask:
            self.assertEqual(ai.narrate("a battle", FALLBACK), FALLBACK)

        ask.assert_not_called()

    @patch.dict(os.environ, {"AI_API_KEY": "test-key"}, clear=True)
    def test_good_answer_returns_lines(self):
        ai = AiManager()
        answer = "The void hums.\n\n  A shadow moves.  \nYou feel watched.\nToo many lines."
        with patch.object(ai, "_ask", return_value=answer):
            story = ai.narrate("a battle", FALLBACK)

        # empty lines removed, spaces stripped, at most 3 lines
        self.assertEqual(story, ("The void hums.", "A shadow moves.", "You feel watched."))

    @patch.dict(os.environ, {"AI_API_KEY": "test-key"}, clear=True)
    def test_no_internet_returns_fallback_and_logs(self):
        ai = AiManager()
        with patch.object(ai, "_ask", side_effect=urllib.error.URLError("offline")):
            with self.assertLogs(level="WARNING") as logs:
                story = ai.narrate("a battle", FALLBACK)

        self.assertEqual(story, FALLBACK)
        self.assertIn("AI not reachable", logs.output[0])

    @patch.dict(os.environ, {"AI_API_KEY": "test-key"}, clear=True)
    def test_unexpected_answer_returns_fallback(self):
        ai = AiManager()
        with patch.object(ai, "_ask", side_effect=KeyError("candidates")):
            with self.assertLogs(level="WARNING"):
                self.assertEqual(ai.narrate("a battle", FALLBACK), FALLBACK)

    @patch.dict(os.environ, {"AI_API_KEY": "test-key"}, clear=True)
    def test_empty_answer_returns_fallback(self):
        ai = AiManager()
        with patch.object(ai, "_ask", return_value="  \n \n"):
            self.assertEqual(ai.narrate("a battle", FALLBACK), FALLBACK)


if __name__ == "__main__":
    unittest.main()
