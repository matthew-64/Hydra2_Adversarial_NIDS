from feature_selection.adversarial_perturbation_selector import AdversarialPerturbationFeatureSelector
import unittest


class TestAdversarialPerturbationSelector(unittest.TestCase):

    def test_get_features_rate(self):
        apfs = AdversarialPerturbationFeatureSelector()
        print(set(apfs.get_features("Evasion: Rate")))
        self.assertEqual(
                {'pkts_per_sec', 'bytes_per_second'},
                set(apfs.get_features("Evasion: Rate")))

    def test_get_features_payload(self):
        apfs = AdversarialPerturbationFeatureSelector()
        self.assertEqual(
                {'bytes', 'src_bytes'},
                set(apfs.get_features("Evasion: Payload")))

    def test_get_features_pairflow(self):
        apfs = AdversarialPerturbationFeatureSelector()
        self.assertEqual(
                {'pair_flow'},
                set(apfs.get_features("Evasion: Pairflow")))

    def test_get_features_rate_pairflow(self):
        apfs = AdversarialPerturbationFeatureSelector()
        self.assertEqual(
                {'pkts_per_sec', 'pair_flow', 'bytes_per_second'},
                set(apfs.get_features("Evasion: Rate+Pairflow")))

    def test_get_features_payload_pairflow(self):
        apfs = AdversarialPerturbationFeatureSelector()
        self.assertEqual(
                {'bytes_per_packet', 'src_bytes', 'bytes', 'pair_flow', 'bytes_per_second'},
                set(apfs.get_features("Evasion: Payload+Pairflow")))

    def test_get_features_payload_rate_pairflow(self):
        apfs = AdversarialPerturbationFeatureSelector()
        self.assertEqual(
                {'pkts_per_sec', 'bytes', 'bytes_per_second', 'pair_flow', 'bytes_per_packet', 'src_bytes'},
                set(apfs.get_features("Evasion: Payload+Rate+Pairflow")))

    def test_invalid_attack_entered(self):
        apfs = AdversarialPerturbationFeatureSelector()
        self.assertRaisesRegex(
                Exception,
                "Invalid attack: ABC",
                apfs.get_features,
                "ABC")


if __name__ == '__main__':
    unittest.main()
