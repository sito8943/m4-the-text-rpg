import os
import time

from rich.console import Console
from rich.panel import Panel

console = Console()

BOX_WIDTH = 50

# --- Console Utilities ---

def clear():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_screen(title, lines=(), style="cyan"):
    """Clears the screen and displays a panel with a title and optional lines of text."""
    clear()
    show_box(title, lines, style)

def show_box(title, lines=(), style="cyan"):
    """Displays a panel with a title and optional lines of text."""
    console.print(Panel("\n".join(lines), title=f"[bold {style}]{title}", border_style=style, width=BOX_WIDTH))

def message(text, style="white"):
    """Displays a coloured message."""
    console.print(text, style=style)

def ask(prompt="Enter your choice: "):
    """Prompts the user for input and returns the input."""
    return console.input(f"[bold yellow]{prompt}")

def pause(text="Press Enter to continue."):
    """Pauses the program until the user presses Enter."""
    console.input(f"[dim]{text}")

def slow_print(text, delay=0.03, style="white"):
    """Prints text letter by letter."""
    for char in text:
        console.print(char, end="", style=style)
        time.sleep(delay)
    console.print()
