from ensemble.ensemble import Ensemble
import numpy as np
import unittest


class TestEnsemble(unittest.TestCase):

    def test_automatic_weight_generation(self):
        dummy_classifier_list = ["classifier1", "classifier2"]
        ensemble = Ensemble(dummy_classifier_list)
        self.assertEqual(
                np.array([1, 1]).all(),
                ensemble.weights.all())

    def test_classifier_list_different_size_to_weight_list(self):
        dummy_classifier_list = ["classifier1", "classifier2"]
        weights = [1]
        test_passed = False
        try:
            ensemble = Ensemble(dummy_classifier_list, weights=weights)
        except Exception as e:
            if str(e) == "classifier_list and weights must have same length":
                test_passed = True
        self.assertTrue(test_passed)


if __name__ == '__main__':
    unittest.main()