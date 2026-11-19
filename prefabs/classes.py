"""Predefined character classes."""

from models.character_class import CharacterClass

# MP is hidden for now. It will be used for spells at the end of the project.
# The "mp" values are kept so spells can use them later.
CLASSES = {
    "warrior": {
        "name": "Warrior", "hp": 120, "mp": 20, "atk": 12, "defense": 8,
        "hp_multiplier": 1.5, "mp_multiplier": 0.5, "atk_multiplier": 1.2, "defense_multiplier": 1.3,
    },
    "hunter": {
        "name": "Hunter", "hp": 100, "mp": 30, "atk": 13, "defense": 6,
        "hp_multiplier": 1.1, "mp_multiplier": 0.8, "atk_multiplier": 1.4, "defense_multiplier": 1.0,
    },
    "rogue": {
        "name": "Rogue", "hp": 95, "mp": 40, "atk": 14, "defense": 5,
        "hp_multiplier": 1.0, "mp_multiplier": 0.8, "atk_multiplier": 1.6, "defense_multiplier": 0.9,
    },
}


def create_class(key):
    """Returns a new CharacterClass from the CLASSES key (warrior, hunter, rogue)."""
    return CharacterClass(**CLASSES[key])
