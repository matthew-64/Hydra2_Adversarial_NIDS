#################################################################################
# Hydra TestManager test suite
#
# File: test_suite.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: TestSuite class to handle the execution of an adversarial attack, as well
#       as generate helpful recommendations and a detection accuracy
#       Contains a number of adversarial tests
#
#
#
# Usage: The run_test() method is called with appropriate parameters to execute
#        an adversarial test and return the results
#
# Args:
#       dir: working directory of the application
#       network_attack: network attack to be performed
#       adversarial_attack: adversarial technique to be applied
#       net: Mininet class network object
#
# Requirements: mininet Python API directory
#
#################################################################################

from __future__ import division
from App.TestManager.main import launch_network

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


#################################################################################
# TestSuite()
#
# Class which contains all adversarial testing functionality
# Executes tests based on test configuration and returns result
#
# A number of adversarial testing functions send different types of traffic
# across the network net, calculating the accuracy of detection and returning it
#
class TestSuite:


    #############################################################################
    # __init__(dir, network_attack, adversarial_attack, net)
    #
    # Initialise class variables from parameters
    # Initialise each network host using net
    #
    # Args:
    #    dir: working directory of the application
    #    network_attack: network attack to be performed
    #    adversarial_attack: adversarial technique to be applied
    #    net: Mininet class network object
    #
    def __init__(self, dir):

        self.dir = dir
        self.network_attack = network_attack
        self.adversarial_attack = adversarial_attack
        self.net = launch_network()

        # Initialise network host variables using net object
        self.h1 = self.net.get('h1')
        self.h2 = self.net.get('h2')
        self.h3 = self.net.get('h3')
        self.h4 = self.net.get('h4')
        self.h5 = self.net.get('h5')
        self.h6 = self.net.get('h6')
        self.h7 = self.net.get('h7')
        self.h8 = self.net.get('h8')
        self.h9 = self.net.get('h9')
        self.h10 = self.net.get('h10')
        self.h11 = self.net.get('h11')
        self.h12 = self.net.get('h12')
        self.h13 = self.net.get('h13')
        self.h14 = self.net.get('h14')


    #############################################################################
    # run_test()
    #
    # Main function to handle the running of a test based on class input parameters
    # Chooses the appropriate test based on the parameters
    #
    # Returns:
    #    result: A string resembling the result of a test
    #
    def run_test(self):

        result = ""
        acc = -1
        if str(self.network_attack) == "SYN Flood":
            if str(self.adversarial_attack) == "Standard":
                acc, result = self.standard_syn_flood(1000, 1)
            elif str(self.adversarial_attack) == "Evasion: Rate":
                acc, result = self.rate_evasion(1000, 45000)
            elif str(self.adversarial_attack) == "Evasion: Payload":
                acc, result = self.payload_evasion(1000, 90)
            elif str(self.adversarial_attack) == "Evasion: Pairflow":
                acc, result = self.pairflow_evasion(1000, 1500)
            elif str(self.adversarial_attack) == "Evasion: Rate+Payload":
                acc, result = self.rate_payload_evasion(1000, 45000, 90)
            elif str(self.adversarial_attack) == "Evasion: Rate+Pairflow":
                acc, result = self.rate_pairflow_evasion(1000, 45000, 45000)
            elif str(self.adversarial_attack) == "Evasion: Payload+Pairflow":
                acc, esult = self.payload_pairflow_evasion(1000, 90, 1500)
            elif str(self.adversarial_attack) == "Evasion: Stealth":
                acc, result = self.stealth_evasion(1000, 90, 1500, 1500)
            else:
                print("Invalid adversarial attack.. " + str(self.adversarial_attack))
                logger.error('Invalid adversarial attack: ' + str(self.adversarial_attack))
        else:
            print("Invalid network attack.. " + str(self.network_attack))
            logger.error('Invalid network attack: ' + str(self.network_attack))

        return acc, result

    def standard_syn_flood(self, pkt_count, speed):
        print("Executing normal SYN Flood attack...")
        src_eth = ['2', '1', '3', '4', '4', '6', '2', '4', '6', '7']
        dst_eth = ['1', '3', '2', '5', '1', '9', '9', '2', '3', '2']

        count = 0
        for i in range(0, len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u' + str(speed) + ' -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + \
                  dst_eth[i]
            host.cmd(cmd)

            count += 1

            perc_progress = (100 / len(src_eth)) * count
            str_progress = '-' * count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(5)
        print("SYN Flood complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, False)

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against rate evasion.  \
                             The classifier has misclassied SYN floods performed at a slower rate of 20pps.  \
                             It is recommended to train against slower attacks."
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result

    #############################################################################
    # rate_evasion()
    #
    # Adversarial evasion attack to perturb packet rate
    #
    # Args:
    #   pkt_count - number of packets to send in attack
    #   speed - flood rate, determined by how many microseconds to wait between packets
    #
    # Returns:
    #    result: A string with the result of the test and description
    #
    def rate_evasion(self, pkt_count, speed):
        print("Executing Slow Rate Evasion attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0
        print("0%")

        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u' + str(speed) + ' -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i]
            host.cmd(cmd)

            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(5)

        print("Slow Rate Evasion complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, False)

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against rate evasion.  \
                     The classifier has misclassied SYN floods performed at a slower rate of 20pps.  \
                     It is recommended to train against slower attacks."
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result


    #############################################################################
    # payload_evasion()
    #
    # Adversarial evasion attack to perturb payload size
    #
    # Args:
    #   pkt_count - number of packets to send in attack
    #   data_size - Additional payload size in bytes added to SYN packet
    #
    # Returns:
    #    result: A string with the result of the test and description
    #
    def payload_evasion(self, pkt_count, data_size):
        print("Executing Increased Payload Evasion attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0
        print("0%")
        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u1500 -c ' + str(pkt_count) + ' -d ' + str(data_size) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i]
            host.cmd(cmd)
            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(5)

        print("Payload Evasion complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, False)

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against payload evasion.  \
                     The classifier has misclassied SYN floods performed with an increased payload size of 130 bytes.  \
                     It is recommended to train with a variety of SYN packet sizes."
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result


    #############################################################################
    # pairflow_evasion()
    #
    # Adversarial evasion attack to forge bidirectional traffic
    #
    # Args:
    #   pkt_count - number of packets to send in attack
    #   ret_speed - Time in microseconds to determine rate of forged traffic
    #
    # Returns:
    #    result: A string with the result of the test and description
    #
    def pairflow_evasion(self, pkt_count, ret_speed):
        print("Executing Pairflow Evasion attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0

        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u1500 -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i] + ' &'
            host.cmd(cmd)
            for j in range(int(pkt_count)):
                time.sleep(ret_speed/1000000)
                cmd_ret = 'nping --tcp syn --source-ip rand --dest-mac 00:00:00:00:00:0' + \
                           str(src_eth[i]) + ' --source-mac 00:00:00:00:00:0' + str(dst_eth[i]) + \
                           ' -c ' + str(1) + ' --data-length 0 --rate ' + str(1) + \
                           ' 10.0.0.' + dst_eth[i] + ' &'
                host.cmd(cmd_ret)
            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(1)

        print("Pairflow Evasion complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, True)/2

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against pair_flow evasion.  \
                     The classifier has misclassied SYN floods performed with forged bidirectional communications.  \
                     It is recommended to use more robust features."
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result


    #############################################################################
    # rate_payload_evasion()
    #
    # Adversarial evasion attack to forge packet rate and payload size
    #
    # Args:
    #   pkt_count - number of packets to send in attack
    #   speed - Time in microseconds to determine rate of flood
    #   data_size - Additional payload size in bytes added to SYN packet
    #
    # Returns:
    #    result: A string with the result of the test and description
    #
    def rate_payload_evasion(self, pkt_count, speed, data_size):
        print("Executing Slow Rate and Increased Payload attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0
        print("0%")

        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u' + str(speed) + ' -c ' + str(pkt_count) + ' -d ' + str(data_size) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i]
            host.cmd(cmd)

            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(5)

        print("Slow Rate and Increased Payload attack complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, False)

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against rate and payload evasion.  \
                     The classifier has misclassied SYN floods performed with an increased payload size of 130 bytes and a slowed rate of 20pps.  \
                     It is recommended to train with a variety of SYN packet sizes sent at varying speeds."
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result


    #############################################################################
    # rate_pairflow_evasion()
    #
    # Adversarial evasion attack to perturb packet rate and forge bidirectional traffic
    #
    # Args:
    #   pkt_count - number of packets to send in attack
    #   speed - Time in microseconds to determine rate of flood
    #   ret_speed - Time in microseconds to determine rate of flood bidirectional traffic
    #
    # Returns:
    #    result: A string with the result of the test and description
    #
    def rate_pairflow_evasion(self, pkt_count, speed, ret_speed):
        print("Executing Slow Rate and Pairflow Evasion attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0

        print("0%")
        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u' + str(speed) + ' -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i] + ' &'
            host.cmd(cmd)
            for j in range(int(pkt_count)):
                time.sleep(ret_speed/1000000)
                cmd_ret = 'nping --tcp syn --source-ip rand --dest-mac 00:00:00:00:00:0' + \
                           str(src_eth[i]) + ' --source-mac 00:00:00:00:00:0' + str(dst_eth[i]) + \
                           ' -c ' + str(1) + ' --data-length 0 --rate ' + str(1) + \
                           ' 10.0.0.' + dst_eth[i] + ' &'
                host.cmd(cmd_ret)
            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(1)

        print("Slow Rate + Pairflow attack complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, True)/2

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against rate and pair_flow evasion.  \
                     The classifier has misclassied SYN floods performed with forged bidirectional communications at slower rates.  \
                     It is recommended to use more robust features and train with varying flood rates."
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result


    #############################################################################
    # payload_pairflow_evasion()
    #
    # Adversarial evasion attack to perturb packet payload size and forge bidirectional traffic
    #
    # Args:
    #   pkt_count - number of packets to send in attack
    #   data_size - Additional payload size in bytes added to SYN packet
    #   ret_speed - Time in microseconds to determine rate of flood bidirectional traffic
    #
    # Returns:
    #    result: A string with the result of the test and description
    #
    def payload_pairflow_evasion(self, pkt_count, data_size, ret_speed):
        print("Executing Increased Payload and Pairflow Evasion attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0

        print("0%")

        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u1500 -c ' + str(pkt_count) + ' -d ' + \
                   str(data_size) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i] + ' &'
            host.cmd(cmd)
            for j in range(int(pkt_count)):
                time.sleep(ret_speed/1000000)
                cmd_ret = 'nping --tcp syn --source-ip rand --dest-mac 00:00:00:00:00:0' + \
                           str(src_eth[i]) + ' --source-mac 00:00:00:00:00:0' + str(dst_eth[i]) + \
                           ' -c ' + str(1) + ' --data-length ' + str(data_size) + ' --rate ' + str(1) + \
                           ' 10.0.0.' + dst_eth[i] + ' &'
                host.cmd(cmd_ret)
            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(1)

        print("Increased Payload and Pairflow attack complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, True)/2

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against payload and pair_flow evasion.  \
                     The classifier has misclassied SYN floods performed with forged bidirectional communications with increase payload sizes.  \
                     It is recommended to use more robust features and train with varying SYN payload sizes"
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result


    #############################################################################
    # stealth_evasion()
    #
    # Adversarial evasion attack to perturb packet payload size and rate and
    # forge bidirectional traffic
    #
    # Args:
    #   pkt_count - number of packets to send in attack
    #   data_size - Additional payload size in bytes added to SYN packet
    #   speed - Time in microseconds to determine rate of flood
    #   ret_speed - Time in microseconds to determine rate of flood bidirectional traffic
    #
    # Returns:
    #    result: A string with the result of the test and description
    #
    def stealth_evasion(self, pkt_count, data_size, speed, ret_speed):
        print("Executing Stealth Evasion attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0

        print("0%")
        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u' + str(speed) + ' -c ' + str(pkt_count) + ' -d ' + \
                   str(data_size) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i] + ' &'
            host.cmd(cmd)
            for j in range(int(pkt_count)):
                time.sleep(ret_speed/1000000)
                cmd_ret = 'nping --tcp syn --source-ip rand --dest-mac 00:00:00:00:00:0' + \
                           str(src_eth[i]) + ' --source-mac 00:00:00:00:00:0' + str(dst_eth[i]) + \
                           ' -c ' + str(1) + ' --data-length ' + str(data_size) + ' --rate  ' + str(1) + \
                           ' 10.0.0.' + dst_eth[i] + ' &'
                host.cmd(cmd_ret)
            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(1)

        print("Stealth Evasion complete!")

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, True) / 2

        print("Detection accuracy: " + str(acc) + "%")

        if acc < 90:
            result = "Detection accuracy: " + str(acc) + "%.  Classifier weakness against rate and payload and pair_flow evasion.  \
                     The classifier has misclassied SYN floods performed with forged bidirectional communications at slower rates with greater payload sizes.  \
                     It is recommended to use more robust features in relation to bidirectional traffic and train with varying flood rates and payload sizes."
        else:
            result = "Detection accuracy: " + str(acc) + "%"

        return acc, result


    #############################################################################
    # calc_acc(src_eth, dst_eth, stealth)
    #
    # Calculate the accuracy of the test based on the src and dst eth combinations
    # used and the intrusions detected by Neptune
    #
    # Args:
    #    src_eth: array of src_eths, each index corresponding to the destination from dst_eth
    #    dst_eth: array of dst_eths, each index corresponding to the source from src_eth
    #    stealth: boolean, True if it is a stealth evasion attack
    #
    # Returns:
    #    acc: float of accuracy
    #
    def calc_acc(self, src_eth, dst_eth, stealth):
        # Read the results of Neptune
        neptune_results_dir = self.dir + "nids_config/intrusion_results.txt"
        with open(neptune_results_dir, 'r') as neptune_results:
            results = neptune_results.read().splitlines()

        intrusions_detected = 0

        for line in results:
            # TODO: change this to src_eth + 1 and then rerun all tests to verify accuracy
            for i in range(0,len(src_eth)):
                # TODO: this filtering should be done in neptune to allow for dimensionality reduction.
                # Actually no, this filtering is fine. Look at what Neptune is doing!
                intrusion_stat = "00:00:00:00:00:0" + src_eth[i] + ",00:00:00:00:00:0" + dst_eth[i] + ",6,2"
                if line == intrusion_stat:
                    intrusions_detected += 1
                elif stealth:
                    # If the bidirectional stealth attacks are also detected
                    intrusion_stat_rev = "00:00:00:00:00:0" + dst_eth[i] + ",00:00:00:00:00:0" + src_eth[i] + ",6,2"
                    if line == intrusion_stat_rev:
                        intrusions_detected += 1

        # Add up the total accuracy and return it
        if intrusions_detected == 0:
            acc = 0
        else:
            acc = (intrusions_detected/len(src_eth))*100

        return acc


    #############################################################################
    # net_host(host_number)
    #
    # Method to return a network host object based on host number
    #
    # Returns:
    #    host: Mininet host object
    #
    def net_host(self,host_number):

        if host_number == 1:
            host = self.h1
        elif host_number == 2:
            host = self.h2
        elif host_number == 3:
            host = self.h3
        elif host_number == 4:
            host = self.h4
        elif host_number == 5:
            host = self.h5
        elif host_number == 6:
            host = self.h6
        elif host_number == 7:
            host = self.h7
        elif host_number == 8:
            host = self.h8
        elif host_number == 9:
            host = self.h9
        elif host_number == 10:
            host = self.h10
        elif host_number == 11:
            host = self.h11
        elif host_number == 12:
            host = self.h12
        elif host_number == 13:
            host = self.h13
        elif host_number == 14:
            host = self.h14
        else:
            host = -1
            logger.error('Invalid host number')

        return host
