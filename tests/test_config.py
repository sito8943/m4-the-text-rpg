import os
import unittest
from unittest.mock import patch

from managers.api_manager import ApiManager, DEFAULT_API_URL, DEFAULT_TIMEOUT


# no cache file is read or written during the tests
@patch("managers.file_manager.FileManager.write_file")
@patch("managers.file_manager.FileManager.read_file", return_value="")
class TestEnvConfig(unittest.TestCase):

    # clear=True removes the real environment, so the tests don't depend on your .env
    @patch.dict(os.environ, {}, clear=True)
    def test_without_env_uses_defaults(self, mock_read, mock_write):
        api = ApiManager()

        self.assertEqual(api._api_url, DEFAULT_API_URL)
        self.assertEqual(api._timeout, DEFAULT_TIMEOUT)

    @patch.dict(os.environ, {"API_URL": "http://test.local/monsters", "API_TIMEOUT": "5"}, clear=True)
    def test_reads_values_from_env(self, mock_read, mock_write):
        api = ApiManager()

        self.assertEqual(api._api_url, "http://test.local/monsters")
        self.assertEqual(api._timeout, 5.0)

    @patch.dict(os.environ, {"API_TIMEOUT": "abc"}, clear=True)
    def test_invalid_timeout_uses_default_and_logs(self, mock_read, mock_write):
        with self.assertLogs(level="WARNING") as logs:
            api = ApiManager()

        self.assertEqual(api._timeout, DEFAULT_TIMEOUT)
        self.assertIn("API_TIMEOUT is not a number", logs.output[0])


if __name__ == "__main__":
    unittest.main()
