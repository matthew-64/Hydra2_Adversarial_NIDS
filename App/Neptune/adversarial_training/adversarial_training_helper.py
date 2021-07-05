import numpy as np
import math
from random import shuffle

#################################################################################
#
# File: adversarial_training_helper.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Helper functions for the AdversarialTrainer class
#
# Usage: see AdversarialTrainer class
#################################################################################

#############################################################################
# generate_mask(feature_labels, perturbed_features)
#
# Generates a mask that will be used to determine which features will be perturbed
# by the AdversarialTrainer
#
# Args:
#    feature_labels: all the labels of the data
#    perturbed_features: the features that should be perturbed in the AdversarialTrainer
#
# Returns:
#    A bool array
#
def generate_mask(feature_labels, perturbed_features):
    bool_list = []
    for label in feature_labels:
        bool_list.append(label in perturbed_features)
    return np.array(bool_list)

#############################################################################
# select_random_portion_of_attack_indexes(labels, proportion)
#
# Identifies all available attack indices in the labels and returns a subsection
# the size of which determined by the proportion variable.
#
# Args:
#    labels: all the labels of the data.
#    proportion: the total proportion of the indices that should be returned
#
# Usage:
#     Will be used in the adversarial trainer to determine the exact attacks that
#     will be perturbed into adversarial examples.
#
# Returns:
#    An array of random attack indexes
#
def select_random_portion_of_attack_indexes(labels, proportion):
    all_attack_indexes = []
    for i in range(0, len(labels)):
        if not labels[i][0] == 1:
            all_attack_indexes.append(i)
    num_required_attacks = math.ceil(len(all_attack_indexes) * proportion)
    shuffle(all_attack_indexes)
    return all_attack_indexes[0:num_required_attacks]

#############################################################################
# calculate_eps(data_being_perturbed, relative_eps, relative_eps_step)
#
# Calculates the eps and eps_step requires to be proportional to the mean values in
# the data
#
# Args:
#    data_being_perturbed: a data frame of all the attacks that will be perturbed
#                          by the AdversarialTrainer
#     relative_eps: attack step size relative the the mean size of the input for each feature
#     relative_eps_step: Relative (to the to mean size of each feature) step size of
#                       input variation for minimal perturbation computation
#
# Usage:
#     Will be used in the adversarial trainer to determine the exact attacks that need to
#     calculate absolute eps and eps_step.
#
# Returns:
#    The scaled values of eps and eps_step in a tuple
#
def calculate_eps(data_being_perturbed, relative_eps, relative_eps_step):
    mean_value = np.mean(np.mean(np.absolute(data_being_perturbed)))
    eps = mean_value * relative_eps
    eps_step = mean_value * relative_eps_step
    return eps, eps_step
