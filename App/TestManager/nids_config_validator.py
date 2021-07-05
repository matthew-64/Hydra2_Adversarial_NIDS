from attack_validator import validate_attack

#################################################################################
# NidsConfigValidator
#
# File: nids_config_validator.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: The NidsConfigValidator will be used to validate the user input into the
#       App/nids_config/config.json config file is formatted correctly and without
#       errors. If required It will give the user feedback on amends that need to
#       be made
#
# Usage: Used in the TestManager main() to ensure the nids_config/config.json file
#        that determines the configuration of Neptune is valid.
#################################################################################

class NidsConfigValidator:

    #############################################################################
    # validate_nids_config(self, config_dict)
    #
    # Validates all required fileds of the nids config file
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    def validate_nids_config(self, config_dict):
        self.__validate_attack_feature_selection_type(config_dict)
        self.__validate_feature_selection_type(config_dict)
        self.__validate_preprocessing(config_dict)
        self.__validate_classifiers(config_dict)
        self.__validate_adversarial_training_types(config_dict)
        self.__validate_ensemble_vote_type(config_dict)
        self.__validate_ensemble_lengths(config_dict)
        self.__validate_adversarial_train_method_compatible(config_dict)
        self.__validate_attack_feature_selection(config_dict)
        self.__validate_feature_selection_xor_ad_training(config_dict)

    #############################################################################
    # __validate_attack_feature_selection_type(config_dict)
    #
    # Validates the attack feature selection type of the nids config
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_attack_feature_selection_type(config_dict):
        valid_inputs = ["", "Evasion: Rate", "Evasion: Payload", "Evasion: Pairflow", "Evasion: Rate+Payload",
                        "Evasion: Payload+Pairflow", "Evasion: Rate+Pairflow", "Evasion: Payload+Rate+Pairflow"]
        if not config_dict["attack_feature_selection"] is None and not config_dict["attack_feature_selection"] in valid_inputs:
            raise Exception("Invalid input for 'attack_feature_selection'. Valid inputs: " + str(valid_inputs))

    #############################################################################
    # __validate_feature_selection_type(config_dict)
    #
    # Validates the feature selection type of the nids config
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_feature_selection_type(config_dict):
        valid_inputs = ["all", "perturbed", "non-perturbed", "all-non-perturbed"]
        if not config_dict["feature_selection_type"] in valid_inputs:
            raise Exception("Invalid input for 'feature_selection_type', Allowed inputs: " + str(valid_inputs))

    #############################################################################
    # __validate_preprocessing(config_dict)
    #
    # Validates the preprocessing type of the nids config
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_preprocessing(config_dict):
        valid_inputs = ["none", "normalise", "standardise", "robust"]
        if not config_dict["preprocessing"] in valid_inputs:
            raise Exception("Invalid input for 'preprocessing'. Valid inputs: " + str(valid_inputs))

    #############################################################################
    # __validate_classifiers(config_dict)
    #
    # Validates the classifiers of the nids config
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_classifiers(config_dict):
        valid_inputs = ["RF", "KNN", "SVM", "LR"]
        for classifier in config_dict["classifiers"]:
            if not classifier in valid_inputs:
                raise Exception("Invalid input for 'classifiers'. Valid inputs: " + str(valid_inputs))

    #############################################################################
    # __validate_adversarial_training_types(config_dict)
    #
    # Validates the adversarial training types of the nids config.
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_adversarial_training_types(config_dict):
        valid_inputs = ["none", "FGSM", "BIM", "PGD", "HSJ"]
        for type in config_dict["adversarial_training_types"]:
            if not type in valid_inputs:
                raise Exception("Invalid input for 'adversarial_training_types'. Valid inputs: " + str(valid_inputs))

    #############################################################################
    # __validate_ensemble_vote_type(config_dict)
    #
    # Validates the ensemble vote type of the nids config
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_ensemble_vote_type(config_dict):
        valid_inputs = ["hard", "soft"]
        if not config_dict["ensemble_vote_type"] in valid_inputs:
            raise Exception("Invalid input for 'ensemble_vote_type'. Valid inputs: " + str(valid_inputs))

    #############################################################################
    # __validate_ensemble_lengths(config_dict)
    #
    # Validates there is the same numbers of classifiers, weights and adversarial
    # training types
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_ensemble_lengths(config_dict):
        is_valid = len(config_dict["classifiers"]) == len(config_dict["weights"]) and\
                    len(config_dict["classifiers"]) == len(config_dict["adversarial_training_types"])
        if not is_valid:
            raise Exception("The 'classifiers', 'weights' and 'adversarial_training_types' are not the same length")

    #############################################################################
    # __validate_adversarial_train_method_compatible(config_dict)
    #
    # The adversarial methods FGSM, BIM abd PGD require classifiers with loss gradients.
    # The classifiers with loss gradients are SVM and LR only. This method validates the
    # adversarial method is compatible with the classifier.
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_adversarial_train_method_compatible(config_dict):
        methods_that_require_loss_gradients = ["FGSM", "BIM", "PGD"]
        classifiers_that_have_loss_gradients = ["SVM", "LR"]
        for i in range(0, len(config_dict["classifiers"])):
            if config_dict["adversarial_training_types"][i] in methods_that_require_loss_gradients \
                    and config_dict["classifiers"][i] not in classifiers_that_have_loss_gradients:
                raise Exception("Classifier " + config_dict["classifiers"][i] + " incompatible with "
                                + config_dict["adversarial_training_types"][i] + ". " + str(methods_that_require_loss_gradients)
                                + " require " + str(classifiers_that_have_loss_gradients))

    #############################################################################
    # __validate_adversarial_train_method_compatible(config_dict)
    #
    # Validates that the attack that any feature selection happens according to
    # is a valid attack.
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_attack_feature_selection(config_dict):
        validate_attack(config_dict["attack_feature_selection"])


    #############################################################################
    # __validate_feature_selection_xor_ad_training(config_dict)
    #
    # Validates that the config has not got adversarial training and feature selection
    # at the same time.
    #
    # Args:
    #    config_dict: the json config file passed as a dict
    #
    # Exception:
    #    Throws exception giving user a solution as to amends that need to be made to
    #    the config file
    #
    @staticmethod
    def __validate_feature_selection_xor_ad_training(config_dict):
        if not config_dict["feature_selection_type"] == "all":
            for ad_train_type in config_dict["adversarial_training_types"]:
                if not ad_train_type == "none":
                    raise Exception("You cannot perform adversarial training while feature selection is not 'all'")

