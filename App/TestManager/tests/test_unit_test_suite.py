import unittest
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController

from test_suite import TestSuite

class UnitTestManagerTestSuite(unittest.TestCase):
    def test_unit_net_host(self):
        try:
            net = Mininet(autoSetMacs = True, cleanup = True)

            s1 = net.addSwitch('s1')

            for n in range(1,15):
                h = net.addHost('h%s' % n)
                net.addLink(h, s1)

            net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
            net.start()

            time.sleep(2)

            hosts = []
            for i in range(1,15):
                hosts.append(net.get('h'+str(i)))

            ts = TestSuite('dir', 'test', 'test', net)

            for index,host in enumerate(hosts):
                index+=1

                self.assertEqual(str(host),str(ts.net_host(index)))

        finally:
            net.stop()

    def test_unit_calc_acc(self):
        try:
            dir = os.getcwd() + "/App/"
            net = Mininet(autoSetMacs = True, cleanup = True)

            s1 = net.addSwitch('s1')

            for n in range(1,15):
                h = net.addHost('h%s' % n)
                net.addLink(h, s1)

            net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
            net.start()

            ts = TestSuite(dir, 'test', 'test', net)

            neptune_results_dir = dir + "nids_config/intrusion_results.txt"
            with open(neptune_results_dir, 'w') as neptune_results:
                for i in range(1,6):
                    neptune_results.write("00:00:00:00:00:0"+str(i)+",00:00:00:00:00:0"+str(i+1)+",6,2\n")

            src_eth = ['1','2','3','4','7']
            dst_eth = ['2','3','4','5','6']
            self.assertEqual(ts.calc_acc(src_eth, dst_eth, False),80.0)

            src_eth = ['0','0','0','0','0']
            dst_eth = ['2','3','4','5','6']
            self.assertEqual(ts.calc_acc(src_eth, dst_eth, False),0.0)

            with open(neptune_results_dir, 'w') as neptune_results:
                self.assertEqual(ts.calc_acc(src_eth, dst_eth, False),0)

        finally:
            net.stop()


if __name__ == '__main__':
    unittest.main()
