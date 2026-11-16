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

    def _load_data(self):
        print("Reading game data...")
        player_data = self.file_manager.read_file()
        if player_data:
            player_data_dict = eval(player_data) # Convert string back to dictionary
            self._data = Character.from_dict(player_data_dict)
            print("Game data loaded: character name is", self._data.name)
        else:
            print("No game data found. Starting fresh.")

    def _save_data(self):
        if self._data:
            player_data = self._data.to_dict()
            self.file_manager.write_file(str(player_data))
            print("Game data saved.")
        else:
            print("No data to save.")
        input("Game saved. Press Enter to return to the game menu.")
        self._start_game()

    def _explore(self):
        print("Exploring the world...")
        # Implement exploration logic here
        input("Press Enter to return to the game menu.")
        self._start_game()

    def _character(self):
        print("Character details:")
        if self._data:
            print(self._data)
        else:
            print("No character data available.")
        input("Press Enter to return to the game menu.")
        self._start_game()

    def _inventory(self):
        print("Inventory is currently empty.")
        # Implement inventory logic here
        input("Press Enter to return to the game menu.")
        self._start_game()

    def _shop(self):
        print("Welcome to the shop!")
        # Implement shop logic here
        input("Press Enter to return to the game menu.")
        self._start_game()

    def _create_character(self):
        name = self.screen_manager.print_create_character_screen()
        self._data = Character(name, CharacterClass(), Weapon(), Inventory())
        self._save_data()
        print(f"Character '{name}' created and saved.")

    def _start_game(self):
        # Start the game logic here
        print("Game is starting...")
        if not self._data:
            self._create_character()

        options = {
            1: self._explore,
            2: self._character,
            3: self._inventory,
            4: self._shop,
            5: self._save_data,
            6: self._exit_game
        }

        choice = self.screen_manager.print_game_menu()
        try:
            choice = int(choice)
            if choice in options:
                options[choice]()
            else:
                print("Invalid choice. Please try again.")
                self._start_game()
        except ValueError:
            print("Invalid input. Please enter a number.")
            self._start_game()

    def _exit_game(self):
        print("Exiting the game. Goodbye!")
        exit()

    def _home_screen(self):

        options = { 
            "1": self._start_game,
            "2": self._exit_game
        }

        choice = self.screen_manager.print_main_menu(data=self._data)
        if choice in options:
            options[choice]()
        else:
            print("Invalid choice. Please try again.")
            self._home_screen()
            self._exit_game()

    def start_game(self):
        self.status = "started"
        print("Game has started.")
        self._load_data()
        self._home_screen()