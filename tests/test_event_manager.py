import unittest
from collections import Counter
from unittest.mock import patch

from managers.event_manager import EventManager
from prefabs.events import EVENT_CHANCES


class TestGenerateEvent(unittest.TestCase):

    def setUp(self):
        self.events = EventManager()

    def _event_for_roll(self, roll):
        """Returns the event when the dice (1-100) shows the given number."""
        with patch("random.randint", return_value=roll):
            return self.events.generate_event()

    def test_chances_add_up_to_100(self):
        self.assertEqual(sum(EVENT_CHANCES.values()), 100)

    def test_each_event_gets_its_range_of_rolls(self):
        # e.g. battle 65, nothing 25, treasure 10 -> 1-65 battle, 66-90 nothing, 91-100 treasure
        first = 1
        for event_type, chance in EVENT_CHANCES.items():
            last = first + chance - 1
            self.assertEqual(self._event_for_roll(first), event_type)
            self.assertEqual(self._event_for_roll(last), event_type)
            first = last + 1

    def test_battle_is_the_most_common_event(self):
        counts = Counter(self.events.generate_event() for _ in range(1000))
        self.assertGreater(counts["battle"], counts["nothing"])
        self.assertGreater(counts["nothing"], counts["treasure"])


if __name__ == "__main__":
    unittest.main()
