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
| `main.py` | Entry point. Only creates the `GameManager` and starts the game. |
| `managers/` | Game logic: menus, actions, events, battles, API, files, log, save/load, screens and validation. |
| `models/` | Game objects: `Character`, `Enemy`, `CharacterClass`, `Weapon`, `Item`, `Inventory`, `Wallet`. |
| `prefabs/` | Game data: classes, enemies, weapons, items, shop prices, events and validation rules. |
| `utils/` | Helpers: console drawing (`console.py`), stat formulas (`stats.py`) and custom decorators (`decorators.py`). |
| `tests/` | Unit tests (`unittest`). |

## Todolist
- [x] Generator function (`yield`)
- [x] Custom decorator
- [ ] `.env` file for config/secrets with `python-dotenv` (+ `.env.example`, `.env` in `.gitignore`)
- [ ] Work on branches and merge through pull requests
- [ ] Logging with the `logging` module
- [ ] Save data in a SQL database (`sqlite3`) instead of JSON
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
- `main.py` only calls `GameManager().start_game()`.
- All other functions are in separate modules (`managers/`, `models/`, `prefabs/`, `utils/`).
- No file has more than 300 lines (the biggest has about 100).

### External files
- **Save data:** `PlayerDataManager.save_data` / `load_data` (`managers/player_data_manager.py`) save and load the character as JSON in `game_data.json`.
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

### Data structures
- **dict:** menu options (`GameManager._game_menu`), battle actions (`BattleManager.start`), prefabs (`CLASSES`, `ENEMIES`, `ITEMS`, `WEAPONS`, `EVENTS`, `EVENT_CHANCES`, `SHOP_ITEMS`, `SHOP_WEAPONS`), save data (`to_dict` / `from_dict`).
- **list:** inventory items (`Inventory.items`, shown and used in `ActionManager._inventory`), battle turn text, log lines.
- **set:** enemies already defeated (`Character.defeated_enemies`), so each name is stored once.
- **generator:** `FileManager.read_lines` (`managers/file_manager.py`) yields the lines of a file one by one with `yield`, so the whole file is not loaded at once. `LogManager.show_log` uses it to show the battle log, and `LogManager.count_wins` loops over it (one line in memory at a time) to show **Battles won** in the character sheet.
- **decorator:** `requires_character` (`utils/decorators.py`) wraps the game menu actions (`_character`, `_explore`, `_inventory`, `_shop` in `ActionManager`). If there is no character it shows an error instead of running the action, so the check is written once.
- **tuple:** fixed data that never changes: `BATTLE_OPTIONS`, `GAME_OPTIONS`, `TREASURE_GOLD`, event stories, and each shop offer `(kind, key, price)` in `ActionManager._shop`.

### Exceptions
- `FileManager.read_file` handles `FileNotFoundError` (creates the file).
- `PlayerDataManager.load_data` handles `json.JSONDecodeError` (broken save file).
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
- 63 tests in `tests/` for `Character`, `Wallet`, `ValidationManager`, `GameManager` (character creation, class choice, starter weapon, New Game, Main Menu, `exit` command), the inventory and the shop (`ActionManager`), event chances (`EventManager`), the `read_lines` generator (`FileManager`), battles won and clearing the log (`LogManager`), the `requires_character` decorator and the API (`ApiManager`, offline fallback, stat conversion). API tests use `@patch`, so they don't need internet.

### Git
- Atomic commits with a prefix (`add:`, `change:`, `fix:`, `feat:`).
- `README.md` and `requirements.txt` included.
