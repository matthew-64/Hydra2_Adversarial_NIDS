#################################################################################
# Unit test Featurizer
#
# File: test_unit_featurizer.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class to unit test the Featurizer class
#
#################################################################################

import unittest
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..')) # Step back to correct directory

from featurizer import Featurizer

#################################################################################
# UnitFeaturizer()
#
# Class containing multiple unit tests implemented using unittest.TestCase
# which tests feature calculation methods from Featurizer.py
#
class UnitFeaturizer(unittest.TestCase):

    def test_unit_pair_flow_ratio(self):
        ft = Featurizer()

        key1 = '00:00:00:00:00:01_00:00:00:00:00:02_6_2'
        key2 = '00:00:00:00:00:02_00:00:00:00:00:01_6_2'
        key3 = '00:00:00:00:00:02_00:00:00:00:00:03_6_2'

        flow_dict = {}
        flow_dict[key1] = "00:00:00:00:00:01,00:00:00:00:00:02,6,2,8,8,0,480,480,0,20,0,1\n"
        flow_dict[key2] = "00:00:00:00:00:02,00:00:00:00:00:01,6,2,8,8,0,480,480,0,10,0,1\n"
        flow_dict[key3] = "00:00:00:00:00:02,00:00:00:00:00:03,6,2,8,8,0,480,480,0,5,0,1\n"

        stat = ['00:00:00:00:00:01','00:00:00:00:00:02','6','2','8','8','0','480','480','0','20','0','1\n']
        stat1 = ['00:00:00:00:00:02','00:00:00:00:00:03','6','2','8','8','0','480','480','0','5','0','1\n']

        ratio_1 = ft.pair_flow_ratio(stat, flow_dict)
        self.assertEqual(2.0, ratio_1)
        ratio_2 = ft.pair_flow_ratio(stat1, flow_dict)
        self.assertEqual(5, ratio_2)

    def test_unit_packet_pair_ratio(self):
        ft = Featurizer()

        ratio_1 = ft.packet_pair_ratio(0, 0)
        self.assertEqual(0, ratio_1)
        ratio_2 = ft.packet_pair_ratio(5, 0)
        self.assertEqual(0, ratio_2)
        ratio_3 = ft.packet_pair_ratio(5, 5)
        self.assertEqual(1, ratio_3)
        ratio_4 = ft.packet_pair_ratio(0, 1)
        self.assertEqual(1, ratio_4)

    def test_unit_packets_per_second(self):
        ft = Featurizer()

        ratio_1 = ft.packets_per_second(0, 0)
        self.assertEqual(0, ratio_1)
        ratio_2 = ft.packets_per_second(5, 0)
        self.assertEqual(5, ratio_2)
        ratio_3 = ft.packets_per_second(5, 5)
        self.assertEqual(1, ratio_3)

    def test_unit_bytes_per_second(self):
        ft = Featurizer()

        ratio_1 = ft.bytes_per_second(0, 0)
        self.assertEqual(0, ratio_1)
        ratio_2 = ft.bytes_per_second(5, 0)
        self.assertEqual(5, ratio_2)
        ratio_3 = ft.bytes_per_second(5, 5)
        self.assertEqual(1, ratio_3)

    def test_unit_bytes_per_packet(self):
        ft = Featurizer()

        ratio_1 = ft.bytes_per_packet(0, 0)
        self.assertEqual(0, ratio_1)
        ratio_2 = ft.bytes_per_packet(0, 5)
        self.assertEqual(0, ratio_2)
        ratio_3 = ft.bytes_per_packet(5, 5)
        self.assertEqual(1, ratio_3)
        ratio_4 = ft.bytes_per_packet(1, 0)
        self.assertEqual(0, ratio_4)

    def test_unit_featurizer(self):
        ft = Featurizer()

        features = '0,0,0,0,1.0'

        key1 = '00:00:00:00:00:01_00:00:00:00:00:02_6_2'
        key2 = '00:00:00:00:00:02_00:00:00:00:00:01_6_2'
        key3 = '00:00:00:00:00:02_00:00:00:00:00:03_6_2'

        flow_dict = {}
        flow_dict[key1] = "00:00:00:00:00:01,00:00:00:00:00:02,6,2,8,8,0,480,480,0,1,0,1\n"
        flow_dict[key2] = "00:00:00:00:00:02,00:00:00:00:00:01,6,2,8,8,0,480,480,0,1,0,1\n"
        flow_dict[key3] = "00:00:00:00:00:02,00:00:00:00:00:03,6,2,8,8,0,480,480,0,1,0,1\n"

        stat = ['00:00:00:00:00:01','00:00:00:00:00:02','6','2','0','0','0','0','0','0','1','0','0']
        self.assertEqual(features,ft.featurizer(stat, flow_dict))

if __name__ == '__main__':
    unittest.main()
