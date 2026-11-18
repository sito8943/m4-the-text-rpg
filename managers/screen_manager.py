import time
import utils.console
class ScreenManager:
    def __init__(self):
        self.current_screen = "main_menu"

    # --- Screens ---

    def print_main_menu(self, data=None):
        first_option = "1. Continue Game" if data else "1. Start Game"
        utils.console.show_screen("Welcome THE TEXT RPG!", [first_option, "2. Exit"])
        return utils.console.ask()

    def message(self, message="", title="Message", wait=0, pause=True, style="cyan"):
        utils.console.show_screen(title, [message], style)
        if wait:
            time.sleep(wait)
        if pause:
            utils.console.pause("Press Enter to continue.")

    def print_create_character_screen(self):
        utils.console.show_screen("Create Your Character")
        return utils.console.ask("Enter your character's name: ")

    def print_character_screen(self, character):
        utils.console.show_screen("Character", str(character).split("\n"))
        utils.console.pause("Press Enter to return to the game menu.")

    def print_event_screen(self, title, story=(), style="cyan"):
        utils.console.show_title(title, style)
        for line in story:
            utils.console.slow_print(line, style=f"italic {style}")
        utils.console.pause("Press Enter to continue.")

    def print_info_screen(self, title, lines=(), style="cyan", prompt=None):
        utils.console.show_screen(title, lines, style)
        if prompt:
            return utils.console.ask(prompt)
        utils.console.pause("Press Enter to continue.")

    def print_inventory_screen(self):
        utils.console.show_screen("Inventory", ["Inventory is currently empty."])
        utils.console.pause("Press Enter to return to the game menu.")

    def print_shop_screen(self):
        utils.console.show_screen("Shop", ["Welcome to the shop!"])
        utils.console.pause("Press Enter to return to the game menu.")

    def print_game_menu(self):
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
