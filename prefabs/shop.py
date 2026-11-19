"""What the shop sells and the price of each thing in gold."""

# Keys of ITEMS in prefabs/items.py -> price
SHOP_ITEMS = {
    "potion": 15,
}

# Keys of WEAPONS in prefabs/weapons.py -> price
# The shop only shows the weapons that are better than the one the player has.
SHOP_WEAPONS = {
    "sword": 40,
    "axe": 80,
    "war_hammer": 150,
}
