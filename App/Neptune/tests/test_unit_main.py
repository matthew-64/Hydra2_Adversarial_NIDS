#################################################################################
# Unit test NeptuneNIDS main.py
#
# File: test_unit_main.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Class to unit test the NeptuneNIDS class in main.py
#
#################################################################################

import unittest
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..')) # Step back to correct directory

from main import NeptuneNIDS

#################################################################################
# UnitMain()
#
# Class containing multiple unit tests implemented using unittest.TestCase
# which tests the NeptuneNIDS methods that initialise and start the application
#
class UnitMain(unittest.TestCase):
    def test_unit_classifier_config(self):
        neptune = NeptuneNIDS()
        cwdir = os.getcwd()
        print(dir)
        models = ['RandomForestClassifier', 'KNeighborsClassifier', 'SVC', 'MLPClassifier']

        for i in range(1,5):
            with open(cwdir + "/nids_config/classifier_type.txt", 'w') as classifier_config:
                classifier_config.write(str(i))

            model = neptune.classifier_config()
            model_name = type(model).__name__

            self.assertEqual(model_name, models[i-1])


    def test_unit_initialise_files(self):
        os.chdir('../')
        cwdir = os.getcwd()
        neptune = NeptuneNIDS()

        neptune.initialise_files()
        dir = cwdir + "/App/Neptune/stats_live"
        # Check if stats_live is empty
        self.assertEqual(len(os.listdir(dir)),0)

        # Check if traffic.txt is present
        traffic_dir = dir + '/traffic.txt'
        self.assertEqual(os.path.isfile(traffic_dir), False)

        intrusion_dir = cwdir + '/App/nids_config/intrusion_results.txt'
        # Check if intrusion results is empty
        self.assertEqual(os.stat(intrusion_dir).st_size, 0)


if __name__ == '__main__':
    unittest.main()
