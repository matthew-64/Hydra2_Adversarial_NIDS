#################################################################################
# Featurizer class
#
# File: featurizer.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class to generate further flow statistic features based on the statistics
#       gathered.  A requirement of flow_cleaning.py
#
# Usage: featurizer(stat, flow_dict) is called by flow_cleaning.py to calculate
#        new features for a specific flow entry
#
#################################################################################

from __future__ import division


#################################################################################
# Featurizer()
#
# Class containing multiple feature generating methods for the FlowCleaning class
#
class Featurizer:


    #############################################################################
    # feaurizer(stat, flow_dict)
    #
    # Main function of Featurizer, calculates all new features
    #
    # Args:
    #    stat: current flow statistic to add features to
    #    flow_dict: dictionary of all recorded flow statistics
    #
    # Returns:
    #    Comma separated string of the new features
    #
    def featurizer(self, stat, flow_dict):

        pkts_per_sec = self.packets_per_second(stat[4], stat[11])
        bytes_per_second = self.bytes_per_second(stat[7], stat[11])
        bytes_per_packet = self.bytes_per_packet(stat[7], stat[4])
        packet_pair_ratio = self.packet_pair_ratio(stat[8], stat[9])
        pair_flow_ratio = self.pair_flow_ratio(stat, flow_dict)

        return str(pkts_per_sec) + "," + str(bytes_per_second) + "," + str(bytes_per_packet) + "," + \
               str(packet_pair_ratio) + "," + str(pair_flow_ratio)


    #############################################################################
    # pair_flow_ratio(stat, flow_dict)
    #
    # Calculate the pair flow ratio for the current investigated stat
    # Pair flow is the ratio of packets src->dst : dst->src
    #
    # Loops through the flow_dict searching for a bidirectional flow of the same
    # protocol to perform the calculation
    #
    # Args: See featurizer function
    #
    # Returns: ratio: float of the pair flow ratio for stat
    #
    def pair_flow_ratio(self, stat, flow_dict):

        key = (str(stat[0]) + "_" + str(stat[1]) + "_" + str(stat[2]) + "_" + str(stat[3]))
        key_stat = flow_dict[key].split(",")

        key_pair = (str(stat[1]) + "_" + str(stat[0]) + "_" + str(stat[2]) + "_" + str(stat[3]))

        ratio = 1
        for i in flow_dict:
            ratio = int(key_stat[10])
            if i == key_pair:
                key_pair_stat = flow_dict[i].split(",")
                ratio = int(key_stat[10])/int(key_pair_stat[10])
                break

        return ratio


    #############################################################################
    # packet_pair_ratio(source_pkts, dest_pkts)
    #
    # Calculate ratio between src packets and dst packets of a flow
    #
    # Returns: float of packet_pair_ratio calculated
    #
    def packet_pair_ratio(self, source_pkts, dest_pkts):
        if int(dest_pkts) == 0:
            return 0
        elif int(source_pkts) == 0:
            return dest_pkts
        else:
            return int(dest_pkts)/int(source_pkts)


    #############################################################################
    # packets_per_second(packet_count, duration)
    #
    # Calculate packets per second of a flow = packet_count/duration
    #
    # Returns: float of packets per second calculated
    #
    def packets_per_second(self, packet_count, duration):
        if int(packet_count) == 0:
            return 0
        elif int(duration) == 0:
            return packet_count
        else:
            return int(packet_count)/int(duration)

    #############################################################################
    # bytes_per_second(byte_count, duration)
    #
    # Calculate bytes per second of a flow = byte_count/duration
    #
    # Returns: float of bytes per second calculated
    #
    def bytes_per_second(self, byte_count, duration):
        if int(byte_count) == 0:
            return 0
        elif int(duration) == 0:
            return byte_count
        else:
            return int(byte_count)/int(duration)


    #############################################################################
    # bytes_per_packet(byte_count, packet_count)
    #
    # Calculate bytes per packet of a flow = byte_count/packet_count
    #
    # Returns: float of bytes per pakcet calculated
    #
    def bytes_per_packet(self, byte_count, packet_count):
        if int(byte_count) == 0:
            return 0
        elif int(packet_count) == 0:
            return 0
        else:
            return int(byte_count)/int(packet_count)
