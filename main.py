"""Entry point of THE TEXT-BASED RPG."""

import managers.game_manager as gm

def main():
    """Creates the game manager and starts the game."""
    manager = gm.GameManager()
    manager.start_game()

if __name__ == "__main__":
    main()