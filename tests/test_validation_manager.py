import unittest

from managers.validation_manager import ValidationManager
from prefabs import validations


class TestValidationManager(unittest.TestCase):

    def setUp(self):
        self.vm = ValidationManager()
        self.name_rules = validations.rules()["name"]

    def _message(self, rule, value):
        return self.name_rules[rule][0](value)

    def test_valid_name_returns_none(self):
        self.assertIsNone(self.vm.validate("Sito", "name"))

    def test_name_with_spaces_is_valid(self):
        self.assertIsNone(self.vm.validate("Sito Mora", "name"))

    def test_empty_name_returns_empty_error(self):
        self.assertEqual(self.vm.validate("", "name"), self._message("empty", ""))

    def test_short_name_returns_length_error(self):
        self.assertEqual(self.vm.validate("ab", "name"), self._message("length", "ab"))

    def test_symbols_return_letters_error(self):
        self.assertEqual(self.vm.validate("x1y", "name"), self._message("letters", "x1y"))

    def test_multiple_failures_return_first_error_only(self):
        # "a1" breaks both "length" and "letters"; "length" comes first
        self.assertEqual(self.vm.validate("a1", "name"), self._message("length", "a1"))

    def test_unknown_rule_set_raises(self):
        with self.assertRaises(KeyError):
            self.vm.validate("Sito", "unknown")


if __name__ == "__main__":
    unittest.main()
