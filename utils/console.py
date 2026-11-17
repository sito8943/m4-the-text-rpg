import os

SCREEN_WIDTH = 80
BOX_WIDTH = 44

# --- Console Utilities ---

def clear():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_screen(title, lines=()):
    """Clears the screen and displays a box with a title and optional lines of text."""
    clear()
    show_box(title, lines)

def message(text):
    """Displays a message to the console."""
    print(text)

def ask(prompt="Enter your choice: "):
    """Prompts the user for input and returns the input."""
    return input(prompt)

def pause(text="Press Enter to continue."):
    """Pauses the program until the user presses Enter."""
    input(text)

def show_box(title, lines=()):
    """Displays a box with a title and optional lines of text."""
    box_width = 44
    print("┌" + "─" * (box_width - 2) + "┐")
    print(box_line(title, box_width, left=True))
    print(box_line("", box_width, left=True))
    for line in lines:
        print(box_line(line, box_width, left=True))
    print("└" + "─" * (box_width - 2) + "┘")

# --- Helpers ---

def box_line(text="", left=False):
    """Formats a line of text to fit within a box."""
    inner = BOX_WIDTH - 2
    content = ("   " + text).ljust(inner) if left else text.center(inner)
    return f"│{content}│"

