"""All game screens. Uses utils.console to draw them."""

import time
import utils.console
class ScreenManager:
    """Draws the game screens and reads the player's input."""

    def __init__(self):
        """Sets the starting screen name."""
        self.current_screen = "main_menu"

    # --- Screens ---

    def print_menu(self, title, options, header=(), style="cyan", story=()):
        """Shows a menu with optional header lines and numbered options. Returns the choice.
        The story lines (optional) are printed letter by letter under the menu."""
        lines = list(header)
        if lines:
            lines.append("")
        for number, label in enumerate(options, start=1):
            lines.append(f"{number}. {label}")
        utils.console.show_screen(title, lines, style)
        for line in story:
            utils.console.slow_print(line, style=f"italic {style}")
        return utils.console.ask().strip().lower()

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

    def print_character_screen(self, character, wins):
        """Shows the character sheet."""
        lines = str(character).split("\n") + [f"Battles won: {wins}"]
        utils.console.show_screen("Character", lines)
        utils.console.pause("Press Enter to return to the game menu.")

    def print_event_screen(self, title, story=(), style="cyan"):
        """Shows a title and prints the story lines letter by letter."""
        utils.console.show_title(title, style)
        for line in story:
            utils.console.slow_print(line, style=f"italic {style}")
        utils.console.pause("Press Enter to continue.")

    def print_info_screen(self, title, lines=(), style="cyan"):
        """Shows a panel with lines and waits for Enter."""
        utils.console.show_screen(title, lines, style)
        utils.console.pause("Press Enter to continue.")
