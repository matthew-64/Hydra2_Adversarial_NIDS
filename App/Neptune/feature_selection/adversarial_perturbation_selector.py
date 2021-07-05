#################################################################################
# AdversarialPerturbationFeatureSelector class
#
# File: adversarial_perturbation_selector.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Class that will predict the features that will be perturbed from the
#       specific adversarial attack
#
# Usage:
#   - Used in FeatureSelector class to determine the adversarial features that should
#     be removed
#   - Used to pass in the features that should be perturbed by the AdversarialTrainer
#################################################################################
class AdversarialPerturbationFeatureSelector:

    #############################################################################
    # get_features(self, ad_attack)
    #
    # Args:
    #    ad_attack: The adversarial attack
    #
    # Returns:
    #    A list of features that will be perturbed by the ad_attack
    #
    # Exception:
    #    If the attack is not recognised, an exception will be thrown informing the user
    def get_features(self, ad_attack):
        if ad_attack == "Evasion: Rate":
            return self.__get_rate_features()
        elif ad_attack == "Evasion: Payload":
            return ["bytes", "src_bytes"]
        elif ad_attack == "Evasion: Pairflow":
            return self.__get_pairflow_features()
        elif ad_attack == "Evasion: Rate+Payload":
            return self.__remove_duplicates(
                self.__get_rate_features() +
                self.__get_payload_features())
        elif ad_attack == "Evasion: Rate+Pairflow":
            return self.__remove_duplicates(
                self.__get_rate_features() +
                self.__get_pairflow_features())
        elif ad_attack == "Evasion: Payload+Pairflow":
            return self.__remove_duplicates(
                self.__get_payload_features() +
                self.__get_pairflow_features())
        elif ad_attack == "Evasion: Payload+Rate+Pairflow":
            return self.__remove_duplicates(
                self.__get_payload_features() +
                self.__get_rate_features() +
                self.__get_pairflow_features())
        else:
            raise Exception("Invalid attack: " + str(ad_attack))

    #############################################################################
    # get_all_adversarial_features(self)
    #
    # Returns:
    #    A list of all features that could be perturbed by any adversarial attack
    #
    def get_all_adversarial_features(self):
        return self.__remove_duplicates(
            self.__get_payload_features() +
            self.__get_rate_features() +
            self.__get_pairflow_features())

    @staticmethod
    def __get_rate_features():
        return ["pkts_per_sec", "bytes_per_second"]

    @staticmethod
    def __get_payload_features():
        return ["bytes", "src_bytes", "bytes_per_second", "bytes_per_packet"]

    @staticmethod
    def __get_pairflow_features():
        return ["pair_flow"]

    @staticmethod
    def __get_all_features():
        return ['ip_proto', 'state_flag', 'pkts', 'src_pkts', 'dst_pkts', 'bytes',
                'src_bytes', 'dst_bytes', 'pkts_per_sec', 'bytes_per_second',
                'bytes_per_packet', 'packet_pair_ratio', 'pair_flow']

    @staticmethod
    def __remove_duplicates(my_list):
        return list(set(my_list))