#################################################################################
# Neptune main program file
#
# File: main.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Main class for the Neptune Intrusion Detection System.  It cleans
#      the application's file system and creates a machine learning classifier
#      from the sklearn library.  The main program loop implements live traffic
#      flow classification
#
# Usage: Program is executed from a terminal using 'sudo python Neptune/main.py'
#       Requires a classifier to be specified in nids_config/classifier_type.txt.
#       Relies on the sklearn libraryself.
#
# Requirements: intrusion_detection.py, flow_cleaning.py, traffic_stats.py.
#
# classifier_functions.py is also recommended for the tuning of classifier
# hyperparameters.  Currently they are tuned for the included training set
# for SYN flood detection
#
#################################################################################

import os
import shutil
import logging
import numpy as np
import time
import json

from subprocess import Popen, PIPE

from intrusion_detection import IntrusionDetection
from traffic_stats import TrafficStats
from classifier_training import ClassifierTraining
from ensemble.ensemble import Ensemble
from classifier_configuration import get_art_classifiers
from feature_selection.feature_selection import FeatureSelector
from feature_selection.feature_selection import FeatureSelectionType
from feature_selection.adversarial_perturbation_selector import AdversarialPerturbationFeatureSelector
from preprocessing.preporcessor import Preprocessor
from adversarial_training.adv_training import AdversarialTrainer

