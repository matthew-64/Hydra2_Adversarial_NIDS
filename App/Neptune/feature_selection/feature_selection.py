from feature_selection.adversarial_perturbation_selector import AdversarialPerturbationFeatureSelector

#################################################################################
# FeatureSelectionType class
#
# File: feature_selection.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Class to act as an enum to avoid hard coded values in FeatureSelector
#       class
#
# Usage: see FeatureSelector below
#################################################################################
class FeatureSelectionType:
    ALL = "all"
    PERTURBED = "perturbed"
    NON_PERTURBED = "non-perturbed"
    ALL_NON_PERTURBED = "all-non-perturbed"


#################################################################################
# FeatureSelector class
#
# File: feature_selection.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: class to filter out features of an attack based on the attack type and
#       the type of features you want to filter
#
# Usage:
#   - Used in FeatureSelector class to determine the adversarial features that should
#     be removed
#   - Used to pass in the features that should be perturbed by the AdversarialTrainer
#################################################################################
class FeatureSelector:

    #############################################################################
    # __init__(self, ad_attack=None, feature_selection_type=FeatureSelectionType.ALL)
    #
    # Args:
    #    ad_attack: The adversarial attack
    #    feature_selection_type: The type of features that should be selected, as
    #                            dictated in FeatureSelectionType
    #
    def __init__(self, ad_attack=None, feature_selection_type=FeatureSelectionType.ALL):
        self.__validate_feature_selection_type(feature_selection_type)
        self.attack = ad_attack
        self.feature_selection_type = feature_selection_type
        self.perturbation_feature_selector = AdversarialPerturbationFeatureSelector()

    #############################################################################
    # get_features(self, data_points)
    #
    # Args:
    #    data: The data with features that will be removed
    #
    # Returns:
    #    the data, but what the required features removed according to
    #    the feature_selection_type defined in the __init__
    #
    def select_features(self, data):
        if self.feature_selection_type == FeatureSelectionType.ALL:
            return data
        elif self.feature_selection_type == FeatureSelectionType.PERTURBED:
            return self.__select_perturbed_features(data)
        elif self.feature_selection_type == FeatureSelectionType.NON_PERTURBED:
            return self.__select_non_perturbed_features(data)
        elif self.feature_selection_type == FeatureSelectionType.ALL_NON_PERTURBED:
            return self.__select_non_perturbed_features_all_attacks(data)


    def __select_perturbed_features(self, data):
        self.feature_selection_type = FeatureSelectionType.PERTURBED
        return data[self.perturbation_feature_selector.get_features(self.attack)]

    def __select_non_perturbed_features(self, data):
        self.feature_selection_type = FeatureSelectionType.NON_PERTURBED
        return data.drop(self.perturbation_feature_selector.get_features(self.attack), axis=1)

    def __select_non_perturbed_features_all_attacks(self, data):
        self.feature_selection_type = FeatureSelectionType.ALL_NON_PERTURBED
        return data.drop(self.perturbation_feature_selector.get_all_adversarial_features(), axis=1)

    #############################################################################
    # __validate_feature_selection_type(type)
    #
    # Used in the __init__, this method will validate that a valid type of
    # preprocessing will be used.
    #
    # Args:
    #    type the type of feature selection specified in the __init__
    #
    # Exception:
    #     An exception will be thrown of the wrong type of feature selection is input.
    #     A list of acceptable inputs will be presented to the user
    #
    @staticmethod
    def __validate_feature_selection_type(feature_selection_type):
        accepted_feature_select_types = [FeatureSelectionType.ALL, FeatureSelectionType.PERTURBED,
                                         FeatureSelectionType.NON_PERTURBED, FeatureSelectionType.ALL_NON_PERTURBED]
        if feature_selection_type not in accepted_feature_select_types:
            raise Exception("Invalid FeatureSelectType. Accepted values: " + str(accepted_feature_select_types))

