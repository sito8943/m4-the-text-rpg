import unittest
from unittest.mock import patch

from managers.game_manager import GameManager


@patch("utils.console.show_title")
@patch("utils.console.slow_print")
class TestCreateCharacter(unittest.TestCase):

    def setUp(self):
        self.gm = GameManager()
        # avoid writing game_data.txt and showing the welcome screen
        self.save = patch.object(self.gm._player_data_manager, "save_data").start()
        patch.object(self.gm._screen_manager, "print_event_screen").start()
        self.addCleanup(patch.stopall)

    @patch("utils.console.ask", return_value="Sito")
    def test_valid_name_creates_character(self, mock_ask, mock_print, mock_title):
        self.gm._create_character()

        self.assertEqual(self.gm._data.name, "Sito")
        self.assertEqual(mock_ask.call_count, 1)
        self.save.assert_called_once_with(self.gm._data)

    @patch("utils.console.ask", side_effect=["", "ab", "x1y", "Sito"])
    def test_retries_until_name_is_valid(self, mock_ask, mock_print, mock_title):
        with patch.object(self.gm._screen_manager, "print_validation_error") as mock_error:
            self.gm._create_character()

        self.assertEqual(self.gm._data.name, "Sito")
        self.assertEqual(mock_ask.call_count, 4)
        self.assertEqual(mock_error.call_count, 3)

    @patch("utils.console.ask", return_value="  Sito  ")
    def test_name_is_stripped(self, mock_ask, mock_print, mock_title):
        self.gm._create_character()

        self.assertEqual(self.gm._data.name, "Sito")

    @patch("utils.console.ask", side_effect=["   ", "Sito"])
    def test_whitespace_only_name_is_rejected(self, mock_ask, mock_print, mock_title):
        self.gm._create_character()

        self.assertEqual(mock_ask.call_count, 2)
        self.assertEqual(self.gm._data.name, "Sito")


if __name__ == "__main__":
    unittest.main()
