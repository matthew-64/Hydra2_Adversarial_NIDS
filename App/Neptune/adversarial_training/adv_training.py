from art.attacks.evasion import FastGradientMethod
from art.attacks.evasion import BasicIterativeMethod
from art.attacks.evasion import ProjectedGradientDescent
from art.attacks.evasion import HopSkipJump
from adversarial_training.adversarial_training_helper import generate_mask
from adversarial_training.adversarial_training_helper import select_random_portion_of_attack_indexes
from adversarial_training.adversarial_training_helper import calculate_eps


#################################################################################
# AdversarialAttackType class
#
# File: adv_training.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Class to act as an enum to avoid hard coded values in AdversarialTrainer
#       class
#
# Usage: see AdversarialTrainer below
#################################################################################
class AdversarialAttackType:
    FGSM = "FGSM"
    BIM = "BIM"
    PGD = "PGD"
    HSJ = "HSJ"


#################################################################################
# AdversarialTrainer class
#
# File: adv_training.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Used to preform adversarial training on a classifier
#
# Usage: Used in the Neptune main() to adversarially train classifiers when required
#################################################################################
class AdversarialTrainer:

    #############################################################################
    # train_on_ad_examples(self, x, y, adversarial_training_method, art_classifier,
    #                      features_to_perturb, proportion_attack_to_perturb=0.4,
    #                      relative_eps=0.3, relative_eps_step=0.1)
    #
    # Calls the insert_ad_samples(...) method to insert adversarial samples into
    # the training data. The classifier will then be trained on this data to detect
    # the adversarial samples
    #
    # Args:
    #    x: The features of the flow samples
    #    y: the labels of the flow samples
    #    adversarial_training_method: the adversarial evasion attack method which will
    #                                 target the art_classifier to produce adversarial
    #                                 samples
    #    art_classifier: A classifier that is from the adversarial-robustness-toolbox
    #    features_to_perturb: The features of x that should be perturbed by the
    #                         adversarial_training_method.
    #    proportion_attack_to_perturb: the proportion of SYN Flood flow samples that will
    #                         be replaced by their adversarial counterpart.
    #    relative_eps: attack step size relative the mean size of the input for each feature
    #    relative_eps_step: Relative (to the to mean size of each feature) step size of
    #                       input variation for minimal perturbation computation
    #
    # Returns:
    #    An adversarially trained ML classifier
    #
    def train_on_ad_examples(self, x, y, adversarial_training_method, art_classifier, features_to_perturb,
                             proportion_attack_to_perturb=0.4, relative_eps=0.3, relative_eps_step=0.1):

        x_with_adv_samples = self.insert_ad_samples(x, y, adversarial_training_method,
                                                    art_classifier, proportion_attack_to_perturb,
                                                    features_to_perturb, relative_eps=relative_eps,
                                                    relitive_eps_step=relative_eps_step)
        art_classifier.fit(x_with_adv_samples, y)
        return art_classifier

    #############################################################################
    # insert_ad_samples(self, x, y, adversarial_training_method, art_classifier,
    #                   features_to_perturb)
    #
    # Calls the insert_ad_samples(...) method to insert adversarial samples into
    # the training data. The classifier will then be trained on this data to recognise
    # the adversarial samples
    #
    # Args:
    #    x: The features of the flow samples
    #    y: the labels of the flow samples
    #    adversarial_training_method: the adversarial evasion attack method which will
    #                                 target the art_classifier to produce adversarial
    #                                 samples.
    #    art_classifier: A classifier that is from the adversarial-robustness-toolbox
    #    features_to_perturb: The features of x that should be perturbed by the
    #                         adversarial_training_method.
    #    proportion_attack_to_perturb: the proportion of SYN Flood flow samples that will
    #                         be replaced by their adversarial counterpart.
    #    relative_eps: attack step size relative the mean size of the input for each feature
    #    relative_eps_step: Relative (to the to mean size of each feature) step size of
    #                       input variation for minimal perturbation computation
    #
    # Returns:
    #     The data with the required proportion of the attacks replaced with adversarial attacks.
    #
    def insert_ad_samples(self, x, y, adversarial_training_method, art_classifier, proportion_attack_to_perturb,
                          features_to_perturb, relative_eps=0.3, relitive_eps_step=0.1):
        
        # Make mask to stop perturbation of protected attributes
        mask = generate_mask(x, features_to_perturb)

        # Select attack indexes to preturb
        attack_indexes_to_perturb = select_random_portion_of_attack_indexes(y, proportion_attack_to_perturb)

        # Make art classifier and train it
        art_classifier.fit(x, y)

        attack = self.__get_attack(adversarial_training_method, art_classifier, x[features_to_perturb],
                                   relative_eps, relitive_eps_step)

        adv_samples = attack.generate(
                x=x.iloc[attack_indexes_to_perturb],
                y=y[attack_indexes_to_perturb],
                mask=mask)

        x.iloc[attack_indexes_to_perturb] = adv_samples

        return x

    #############################################################################
    # __get_attack(self, adversarial_training_method, classifier, data_to_be_perturbed, relative_eps,
    #              relative_eps_step)
    # Configures and returns an adversarial attack object to be used for the generation of
    # adversarial examples
    #
    # Args:
    #    adversarial_training_method: the adversarial evasion attack method which will
    #                                 target the art_classifier to produce adversarial
    #                                 samples.
    #    art_classifier: A classifier that is from the adversarial-robustness-toolbox
    #    data_to_be_perturbed: The sub section of the data which will be passed to the
    #                          adversarial_training_method in order to produce adversarial
    #                          examples
    #    relative_eps: attack step size relative the mean size of the input for each feature
    #    relative_eps_step: Relative (to the to mean size of each feature) step size of
    #                       input variation for minimal perturbation computation
    #
    # Returns:
    #    An adversarial attack that will be used to produce adversarial samples
    #
    def __get_attack(self, adversarial_training_method, art_classifier, data_to_be_perturbed, relative_eps,
                     relitive_eps_step):
        eps, eps_step = calculate_eps(data_to_be_perturbed, relative_eps, relitive_eps_step)
        if adversarial_training_method == AdversarialAttackType.FGSM:
            return FastGradientMethod(art_classifier, eps=eps, eps_step=eps_step)
        elif adversarial_training_method == AdversarialAttackType.BIM:
            return BasicIterativeMethod(art_classifier, eps=eps, eps_step=eps_step)
        elif adversarial_training_method == AdversarialAttackType.PGD:
            return ProjectedGradientDescent(art_classifier, eps=eps, eps_step=eps_step)
        elif adversarial_training_method == AdversarialAttackType.HSJ:
            return HopSkipJump(art_classifier)

