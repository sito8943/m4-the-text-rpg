import os

SCREEN_WIDTH = 80
BOX_WIDTH = 44

class ScreenManager:
    def __init__(self):
        self.current_screen = "main_menu"

    def _clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _center(self, text):
        return text.center(SCREEN_WIDTH).rstrip()

    def _box_line(self, text="", left=False):
        inner = BOX_WIDTH - 2
        content = ("   " + text).ljust(inner) if left else text.center(inner)
        return f"│{content}│"

    def print_main_menu(self, data=None):
        self._clear_screen()
        print("┌" + "─" * (BOX_WIDTH - 2) + "┐")
        print(self._box_line("Welcome to the Game!", left=True))
        print(self._box_line("", left=True))
        if data:
            print(self._box_line("1. Continue Game", left=True))
        else:
            print(self._box_line("1. Start Game", left=True))
        print(self._box_line("2. Exit", left=True))
        print("└" + "─" * (BOX_WIDTH - 2) + "┘")
        return input("Enter your choice: ")

    def print_create_character_screen(self):
        self._clear_screen()
        print("┌" + "─" * (BOX_WIDTH - 2) + "┐")
        print(self._box_line("Create Your Character", left=True))
        print(self._box_line("", left=True))
        name = input("Enter your character's name: ")
        print("└" + "─" * (BOX_WIDTH - 2) + "┘")
        return name

    def print_game_menu(self):
        self._clear_screen()
        print("┌" + "─" * (BOX_WIDTH - 2) + "┐")
        print(self._box_line("Game Menu", left=True))
        print(self._box_line("", left=True))
        print(self._box_line("1. Explore", left=True))
        print(self._box_line("2. Character", left=True))
        print(self._box_line("3. Inventory", left=True))
        print(self._box_line("4. Shop", left=True))
        print(self._box_line("5. Save", left=True))
        print(self._box_line("6. Exit", left=True))
        print("└" + "─" * (BOX_WIDTH - 2) + "┘")
        return input("Enter your choice:")