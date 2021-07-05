#################################################################################
# Hydra testing to evaluate perturbation effects on detection accuracy
#
# File: test_evasion_eval.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: TestSuite class to evaluate the effects that perturbing different features
#       by different amounts has on detection accuracy
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
# EvasionEval()
#
# Class which contains all adversarial testing evaluation
# Executes tests based on test configuration and returns result
#
#
class EvasionEval:


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
    def __init__(self, dir, network_attack, adversarial_attack, net):

        self.dir = dir
        self.network_attack = network_attack
        self.adversarial_attack = adversarial_attack
        self.net = net

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
        if str(self.network_attack) == "SYN Flood":
            # Fixed packet count for adversarial classification evaluation
            if str(self.adversarial_attack) == "packet_rate":
                result = self.packet_rate(2000)
            elif str(self.adversarial_attack) == "packet_size":
                result = self.packet_size(2000)
            elif str(self.adversarial_attack) == "pair_flow":
                result = self.pair_flow(2000)
            elif str(self.adversarial_attack) == "base100":
                result = self.base_detection(100)
            elif str(self.adversarial_attack) == "base1000":
                result = self.base_detection(1000)
            elif str(self.adversarial_attack) == "base2000":
                result = self.base_detection(2000)
            elif str(self.adversarial_attack) == "base5000":
                result = self.base_detection(5000)
            else:
                print("Invalid adversarial attack..")
                logger.error('Invalid adversarial attack: ' + str(self.adversarial_attack))
        else:
            print("Invalid network attack..")
            logger.error('Invalid network attack: ' + str(self.network_attack))

        return result


    def pair_flow(self, pkt_count):
        print("Executing Stealth Evasion attack..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0
        speeds = [1,1500,3000,5000,7500,15000,30000,45000,60000,75000]

        print("0%")
        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u1500 -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i] + ' &'
            host.cmd(cmd)
            for j in range(int(pkt_count)):
                time.sleep(int(speeds[i])/1000000)
                cmd_ret = 'nping --tcp syn --source-ip rand --dest-mac 00:00:00:00:00:0' + \
                           str(src_eth[i]) + ' --source-mac 00:00:00:00:00:0' + str(dst_eth[i]) + \
                           ' -c ' + str(1) + ' --rate ' + str(1) + \
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

        acc = self.calc_acc(src_eth, dst_eth, True)

        print("Detection accuracy: " + str(acc))


        result = "pair_flow " + str(speed) + " accuracy: " + str(acc)

        return result


    def packet_rate(self, pkt_count):
        #print("Testing packet_rate perturbation: " + str(speed))
        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0
        speeds = [1,1500,3000,5000,7500,15000,30000,45000,60000,75000]

        print("0%")
        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u' + str(speeds[i]) + ' -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i]
            host.cmd(cmd)

            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(5)

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, False)

        print("Detection accuracy: " + str(acc))

        result = "packet_rate " + str(speed) + " accuracy: " + str(acc)

        return result


    def packet_size(self, pkt_count):
        print("Executing Size Evasion test..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0
        data_sizes = [0,10,20,30,40,50,60,70,80,90]

        print("0%")

        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u1500 -c ' + str(pkt_count) + ' -d ' + str(data_sizes[i]) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i]
            host.cmd(cmd)
            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(5)

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, False)

        print("Detection accuracy: " + str(acc))


        result = "data_size " + str(data_size) + " accuracy: " + str(acc)

        return result


    def base_detection(self, pkt_count):
        print("Executing base detection evaluation..")

        src_eth = ['2','1','3','4','4','6','2','4','6','7']
        dst_eth = ['1','3','2','5','1','9','9','2','3','2']

        # Send attack traffic
        count = 0
        speeds = [1,100,500,1000,1500,3000,5000,7500,15000,20000]

        print("0%")

        for i in range(0,len(src_eth)):
            host = self.net_host(int(src_eth[i]))
            cmd = 'hping3 -i u' + str(speeds[i]) + ' -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst_eth[i]
            host.cmd(cmd)
            count += 1

            perc_progress = (100/len(src_eth))*count
            str_progress = '-'*count
            print(str(perc_progress) + '% ' + str_progress)
            time.sleep(2)

        print("Aggregating results, please wait..")
        time.sleep(20)

        acc = self.calc_acc(src_eth, dst_eth, False)

        print("Detection accuracy: " + str(acc))


        result = str(pkt_count) + ': ' + str(acc)

        return result


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
            for i in range(0,len(src_eth)):
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
