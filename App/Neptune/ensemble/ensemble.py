import numpy as np
import random


#################################################################################
# EnsembleVotingType class
#
# File: ensemble.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Class to act as an enum to avoid hard coded values in Ensemble
#       class
#
# Usage: see Ensemble below
#################################################################################
class EnsembleVotingType:
    HARD = "hard"
    SOFT = "soft"


#################################################################################
# Ensemble class
#
# File: ensemble.py
# Name: Matthew Elliott
# Date: 04/04/2021
# Course: CSC4006 - Research and Development Project
# Desc: Custom class for an ensemble of classifiers that can be individually trained
#       and is compatible with the adversarial-robustness-toolbox
#
# Usage: Used in the Neptune main() to adversarially train classifiers where required
#################################################################################
class Ensemble:

    #############################################################################
    # __init__(self, classifier_list, voting_type=EnsembleVotingType.HARD, weights=None)
    #
    # Args:
    #    classifier_list: The classifiers that will be used in the ensemble
    #    voting_type: Dictates the voting method of the classifier
    #    weights: dictates how much weight each individual classifier has in the ensemble
    #
    def __init__(self, classifier_list, voting_type=EnsembleVotingType.HARD, weights=None):
        if weights is None:
            self.weights = np.ones((1, len(classifier_list)))[0]
        else:
            self.__validate_classifier_and_weights_length(classifier_list, weights)
            self.weights = weights
        self.classifier_list = classifier_list
        self.voting_type = voting_type

    #############################################################################
    # predict(self, data_points)
    #
    # For a list of data points, it will predict the most likely label for each data point
    #
    # Args:
    #    data_points: a list of data_points to be classified by the ensemble
    #
    # Returns:
    #    A list of label predictions. One prediction per data point passed
    #
    def predict(self, data_points):
        if self.voting_type == EnsembleVotingType.HARD:
            return self.__hard_vote(data_points)
        elif self.voting_type == EnsembleVotingType.SOFT:
            return self.__soft_vote(data_points)

    #############################################################################
    # __hard_vote(self, data)
    #
    # Implements a hard voting system for classifiers determining the outcome.
    # the hard voting type will act as a basic voting type where each classifier
    # votes on the label(s) of the data.
    #
    # Args:
    #    data: the data to be classified by the ensemble
    #
    # Returns:
    #    A list of label predictions for the data passed to it
    #
    def __hard_vote(self, data):
        all_predictions = self.__get_all_predictions(data)
        voting_prediction = []
        # Iterate through all the predictions from the data points in order
        for prediction_pos in range(0, len(data)):
            # To store how many votes for each type of prediction available
            votes = {}
            # A prediction stores all the predictions on a single classifier
            for prediction, weight, in zip(all_predictions, self.weights):
                this_prediction = prediction[prediction_pos]
                this_prediction_values = self.__get_max_value_positions(this_prediction)

                # For loop required when there is a tie
                for value in this_prediction_values:
                    if value in list(votes.keys()):
                        votes[value] += weight
                    else:
                        votes[value] = weight

            max_key_values = self.__get_majority_voting(votes)

            # Randomly select a victor if there is a tie
            voting_prediction.append(random.choice(max_key_values))
        return np.array(voting_prediction)

    #############################################################################
    # __soft_vote(self, data)
    #
    # Implements a soft voting system for classifiers determining the outcome. The
    # probabilities for each possible label that each classifier predicts per data point
    # will be summed. The victor will be the label with the highest probability.
    # See inline comments on how this is achieved.
    #
    # Args:
    #    data: the data to be classified by the ensemble
    #
    # Returns:
    #    A list of label predictions for the data passed to it
    #
    def __soft_vote(self, data):
        all_predictions = self.__get_all_predictions(data)

        # Adjust for weights
        for i in range(0, len(self.weights)):
            all_predictions[i] = all_predictions[i] * self.weights[i]

        prediction_probability_result = sum(all_predictions)
        voting_prediction = []
        for this_prediction in prediction_probability_result:
            max_value_pos = random.choice(self.__get_max_value_positions(this_prediction))
            voting_prediction.append(max_value_pos)
        return np.array(voting_prediction)

    #############################################################################
    # __get_all_predictions(self, data)
    #
    # Each classifier in the ensemble will predict the labels of the data
    #
    # Args:
    #    data: The data to be classifier separately by each classifier
    #
    # Returns:
    #    A list of the list of the predictions of each classifier.
    #
    def __get_all_predictions(self, data):
        all_predictions = []
        for classifier in self.classifier_list:
            all_predictions.append(classifier.predict(data))
        return all_predictions

    #############################################################################
    # __get_max_value_positions(this_list)
    #
    # Used for converting the array of probabilities each classifier produces into
    # a single label that has the highest probability
    #
    # Args:
    #    this_list: A list of probabilities for the label value
    #
    # Returns:
    #    The label which has the highest probability
    #
    @staticmethod
    def __get_max_value_positions(this_list):
        return np.where(this_list == np.amax(this_list))[0]

    #############################################################################
    # __get_majority_voting(votes)
    #
    # Used for determining the outcome of a vote. It will return the label(s) with
    # the highest votes.
    #
    # Args:
    #    votes: A dict of label -> number of votes
    #
    # Returns:
    #    The label which has the most votes
    #
    @staticmethod
    def __get_majority_voting(votes):
        max_value = 0
        max_key_values = []
        for key, value in votes.items():
            if value > max_value:
                max_key_values = [key]
                max_value = value
            elif value == max_value:
                max_key_values.append(key)
        return max_key_values

    #############################################################################
    # __validate_classifier_and_weights_length(classifier_list, weights)
    #
    # Used in the __init(...)___ of the ensemble to verify the weight and classifier
    # lists are the same size
    #
    # Args:
    #    classifier_list: The classifiers that will be used in the ensemble
    #    weights: dictates how much weight each individual classifier has in the ensemble
    #
    @staticmethod
    def __validate_classifier_and_weights_length(classifier_list, weights):
        if len(weights) != len(classifier_list):
            raise Exception("classifier_list and weights must have same length")