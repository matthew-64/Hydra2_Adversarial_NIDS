from feature_selection.feature_selection import FeatureSelector
from feature_selection.feature_selection import FeatureSelectionType
import pandas as pd
import unittest
import pandas.util.testing as pd_test


def read_test_data():
    return pd.read_csv("../test_resources/test_output.csv")


class TestFeatureSelection(unittest.TestCase):

    def test_raise_exception_invalid_feature_selection_type(self):
        test_passed = False
        try:
            feature_selector = FeatureSelector("Evasion: Pairflow", feature_selection_type="abc")
        except Exception as e:
            test_passed = str(e) == "Invalid FeatureSelectType. Accepted values: ['all', 'perturbed', " \
                                    "'non-perturbed', 'all-non-perturbed']"
        self.assertTrue(test_passed)

    def test_feature_selection_all(self):
        test_data = read_test_data()
        feature_selector = FeatureSelector("Evasion: Pairflow", feature_selection_type=FeatureSelectionType.ALL)

        pd_test.assert_frame_equal(
                test_data,
                feature_selector.select_features(test_data))

    def test_feature_selection_perturbed(self):
        test_data = read_test_data()
        feature_selector = FeatureSelector("Evasion: Pairflow", feature_selection_type=FeatureSelectionType.PERTURBED)

        pd_test.assert_frame_equal(
                test_data[["pair_flow"]],
                feature_selector.select_features(test_data))

    def test_feature_selection_non_perturbed(self):
        test_data = read_test_data()
        feature_selector = FeatureSelector("Evasion: Pairflow", feature_selection_type=FeatureSelectionType.NON_PERTURBED)

        pd_test.assert_frame_equal(
                test_data.drop(["pair_flow"], axis=1),
                feature_selector.select_features(test_data))

    def test_feature_selection_all_non_perturbed(self):
        test_data = read_test_data()
        feature_selector = FeatureSelector("Evasion: Pairflow", feature_selection_type=FeatureSelectionType.ALL_NON_PERTURBED)
        pd_test.assert_frame_equal(
                test_data[['eth_src', 'eth_dst', 'ip_proto', 'state_flag', 'pkts', 'src_pkts',
                          'dst_pkts', 'dst_bytes', 'packet_pair_ratio']],
                feature_selector.select_features(test_data))


if __name__ == '__main__':
    unittest.main()
