from art.estimators.classification.scikitlearn import ScikitlearnRandomForestClassifier
from art.estimators.classification.scikitlearn import ScikitlearnSVC
from art.estimators.classification.scikitlearn import SklearnClassifier
from art.estimators.classification.scikitlearn import ScikitlearnLogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

#################################################################################
#
# File: classifier_configuration.py
# Name: Matthew Elliott
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
#
#################################################################################


#############################################################################
# get_art_classifiers(classifiers)
#
# Main function of Featurizer, calculates all new features
#
# Args:
#    classifiers: a list of strings that describe the classifiers required
#
# Returns:
#    A list of classifiers that are from the adversarial-robustness-toolbox, and
#    thus compatable with the AdversarialTrainer class
#
def get_art_classifiers(classifiers):
    required_classifiers = []
    for claffifier_type in classifiers:
        if claffifier_type == "RF":
            required_classifiers.append(ScikitlearnRandomForestClassifier(RandomForestClassifier(bootstrap=True, min_samples_leaf=2,
                                                                            n_estimators=200, max_features='sqrt',
                                                                            min_samples_split=10, max_depth=50)))
        elif claffifier_type == "KNN":
            required_classifiers.append(SklearnClassifier(KNeighborsClassifier(p=1, weights='distance',
                                                                            algorithm='auto', n_neighbors=15)))
        elif claffifier_type == "SVM":
            required_classifiers.append(ScikitlearnSVC(SVC(kernel='linear', C=0.001, gamma=0.01, probability=True)))
        elif claffifier_type == "LR":
            required_classifiers.append(ScikitlearnLogisticRegression(LogisticRegression(C=0.1, penalty='l2', solver='lbfgs',
                                                                    multi_class='ovr', max_iter=1000)))
        else:
            raise Exception("No classifier found with " + str(claffifier_type) + "key")
    return required_classifiers
