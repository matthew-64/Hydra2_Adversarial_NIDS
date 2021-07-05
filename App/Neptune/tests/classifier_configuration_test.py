from art.estimators.classification.scikitlearn import ScikitlearnRandomForestClassifier
from art.estimators.classification.scikitlearn import ScikitlearnSVC
from art.estimators.classification.scikitlearn import ScikitlearnLogisticRegression
from sklearn.neighbors._classification import KNeighborsClassifier
from classifier_configuration import get_art_classifiers
import pandas as pd
import unittest


def read_test_data():
    return pd.read_csv("../test_resources/test_output.csv")


class TestFeatureSelection(unittest.TestCase):

    def test_get_RF(self):
        classifier = get_art_classifiers(["RF"])[0]
        self.assertEqual(
                ScikitlearnRandomForestClassifier,
                type(classifier))

    def test_get_KNN(self):
        classifier = get_art_classifiers(["KNN"])[0]
        self.assertEqual(
                KNeighborsClassifier,
                type(classifier.model))

    def test_get_SVM(self):
        classifier = get_art_classifiers(["SVM"])[0]
        self.assertEqual(
                ScikitlearnSVC,
                type(classifier))

    def test_get_LR(self):
        classifier = get_art_classifiers(["LR"])[0]
        self.assertEqual(
                ScikitlearnLogisticRegression,
                type(classifier))


if __name__ == '__main__':
    unittest.main()
