"""Predefined enemies."""

from models.character_class import CharacterClass
from models.enemy import Enemy
from prefabs.weapons import create_weapon

ENEMIES = {
    "slime": {
        "name": "Slime", "weapon": "unarmed", "xp_reward": 5, "gold_reward": 2,
        "cclass": {"name": "Slime", "hp": 40, "mp": 0, "atk": 4, "defense": 1},
    },
    "goblin": {
        "name": "Goblin", "weapon": "dagger", "xp_reward": 10, "gold_reward": 5,
        "cclass": {"name": "Goblin", "hp": 60, "mp": 10, "atk": 7, "defense": 3},
    },
    "wolf": {
        "name": "Wolf", "weapon": "unarmed", "xp_reward": 12, "gold_reward": 3,
        "cclass": {"name": "Wolf", "hp": 70, "mp": 0, "atk": 10, "defense": 2},
    },
    "orc": {
        "name": "Orc", "weapon": "axe", "xp_reward": 25, "gold_reward": 15,
        "cclass": {"name": "Orc", "hp": 120, "mp": 0, "atk": 12, "defense": 6,
                   "hp_multiplier": 1.5},
    },
}


def create_enemy(key, level=1):
    """Returns a new Enemy from the ENEMIES key at the given level."""
    data = ENEMIES[key]
    return Enemy(
        name=data["name"],
        cclass=CharacterClass(**data["cclass"]),
        weapon=create_weapon(data["weapon"]),
        level=level,
        xp_reward=data["xp_reward"],
        gold_reward=data["gold_reward"],
    )
