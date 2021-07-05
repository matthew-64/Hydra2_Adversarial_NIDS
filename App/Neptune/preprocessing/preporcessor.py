from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
import pandas as pd


#################################################################################
# PreprocessingType class
#
# File: preprocessor.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Class to act as an enum to avoid hard coded values in Preprocessor class
#
# Usage: see Preprocessor below
#################################################################################
class PreprocessingType:
    NORMALISE = "normalise"
    STANDARDISE = "standardise"
    ROBUST = "robust"
    NONE = "none"


#################################################################################
# FeatureSelector class
#
# File: preprocessor.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Class that will preprocesses data according to the specified PreprocessingType
#
# Usage:
#   - Used in FeatureSelector class to determine the adversarial features that should
#     be removed
#   - Used to pass in the features that should be perturbed by the AdversarialTrainer
#################################################################################
class Preprocessor:

    #############################################################################
    # __init__(self, preprocessing_type=PreprocessingType.NONE)
    #
    # Args:
    #    ad_attack: The adversarial attack
    #    feature_selection_type: The type of features that should be selected, as
    #                            dictated in FeatureSelectionType
    #
    def __init__(self, preprocessing_type=PreprocessingType.NONE):
        self.__validate_preprocessing_type(preprocessing_type)
        self.preprocessing_type = preprocessing_type
        self.preprocessor = None

    #############################################################################
    # fit(self, data)
    #
    # Args:
    #    data: the data that the preprocessor will fit to
    #
    # Returns:
    #     Preprocessing object that is fitted to the data
    #
    def fit(self, data):
        if self.preprocessing_type == PreprocessingType.NORMALISE:
            self.preprocessor = Normalizer().fit(data)
        elif self.preprocessing_type == PreprocessingType.STANDARDISE:
            self.preprocessor = StandardScaler().fit(data)
        elif self.preprocessing_type == PreprocessingType.ROBUST:
            self.preprocessor = RobustScaler().fit(data)
        return self

    #############################################################################
    # transform(self, data)
    #
    # Args:
    #    data: the data that the specific preprocessor will transform
    #
    # Returns:
    #     the preprocessed data
    #
    # Exception:
    #      If the preprocessor object has not been fitted, a transformation cannot happen
    #
    def transform(self, data):
        columns = data.columns.values
        values = data.to_numpy()
        if len(values) == 0:
            print("Warning: Found array with 0 sample(s) while a minimum of 1 is required")
        try:
            if self.preprocessing_type == PreprocessingType.NORMALISE or \
                    self.preprocessing_type == PreprocessingType.STANDARDISE or \
                    self.preprocessing_type == PreprocessingType.ROBUST:
                values = self.preprocessor.transform(data)
        except AttributeError as ae:
            raise AttributeError("This preprocessor instance is not fitted yet. "
                                 "Call 'fit' with appropriate arguments before using this estimator.") from ae
        return pd.DataFrame(data=values, columns=columns)

    #############################################################################
    # fit_transform(self, data)
    #
    #  In sequence, it will fit and then transform the data, meaning two seperat functions will
    #  not need to be called
    #
    # Args:
    #    data: the data that the Preprocessor will transform
    #
    # Returns:
    #     the preprocessed data
    #
    def fit_transform(self, data):
        return self.fit(data).transform(data)

    #############################################################################
    # __validate_preprocessing_type(type)
    #
    # Used in the __init__, this method will validate that the type of preprocessing
    # specified is of type PreprocessingType
    #
    # Args:
    #    pp_type: the value of preprocessing_type specified in the __init__
    #
    # Exception:
    #     An exception will be thrown if the pp_type is not a valid form member of
    #     PreprocessingType
    #
    @staticmethod
    def __validate_preprocessing_type(pp_type):
        accepted_preprocessing_types = [
                PreprocessingType.NORMALISE,
                PreprocessingType.STANDARDISE,
                PreprocessingType.ROBUST,
                PreprocessingType.NONE]
        if pp_type not in accepted_preprocessing_types:
            raise Exception("Invalid preprocessing type. Accepted preprocessing types: " +
                            str(accepted_preprocessing_types))
