# THE TEXT-BASED RPG

> **Not Ogabek?** This README is the project report for grading. To install and play the game, read [HOW_TO.md](HOW_TO.md).

## Authors
- Carlos Andrés Mora González

## Description
This is an event-driven, text-based role-playing game (RPG) that runs in the terminal. In it, you create your character and venture into the vast world of the "terminal void"—an environment filled with characters and combat.

You can explore, fight enemies in turn-based battles, find treasure, level up, check your character sheet, read the battle log and save your progress. Everything happens from an interactive menu; the game only closes when you choose **Exit** or type `exit`.

## Purpose
Give the player a small, replayable adventure in the terminal, and practise building a real Python project: split into modules, with saved data, a log file, input validation and unit tests.

## How to run
```
pip3 install -r requirements.txt
cp .env.example .env   # optional: the game has default values
python3 ./main.py
```

Requirements, step-by-step setup and how to play: see [HOW_TO.md](HOW_TO.md).

## How to run tests
```
python3 -m unittest discover tests -v
```

Note: Why unittest instead of pytest? Because it comes with python :)
Note: Why unit tests with classes? Because unittest force you to use classes :)
Note: Why @patch? Because is for mocking and preventing the real calling of methods which affect files or other external things :)

## Project structure

| Folder | Content |
|---|---|
| `main.py` | Entry point. Only loads the config (`config.setup`), creates the `GameManager` and starts the game. |
| `managers/` | Game logic: menus, actions, events, battles, API, files, SQLite database, log, save/load, screens and validation. |
| `models/` | Game objects: `Character`, `Enemy`, `CharacterClass`, `Weapon`, `Item`, `Inventory`, `Wallet`. |
| `prefabs/` | Game data: classes, enemies, weapons, items, shop prices, events and validation rules. |
| `utils/` | Helpers: `.env` and logging setup (`config.py`), console drawing (`console.py`), stat formulas (`stats.py`) and custom decorators (`decorators.py`). |
| `tests/` | Unit tests (`unittest`). |

## Todolist
- [x] Generator function (`yield`)
- [x] Custom decorator
- [x] `.env` file for config/secrets with `python-dotenv` (+ `.env.example`, `.env` in `.gitignore`)
- [x] Work on branches and merge through pull requests
- [x] Logging with the `logging` module
- [x] Save data in a SQL database (`sqlite3`) instead of JSON
- [ ] Connect an AI
- [ ] Atomic commits on new days
- [ ] GIF/video of the game in the README
- [ ] Link the public APK deploy in the README
- [ ] README: Screenshots, Usage, Approximate Total, Acknowledgments and Support sections
- [ ] README "Graded points": add the new final criteria
- [ ] On-time submission

## Graded points
List of the criteria this project covers and where to find them.

### Menu
- **Interactive menu:** `GameManager._home_screen` and `GameManager._game_menu` (`managers/game_manager.py`) show the menus in a `while True` loop. After any action the program goes back to the menu.
- **Start over without restarting the app:** **Main Menu** (game menu) goes back to the home screen, and **New Game** (`GameManager._new_game`) asks for confirmation, empties the battle log (`LogManager.clear_log`) and replaces the current character with a new one.
- **One menu function:** home, game and battle menus are all drawn by `ScreenManager.print_menu`, so they look and behave the same.
- **Exit only with a specific command:** the program closes only when the player types `exit` (any case) or picks the **Exit** option in the home or game menu (`EXIT_COMMAND` and `GameManager._exit_game`).
- **Well-thought-out design:** `utils/console.py` uses `rich` for coloured panels and titles; `slow_print` writes story text letter by letter; `ScreenManager.message` can add delays (`wait`).

### Decomposition
- `main.py` only calls `config.setup()` and `GameManager().start_game()`.
- All other functions are in separate modules (`managers/`, `models/`, `prefabs/`, `utils/`).
- No file has more than 300 lines (the biggest has about 100).

### External files
- **SQL database:** the character is saved in a SQLite database, `game.db` (`sqlite3`, standard library).
  - `DatabaseManager` (`managers/database_manager.py`) creates the tables and runs the SQL: `CREATE TABLE IF NOT EXISTS`, `DELETE`, `INSERT` and `SELECT`.
  - 3 tables: `character` (one row: name, level, HP, XP, gold, class, weapon), `inventory` (one row per item) and `defeated_enemies` (one row per enemy; `PRIMARY KEY` keeps names unique, like the `set`).
  - Values are passed with `?` placeholders, never inside the SQL text, to prevent SQL injection.
  - `PlayerDataManager.save_data` / `load_data` (`managers/player_data_manager.py`) use it with `Character.to_dict` / `from_dict`.
- **Log file:** every battle turn is written to `battle_log.txt` instead of being kept only on screen.
  - Send new data to the file: `LogManager.write_log`.
  - Display the contents of the file: `LogManager.show_log` (menu option **5. Log**).
- **API cache:** monsters downloaded from the API are saved in `monsters_cache.json`, so they are not downloaded again and still work offline.
- **File access:** `FileManager` (`managers/file_manager.py`) reads, appends and writes files.

