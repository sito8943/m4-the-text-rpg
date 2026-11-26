"""Entry point of THE TEXT-BASED RPG."""

import utils.config as config
import managers.game_manager as gm

def main():
    """Loads the .env config and logging, creates the game manager and starts the game."""
    config.setup()
    manager = gm.GameManager()
    manager.start_game()

if __name__ == "__main__":
    main()
