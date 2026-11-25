import unittest
import urllib.error
from unittest.mock import patch

from managers.api_manager import ApiManager
from managers.event_manager import EventManager
from managers.player_data_manager import PlayerDataManager


# no cache file is read or written during the tests
@patch("managers.file_manager.FileManager.write_file")
@patch("managers.file_manager.FileManager.read_file", return_value="")
class TestLogging(unittest.TestCase):

    def test_no_internet_logs_warning(self, mock_read, mock_write):
        api = ApiManager()
        with patch.object(api, "_get_json", side_effect=urllib.error.URLError("offline")):
            with self.assertLogs(level="WARNING") as logs:
                api.fetch_monster(1)

        self.assertIn("API not reachable, using cache", logs.output[0])

    def test_broken_save_logs_error(self, mock_read, mock_write):
        mock_read.return_value = "{ broken json"
        manager = PlayerDataManager()
        with patch.object(manager._screen_manager, "message"):
            with self.assertLogs(level="ERROR") as logs:
                self.assertIsNone(manager.load_data())

        self.assertIn("Save file is invalid", logs.output[0])

    def test_prefab_enemy_logs_warning(self, mock_read, mock_write):
        events = EventManager()
        with patch.object(events._api_manager, "fetch_monster", return_value=None):
            with self.assertLogs(level="WARNING") as logs:
                enemy = events._spawn_enemy(1)

        self.assertIsNotNone(enemy)
        self.assertIn("using prefab enemy", logs.output[0])


if __name__ == "__main__":
    unittest.main()
