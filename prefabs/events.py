"""Exploration event types, their stories and the treasure gold range."""

# Chance (in %) of each event when exploring. They must add up to 100.
EVENT_CHANCES = {
    "battle": 60,
    "nothing": 25,
    "treasure": 15,
}

EVENTS = {
    "battle": {
        "title": "Battle", "style": "red",
        "story": (
            "A shadow moves between the lines of code...",
            "Something hostile blocks your path.",
        ),
    },
    "treasure": {
        "title": "Treasure", "style": "yellow",
        "story": (
            "Your foot hits something hard in the void...",
            "It's a hidden treasure chest!",
        ),
    },
    "nothing": {
        "title": "Explore", "style": "green",
        "story": (
            "You walk into the terminal void...",
            "The air smells like burnt circuits.",
            "Nothing happens. For now.",
        ),
    },
}

TREASURE_GOLD = (5, 20)
