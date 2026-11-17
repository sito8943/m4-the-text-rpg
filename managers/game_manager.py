

import managers.player_data_manager as pdm
import managers.screen_manager as sm
import managers.action_manager as am
from models.character_class import CharacterClass
from models.character import Character
from models.weapon import Weapon
from models.inventory import Inventory

class GameManager:
    _data = None

    def __init__(self):
        self.status = "initialized"
        self._action_manager = am.ActionManager()
        self._player_data_manager = pdm.PlayerDataManager()
        self._screen_manager = sm.ScreenManager()

    # --- Lifecycle ---

    def start_game(self):
        self.status = "started"
        self._player_data_manager.load_data()
        self._home_screen()

    def _exit_game(self):
        self._screen_manager.message("Exiting the game. Goodbye!")
        exit()

    # --- Menus ---

    def _home_screen(self):

        options = {
            "1": self._game_menu,
            "2": self._exit_game
        }

        choice = self._screen_manager.print_main_menu(data=self._data)
        if choice in options:
            options[choice]()
        else:
            self._screen_manager.pause("Invalid choice. Press Enter to try again.")
            self._home_screen()

    def _game_menu(self):
        if not self._data:
            self._create_character()

        options = {
            1: lambda: self._action_manager.do_action("explore"),
            2: lambda: self._action_manager.do_action("character", data=self._data),
            3: lambda: self._action_manager.do_action("inventory"),
            4: lambda: self._action_manager.do_action("shop"),
            5: self._save_game,
            6: self._exit_game
        }

        choice = self._screen_manager.print_game_menu()
        try:
            choice = int(choice)
            if choice in options:
                options[choice]()
            else:
                self._screen_manager.pause("Invalid choice. Press Enter to try again.")
                self._game_menu()
        except ValueError:
            self._screen_manager.pause("Invalid input. Please enter a number. Press Enter to try again.")
            self._game_menu()

    # --- Save / Load ---
   
    def _save_game(self):
        self._player_data_manager.save_data(self._data)
        self._screen_manager.pause("Press Enter to return to the game menu.")
        self._game_menu()

    # --- Character ---

    def _create_character(self):
        name = self._screen_manager.print_create_character_screen()
        self._data = Character(name, CharacterClass(), Weapon(), Inventory())
        self._player_data_manager.save_data(self._data)
        self._screen_manager.message(f"Character '{name}' created and saved.")
        self._screen_manager.pause()

