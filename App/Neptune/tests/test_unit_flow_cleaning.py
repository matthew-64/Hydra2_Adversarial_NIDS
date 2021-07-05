#################################################################################
# Unit test FlowCleaning
#
# File: test_unit_flow_cleaning.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class to unit test the FlowCleaning class
#
#################################################################################

import unittest
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..')) # Step back to correct directory

from flow_cleaning import FlowCleaning

#################################################################################
# UnitFlowCleaning()
#
# Class containing multiple unit tests implemented using unittest.TestCase
# which tests flow cleaning methods from the FlowCleaning class
#
class UnitFlowCleaning(unittest.TestCase):

    maxDiff = None


    def test_unit_batch_aggregate(self):
        fc = FlowCleaning()
        cwdir = os.getcwd()
        key1 = '00:13:80:5c:32:c0_00:21:56:ef:bc:00_6_2'
        key2 = '00:13:80:5c:32:c1_00:21:56:ef:bc:00_6_2'
        dict = {}
        dict[key1] = "00:13:80:5c:32:c0,00:21:56:ef:bc:00,6,2,8,8,0,480,480,0,2,0,1\n"
        dict[key2] = "00:13:80:5c:32:c1,00:21:56:ef:bc:00,6,2,4,4,0,240,240,0,1,0,0\n"

        # Directory for testing statistics
        test_stats_dir = cwdir + '/App/Neptune/tests/test_stats/output_test.csv'
        test_target_dir = cwdir + '/App/Neptune/tests/test_stats/output_test_target.txt'
        live = False

        test_stats = open(test_stats_dir, 'r')
        test_target = open(test_target_dir, 'r')
        test_dict = fc.batch_aggregate(test_stats, test_target, live)

        self.assertDictEqual(dict,test_dict)

    def test_unit_aggregate_stats(self):
        fc = FlowCleaning()
        dir = os.getcwd() + '/App/Neptune/tests/test_stats/'
        fc.aggregate_stats(dir)

        agg_stats_file = open(dir+'FlowStats_cleaned.csv','r')
        agg_target_file = open(dir+'FlowStats_target_cleaned.txt', 'r')

        agg_stats = agg_stats_file.readlines()
        agg_target = agg_target_file.readlines()

        test_agg_stats = ['eth_src,eth_dst,ip_proto,state_flag,pkts,src_pkts,dst_pkts,bytes,src_bytes,dst_bytes,pkts_per_sec,bytes_per_second,bytes_per_packet,packet_pair_ratio,pair_flow\n','18:66:da:9b:e3:7d,b8:ac:6f:36:08:f5,6,-1,26,14,12,6318,3522,2796,2.6,631.8,243,0.793867120954,1\n','18:66:da:9b:e3:71,b8:ac:6f:36:08:f5,6,-1,26,14,12,6318,3522,2796,2.6,631.8,243,0.793867120954,1\n']
        test_agg_target = ['target\n','0\n','1\n']

        self.assertEqual(test_agg_stats, agg_stats)
        self.assertEqual(test_agg_target, agg_target)


if __name__ == '__main__':
    unittest.main()
