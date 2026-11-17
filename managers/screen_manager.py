import utils.console
class ScreenManager:
    def __init__(self):
        self.current_screen = "main_menu"

    # --- Screens ---

    def print_main_menu(self, data=None):
        first_option = "1. Continue Game" if data else "1. Start Game"
        utils.console.show_screen("Welcome to the Game!", [first_option, "2. Exit"])
        return utils.console.ask()

    def print_create_character_screen(self):
        utils.console.show_screen("Create Your Character")
        return utils.console.ask("Enter your character's name: ")

    def print_game_menu(self):
        utils.console.show_screen("Game Menu", [
            "1. Explore",
            "2. Character",
            "3. Inventory",
            "4. Shop",
            "5. Save",
            "6. Exit",
        ])
        return utils.console.ask()
