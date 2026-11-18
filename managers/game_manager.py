
import managers.player_data_manager as pdm
import managers.screen_manager as sm
import managers.action_manager as am
import managers.validation_manager as vm
from models.character_class import CharacterClass
from models.character import Character
from models.weapon import Weapon
from models.inventory import Inventory

class GameManager:
    _data = None

    def __init__(self):
        self.status = "initialized"
        self._validation_manager = vm.ValidationManager()
        self._action_manager = am.ActionManager()
        self._player_data_manager = pdm.PlayerDataManager()
        self._screen_manager = sm.ScreenManager()

    # --- Lifecycle ---

    def start_game(self):
        self.status = "started"
        self._data = self._player_data_manager.load_data()
        self._home_screen()

    def _exit_game(self):
        self._screen_manager.message("Exiting the game. Goodbye!", wait=1, pause=False, style="magenta")
        exit()

    # --- Menus ---

    def _home_screen(self):

        options = {
            "1": self._game_menu,
            "2": self._exit_game
        }

        while True:
            choice = self._screen_manager.print_main_menu(data=self._data)
            if choice in options:
                options[choice]()
            else:
                self._screen_manager.message("Invalid choice.", style="red")

    def _game_menu(self):
        if not self._data:
            self._create_character()

        options = {
            1: lambda: self._action_manager.do_action("explore", data=self._data),
            2: lambda: self._action_manager.do_action("character", data=self._data),
            3: lambda: self._action_manager.do_action("inventory"),
            4: lambda: self._action_manager.do_action("shop"),
            5: lambda: self._action_manager.do_action("log"),
            6: self._save_game,
            7: self._exit_game
        }

        while True:
            choice = self._screen_manager.print_game_menu()
            try:
                choice = int(choice)
            except ValueError:
                self._screen_manager.message("Invalid input. Please enter a number.", style="red")
                continue
            if choice in options:
                options[choice]()
            else:
                self._screen_manager.message("Invalid choice.", style="red")

    # --- Save / Load ---
   
    def _save_game(self):
        self._player_data_manager.save_data(self._data)

    # --- Character ---

    def _create_character(self):
        while True:
            name = self._screen_manager.print_create_character_screen()
            error = self._validation_manager.validate(name, "name")
            if not error:
                break
            self._screen_manager.message(error, "Invalid Name", style="red")
        self._data = Character(name, CharacterClass(), Weapon(), Inventory())
        self._player_data_manager.save_data(self._data)
        self._screen_manager.print_event_screen("Welcome", (
            f"Welcome, {name}...",
            "The terminal void has been waiting for you.",
            "Your adventure begins now.",
        ), style="green")

