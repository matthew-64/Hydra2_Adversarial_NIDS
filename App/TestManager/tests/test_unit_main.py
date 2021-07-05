#################################################################################
# Unit test TestManager main.py
#
# File: test_unit_main.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class to unit test the main.py of TestManager package
#
#################################################################################

import unittest
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0], '..')) # Step back to correct directory

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController

#################################################################################
# UnitTestManagerMain()
#
# Class containing multiple unit tests implemented using unittest.TestCase
# which tests the network launching
#
class UnitTestManagerMain(unittest.TestCase):
    def test_unit_launch_network(self):
        try:
            net = Mininet(autoSetMacs = True, cleanup = True)

            s1 = net.addSwitch('s1')

            for n in range(1,15):
                h = net.addHost('h%s' % n)
                net.addLink(h, s1)

            net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
            net.start()

            time.sleep(5)

            hosts = []
            for i in range(1,15):
                if i != 10:
                    hosts.append(net.get('h'+str(i)))

            self.assertEqual(net.ping(hosts),0.0)
        finally:
            net.stop()

if __name__ == '__main__':
    unittest.main()
