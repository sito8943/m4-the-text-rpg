import time

import managers.file_manager as fm
import managers.screen_manager as sm

LOG_LINES_SHOWN = 15

class LogManager:
    def __init__(self):
        self._screen_manager = sm.ScreenManager()
        self._file_manager = fm.FileManager("battle_log.txt")

    def write_log(self, text):
        self._file_manager.append_file(f"{time.strftime('%H:%M:%S')} | {text}\n")

    def show_log(self):
        lines = self._file_manager.read_file().splitlines()[-LOG_LINES_SHOWN:]
        if not lines:
            lines = ["Log is empty."]
        self._screen_manager.print_info_screen("Battle Log", lines)
