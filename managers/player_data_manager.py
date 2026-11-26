"""Save and load of the player's character in the SQLite database."""

import logging
import sqlite3

import managers.screen_manager as sm
import managers.database_manager as dbm

from models.character import Character

class PlayerDataManager:
    """Saves and loads the character in game.db."""

    def __init__(self):
        """Creates the database manager and the screen manager."""
        self.player_data = {}
        self._database_manager = dbm.DatabaseManager()
        self._screen_manager = sm.ScreenManager()

    def load_data(self):
        """Returns the saved Character, or None if there is no valid save."""
        self._screen_manager.message("Reading game data...", wait=1, pause=False)
        try:
            player_data_dict = self._database_manager.load_character()
        except sqlite3.DatabaseError:
            self._screen_manager.message("Save file is invalid or outdated. Starting fresh.", wait=1, pause=False, style="red")
            logging.error("Save file is invalid, starting fresh")
            return None
        if player_data_dict is None:
            self._screen_manager.message("No game data found. Starting fresh.", wait=1, pause=False)
            return None
        data = Character.from_dict(player_data_dict)
        self._screen_manager.message(f"Game data loaded: character name is {data.name}", wait=1, pause=False, style="green")
        logging.info(f"Game loaded: {data.name}")
        return data

    def save_data(self, data):
        """Writes the character to the database."""
        if not data:
            self._screen_manager.message("No data to save.", wait=1, pause=False, style="red")
            return
        try:
            self._database_manager.save_character(data.to_dict())
        except sqlite3.DatabaseError:
            self._screen_manager.message("Could not save the game.", wait=1, pause=False, style="red")
            logging.error("Could not save the game")
            return
        self._screen_manager.message("Game data saved.", wait=1, pause=False, style="green")
