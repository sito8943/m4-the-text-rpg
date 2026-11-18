import unittest
from unittest.mock import patch

from models.wallet import Wallet


@patch("builtins.print")
class TestWallet(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet("Test", gold=100)

    def test_spend_with_enough_gold(self, _):
        self.assertTrue(self.wallet.spend_gold(30))
        self.assertEqual(self.wallet.gold, 70)

    def test_spend_exact_gold(self, _):
        self.assertTrue(self.wallet.spend_gold(100))
        self.assertEqual(self.wallet.gold, 0)

    def test_spend_without_enough_gold_fails(self, _):
        self.wallet.gold = 10

        self.assertFalse(self.wallet.spend_gold(30))
        self.assertEqual(self.wallet.gold, 10)

    def test_add_gold(self, _):
        self.wallet.add_gold(25)

        self.assertEqual(self.wallet.gold, 125)


if __name__ == "__main__":
    unittest.main()
