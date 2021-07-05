import unittest
import numpy as np
from adversarial_training.adversarial_training_helper import generate_mask
from adversarial_training.adversarial_training_helper import select_random_portion_of_attack_indexes


class TestAdversarialTrainerHelper(unittest.TestCase):

    def test_generate_mask(self):
        feature_labels = ["a", "b", "c", "d", "e"]
        perturbed_labels = ["c", "b", "d"]
        print(generate_mask(feature_labels, perturbed_labels))
        self.assertEqual(
                generate_mask(feature_labels, perturbed_labels).all(),
                np.array([False, True, True, True, False]).all())


if __name__ == '__main__':
    unittest.main()
