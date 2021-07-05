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
import random

from subprocess import Popen, PIPE

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController
from itertools import combinations


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

    net_assigned = False
    try:

        # Configure and launch Mininet
        setLogLevel('info')
        net = launch_network()
        net_assigned = True

        malicious_test_traffic(net)


    except KeyboardInterrupt:
        print("\nStopping network..\n")
        if net_assigned:
            net.stop()

        sys.exit(0)

    finally:
        if net_assigned:
            print("\nStopping network..\n")
            net.stop()
        time.sleep(5)


#################################################################################
# malicious_test_traffic()
#
# Method used to generate part of the malicious testing dataset
#
# Args:
#    net: the mininet Python API object
#
def malicious_test_traffic(net):
    L = [1,2,3,4,5,6,7,8,9,11,12,13,14]
    combs = [",".join(map(str, comb)) for comb in combinations(L, 2)]

    combs_1 = combs[:len(combs)//2]
    combs_2 = combs[len(combs)//2:]

    print("Ready to test..")
    time.sleep(10)

    total_packets = 0
    count = 0
    for i in combs_1:
        if total_packets > 50000:
            break
        elif count > 0:
            break
        count += 1
        print("Total packets: " + str(total_packets))

        result = [x.strip() for x in i.split(',')]
        src = result[0]
        dst = result[1]

        host = net_host(int(src), net)

        speed = random.randrange(1000,1000000)
        pkt_count = random.randrange(1,100)
        print("Pkts: " + str(pkt_count) + " Speed: " + str(speed))
        cmd = 'hping3 -i u' + str(speed) + ' -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst
        host.cmd(cmd)

        total_packets += pkt_count

    for i in combs_2:
        if total_packets > 350000:
            break

        print("Total packets: " + str(total_packets))

        result = [x.strip() for x in i.split(',')]
        src = result[0]
        dst = result[1]

        host = net_host(int(src), net)

        speed = random.randrange(1,10000)
        pkt_count = random.randrange(2000,30000)
        print("Pkts: " + str(pkt_count) + " Speed: " + str(speed))
        cmd = 'hping3 -i u' + str(speed) + ' -c ' + str(pkt_count) + ' -S -p 80 --rand-source 10.0.0.' + dst
        host.cmd(cmd)

        total_packets += pkt_count


#############################################################################
# net_host(host_number)
#
# Method to return a network host object based on host number
#
# Returns:
#    host: Mininet host object
#
def net_host(host_number,net):

    if host_number == 1:
        host = net.get('h1')
    elif host_number == 2:
        host = net.get('h2')
    elif host_number == 3:
        host = net.get('h3')
    elif host_number == 4:
        host = net.get('h4')
    elif host_number == 5:
        host = net.get('h5')
    elif host_number == 6:
        host = net.get('h6')
    elif host_number == 7:
        host = net.get('h7')
    elif host_number == 8:
        host = net.get('h8')
    elif host_number == 9:
        host = net.get('h9')
    elif host_number == 10:
        host = net.get('h10')
    elif host_number == 11:
        host = net.get('h11')
    elif host_number == 12:
        host = net.get('h12')
    elif host_number == 13:
        host = net.get('h13')
    elif host_number == 14:
        host = net.get('h14')
    elif host_number == 15:
        host = net.get('h15')
    elif host_number == 16:
        host = net.get('h16')
    elif host_number == 17:
        host = net.get('h17')
    elif host_number == 18:
        host = net.get('h18')
    elif host_number == 19:
        host = net.get('h19')
    elif host_number == 20:
        host = net.get('h20')
    else:
        host = -1
        print('Invalid host number: ' + str(host_number))
        sys.exit(0)

    return host


#################################################################################
# launch_network()
#
# Launches the Mininet network, connecting to the remote controller
#
# Returns:
#    net: the Mininet class network object
#
def launch_network():

    net = Mininet(cleanup = True)

    s1 = net.addSwitch('s1')

    for n in range(1,21):
        h = net.addHost('h%s' % n)
        net.addLink(h, s1)

    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    net.start()

    time.sleep(5)
    print("Network started..")

    return net


if __name__ == '__main__':

    main()
