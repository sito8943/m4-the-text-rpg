import json

import managers.file_manager as fm
import managers.screen_manager as sm
from models.character_class import CharacterClass
from models.weapon import Weapon
from models.inventory import Inventory
from models.character import Character

class GameManager:
    _data = None

    def __init__(self):
        self.status = "initialized"
        self.screen_manager = sm.ScreenManager()
        self.file_manager = fm.FileManager("game_data.txt")

    # --- Lifecycle ---

    def start_game(self):
        self.status = "started"
        self._load_data()
        self._home_screen()

    def _exit_game(self):
        self.screen_manager.message("Exiting the game. Goodbye!")
        exit()

    # --- Menus ---

    def _home_screen(self):

        options = {
            "1": self._game_menu,
            "2": self._exit_game
        }

        choice = self.screen_manager.print_main_menu(data=self._data)
        if choice in options:
            options[choice]()
        else:
            self.screen_manager.pause("Invalid choice. Press Enter to try again.")
            self._home_screen()

    def _game_menu(self):
        if not self._data:
            self._create_character()

        options = {
            1: self._explore,
            2: self._character,
            3: self._inventory,
            4: self._shop,
            5: self._save_game,
            6: self._exit_game
        }

        choice = self.screen_manager.print_game_menu()
        try:
            choice = int(choice)
            if choice in options:
                options[choice]()
            else:
                self.screen_manager.pause("Invalid choice. Press Enter to try again.")
                self._game_menu()
        except ValueError:
            self.screen_manager.pause("Invalid input. Please enter a number. Press Enter to try again.")
            self._game_menu()

    # --- Save / Load ---

    def _load_data(self):
        self.screen_manager.message("Reading game data...")
        player_data = self.file_manager.read_file()
        if player_data:
            try:
                player_data_dict = json.loads(player_data)
            except json.JSONDecodeError:
                self.screen_manager.message("Save file is invalid or outdated. Starting fresh.")
                return
            self._data = Character.from_dict(player_data_dict)
            self.screen_manager.message(f"Game data loaded: character name is {self._data.name}")
        else:
            self.screen_manager.message("No game data found. Starting fresh.")

    def _save_data(self):
        if self._data:
            player_data = self._data.to_dict()
            self.file_manager.write_file(json.dumps(player_data, indent=2))
            self.screen_manager.message("Game data saved.")
        else:
            self.screen_manager.message("No data to save.")

    def _save_game(self):
        self._save_data()
        self.screen_manager.pause("Press Enter to return to the game menu.")
        self._game_menu()

    # --- Character ---

    def _create_character(self):
        name = self.screen_manager.print_create_character_screen()
        self._data = Character(name, CharacterClass(), Weapon(), Inventory())
        self._save_data()
        self.screen_manager.message(f"Character '{name}' created and saved.")
        self.screen_manager.pause()

    def _character(self):
        if self._data:
            self.screen_manager.show_screen("Character", str(self._data).split("\n"))
        else:
            self.screen_manager.show_screen("Character", ["No character data available."])
        self.screen_manager.pause("Press Enter to return to the game menu.")
        self._game_menu()

    # --- Game actions ---

    def _explore(self):
        self.screen_manager.show_screen("Explore", ["Exploring the world..."])
        # Implement exploration logic here
        self.screen_manager.pause("Press Enter to return to the game menu.")
        self._game_menu()

    def _inventory(self):
        self.screen_manager.show_screen("Inventory", ["Inventory is currently empty."])
        # Implement inventory logic here
        self.screen_manager.pause("Press Enter to return to the game menu.")
        self._game_menu()

    def _shop(self):
        self.screen_manager.show_screen("Shop", ["Welcome to the shop!"])
        # Implement shop logic here
        self.screen_manager.pause("Press Enter to return to the game menu.")
        self._game_menu()
