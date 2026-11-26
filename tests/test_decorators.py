import unittest
from unittest.mock import patch

from managers.action_manager import ActionManager
from models.character import Character
from models.character_class import CharacterClass
from models.inventory import Inventory
from models.weapon import Weapon


class TestRequiresCharacter(unittest.TestCase):

    def setUp(self):
        self.am = ActionManager()
        # don't print anything on screen
        self.message = patch.object(self.am._screen_manager, "message").start()
        self.sheet = patch.object(self.am._screen_manager, "print_character_screen").start()
        self.addCleanup(patch.stopall)

    def test_without_character_shows_error_and_skips_action(self):
        self.am.do_action("character", data=None)

        self.message.assert_called_once_with("No character data available.", style="red")
        self.sheet.assert_not_called()

    def test_with_character_runs_action(self):
        character = Character("Sito", CharacterClass(), Weapon(), Inventory())
        with patch.object(self.am._log_manager, "count_wins", return_value=2):
            self.am.do_action("character", data=character)

        self.message.assert_not_called()
        self.sheet.assert_called_once_with(character, 2)

    def test_shop_without_character_does_not_crash(self):
        self.am.do_action("shop", data=None)

        self.message.assert_called_once_with("No character data available.", style="red")


if __name__ == "__main__":
    unittest.main()
