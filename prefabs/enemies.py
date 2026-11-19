"""Predefined enemies (used when the D&D API is not available) and API enemy conversion."""

import utils.stats as st

from models.character_class import CharacterClass
from models.weapon import Weapon
from models.enemy import Enemy
from prefabs.weapons import create_weapon

ENEMIES = {
    "slime": {
        "name": "Slime", "weapon": "unarmed", "xp_reward": 5, "gold_reward": 2,
        "cclass": {"name": "Slime", "hp": 40, "mp": 0, "atk": 4, "defense": 1},
    },
    "goblin": {
        "name": "Goblin", "weapon": "dagger", "xp_reward": 10, "gold_reward": 5,
        "cclass": {"name": "Goblin", "hp": 60, "mp": 10, "atk": 10, "defense": 3},
    },
    "wolf": {
        "name": "Wolf", "weapon": "unarmed", "xp_reward": 12, "gold_reward": 3,
        "cclass": {"name": "Wolf", "hp": 70, "mp": 0, "atk": 14, "defense": 2},
    },
    "orc": {
        "name": "Orc", "weapon": "axe", "xp_reward": 25, "gold_reward": 15,
        "cclass": {"name": "Orc", "hp": 120, "mp": 0, "atk": 18, "defense": 6,
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
        xp_reward=data["xp_reward"] + st.xp_to_next_level(level) // 3,
        gold_reward=data["gold_reward"],
    )


def create_api_enemy(monster, level=1):
    """Returns a new Enemy from a D&D API monster dict, scaled to this game's stats."""
    hp = min(20 + monster["hit_points"], 150)
    xp_reward = st.xp_to_next_level(level) // 3 + int(monster["xp"] ** 0.5)
    return Enemy(
        name=monster["name"],
        cclass=CharacterClass(name=monster["name"], hp=hp, mp=0,
                              atk=2 + monster["attack_bonus"] // 2, defense=monster["armor_class"] // 3),
        weapon=Weapon(monster["attack_name"], max(1, st.dice_average(monster["damage_dice"]) // 2)),
        level=level,
        xp_reward=xp_reward,
        gold_reward=xp_reward // 2,
    )
