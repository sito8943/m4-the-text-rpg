import json

import managers.file_manager as fm
import managers.screen_manager as sm

from models.character import Character

class PlayerDataManager:
    def __init__(self):
        self.player_data = {}
        self._screen_manager = sm.ScreenManager()
        self._file_manager = fm.FileManager("game_data.txt")

    def load_data(self):
        self._screen_manager.message("Reading game data...", wait=1, pause=False)
        player_data = self._file_manager.read_file()
        if player_data:
            try:
                player_data_dict = json.loads(player_data)
            except json.JSONDecodeError:
                self._screen_manager.message("Save file is invalid or outdated. Starting fresh.", wait=1, pause=False, style="red")
                return None
            data = Character.from_dict(player_data_dict)
            self._screen_manager.message(f"Game data loaded: character name is {data.name}", wait=1, pause=False, style="green")
            return data
        else:
            self._screen_manager.message("No game data found. Starting fresh.", wait=1, pause=False)
            return None

    def save_data(self, data):
        if data:
            player_data = data.to_dict()
            self._file_manager.write_file(json.dumps(player_data, indent=2))
            self._screen_manager.message("Game data saved.", wait=1, pause=False, style="green")
        else:
            self._screen_manager.message("No data to save.", wait=1, pause=False, style="red")