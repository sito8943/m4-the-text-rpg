import json

import managers.file_manager as fm
import managers.screen_manager as sm

from models.character import Character

class PlayerDataManager:
    def __init__(self):
        self.player_data = {}
        self._screen_manager = sm.ScreenManager()
        self._file_manager = fm.FileManager("game_data.txt")

    def _load_data(self):
        self._screen_manager.message("Reading game data...")
        player_data = self._file_manager.read_file()
        if player_data:
            try:
                player_data_dict = json.loads(player_data)
            except json.JSONDecodeError:
                self._screen_manager.message("Save file is invalid or outdated. Starting fresh.")
                return
            self._data = Character.from_dict(player_data_dict)
            self._screen_manager.message(f"Game data loaded: character name is {self._data.name}")
        else:
            self._screen_manager.message("No game data found. Starting fresh.")

    def _save_data(self):
        if self._data:
            player_data = self._data.to_dict()
            self._file_manager.write_file(json.dumps(player_data, indent=2))
            self._screen_manager.message("Game data saved.")
        else:
            self._screen_manager.message("No data to save.")