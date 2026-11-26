import os
import unittest

from managers.file_manager import FileManager

TEST_FILE = "test_lines.txt"


class TestFileManager(unittest.TestCase):

    def tearDown(self):
        # remove the test file so it does not stay in the project
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_read_lines_yields_each_line(self):
        file_manager = FileManager(TEST_FILE)
        file_manager.write_file("a\nb\nc\n")
        self.assertEqual(list(file_manager.read_lines()), ["a", "b", "c"])

    def test_read_lines_missing_file_yields_nothing(self):
        file_manager = FileManager(TEST_FILE)
        self.assertEqual(list(file_manager.read_lines()), [])


if __name__ == "__main__":
    unittest.main()
