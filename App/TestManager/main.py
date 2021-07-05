#################################################################################
# Hydra TestManager main script
#
# File: main.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Script to handle the execution of a submitted adversarial test from the
#       Hydra web application.  Handles launching of the NIDS Neptune, as well
#       as the Mininet SDN.  Calls the TestSuite class to perform the requested
#       adversarial attack.
#
#
# Usage: Program is executed from a terminal using 'sudo python TestManager/main.py'
#        with appropriate arguments
#
# Args:
#       target_classifier: machine learning clasifier to be used in test
#       network_attack: network attack to be performed in test
#       adversarial_attack: adversarial technique applied to network attack
#
# Requirements: test_suite.py and mininet Python API directory
#
#################################################################################

from __future__ import division

import os
import sys
import logging
import time
import csv
from subprocess import Popen, PIPE

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController

from test_suite import TestSuite
from nids_config_validator import NidsConfigValidator
from attack_validator import validate_attack
import json

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

    start_time = time.time()
    dir = os.getcwd() + "/App/"
    net_assigned = False

    config_validator = NidsConfigValidator()
    config_validator.validate_nids_config(json.load(open(dir + "/nids_config/config.json")))

    try:
        network_attack = "SYN Flood"
        adversarial_attack = sys.argv[1]
        validate_attack(adversarial_attack)

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
        launch_nids(dir)

        print("\n")
        # Initialise test suite and execute attack
        ts = TestSuite(dir, network_attack, adversarial_attack, net)
        acc, result = ts.run_test()
        finish_time = time.time()

        with open("/opt/adversarialtestingsdn/App/TestManager/log/attack_output_log.csv", "a", newline="") as log:
            writer = csv.writer(log)
            writer.writerow([start_time, finish_time, "NA", network_attack, adversarial_attack, acc])

        time.sleep(5)
        results_dir = dir + "TestManager/test_results/results.txt"
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
def launch_nids(dir):
    print("Launching Neptune..")

    time.sleep(2)

    neptune_cmd = "sudo python3 -W ignore " + dir + "Neptune/" + "main.py"
    Popen(['gnome-terminal', '-e', neptune_cmd], stdout=PIPE)

    print("DIR = " + dir)
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
