"""All game screens. Uses utils.console to draw them."""

import time
import utils.console
class ScreenManager:
    """Draws the game screens and reads the player's input."""

    def __init__(self):
        """Sets the starting screen name."""
        self.current_screen = "main_menu"

    # --- Screens ---

    def print_main_menu(self, data=None):
        """Shows the home menu and returns the player's choice."""
        first_option = "1. Continue Game" if data else "1. Start Game"
        utils.console.show_screen("Welcome THE TEXT RPG!", [first_option, "2. Exit"])
        return utils.console.ask()

    def message(self, message="", title="Message", wait=0, pause=True, style="cyan"):
        """Shows a message panel. Can wait some seconds and/or wait for Enter."""
        utils.console.show_screen(title, [message], style)
        if wait:
            time.sleep(wait)
        if pause:
            utils.console.pause("Press Enter to continue.")

    def print_create_character_screen(self, onlyAsk=False):
        """Shows the character creation intro and returns the typed name (stripped)."""
        if onlyAsk is False:
            utils.console.show_title("Create Your Character", style="green")
            utils.console.slow_print("You are about to start your adventure!", style=f"italic green")
            utils.console.slow_print("Let's start with your character!", style=f"italic green")        
        return utils.console.ask("Enter your character's name: ").strip()

    def print_validation_error(self, error):
        """Shows a validation error in red."""
        utils.console.slow_print(error, style="italic red")

    def print_character_screen(self, character):
        """Shows the character sheet."""
        utils.console.show_screen("Character", str(character).split("\n"))
        utils.console.pause("Press Enter to return to the game menu.")

    def print_event_screen(self, title, story=(), style="cyan"):
        """Shows a title and prints the story lines letter by letter."""
        utils.console.show_title(title, style)
        for line in story:
            utils.console.slow_print(line, style=f"italic {style}")
        utils.console.pause("Press Enter to continue.")

    def print_info_screen(self, title, lines=(), style="cyan", prompt=None):
        """Shows a panel with lines. Returns the answer if a prompt is given."""
        utils.console.show_screen(title, lines, style)
        if prompt:
            return utils.console.ask(prompt)
        utils.console.pause("Press Enter to continue.")

    def print_inventory_screen(self):
        """Shows the inventory screen."""
        utils.console.show_screen("Inventory", ["Inventory is currently empty."])
        utils.console.pause("Press Enter to return to the game menu.")

    def print_shop_screen(self):
        """Shows the shop screen."""
        utils.console.show_screen("Shop", ["Welcome to the shop!"])
        utils.console.pause("Press Enter to return to the game menu.")

    def print_game_menu(self):
        """Shows the game menu and returns the player's choice."""
        utils.console.show_screen("Game Menu", [
            "1. Explore",
            "2. Character",
            "3. Inventory",
            "4. Shop",
            "5. Log",
            "6. Save",
            "7. Exit",
        ])
        return utils.console.ask()
