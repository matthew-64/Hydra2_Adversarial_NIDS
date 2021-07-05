from preprocessing.preporcessor import Preprocessor
import pandas as pd
import unittest


def read_test_data():
    return pd.read_csv("../test_resources/test_output.csv")


class TestFeatureSelection(unittest.TestCase):

    def test_invalid_preprocessing_type(self):
        test_passed = False
        try:
            preprocessor = Preprocessor(preprocessing_type="abc")
        except Exception as e:
            test_passed = str(e) == "Invalid preprocessing type. Accepted preprocessing types: " \
                                    "['normalise', 'standardise', 'robust', 'none']"
        self.assertTrue(test_passed)

    def test_exception_raised_fit_before_transform(self):
        test_data = read_test_data()
        preprocessor = Preprocessor(preprocessing_type="normalise")
        self.assertRaisesRegex(
                AttributeError,
                "This preprocessor instance is not fitted yet. Call 'fit' with appropriate arguments before using this "
                "estimator",
                preprocessor.transform,
                test_data)


if __name__ == '__main__':
    unittest.main()
