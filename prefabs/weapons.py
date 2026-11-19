"""Predefined weapons."""

from models.weapon import Weapon

WEAPONS = {
    "unarmed": {"name": "Unarmed", "damage": 1},
    "dagger": {"name": "Dagger", "damage": 3},
    "sword": {"name": "Sword", "damage": 5},
    "bow": {"name": "Bow", "damage": 4},
    "staff": {"name": "Staff", "damage": 3},
    "axe": {"name": "Axe", "damage": 7},
    "war_hammer": {"name": "War Hammer", "damage": 10},
}


def create_weapon(key):
    """Returns a new Weapon from the WEAPONS key."""
    return Weapon(**WEAPONS[key])
