import unittest
from unittest.mock import patch

import utils.stats as st
from models.character import Character
from models.character_class import CharacterClass
from models.inventory import Inventory
from models.weapon import Weapon


@patch("builtins.print")
class TestCharacter(unittest.TestCase):

    def setUp(self):
        # default class: hp 100, mp 50, multipliers 1.0
        self.hero = Character("Test", CharacterClass(), Weapon(), Inventory())

    # --- gain_xp ---

    def test_gain_xp_below_threshold_keeps_level(self, _):
        self.hero.gain_xp(30)

        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.xp, 30)

    def test_gain_xp_exact_threshold_levels_up(self, _):
        self.hero.gain_xp(50)

        self.assertEqual(self.hero.level, 2)
        self.assertEqual(self.hero.xp, 0)

    def test_gain_xp_can_level_up_multiple_times(self, _):
        self.hero.gain_xp(160)  # 50 (lvl 1->2) + 100 (lvl 2->3) = 150, 10 left

        self.assertEqual(self.hero.level, 3)
        self.assertEqual(self.hero.xp, 10)

    def test_level_up_restores_hp_and_mp(self, _):
        self.hero.hp = 1
        self.hero.mp = 0

        self.hero.gain_xp(50)

        self.assertEqual(self.hero.hp, st.max_hp(self.hero.cclass, 2))
        self.assertEqual(self.hero.mp, st.max_mp(self.hero.cclass, 2))

    # --- take_damage ---

    def test_take_damage_reduces_hp(self, _):
        self.hero.take_damage(30)

        self.assertEqual(self.hero.hp, 70)

    def test_take_damage_exact_hp_reaches_zero(self, _):
        self.hero.take_damage(100)

        self.assertEqual(self.hero.hp, 0)

    def test_take_damage_never_goes_below_zero(self, _):
        self.hero.take_damage(150)

        self.assertEqual(self.hero.hp, 0)

    # --- heal ---

    def test_heal_increases_hp(self, _):
        self.hero.hp = 50

        self.hero.heal(20)

        self.assertEqual(self.hero.hp, 70)

    def test_heal_never_exceeds_max_hp(self, _):
        self.hero.hp = 90

        self.hero.heal(50)

        self.assertEqual(self.hero.hp, st.max_hp(self.hero.cclass, self.hero.level))

    # --- to_dict / from_dict ---

    def test_dict_round_trip_keeps_data(self, _):
        self.hero.gain_xp(70)
        self.hero.take_damage(15)
        self.hero.wallet.add_gold(40)
        self.hero.defeated_enemies.add("Goblin")

        copy = Character.from_dict(self.hero.to_dict())

        self.assertEqual(copy.to_dict(), self.hero.to_dict())


if __name__ == "__main__":
    unittest.main()
