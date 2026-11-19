"""Predefined items."""

from models.item import Item

ITEMS = {
    "potion": {
        "name": "Potion", "description": "Restores 30 HP.",
        "item_type": "potion", "effect": {"hp": 30},
    },
    # MP is hidden for now. It will be used for spells at the end of the project.
    # "ether": {
    #     "name": "Ether", "description": "Restores 20 MP.",
    #     "item_type": "potion", "effect": {"mp": 20},
    # },
    # "elixir": {
    #     "name": "Elixir", "description": "Restores 50 HP and 50 MP.",
    #     "item_type": "potion", "effect": {"hp": 50, "mp": 50},
    # },
}

def create_item(key):
    """Returns a new Item from the ITEMS key (potion)."""
    data = ITEMS[key]
    return Item(data["name"], data["description"], data["item_type"], dict(data["effect"]))
