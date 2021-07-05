#################################################################################
# test_main.py
#
# File: test_main.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Similar to the TestManager main.py.  Script to handle the execution of
#       evasion evaluation tests.  Handles launching of the NIDS Neptune, as well
#       as the Mininet SDN.  Calls the test_evasion_eval to perform the requested
#       perturbations and returns the detection accuracy
#
#
# Usage: Program is executed from a terminal using 'sudo python
#        TestManager/tests/test_main.py' with appropriate arguments to evaluate
#        evasion potential
#
# Args:
#       target_classifier: machine learning clasifier to be used in test
#       network_attack: network attack to be performed in test
#       adversarial_attack: adversarial technique applied to network attack
#
# Requirements: test_evasion_eval.py and mininet Python API directory
#
#################################################################################

from __future__ import division

import os
import time
import sys
import logging

from subprocess import Popen, PIPE

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController

from test_evasion_eval import EvasionEval


#################################################################################
# main()
#
# Main method for the TestManager package to handle an adversarial test
# Launches Neptune and Mininet before calling the TestSuite to perform the test
# Outputs results to file
#
# Args:
#    target_classifier: machine learning clasifier to be used in test
#    network_attack: network attack to be performed in test
#    adversarial_attack: adversarial technique applied to network attack
#
# Terminates Neptune and Mininet when finished
#
def main():
    dir = os.getcwd() + "/App/"
    net_assigned = False
    try:
        # Read testing arguments
        target_classifier = sys.argv[1]
        network_attack = sys.argv[2]
        adversarial_attack = sys.argv[3]

        training_dir = dir + "nids_config/training_status.txt"

        # Configure and launch Mininet
        setLogLevel('info')
        net = launch_network()
        net_assigned = True

        #Launch NIDS
        try:
            with open(training_dir,'w') as training_status:
                training_status.write("")
        except:
            logging.error('Unable to open training status directory')
        launch_nids(dir, target_classifier)

        print("\n")
        # Initialise test suite and execute attack
        ts = EvasionEval(dir, network_attack, adversarial_attack, net)
        result = ts.run_test()

        time.sleep(5)
        results_dir = dir + "TestManager/tests/test_results/results.txt"
        try:
            with open(results_dir,"a+") as results:
                # Write results based on what the test has returned
                output = result
                results.write(str(output))
                results.write("\n")
        except:
            logging.error('Unable to open and write to results file')

    except KeyboardInterrupt:
        print("Stopping Neptune..")
        os.system('sudo pkill -f Neptune/main.py')

        print("\nStopping network..\n")
        if net_assigned:
            net.stop()

        sys.exit(0)

    finally:
        print("Stopping Neptune..")
        os.system('sudo pkill -f Neptune/main.py')

        if net_assigned:
            print("\nStopping network..\n")
            net.stop()
        time.sleep(5)

        with open(training_dir,'w') as training_status:
            training_status.write("")


#################################################################################
# launch_nids(dir, target_classifier)
#
# Function to launch the intrusion detection system Neptune in a child terminal
# with appropriate congiguration
# Sleeps until Neptune has trained its classifier
#
# Args:
#    dir: base directory of application
#    target_classifier: classifier to be used by Neptune
#
def launch_nids(dir, target_classifier):
    print("Launching Neptune..")

    classifier_dir = dir + "nids_config/classifier_type.txt"
    try:
        with open(classifier_dir,"w") as classifier_config:
            print("Target: " + str(target_classifier))
            # Write classifier type to Neptune configuration file

            # TODO: make test work for this configuration
            # if str(target_classifier) == "1":
            #     classifier_config.write("1")
            # elif str(target_classifier) == "2":
            #     print("KNN Selected!")
            #     classifier_config.write("2")
            # elif str(target_classifier) == "3":
            #     classifier_config.write("3")
            # elif str(target_classifier) == "4":
            #     classifier_config.write("4")
            # elif str(target_classifier) == "5":
            #     classifier_config.write("5")
            # else:
            #     print(str(target_classifier))
            #     classifier_config.write("-1")
            #     print("Invalid classifier")


            if str(target_classifier) == "Random Forest Model":
                classifier_config.write("1")
            elif str(target_classifier) == "KNN":
                classifier_config.write("2")
            elif str(target_classifier) == "SVM":
                classifier_config.write("3")
            elif str(target_classifier) == "Neural Network":
                classifier_config.write("4")
            elif str(target_classifier) == "Logistic Regression":
                classifier_config.write("5")
            else:
                print(str(target_classifier))
                classifier_config.write("-1")
                print("Invalid classifier")
    except:
        logging.error('Unable to open and write to classifier config directory')

    time.sleep(2)

    # Launch Neptune in child terminal
    neptune_cmd = "sudo python -W ignore " + dir + "Neptune/"+ "main.py"
    Popen(['gnome-terminal', '-e', neptune_cmd], stdout=PIPE)

    training_status_dir = dir + "nids_config/training_status.txt"
    training_wait = True

    # Wait for Neptune to train classifier
    while(training_wait):
        time.sleep(1)
        with open(training_status_dir, "r") as training_status:
            for line in training_status:
                if str(line) == '1':
                    training_wait = False

    time.sleep(2)


#################################################################################
# launch_network()
#
# Launches the Mininet network, connecting to the remote controller
#
# Returns:
#    net: the Mininet class network object
#
def launch_network():

    net = Mininet(autoSetMacs = True, cleanup = True)

    s1 = net.addSwitch('s1')

    for n in range(1,15):
        h = net.addHost('h%s' % n)
        net.addLink(h, s1)

    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    net.start()

    time.sleep(5)
    print("Network started..")

    return net


#################################################################################
# logo()
#
# Display Hydra logo on app launch using print()
#
def logo():
    """
    Prints the logo of Hydra
    """

    logo = '''

            ---------------------------------------------------
                 _   _  _  _  _  _ _ _     ____    ___
                | | | || || || ||   _  |  |  _ /  / _ /
                | |_| || /| |/ ||  | |  | | |_) )| |_| |
                |  _  | /_   _/ |  | |  | |  __/ |  _  |
                | | | |   | |   |  |_/ /  | |    | | | |
                |_| |_|   |_|   |_____/   |_|    |_| |_|
            ---------------------------------------------------
    '''
    print(logo)

if __name__ == '__main__':
    logo()
    main()
