#################################################################################
# Classifier training class
#
# File: featurizer.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class to train a classifier
#
#
#################################################################################

from sklearn.preprocessing import OneHotEncoder

import os
import logging
import pandas as pd

from flow_cleaning import FlowCleaning
from feature_selection.feature_selection import FeatureSelector
from preprocessing.preporcessor import Preprocessor
#################################################################################
# ClassifierTraining()
#
# Class containing classifier training functionality
#
class ClassifierTraining:

    flow_clean = FlowCleaning()

    #############################################################################
    # model_training(retrain, poll_dur)
    #
    # Performs flow cleaning on each training batch and aggregates them
    # Trains ML classifier on aggregated training stats
    #
    # Args:
    #    retrain: True if live retraining implemented
    #    poll_dur: Time in seconds between each live batch
    #
    def model_training(self, ml_flow, retrain, poll_dur):
        os.chdir(os.getcwd() + "/")

        if not retrain:
            self.flow_clean.flow_stat_clean(False, -1, poll_dur)

            try:
                self.flow_clean.aggregate_stats('Neptune/stats_training/')
            except:
                logging.error('Unable to generate aggregated files')

        flow_input = pd.read_csv(
            'Neptune/stats_training/FlowStats_cleaned.csv')
        flow_target = pd.read_csv(
            'Neptune/stats_training/FlowStats_target_cleaned.txt')

        # Fit the flow statistics to the machine learning classifier, excluding mac
        flow_input = flow_input.iloc[:,2:].apply(pd.to_numeric)
        flow_target = flow_target.apply(pd.to_numeric, errors='ignore')

        ml_flow.fit(flow_input, flow_target.values.ravel())

        print("Training complete")
        # Write to training_status.txt - '1' = training complete
        try:
            with open('nids_config/training_status.txt','w') as training_status:
                training_status.write("1")
        except:
            logging.error('Failed to open training_status file')

        return ml_flow

    def model_training1(self, ml_flow, retrain, poll_dur, one_hot_encoder=OneHotEncoder(sparse=False),
                        feature_selector=FeatureSelector(), preprocessor=Preprocessor()):
        os.chdir(os.getcwd() + "/")

        # if not retrain:
        #     self.flow_clean.flow_stat_clean(False, -1, poll_dur)
        #
        #     try:
        #         self.flow_clean.aggregate_stats('Neptune/stats_training/')
        #     except:
        #         logging.error('Unable to generate aggregated files')
        #
        # flow_input = pd.read_csv(
        #     'Neptune/stats_training/FlowStats_cleaned.csv')
        # flow_target = pd.read_csv(
        #     'Neptune/stats_training/FlowStats_target_cleaned.txt')
        #
        # # Fit the flow statistics to the machine learning classifier, excluding mac
        # flow_input = flow_input.iloc[:,2:].apply(pd.to_numeric)
        #
        # # Select only the relevant features
        # flow_input = feature_selector.select_features(flow_input)
        #
        # # Perform preprocessing
        # flow_input = preprocessor.fit_transform(flow_input)
        #
        # flow_target = flow_target.apply(pd.to_numeric, errors='ignore')
        # flow_target = one_hot_encoder.fit_transform(flow_target)

        flow_input, flow_target = self.get_train_data(retrain, poll_dur, one_hot_encoder, feature_selector, preprocessor)

        ml_flow.fit(flow_input, flow_target)

        print("Training complete")
        # Write to training_status.txt - '1' = training complete
        # TODO: Figure out what the purpose of this is and perhaps move it ot the main...
        # try:
        #     with open('nids_config/training_status.txt','w') as training_status:
        #         training_status.write("1")
        # except:
        #     logging.error('Failed to open training_status file')

        return ml_flow

    def get_train_data(self, retrain, poll_dur, one_hot_encoder=OneHotEncoder(sparse=False),
                        feature_selector=FeatureSelector(), preprocessor=Preprocessor()):
        os.chdir(os.getcwd() + "/")

        if not retrain:
            self.flow_clean.flow_stat_clean(False, -1, poll_dur)

            try:
                self.flow_clean.aggregate_stats('Neptune/stats_training/')
            except:
                logging.error('Unable to generate aggregated files')

        flow_input = pd.read_csv(
            'Neptune/stats_training/FlowStats_cleaned.csv')
        flow_target = pd.read_csv(
            'Neptune/stats_training/FlowStats_target_cleaned.txt')

        # Fit the flow statistics to the machine learning classifier, excluding mac
        flow_input = flow_input.iloc[:,2:].apply(pd.to_numeric)

        # Select only the relevant features
        flow_input = feature_selector.select_features(flow_input)

        # Perform preprocessing
        flow_input = preprocessor.fit_transform(flow_input)

        flow_target = flow_target.apply(pd.to_numeric, errors='ignore')
        flow_target = one_hot_encoder.fit_transform(flow_target)

        return flow_input, flow_target