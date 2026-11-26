import os
import unittest

from managers.file_manager import FileManager
from managers.log_manager import LogManager

TEST_FILE = "test_log.txt"


class TestLogManager(unittest.TestCase):

    def setUp(self):
        # use a test file instead of the real battle_log.txt
        self.log_manager = LogManager()
        self.log_manager._file_manager = FileManager(TEST_FILE)

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_count_wins_counts_only_victories(self):
        self.log_manager._file_manager.write_file(
            "10:00:00 | Battle started: Alan vs Goblin (level 1)\n"
            "10:00:05 | Alan defeated Goblin (+50 XP, +10 gold)\n"
            "10:01:00 | Alan was defeated by Drow\n"
            "10:02:00 | Malan defeated Orc (+100 XP, +20 gold)\n"
            "10:03:00 | Alan defeated Orc (+100 XP, +20 gold)\n"
        )
        self.assertEqual(self.log_manager.count_wins("Alan"), 2)

    def test_count_wins_empty_log_is_zero(self):
        self.assertEqual(self.log_manager.count_wins("Alan"), 0)

    def test_clear_log_empties_the_file(self):
        self.log_manager.write_log("Alan defeated Goblin")
        self.log_manager.clear_log()
        self.assertEqual(list(self.log_manager._file_manager.read_lines()), [])


if __name__ == "__main__":
    unittest.main()
