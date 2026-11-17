EVENT_TYPES = ("battle", "treasure", "nothing")

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