#################################################################################
# NeptuneNIDS()
#
# Neptune main class to perform network intrusion detection on live traffic
#
# Attributes:
#    batch_number: Each execution begins counting live traffic batches from 1
#    traffic_stats: TrafficStats object for polling for live flow statistics
#    intrusion_detection: IntrusionDetection object to perform ID on flow stats
#    classifier_train: ClassifierTraining object to train the classifier
#
class NeptuneNIDS():

    batch_number = 1
    traffic_stats = TrafficStats()
    intrusion_detection = IntrusionDetection()
    classifier_train = ClassifierTraining()
    adversarial_trainer = AdversarialTrainer()
    perturbation_feature_selector = AdversarialPerturbationFeatureSelector()


    #############################################################################
    # __init__()
    #
    # NeptuneNIDS constructor
    #
    # Sets working directory and initialises file system for new execution
    # Initialises the machine learning classifier
    #
    def __init__(self):
        os.chdir(os.getcwd() + "/App/")

        self.initialise_files()

    #############################################################################
    # main()
    #
    # Main method of Neptune, performs main intrusion detection cycle
    # Trains on training statistics, repeatedly requests live statistics and
    # performs intrusion detection based on the detection frequency setting
    #
    def main(self):
        # Launch the Argus network auditor as a daemon
        dir = os.getcwd() + "/Neptune/stats_live/traffic.txt"
        cmd = "sudo argus -d -m -i s1-eth10 -w " + dir + " &"
        Popen(['gnome-terminal', '-e', cmd], stdout=PIPE)

        nids_config = json.load(open("nids_config/config.json", "r"))

        # Create untrained ensemble
        ensemble = Ensemble(
                get_art_classifiers(nids_config["classifiers"]),
                voting_type=nids_config["ensemble_vote_type"],
                weights=nids_config["weights"])

        # Configuure feature selection
        feature_selector = FeatureSelector(
                # TODO: check of this throws an error is this field doesn't exist. I don't think it should
                # In readme, spefify that it needs to be left blank
                ad_attack=nids_config["attack_feature_selection"],
                feature_selection_type=nids_config["feature_selection_type"])

        # Configure pre processing
        preprocessor = Preprocessor(nids_config["preprocessing"])

        loop_count = 0
        polling_freq = 10
        detection_freq = 10
        retraining_freq = 5

        live_training_flag = False
        trained = [0] * len(nids_config["weights"])
        retraining = [0] * len(nids_config["weights"])
        intrusions = []


        # TODO: Let's see if moving this make any difference...
        flow_input, flow_target = self.classifier_train.get_train_data(
            False,
            polling_freq,
            feature_selector=feature_selector,
            preprocessor=preprocessor)

        while True:
            for i in range(0, len(nids_config["weights"])):

                if not trained[i]:
                    print("Training Classifier " + str(nids_config["classifiers"][i]) + "...")

                    if nids_config["adversarial_training_types"][i] == "none":
                        ensemble.classifier_list[i] = self.classifier_train.model_training1(
                                ensemble.classifier_list[i],
                                False,
                                polling_freq,
                                feature_selector=feature_selector,
                                preprocessor=preprocessor)
                    else:
                        features_to_preturb = self.perturbation_feature_selector.get_features(
                                nids_config["attack_feature_selection"])

                        ensemble.classifier_list[i] = self.adversarial_trainer.train_on_ad_examples(
                                flow_input,
                                flow_target,
                                nids_config["adversarial_training_types"][i],
                                ensemble.classifier_list[i],
                                features_to_preturb)
                    trained[i] = 1
                elif retraining[i]:
                    print("Retraining Classifier " + str(nids_config["classifiers"][i]) + "...")
                    ensemble.classifier_list[i] = self.classifier_train.model_training1(
                            ensemble.classifier_list[i],
                            True,
                            polling_freq,
                            feature_selector=feature_selector,
                            preprocessor=preprocessor)
                    retraining[i] = 0

            if sum(trained) == len(trained):
                try:
                    with open('nids_config/training_status.txt', 'w') as training_status:
                        training_status.write("1")
                except:
                    logging.error('Failed to open training_status file')

            # Wait for traffic to start flowing
            if self.batch_number == 1:
                time.sleep(10)

            self.traffic_stats.request_stats(self.batch_number, False)

            loop_count += 1
            time.sleep(1)
            if loop_count % (detection_freq / polling_freq) == 0:
                intrusions = self.intrusion_detection.intrusion_detection(intrusions, ensemble,
                                                                          live_training_flag,
                                                                          self.batch_number, polling_freq,
                                                                          feature_selector=feature_selector,
                                                                          preprocessor=preprocessor)

                time.sleep(polling_freq)

                if loop_count % retraining_freq == 0 and live_training_flag:
                    retraining = True

                self.batch_number += 1



    #############################################################################
    # initialise_files()
    #
    # Resets the Neptune file system for a new execution
    # Deletes files from the previous execution and resets the configuration
    # settings
    #
    def initialise_files(self):

        stats_live_dir = os.getcwd() + "/Neptune/stats_live"

        try:
            shutil.rmtree(stats_live_dir)
            os.makedirs(stats_live_dir)
        except:
            logging.error('Could not initialise stats_live directory')

        try:
            with open('nids_config/intrusion_results.txt', 'w') as intrusion_results:
                print("")
        except:
            logging.error('Could not open intrusion_results file')

        live_traffic_dir = "stats_live/traffic.txt"
        if os.path.exists(live_traffic_dir):
            os.remove(live_traffic_dir)


    #############################################################################
    # logo()
    #
    # Display Neptune logo on app launch using print()
    #
    def logo(self):
        os.system('clear')
        logo = '''

        *********************************************************************
                _   __                  __
               / | / /  ___     ____   / /_  __  __   ____   ___
              /  |/ /  / _ /   / __ / / __/ / / / /  / __ / / _ /
             / /|  /  /  __/  / /_/ // /_  / /_/ /  / / / //  __/
            /_/ |_/   /___/  / .___/ /__/  /__,_/  /_/ /_/ /___/
                            /_/
        *********************************************************************
        '''

        print(logo)


if __name__ == '__main__':
    ids = NeptuneNIDS()
    # ids.main1()
    try:
        ids.logo()
        # ids.main()
        ids.main()
    finally:
        os.system("sudo pkill -f 'argus'") # Terminate Argus daemon
        time.sleep(10)
