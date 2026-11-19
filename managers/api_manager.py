"""Monsters from the D&D 5e API (https://www.dnd5eapi.co), cached in monsters_cache.json."""

import json
import random
import urllib.error
import urllib.request

import managers.file_manager as fm

API_URL = "https://www.dnd5eapi.co/api/2014/monsters"
TIMEOUT = 3
CACHE_FILE = "monsters_cache.json"


def challenge_ratings(level):
    """Returns the D&D challenge ratings that fit a character level."""
    if level <= 1:
        return (0.125, 0.25)
    if level == 2:
        return (0.25, 0.5)
    if level == 3:
        return (0.5, 1)
    return (min(level // 2, 10),)


class ApiManager:
    """Gets monsters from the D&D 5e API and keeps them in a local cache."""

    def __init__(self):
        """Creates the file manager for the cache and loads it."""
        self._file_manager = fm.FileManager(CACHE_FILE)
        self._cache = self._load_cache()

    def fetch_monster(self, level):
        """Returns a random monster dict for the level, or None if API and cache both fail."""
        ratings = challenge_ratings(level)
        try:
            indexes = self._monster_list(ratings)
            if not indexes:
                return self._cached_monster(ratings)
            index = random.choice(indexes)
            if index not in self._cache["monsters"]:
                self._cache["monsters"][index] = self._simplify(self._get_json(f"{API_URL}/{index}"))
                self._save_cache()
            return self._cache["monsters"][index]
        except urllib.error.URLError:
            # no internet or the API is down
            return self._cached_monster(ratings)
        except TimeoutError:
            # the API took too long to answer
            return self._cached_monster(ratings)
        except json.JSONDecodeError:
            # the API answered something that is not JSON
            return self._cached_monster(ratings)
        except KeyError:
            # the JSON does not have the fields we expect
            return self._cached_monster(ratings)

    def _cached_monster(self, ratings):
        """Returns a random cached monster with one of the ratings, or None if there is none."""
        cached = [m for m in self._cache["monsters"].values() if m["challenge_rating"] in ratings]
        if not cached:
            return None
        return random.choice(cached)

    def _monster_list(self, ratings):
        """Returns the monster indexes for the ratings, from the cache or the API."""
        key = ",".join(str(rating) for rating in ratings)
        if key not in self._cache["lists"]:
            data = self._get_json(f"{API_URL}?challenge_rating={key}")
            self._cache["lists"][key] = [monster["index"] for monster in data["results"]]
            self._save_cache()
        return self._cache["lists"][key]

    def _get_json(self, url):
        """Downloads a URL and returns its JSON."""
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))

    def _simplify(self, data):
        """Keeps only the monster fields the game uses."""
        attacks = [action for action in data.get("actions", [])
                   if action.get("attack_bonus") is not None and action.get("damage")]
        attack = attacks[0] if attacks else {"name": "Claws", "attack_bonus": 2, "damage": [{"damage_dice": "1d4"}]}
        return {
            "name": data["name"],
            "hit_points": data["hit_points"],
            "armor_class": data["armor_class"][0]["value"],
            "challenge_rating": data["challenge_rating"],
            "xp": data["xp"],
            "attack_name": attack["name"],
            "attack_bonus": attack["attack_bonus"],
            "damage_dice": attack["damage"][0].get("damage_dice", "1d4"),
        }

    def _load_cache(self):
        """Returns the cache from the file, or an empty cache if it is missing or broken."""
        try:
            cache = json.loads(self._file_manager.read_file() or "{}")
        except json.JSONDecodeError:
            cache = {}
        cache.setdefault("lists", {})
        cache.setdefault("monsters", {})
        return cache

    def _save_cache(self):
        """Writes the cache to the file."""
        self._file_manager.write_file(json.dumps(self._cache, indent=2))
