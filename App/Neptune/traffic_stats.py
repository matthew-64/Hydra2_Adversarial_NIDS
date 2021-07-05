#################################################################################
# Neptune flow statistic collection class
#
# File: traffic_stats.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class with two core functionality.  Uses Argus for traffic flow statistic
#       collection.  Launch Argus and periodically poll for flow statistics to
#       create a training or testing dataset or to only poll for the past x seconds
#       of traffic when requested
#
#
# Usage: 1.) Use from a terminal 'sudo python traffic_stats.py' to begin traffic
#            collection to create a training or testing dataset.  The malicious class variable
#            is set at 0 or 1 depending on the traffic collected (supervised learning)
#        2.) Call the request stats method by itself from another class (Neptune)
#            This polls for the past x seconds of flow statistics and writes them to
#            a file.  This enables Neptune's live classification
#
# Requirements: Argus third party application installed on machine.
#               Popen module to run Argus as a daemon
#
#################################################################################

import os
import sys
import time
import logging

from subprocess import Popen, PIPE


#################################################################################
# TrafficStats()
#
#
# Class to handle the polling and writing of new flow stats from Argus using the
# Argus server and the Argus 'ra' client.  Writes traffic statistics to appropriate
# directory
#
class TrafficStats():

    #############################################################################
    # __init__()
    #
    #
    # Initialise class for traffic collection if it is training or live
    #
    # Attributes:
    #    malicious: Ground truth value for recording training statistics
    #    batch_number: Batch number to begin writing from, live execution
    #                  always starts at 1, training continues from the last
    #                  batch
    #
    def __init__(self):
        self.malicious = 1

        if os.path.isfile('stats_training/output1.csv'):
            file_exists = True
            file_num = 2

            while (file_exists):
                dir = 'stats_training/output' + str(file_num) + '.csv'
                if not os.path.isfile(dir):
                    file_exists = False
                else:
                    file_num += 1

            self.batch_number = file_num

        else:
            self.batch_number = 1


    #############################################################################
    # monitor()
    #
    # Main method to periodically call for flow statistics from Argus at a
    # 10 second interval.  Used for generating training set.
    #
    # Outputs flow statistics to training directory
    #
    def monitor(self):

        # Start Argus auditing
        training = True

        output_dir = os.getcwd() + "/stats_training/traffic.txt"

        if training:
            cmd = "sudo argus -m -d -i s1-eth10 -w " + output_dir + " &"
        Popen(['gnome-terminal', '-e', cmd], stdout=PIPE)

        # Flow stat collection loop
        while True:
            try:
                time.sleep(10)
                self.request_stats(self.batch_number, training)
                self.batch_number += 1
            except KeyboardInterrupt:
                sys.exit()


    #############################################################################
    # request_stats(self, batch_number, training)
    #
    # Method to request stats from Argus using the Argus client 'ra'
    # This is a system command executed using the os module.  This method is
    # used by Neptune to request live statistics and is also used by the monitor()
    # method of this TrafficStats class for generating training set
    #
    # Args:
    #    batch_number: number to write new batch file name
    #    training: boolean value True if training
    #
    def request_stats(self, batch_number, training):
        training_output_dir = os.getcwd() + "/Neptune/stats_training/traffic.txt"
        training_csv_output_dir = os.getcwd() + "/Neptune/stats_training/output"
        live_output_dir = os.getcwd() + "/Neptune/stats_live/traffic.txt"
        live_csv_output_dir = os.getcwd() + "/Neptune/stats_live/output"


        print("--Polling for recent flow statistics--")
        if training:
            cmd = "sudo ra -r " + training_output_dir + " - tcp -t -20s -s 'smac:16', 'dmac:16', 'saddr:16', 'sport:10', 'daddr:16', 'dport:10', 'proto','mean', 'pkts:10', 'spkts:10', 'dpkts:10', 'bytes:10', 'sbytes:10', 'dbytes:10', 'rate:15', 'state', 'dur:9' -nn -z -c ',' > " + training_csv_output_dir + str(batch_number) + ".csv"

        else:
            cmd = "sudo ra -r " + live_output_dir + " -t -20s -s 'smac:16', 'dmac:16', 'saddr:16', 'sport:10', 'daddr:16', 'dport:10', 'proto', 'mean', 'pkts:10', 'spkts:10', 'dpkts:10', 'bytes:10', 'sbytes:10', 'dbytes:10', 'rate:15', 'state', 'dur:9' -nn -z -c ',' > " + live_csv_output_dir + str(batch_number) + ".csv"
        os.system(cmd)

        if training:
            # Write flow stats and target to corresponding training batch
            num_lines = sum(1 for line in
                            open(training_csv_output_dir + str(batch_number) + ".csv"))

            target_dir = training_csv_output_dir + str(batch_number) + "_target.txt"
            try:
                with open(target_dir, 'w') as target:
                    target.write('target\n')
                    for i in range(int(num_lines) - 1):
                        target.write(str(self.malicious) + "\n")
            except:
                logging.error('Unable to open target_dir for training')


if __name__ == '__main__':
    try:
        ts = TrafficStats()
        ts.monitor()
    finally:
        os.system("sudo pkill -f 'argus'") # Terminate Argus daemon
