import os

SCREEN_WIDTH = 80
BOX_WIDTH = 44

class ScreenManager:
    def __init__(self):
        self.current_screen = "main_menu"

    # --- Generic tools ---

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def show_box(self, title, lines=()):
        print("┌" + "─" * (BOX_WIDTH - 2) + "┐")
        print(self._box_line(title, left=True))
        print(self._box_line("", left=True))
        for line in lines:
            print(self._box_line(line, left=True))
        print("└" + "─" * (BOX_WIDTH - 2) + "┘")

    def show_screen(self, title, lines=()):
        self.clear()
        self.show_box(title, lines)

    def message(self, text):
        print(text)

    def ask(self, prompt="Enter your choice: "):
        return input(prompt)

    def pause(self, text="Press Enter to continue."):
        input(text)

    # --- Helpers ---

    def _center(self, text):
        return text.center(SCREEN_WIDTH).rstrip()

    def _box_line(self, text="", left=False):
        inner = BOX_WIDTH - 2
        content = ("   " + text).ljust(inner) if left else text.center(inner)
        return f"│{content}│"

    # --- Screens ---

    def print_main_menu(self, data=None):
        first_option = "1. Continue Game" if data else "1. Start Game"
        self.show_screen("Welcome to the Game!", [first_option, "2. Exit"])
        return self.ask()

    def print_create_character_screen(self):
        self.show_screen("Create Your Character")
        return self.ask("Enter your character's name: ")

    def print_game_menu(self):
        self.show_screen("Game Menu", [
            "1. Explore",
            "2. Character",
            "3. Inventory",
            "4. Shop",
            "5. Save",
            "6. Exit",
        ])
        return self.ask()
