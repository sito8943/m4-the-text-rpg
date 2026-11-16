from models.character_class import CharacterClass

CLASSES = {
    "warrior": {
        "name": "Warrior", "hp": 120, "mp": 20, "atk": 12, "defense": 8,
        "hp_multiplier": 1.5, "mp_multiplier": 0.5, "atk_multiplier": 1.2, "defense_multiplier": 1.3,
    },
    "mage": {
        "name": "Mage", "hp": 80, "mp": 100, "atk": 6, "defense": 4,
        "hp_multiplier": 0.8, "mp_multiplier": 1.8, "atk_multiplier": 1.5, "defense_multiplier": 0.7,
    },
    "rogue": {
        "name": "Rogue", "hp": 95, "mp": 40, "atk": 14, "defense": 5,
        "hp_multiplier": 1.0, "mp_multiplier": 0.8, "atk_multiplier": 1.6, "defense_multiplier": 0.9,
    },
}


def create_class(key):
    return CharacterClass(**CLASSES[key])
