#################################################################################
# Neptune flow preprocessing/cleaning class
#
# File: flow_cleaning.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class to implement flow cleaning on flow statistics to extract new features
#       and remove those not required.  Used in both training and live traffic
#       classification.
#
#
# Usage: Main method to handle cleaning is flow_stat_clean().  Calling it with the
#        appropriate parameters handles the preprocessing of batch of flows and
#        outputs them to a new cleaned file
#
# Requirements: featurizer.py
#
#################################################################################

import os
import logging

from featurizer import Featurizer


#################################################################################
# FlowCleaning()
#
# Class to pre-process flow stats from a batch
# This includes aggregating flow statistics on a device basis and calculating
# new features and removing unnecessary features
#
# Attributes:
#    featurizer: Object of the Featurizer class to add new features to flow stats
#
class FlowCleaning:

    featurizer = Featurizer()


    #############################################################################
    # flow_stat_clean(live, batch_number, poll_dur)
    #
    # Function to handle the full cleaning process
    # Either cleans all training batches
    # or cleans the batch with specified batch number for live classification
    #
    # Args:
    #    live: boolean True if live classification or False for training
    #    batch_number: batch_number to specify file to clean for live classification
    #    poll_dur: polling duration of stats used in feature generation
    #
    # Outputs cleaned flow batch to a new .csv file ready for classification
    #
    def flow_stat_clean(self, live, batch_number, poll_dur):

        if not live:
            file_num = 1
            # Clean all files in the training directory
            while(os.path.isfile("Neptune/stats_training/output" + str(file_num) + ".csv")):
                flow = "Neptune/stats_training/output" + str(file_num) + ".csv"
                target = "Neptune/stats_training/output" + str(file_num) + "_target.txt"

                # print(flow)
                # print(target)
                flow_stats = open(flow, 'r')
                flow_target = open(target, 'r')
                # print
                try:
                    flow_stats = open(flow, 'r')
                    flow_target = open(target, 'r')
                except:
                    logging.error('Unable to open stats and target files: {}, {}'.format(flow_stats, flow_target))

                batch_agg = self.batch_aggregate(flow_stats, flow_target, False)

                clean_dir = "Neptune/stats_training/output" + str(file_num) + "_cleaned.csv"
                target_dir = "Neptune/stats_training/output" + str(file_num) + "_target_cleaned.txt"

                self.batch_cleaning(clean_dir, target_dir, batch_agg, False, poll_dur)
                file_num += 1
        else:
            file_num = batch_number
            flow_dir = "Neptune/stats_live/output" + str(file_num) + ".csv"
            try:
                flow_stats = open(flow_dir, 'r')
            except:
                logging.error('Unable to open: ' + str(flow_dir))

            batch_agg = self.batch_aggregate(flow_stats, -1, True)

            clean_dir = "Neptune/stats_live/output" + str(file_num) + "_cleaned.csv"

            self.batch_cleaning(clean_dir, -1, batch_agg, True, poll_dur)


    #############################################################################
    # batch_cleaning(clean_dir, target_dir, batch_agg, live, poll_dur)
    #
    # Ouputs the cleaned stats with new features to the appropriate file
    #
    # Args:
    #    clean_dir: directory for the output of cleaned stats
    #    target_dir: directory for the adjusts target/ground truth values
    #    batch_agg: dictionary of cleaned statistics
    #    live: boolean True if live classification
    #    poll_dur: polling duration of stats used in feature generation
    #
    def batch_cleaning(self, clean_dir, target_dir, batch_agg, live, poll_dur):

        try:
            flow_cleaned = open(clean_dir, 'w')
        except:
            logging.error('Unable to open flow_cleaned file')

        # Final cleaned feature labels
        flow_cleaned.write("eth_src,eth_dst,ip_proto,state_flag,pkts,src_pkts,dst_pkts,bytes,src_bytes,dst_bytes," +
                           "pkts_per_sec,bytes_per_second,bytes_per_packet,packet_pair_ratio,pair_flow\n")
        if not live:
            try:
                target_cleaned = open(target_dir, 'w')
                target_cleaned.write("target\n")
            except:
                logging.error('Unable to open target cleaned file')


        # Generate new features for each flow and write each flow stat to file
        for i in batch_agg:
            stat = batch_agg[i].split(",")
            stat[11] = int(poll_dur)
            features = self.featurizer.featurizer(stat, batch_agg)

            flow_cleaned.write("{},{},{},{},{},{},{},{},{},{},{}\n"
                                     .format(stat[0], stat[1], stat[2], stat[3], stat[4], stat[5], stat[6], stat[7], stat[8],
                                             stat[9], features))
            if not live:
                if '\n' not in str(stat[11]):
                    target_cleaned.write("{}".format(stat[12]))
                else:
                    target_cleaned.write("{}".format(stat[12]))


    #############################################################################
    # batch_aggregate(flow_stats, flow_target, live)
    #
    # Aggregates flows with same src and dst and same protocols together
    # This provides statistics on an eth_src->eth_dst basis
    # Also generates new flow values to enable further features to be calculated
    # by the Featurizer class
    #
    # Args:
    #    flow_stats: array of flow stat records
    #    flow_target: array of ground truth values corresponding to flow stats
    #
    # Returns:
    #    batch_dict: dictionary of aggregated flow statistics using src, dst
    #                and protocol as unique key values
    #
    def batch_aggregate(self, flow_stats, flow_target, live):

        if not live:
            target_lines = flow_target.readlines()
        batch_dict = {}

        line_number = 0
        first_line_flag = True
        clean_calc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        flow_stats.seek(0)
        for line in flow_stats:
            if first_line_flag:
                first_line_flag = False
                line_number += 1
                continue

            stats = line.split(",")
            if str(stats[6]) == 'man':
                continue

            if 's' in str(stats[15]):
                state_flag = 2
            else:
                state_flag = -1

            key = (str(stats[0]) + "_" + str(stats[1]) + "_" + str(stats[6]) + "_" + str(state_flag))
            target = -1
            if not live:
                target = str(target_lines[line_number])

            # If flow stat exists in dictionary, aggregate the counted values such as pkt_count
            if key in batch_dict:
                old_stats = batch_dict[key].split(",")
                for i in range(len(old_stats)):
                    if i >= 4 and i <= 9:
                        clean_calc[i] = int(stats[i+4]) + int(old_stats[i])
                    elif i == 10:
                        clean_calc[i] = int(old_stats[i]) + 1

                # Set target value based on previous flow stat
                if old_stats[len(old_stats)-1] == 1 and target == 0:
                    target = 1

                batch_dict[key] = (str(stats[0]) + "," + str(stats[1]) + "," + str(stats[6]) + "," + str(state_flag) +
                                   "," + str(clean_calc[4]) + "," + str(clean_calc[5]) + "," + str(clean_calc[6]) + ","
                                   + str(clean_calc[7]) + "," + str(clean_calc[8]) + "," + str(clean_calc[9]) + "," +
                                   str(clean_calc[10]) + "," + str(0) + "," + str(target))

            else:
                batch_dict[key] = (str(stats[0]) + "," + str(stats[1]) + "," + str(stats[6]) + "," + str(state_flag) +
                                   "," + str(stats[8]) + "," + str(stats[9]) + "," + str(stats[10]) + "," + str(stats[11]) +
                                   "," + str(stats[12]) + "," + str(stats[13]) + "," + str(1) + "," + str(0) + "," +
                                   str(target))


            line_number += 1

        return batch_dict


    #############################################################################
    # aggregate_stats(dir)
    #
    # Aggregates all individual cleaned stat files in the training directory
    # into one file to train on
    #
    # Outputs aggregated flow file and target file
    #
    def aggregate_stats(self, dir):

        flow_stats = open(dir + "FlowStats_cleaned.csv", "w")
        flow_target = open(dir + "FlowStats_target_cleaned.txt", "w")

        # Process first file and include header labels
        file_num = 1
        for line in open(dir + "output" + str(file_num) + "_cleaned.csv"):
            flow_stats.write(line)
        for line in open(dir + "output" + str(file_num) + "_target_cleaned.txt"):
            flow_target.write(line)
        file_num += 1

        # Process remainder, excluding label headers
        while(os.path.isfile(dir + "output" + str(file_num) + "_cleaned.csv")):
            with open(dir + "output" + str(file_num) + "_cleaned.csv") as flow:
                # print(flow.name)
                flow_lines = flow.readlines()
                flow_lines.pop(0) # Remove header values
                for line in flow_lines:
                    flow_stats.write(line)
            with open(dir + "output" + str(file_num) + "_target_cleaned.txt") as target:
                # print(target.name)
                target_lines = target.readlines()
                target_lines.pop(0) # Remove header values
                for line in target_lines:
                    flow_target.write(line)
            file_num += 1
        flow_stats.close()
