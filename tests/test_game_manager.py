import unittest
from unittest.mock import patch

from managers.game_manager import GameManager
from models.character import Character
from models.character_class import CharacterClass
from models.inventory import Inventory
from models.weapon import Weapon


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


class TestNewGame(unittest.TestCase):

    def setUp(self):
        self.gm = GameManager()
        self.gm._data = Character("Old", CharacterClass(), Weapon(), Inventory())
        # don't open the real game menu
        self.game_menu = patch.object(self.gm, "_game_menu").start()
        self.menu = patch.object(self.gm._screen_manager, "print_menu").start()
        self.addCleanup(patch.stopall)

    def test_confirm_removes_character_and_starts(self):
        self.menu.return_value = "1"
        self.gm._new_game()

        self.assertIsNone(self.gm._data)
        self.game_menu.assert_called_once()

    def test_cancel_keeps_character(self):
        self.menu.return_value = "2"
        self.gm._new_game()

        self.assertEqual(self.gm._data.name, "Old")
        self.game_menu.assert_not_called()

    def test_without_character_starts_without_asking(self):
        self.gm._data = None
        self.gm._new_game()

        self.menu.assert_not_called()
        self.game_menu.assert_called_once()


class TestGameMenu(unittest.TestCase):

    def test_main_menu_option_returns_to_home(self):
        gm = GameManager()
        gm._data = Character("Sito", CharacterClass(), Weapon(), Inventory())
        with patch.object(gm._screen_manager, "print_menu", return_value="7") as menu:
            gm._game_menu()  # would loop forever if "7" did not return

        menu.assert_called_once()


if __name__ == "__main__":
    unittest.main()
