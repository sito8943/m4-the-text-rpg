"""Main game flow: home screen, game menu, character creation and exit."""

import managers.player_data_manager as pdm
import managers.screen_manager as sm
import managers.action_manager as am
import managers.validation_manager as vm
from models.character_class import CharacterClass
from models.character import Character
from models.weapon import Weapon
from models.inventory import Inventory
from prefabs.items import create_item

STARTER_POTIONS = 2
EXIT_COMMAND = "exit"
HOME_OPTIONS = ("New Game", "Exit (or type exit)")
GAME_OPTIONS = ("Explore", "Character", "Inventory", "Shop", "Log", "Save", "Main Menu", "Exit (or type exit)")
NEW_GAME_OPTIONS = ("Yes, start over", "No, go back")

class GameManager:
    """Controls the game lifecycle and the main menus."""

    _data = None

    def __init__(self):
        """Creates the managers the game needs."""
        self.status = "initialized"
        self._validation_manager = vm.ValidationManager()
        self._action_manager = am.ActionManager()
        self._player_data_manager = pdm.PlayerDataManager()
        self._screen_manager = sm.ScreenManager()

    # --- Lifecycle ---

    def start_game(self):
        """Loads the saved data and opens the home screen."""
        self.status = "started"
        self._data = self._player_data_manager.load_data()
        self._home_screen()

    def _exit_game(self):
        """Shows a goodbye message and closes the program."""
        self._screen_manager.message("Exiting the game. Goodbye!", wait=1, pause=False, style="magenta")
        exit()

    # --- Menus ---

    def _home_screen(self):
        """Shows the home menu in a loop until the player exits."""
        options = {
            "1": self._game_menu,
            "2": self._new_game,
            "3": self._exit_game,
            EXIT_COMMAND: self._exit_game
        }

        while True:
            labels = ("Continue Game" if self._data else "Start Game",) + HOME_OPTIONS
            choice = self._screen_manager.print_menu("Welcome THE TEXT RPG!", labels)
            if choice in options:
                options[choice]()
            else:
                self._screen_manager.message("Invalid choice.", style="red")

    def _game_menu(self):
        """Shows the game menu in a loop until the player goes back to the main menu.
        Creates a character first if there is none."""
        if not self._data:
            self._create_character()

        options = {
            "1": lambda: self._action_manager.do_action("explore", data=self._data),
            "2": lambda: self._action_manager.do_action("character", data=self._data),
            "3": lambda: self._action_manager.do_action("inventory"),
            "4": lambda: self._action_manager.do_action("shop"),
            "5": lambda: self._action_manager.do_action("log"),
            "6": self._save_game,
            "7": None,  # Main Menu: leave this loop and go back to the home screen
            "8": self._exit_game,
            EXIT_COMMAND: self._exit_game
        }

        while True:
            choice = self._screen_manager.print_menu("Game Menu", GAME_OPTIONS)
            if choice not in options:
                self._screen_manager.message("Invalid choice.", style="red")
            elif options[choice] is None:
                return
            else:
                options[choice]()

    def _new_game(self):
        """Asks for confirmation, then replaces the current character with a new one."""
        if self._data:
            choice = self._screen_manager.print_menu("New Game", NEW_GAME_OPTIONS, (
                f"{self._data.name} (level {self._data.level}) will be lost.",
                "Are you sure?",
            ), style="red")
            if choice != "1":
                return
        self._data = None
        self._game_menu()

    # --- Save / Load ---
   
    def _save_game(self):
        """Saves the current character to the save file."""
        self._player_data_manager.save_data(self._data)

    # --- Character ---

    def _create_character(self):
        """Asks for a valid name, creates the character with starter potions and saves it."""
        name = self._screen_manager.print_create_character_screen()
        while error := self._validation_manager.validate(name, "name"):
            self._screen_manager.print_validation_error(error)
            name = self._screen_manager.print_create_character_screen(onlyAsk=True)

        self._data = Character(name, CharacterClass(), Weapon(), Inventory())
        for _ in range(STARTER_POTIONS):
            self._data.inventory.add_item(create_item("potion"))
        self._player_data_manager.save_data(self._data)
        self._screen_manager.print_event_screen("Welcome", (
            f"Welcome, {name}...",
            "The terminal void has been waiting for you.",
            "You carry 2 potions. Use them wisely.",
            "Your adventure begins now.",
        ), style="green")