### API
- Enemies come from the [D&D 5e API](https://www.dnd5eapi.co) (334 monsters, free, no key).
- `ApiManager.fetch_monster` (`managers/api_manager.py`) picks a random monster whose challenge rating fits the character level (`challenge_ratings`).
- `create_api_enemy` (`prefabs/enemies.py`) converts the monster's HP, armor, attack and XP to this game's stats.
- Uses `urllib` from the standard library, so no extra package is needed.
- If there is no internet: a cached monster is used. If there is no cache either: an enemy from `prefabs/enemies.py` is used (`EventManager._spawn_enemy`).

### Config (.env)
- Settings live in a `.env` file, loaded with `python-dotenv` by `utils/config.py` (`setup`), which `main.py` calls first.
- `.env.example` is the template in the repo. `.env` is in `.gitignore`, so secrets are never committed.
- Values: `API_URL` and `API_TIMEOUT` (read in `ApiManager.__init__`), `LOG_LEVEL` (read in `config.setup`).
- Every value has a default, so the game works without a `.env`.
- Validation: `API_TIMEOUT` that is not a number (`ValueError`) and an unknown `LOG_LEVEL` use the default and write a warning to `game.log`.

### Logging
- The `logging` module writes a technical log to `game.log` (for the developer). It is separate from `battle_log.txt`, which is part of the game and is shown to the player.
- Set up once in `utils/config.py` (`setup`, called first in `main.py`) with `logging.basicConfig` (file, level `INFO`, format `date | level | message`).
- **info:** game started, game loaded, game saved, new game, game closed (`GameManager`, `PlayerDataManager`).
- **warning:** the API fails and the cache is used (`ApiManager.fetch_monster`), or both fail and a prefab enemy is used (`EventManager._spawn_enemy`).
- **error:** broken or unwritable save database (`PlayerDataManager`) or broken monster cache (`ApiManager._load_cache`).

### Data structures
- **dict:** menu options (`GameManager._game_menu`), battle actions (`BattleManager.start`), prefabs (`CLASSES`, `ENEMIES`, `ITEMS`, `WEAPONS`, `EVENTS`, `EVENT_CHANCES`, `SHOP_ITEMS`, `SHOP_WEAPONS`), save data (`to_dict` / `from_dict`).
- **list:** inventory items (`Inventory.items`, shown and used in `ActionManager._inventory`), battle turn text, log lines.
- **set:** enemies already defeated (`Character.defeated_enemies`), so each name is stored once.
- **generator:** `FileManager.read_lines` (`managers/file_manager.py`) yields the lines of a file one by one with `yield`, so the whole file is not loaded at once. `LogManager.show_log` uses it to show the battle log, and `LogManager.count_wins` loops over it (one line in memory at a time) to show **Battles won** in the character sheet.
- **decorator:** `requires_character` (`utils/decorators.py`) wraps the game menu actions (`_character`, `_explore`, `_inventory`, `_shop` in `ActionManager`). If there is no character it shows an error instead of running the action, so the check is written once.
- **tuple:** fixed data that never changes: `BATTLE_OPTIONS`, `GAME_OPTIONS`, `TREASURE_GOLD`, event stories, and each shop offer `(kind, key, price)` in `ActionManager._shop`.

### Exceptions
- `FileManager.read_file` handles `FileNotFoundError` (creates the file).
- `PlayerDataManager.load_data` and `save_data` handle `sqlite3.DatabaseError` (broken `game.db`).
- `ApiManager.fetch_monster` handles `URLError` (no internet), `TimeoutError` (slow API), `json.JSONDecodeError` (bad answer) and `KeyError` (missing fields), and falls back to the cache.
- `ApiManager._load_cache` handles `json.JSONDecodeError` (broken cache file).

### Data validation
- `ValidationManager.validate` (`managers/validation_manager.py`) checks a value against a rule set and returns the first error.
- Rules live in `prefabs/validations.py`: the name cannot be empty, needs at least 3 letters and can only contain letters and spaces.
- `GameManager._create_character` asks again until the name is valid.
- `GameManager._choose_class` asks again until the player picks one of the classes in `prefabs/classes.py`.
- Menus reject invalid choices and show an error.

### Functions documentation
- Every module, class and function has a docstring.

### Unit tests
- 73 tests in `tests/` for `Character`, `Wallet`, `ValidationManager`, `GameManager` (character creation, class choice, starter weapon, New Game, Main Menu, `exit` command), the inventory and the shop (`ActionManager`), event chances (`EventManager`), the `read_lines` generator (`FileManager`), battles won and clearing the log (`LogManager`), the `requires_character` decorator, `logging` messages (`assertLogs`), `.env` values (`patch.dict(os.environ)`), the SQLite save (`DatabaseManager`) and the API (`ApiManager`, offline fallback, stat conversion). API tests use `@patch`, so they don't need internet.

### Git
- Atomic commits with a prefix (`add:`, `change:`, `fix:`, `feat:`).
- `README.md` and `requirements.txt` included.
- **Pull requests:** each final feature was developed on its own branch and merged through a pull request ([#1](https://github.com/sito8943/m4-the-text-rpg-midterm/pull/1) generator, [#2](https://github.com/sito8943/m4-the-text-rpg-midterm/pull/2) decorator, [#3](https://github.com/sito8943/m4-the-text-rpg-midterm/pull/3) logging, [#4](https://github.com/sito8943/m4-the-text-rpg-midterm/pull/4) .env).
