from nids_config_validator import NidsConfigValidator
import unittest
import json


def load_json(file_path):
    return json.load(open(file_path))


class TestNidsConfigValidator(unittest.TestCase):

    def test_valid_feature_selection_config_no_error(self):
        nids_config_validator = NidsConfigValidator()
        nids_config_validator.validate_nids_config(load_json("test_resources/nids_config_valid_feature_selection.json"))

    def test_valid_ad_training_config_no_error(self):
        nids_config_validator = NidsConfigValidator()
        nids_config_validator.validate_nids_config(load_json("test_resources/nids_config_valid_ad_train.json"))

    def test_invalid_classifier(self):
        nids_config_validator = NidsConfigValidator()
        self.assertRaisesRegex(
                Exception,
                "Invalid input for 'classifiers'",
                nids_config_validator.validate_nids_config,
                load_json("test_resources/nids_config_invalid_classifier.json"))

    def test_invalid_ad_training(self):
        nids_config_validator = NidsConfigValidator()
        self.assertRaisesRegex(
                Exception,
                "Invalid input for 'adversarial_training_types'",
                nids_config_validator.validate_nids_config,
                load_json("test_resources/nids_config_invalid_ad_training.json"))

    def test_invalid_feature_selection(self):
        nids_config_validator = NidsConfigValidator()
        self.assertRaisesRegex(
                Exception,
                "Invalid input for 'feature_selection_type'",
                nids_config_validator.validate_nids_config,
                load_json("test_resources/nids_config_invalid_feature_selection.json"))

    def test_invalid_ensemble_length(self):
        nids_config_validator = NidsConfigValidator()
        self.assertRaisesRegex(
                Exception,
                "The 'classifiers', 'weights' and 'adversarial_training_types' are not the same length",
                nids_config_validator.validate_nids_config,
                load_json("test_resources/nids_config_invalid_ensemble_length.json"))

    def test_invlalid_ensemble_vote_type(self):
        nids_config_validator = NidsConfigValidator()
        self.assertRaisesRegex(
                Exception,
                "Invalid input for 'ensemble_vote_type'",
                nids_config_validator.validate_nids_config,
                load_json("test_resources/nids_config_invalid_ensemble_vote_type.json"))

    def test_incompatible_classifier(self):
        nids_config_validator = NidsConfigValidator()
        self.assertRaisesRegex(
                Exception,
                "Classifier RF incompatible with FGSM",
                nids_config_validator.validate_nids_config,
                load_json("test_resources/nids_config_incompatible_classifier.json"))

    def test_not_feature_selection_and_ad_training(self):
        nids_config_validator = NidsConfigValidator()
        self.assertRaisesRegex(
                Exception,
                "You cannot perform adversarial training while feature selection is not 'all'",
                nids_config_validator.validate_nids_config,
                load_json("test_resources/nids_config_feat_selection_and_ad_training.json"))


if __name__ == '__main__':
    unittest.main()