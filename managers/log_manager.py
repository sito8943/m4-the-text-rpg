"""Battle log stored in battle_log.txt."""

import time

import managers.file_manager as fm
import managers.screen_manager as sm

LOG_LINES_SHOWN = 15

class LogManager:
    """Writes battle events to the log file and shows them."""

    def __init__(self):
        """Creates the screen manager and the file manager for battle_log.txt."""
        self._screen_manager = sm.ScreenManager()
        self._file_manager = fm.FileManager("battle_log.txt")

    def write_log(self, text):
        """Appends a line with the current time to the log file."""
        self._file_manager.append_file(f"{time.strftime('%H:%M:%S')} | {text}\n")

    def show_log(self):
        """Shows the last LOG_LINES_SHOWN lines of the log file."""
        lines = self._file_manager.read_file().splitlines()[-LOG_LINES_SHOWN:]
        if not lines:
            lines = ["Log is empty."]
        self._screen_manager.print_info_screen("Battle Log", lines)
