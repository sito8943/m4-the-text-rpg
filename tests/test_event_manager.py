import unittest
from collections import Counter
from unittest.mock import patch

from managers.event_manager import EventManager


class TestGenerateEvent(unittest.TestCase):

    def setUp(self):
        self.events = EventManager()

    def _event_for_roll(self, roll):
        """Returns the event when the dice (1-100) shows the given number."""
        with patch("random.randint", return_value=roll):
            return self.events.generate_event()

    def test_rolls_1_to_60_are_battle(self):
        self.assertEqual(self._event_for_roll(1), "battle")
        self.assertEqual(self._event_for_roll(60), "battle")

    def test_rolls_61_to_85_are_nothing(self):
        self.assertEqual(self._event_for_roll(61), "nothing")
        self.assertEqual(self._event_for_roll(85), "nothing")

    def test_rolls_86_to_100_are_treasure(self):
        self.assertEqual(self._event_for_roll(86), "treasure")
        self.assertEqual(self._event_for_roll(100), "treasure")

    def test_battle_is_the_most_common_event(self):
        counts = Counter(self.events.generate_event() for _ in range(1000))
        self.assertGreater(counts["battle"], counts["nothing"])
        self.assertGreater(counts["nothing"], counts["treasure"])


if __name__ == "__main__":
    unittest.main()
