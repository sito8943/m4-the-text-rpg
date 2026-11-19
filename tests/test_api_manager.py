import unittest
import urllib.error
from unittest.mock import patch

from managers.api_manager import ApiManager, challenge_ratings
from prefabs.enemies import create_api_enemy
from utils.stats import dice_average

GOBLIN = {
    "name": "Goblin", "hit_points": 7, "armor_class": 15, "challenge_rating": 0.25,
    "xp": 50, "attack_name": "Scimitar", "attack_bonus": 4, "damage_dice": "1d6+2",
}


# no cache file is read or written during the tests
@patch("managers.file_manager.FileManager.write_file")
@patch("managers.file_manager.FileManager.read_file", return_value="")
class TestApiManager(unittest.TestCase):

    def test_uses_api_monster(self, mock_read, mock_write):
        api = ApiManager()
        api._cache["lists"]["0.125,0.25"] = ["goblin"]
        api._cache["monsters"]["goblin"] = GOBLIN
        self.assertEqual(api.fetch_monster(1)["name"], "Goblin")

    def test_no_internet_and_no_cache_returns_none(self, mock_read, mock_write):
        api = ApiManager()
        with patch.object(api, "_get_json", side_effect=urllib.error.URLError("offline")):
            self.assertIsNone(api.fetch_monster(1))

    def test_no_internet_uses_cached_monster(self, mock_read, mock_write):
        api = ApiManager()
        api._cache["monsters"]["goblin"] = GOBLIN
        with patch.object(api, "_get_json", side_effect=urllib.error.URLError("offline")):
            self.assertEqual(api.fetch_monster(1)["name"], "Goblin")

    def test_timeout_uses_cached_monster(self, mock_read, mock_write):
        api = ApiManager()
        api._cache["monsters"]["goblin"] = GOBLIN
        with patch.object(api, "_get_json", side_effect=TimeoutError()):
            self.assertEqual(api.fetch_monster(1)["name"], "Goblin")

    def test_broken_cache_file_starts_empty(self, mock_read, mock_write):
        mock_read.return_value = "{not json"
        api = ApiManager()
        self.assertEqual(api._cache, {"lists": {}, "monsters": {}})


class TestApiHelpers(unittest.TestCase):

    def test_challenge_ratings_grow_with_level(self):
        self.assertEqual(challenge_ratings(1), (0.125, 0.25))
        self.assertEqual(challenge_ratings(6), (3,))
        self.assertEqual(challenge_ratings(50), (10,))

    def test_dice_average(self):
        self.assertEqual(dice_average("1d6+2"), 5)
        self.assertEqual(dice_average("2d8"), 9)
        self.assertEqual(dice_average("nonsense"), 2)

    def test_create_api_enemy_scales_stats(self):
        enemy = create_api_enemy(GOBLIN, level=1)
        self.assertEqual(enemy.name, "Goblin")
        self.assertEqual(enemy.hp, 27)
        self.assertEqual(enemy.weapon.name, "Scimitar")
        self.assertEqual(enemy.xp_reward, 14)


if __name__ == "__main__":
    unittest.main()
