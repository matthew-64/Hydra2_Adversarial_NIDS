from attack_validator import validate_attack
import unittest
import json


def load_json(file_path):
    return json.load(open(file_path))


class TestNidsConfigValidator(unittest.TestCase):

    def test_invalid_classifier(self):
        validate_attack("abc")
        self.assertRaisesRegex(
                Exception,
                "valid attacks:",
                validate_attack,
                "abc")

if __name__ == '__main__':
    unittest.main()