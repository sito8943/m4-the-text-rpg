"""Predefined character classes."""

from models.character_class import CharacterClass

# MP is hidden for now. It will be used for spells at the end of the project.
# The "mp" values are kept so spells can use them later.
CLASSES = {
    "warrior": {
        "name": "Warrior", "hp": 100, "mp": 20, "atk": 10, "defense": 2,
        "hp_multiplier": 2, "mp_multiplier": 0.5, "atk_multiplier": 1, "defense_multiplier": 0.8,
    },
    "hunter": {
        "name": "Hunter", "hp": 80, "mp": 30, "atk": 11, "defense": 1,
        "hp_multiplier": 1.2, "mp_multiplier": 0.8, "atk_multiplier": 1.2, "defense_multiplier": 0.4,
    },
    "rogue": {
        "name": "Rogue", "hp": 75, "mp": 40, "atk": 12, "defense": 0,
        "hp_multiplier": 0.8, "mp_multiplier": 0.8, "atk_multiplier": 1.5, "defense_multiplier": 0.2,
    },
}

# Weapon each class starts with (keys of WEAPONS in prefabs/weapons.py).
# It is not inside CLASSES because CLASSES is passed straight to CharacterClass.
STARTER_WEAPONS = {
    "warrior": "sword",
    "hunter": "bow",
    "rogue": "dagger",
}


def create_class(key):
    """Returns a new CharacterClass from the CLASSES key (warrior, hunter, rogue)."""
    return CharacterClass(**CLASSES[key])
