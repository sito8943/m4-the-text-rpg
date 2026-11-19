# THE TEXT-BASED RPG

## Authors
- Carlos Andrés Mora González

## Description
This is an event-driven, text-based role-playing game (RPG) that runs in the terminal. In it, you create your character and venture into the vast world of the "terminal void"—an environment filled with characters and combat.

You can explore, fight enemies in turn-based battles, find treasure, level up, check your character sheet, read the battle log and save your progress. Everything happens from an interactive menu; the game only closes when you choose **Exit**.

## Purpose
Give the player a small, replayable adventure in the terminal, and practise building a real Python project: split into modules, with saved data, a log file, input validation and unit tests.

## How to run

```
pip3 install -r requirements.txt
python3 ./main.py
```

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
| `prefabs/` | Game data: classes, enemies, weapons, items, events and validation rules. |
| `utils/` | Helpers: console drawing (`console.py`) and stat formulas (`stats.py`). |
| `tests/` | Unit tests (`unittest`). |

## Todolist
- [x] Interactive menu that returns after every action
- [x] New Game and Main Menu options to start over without restarting the app
- [x] Character creation with name validation
- [x] Explore with random events (battle, treasure, nothing)
- [x] Turn-based battles (attack, use potion, flee)
- [x] XP, levels and gold
- [x] Save and load the game (`game_data.txt`)
- [x] Battle log file (`battle_log.txt`) with a screen to read it
- [x] Coloured screens and slow-printed text with `rich`
- [x] Unit tests
- [ ] Inventory screen: list and use items
- [ ] Shop: buy items with gold
- [ ] Choose a class (warrior, mage, rogue) when creating the character
- [x] Enemies from the D&D 5e API, with a local cache and prefab enemies as backup

## Graded points
List of the criteria this project covers and where to find them.

### Menu
- **Interactive menu:** `GameManager._home_screen` and `GameManager._game_menu` (`managers/game_manager.py`) show the menus in a `while True` loop. After any action the program goes back to the menu.
- **Start over without restarting the app:** **Main Menu** (game menu) goes back to the home screen, and **New Game** (`GameManager._new_game`) asks for confirmation and replaces the current character with a new one.
- **One menu function:** home, game and battle menus are all drawn by `ScreenManager.print_menu`, so they look and behave the same.
- **Exit only with a specific command:** the program closes only when the player types `exit` (any case) or picks the **Exit** option in the home or game menu (`EXIT_COMMAND` and `GameManager._exit_game`).
- **Well-thought-out design:** `utils/console.py` uses `rich` for coloured panels and titles; `slow_print` writes story text letter by letter; `ScreenManager.message` can add delays (`wait`).

### Decomposition
- `main.py` only calls `GameManager().start_game()`.
- All other functions are in separate modules (`managers/`, `models/`, `prefabs/`, `utils/`).
- No file has more than 300 lines (the biggest has about 100).

### External files
- **Save data:** `PlayerDataManager.save_data` / `load_data` (`managers/player_data_manager.py`) save and load the character as JSON in `game_data.txt`.
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
- **dict:** menu options (`GameManager._game_menu`), battle actions (`BattleManager.start`), prefabs (`CLASSES`, `ENEMIES`, `ITEMS`, `WEAPONS`, `EVENTS`), save data (`to_dict` / `from_dict`).
- **list:** inventory items (`Inventory.items`), battle turn text, log lines.
- **set:** enemies already defeated (`Character.defeated_enemies`), so each name is stored once.
- **tuple:** fixed data that never changes: `EVENT_TYPES`, `BATTLE_OPTIONS`, `TREASURE_GOLD`, event stories.

### Exceptions
- `FileManager.read_file` handles `FileNotFoundError` (creates the file).
- `PlayerDataManager.load_data` handles `json.JSONDecodeError` (broken save file).
- `ApiManager.fetch_monster` handles `URLError` (no internet), `TimeoutError` (slow API), `json.JSONDecodeError` (bad answer) and `KeyError` (missing fields), and falls back to the cache.
- `ApiManager._load_cache` handles `json.JSONDecodeError` (broken cache file).

### Data validation
- `ValidationManager.validate` (`managers/validation_manager.py`) checks a value against a rule set and returns the first error.
- Rules live in `prefabs/validations.py`: the name cannot be empty, needs at least 3 letters and can only contain letters and spaces.
- `GameManager._create_character` asks again until the name is valid.
- Menus reject invalid choices and show an error.

### Functions documentation
- Every module, class and function has a docstring.

### Unit tests
- 40 tests in `tests/` for `Character`, `Wallet`, `ValidationManager`, `GameManager` (character creation, New Game, Main Menu, `exit` command) and the API (`ApiManager`, offline fallback, stat conversion). API tests use `@patch`, so they don't need internet.

### Git
- Atomic commits with a prefix (`add:`, `change:`, `fix:`, `feat:`).
- `README.md` and `requirements.txt` included.
