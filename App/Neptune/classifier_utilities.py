#################################################################################
# Neptune classifier functions script
#
# File: classifier_functions.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Utility script to perform cross validation and return accuracy, as well as RFE
#       for feature ranking.  This functionality can be applied to all available
#       classifiers in Neptune.  This script runs stand alone to the main Neptune
#       application
#       Also contains functionality to evaluate optimium hyperparameters for
#       classifiers
#
# Usage: This script only requires training traffic stats.  Execute the main
#        method using "sudo python classifier_accuracy.py 'Random Forest Model' '1'"
#
# Args: First argument is the classifier type:
#            - 'Random Forest Model'
#            - 'SVM'
#            - 'KNN'
#            - 'Neural Network'
#            - 'Logistic Regression'
#            - 'KMeans'
#        Second argument is the functionality of the script:
#            - '1' = Cross validated accuracy
#            - '2' = RFE feature ranking
#            - '3' = Hyperparameter tuning
#            - '4' = Testing accuracy
#
# Requirements: flow_cleaning.py
#
#################################################################################

import os
import sys
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix

from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import f1_score

from flow_cleaning import FlowCleaning


#################################################################################
# main()
#
# Machine learning model evaluation script, main method.  Cleans training data
# and performs functions on chosen classifier based on system arguments
#
# Prints results to console
#
def main():
    os.chdir(os.getcwd() + '/App/')
    classifier = sys.argv[1]
    functionality = sys.argv[2]

    with open('Neptune/stats_training/FlowStats_target_cleaned.txt', 'w') as flow_target_cleaned:
        flow_target_cleaned.write("target\n")

    ml_flow = classifier_config(classifier)

    # Clean training flow batches
    print("Cleaning flows..")
    fc = FlowCleaning()
    fc.flow_stat_clean(False, -1, 10)
    try:
        fc.aggregate_stats('Neptune/stats_training/')
    except:
        logging.error('Unable to generate aggregated files')

    flow_input = pd.read_csv(
    'Neptune/stats_training/FlowStats_cleaned.csv')
    flow_target = pd.read_csv(
    'Neptune/stats_training/FlowStats_target_cleaned.txt')

    # Extract mac addresses from feature inputs
    flow_input = flow_input.iloc[:,2:].apply(pd.to_numeric)
    # Convert to lists for iteration
    flow_input = list(flow_input.values.tolist())

    if int(functionality) == 1:
        cv_accuracy(ml_flow, flow_input, flow_target.values.ravel())
    elif int(functionality) == 2:
        rfe(ml_flow, flow_input, flow_target.values.ravel())
    elif int(functionality) == 3:
        tune_hyperparameters(classifier, flow_input, flow_target.values.ravel())
    elif int(functionality) == 4:
        testing_accuracy(ml_flow, flow_input, flow_target.values.ravel())
    else:
        print("Invalid function choice, exiting..")
        sys.exit(0)


#################################################################################
# cv_accuracy(model, input_data, input_target)
#
# Perform cross validation on classifier with training data
#
# Args:
#    model: machine learning model to use
#    input_data: Input features for classification
#    input_target: Target or ground truth values for training data
#
# Prints the mean cross validation accuracy for chosen classifier
#
def cv_accuracy(model, input_data, input_target):
    print("Running cross validation..")

    cross_val_score_stat = cross_val_score(model, input_data, input_target, scoring='accuracy', cv=5)
    mean_cross_val_score = cross_val_score_stat.mean()

    print("Mean Accuracy: ", mean_cross_val_score)


#################################################################################
# testing_accuracy(model, input_data, input_target)
#
# Evaluate accuracy over testing set and report confusion matrix
#
# Args:
#    model: machine learning model to use
#    input_data: Input features for classification
#    input_target: Target or ground truth values for training data
#    test_data: test features for classification
#    test_target: Target or ground truth values for test data
#
# Prints accuracy over the testing dataset
#
def testing_accuracy(model, input_data, input_target):
    print("Evaluating testing accuracy..")

    model.fit(input_data, input_target)

    test_data = pd.read_csv(
    'Neptune/stats_testing/FlowStats_cleaned.csv')
    test_target = pd.read_csv(
    'Neptune/stats_testing/FlowStats_target_cleaned.txt')

    # Extract mac addresses from feature inputs
    test_data = test_data.iloc[:,2:].apply(pd.to_numeric)
    # Convert to lists for iteration
    test_data = list(test_data.values.tolist())

    # Report classification accuracy
    acc = model.score(test_data, test_target.values.ravel())
    print("Testing classification accuracy: " + str(acc*100) + "%")

    predict = model.predict(test_data)
    print(predict)

    # Report the confusion matrix
    tn, fp, fn, tp = confusion_matrix(test_target, predict).ravel()
    print(tn,fp,fn,tp)

    print(f1_score(test_target, predict))



#################################################################################
# rfe(model, input_data, input_target)
#
# Performs Recursive Feature Elimination on input data to determine feature
# important rankings
#
# Args:
#    model: machine learning model to use
#    input_data: Input features for classification
#    input_target: Target or ground truth values for training data
#
# Prints feature rankings
#
def rfe(model, input_data, input_target):

    input_data = np.asarray(input_data)

    rfe = RFE(model, 1)
    fit = rfe.fit(input_data, input_target)

    print("Num Features: %d") % fit.n_features_
    print("Selected Features: %s") % fit.support_
    print("Feature Ranking: %s") % fit.ranking_


#################################################################################
# report(results, n_top=3)
# https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74
#
# Utility function to report the best cross validated scores with associated hyperparameters
#
# Args:
#    results: results from the randomized search cross validation
#    n_top = 3: report the top 3 scores and hyperparameters
#
# Prints scores and rankings
#
def report_accuracy(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.10f} (std: {1:.10f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")


#################################################################################
# tune_hyperparameters(classifier, input_data, input_target)
#
# Utility function to call the appropriate functions to tune the hyperparameters
# for a given classifier
#
# Args:
#    classifier: machine learning classifier string name to tune hyperparameters for
#    input_data: list of input training data
#    input_target: array of training target values
#
def tune_hyperparameters(classifier, input_data, input_target):
    if classifier == 'Random Forest Model':
        tune_rf(input_data, input_target)

    elif classifier == 'SVM':
        tune_svm(input_data, input_target)

    elif classifier == 'KNN':
        tune_knn(input_data, input_target)

    elif classifier == 'Neural Network':
        tune_mlp(input_data, input_target)

    elif classifier == 'Logistic Regression':
        tune_lr(input_data, input_target)

    elif classifier == 'KMeans':
        tune_kmeans(input_data, input_target)

    else:
        print("Invalid classifier argument, exiting..")
        sys.exit(0)


#################################################################################
# tune_rf(input_data, input_target)
#
# Carries out randomized search cross validation to find the optimum hyperparameters
# for the random forest classifier on the training set
#
# Args:
#    input_data: list of input training data
#    input_target: array of training target values
#
def tune_rf(input_data, input_target):
    # Random hyperparameter grid code source:
    # https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74

    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]

    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
           'max_features': max_features,
           'max_depth': max_depth,
           'min_samples_split': min_samples_split,
           'min_samples_leaf': min_samples_leaf,
           'bootstrap': bootstrap}

    rf = RandomForestClassifier()

    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,
                n_iter = 20, cv = 5, verbose=2, random_state=42, n_jobs = -1)

    rf_random.fit(input_data, input_target)

    report_accuracy(rf_random.cv_results_)


#################################################################################
# tune_svm(input_data, input_target)
#
# Carries out randomized search cross validation to find the optimum hyperparameters
# for the svm classifier on the training set
#
# Args:
#    input_data: list of input training data
#    input_target: array of training target values
#
def tune_svm(input_data, input_target):

    Cs = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    gammas = [0.0001,0.001, 0.01, 0.1, 1]
    kernel = ['linear','rbf']

    # Create the random grid
    random_grid = {'C': Cs,
           'gamma': gammas,
           'kernel': kernel}

    svc = SVC()

    svc_random = RandomizedSearchCV(estimator = svc, param_distributions = random_grid,
                n_iter = 20, cv = 5, verbose=2, random_state=42, n_jobs = -1)

    svc_random.fit(input_data, input_target)

    report_accuracy(svc_random.cv_results_)


#################################################################################
# tune_knn(input_data, input_target)
#
# Carries out randomized search cross validation to find the optimum hyperparameters
# for the knn classifier on the training set
#
# Args:
#    input_data: list of input training data
#    input_target: array of training target values
#
def tune_knn(input_data, input_target):

    nn = [int(x) for x in np.linspace(start = 2, stop = 15, num = 10)]
    weights = ['uniform','distance']
    alg = ['auto','ball_tree','kd_tree']
    p = [1,2,3,4,5,6,7,8,9,10]

    # Create the random grid
    random_grid = {'n_neighbors': nn,
           'weights': weights,
           'algorithm': alg,
           'p': p}

    knn = KNeighborsClassifier()

    knn_random = RandomizedSearchCV(estimator = knn, param_distributions = random_grid,
                n_iter = 20, cv = 5, verbose=2, random_state=42, n_jobs = -1)

    knn_random.fit(input_data, input_target)

    report_accuracy(knn_random.cv_results_)


#################################################################################
# tune_mlp(input_data, input_target)
#
# Carries out randomized search cross validation to find the optimum hyperparameters
# for the mlp classifier on the training set
#
# Args:
#    input_data: list of input training data
#    input_target: array of training target values
#
def tune_mlp(input_data, input_target):

    hidden_layer_sizes = [(100,), (50,50,50), (50,100,50), (5,2)]
    alpha = [0.000001,0.00001,0.0001,0.001,0.01,0.1,1]
    solver = ['lbfgs','sgd','adam']
    random_state = [1]

    random_grid = {'hidden_layer_sizes': hidden_layer_sizes,
            'alpha': alpha,
            'solver': solver,
            'random_state': random_state}

    mlp = MLPClassifier()

    mlp_random = RandomizedSearchCV(estimator = mlp, param_distributions = random_grid,
                n_iter = 20, cv = 5, verbose=2, random_state=42, n_jobs = -1)

    mlp_random.fit(input_data, input_target)

    report_accuracy(mlp_random.cv_results_)


#################################################################################
# tune_lr(input_data, input_target)
#
# Carries out randomized search cross validation to find the optimum hyperparameters
# for the logistic regression classifier on the training set
#
# Args:
#    input_data: list of input training data
#    input_target: array of training target values
#
def tune_lr(input_data, input_target):

    C = [0.0001,0.001,0.01,0.1,1,10,100,1000]
    penalty = ['l2']
    solver = ['lbfgs','newton-cg','liblinear','sag','saga']
    multi_class = ['ovr']

    random_grid = {'C': C,
            'penalty': penalty,
            'solver': solver,
            'multi_class': multi_class}

    lr = LogisticRegression(random_state=0)

    lr_random = RandomizedSearchCV(estimator = lr, param_distributions = random_grid,
                n_iter = 20, cv = 5, verbose=2, random_state=42, n_jobs = -1)

    lr_random.fit(input_data, input_target)

    report_accuracy(lr_random.cv_results_)


#################################################################################
# tune_kmeans(input_data, input_target)
#
# Carries out randomized search cross validation to find the optimum hyperparameters
# for the k means classifier on the training set
#
# Args:
#    input_data: list of input training data
#    input_target: array of training target values
#
def tune_kmeans(input_data, input_target):

    n_clusters = [int(x) for x in np.linspace(start = 1, stop = 30, num = 20)]
    max_iter = [50,100,200,300,400,500]
    tol = [0.00001,0.0001,0.001,0.01]
    random_state = [1]

    random_grid = {'n_clusters': n_clusters,
            'max_iter': max_iter,
            'tol': tol,
            'random_state': random_state}

    kmeans = KMeans()

    kmeans_random = RandomizedSearchCV(estimator = kmeans, param_distributions = random_grid,
                n_iter = 20, cv = 5, verbose=2, random_state=42, n_jobs = -1)

    kmeans_random.fit(input_data, input_target)

    report_accuracy(kmeans_random.cv_results_)


#################################################################################
# classifier_config(classifier)
#
# Initialise machine learning object based on classifier argument
#
# Args:
#    classifier: String name of ML classifier
#
# Returns:
#    ml_flow: sklearn machine learning model
#
def classifier_config(classifier):

    if classifier == 'Random Forest Model':
        ml_flow = RandomForestClassifier(bootstrap=True, min_samples_leaf=2,
        n_estimators=200, max_features='sqrt', min_samples_split=10, max_depth=50)
    elif classifier == 'SVM':
        ml_flow = SVC(kernel='linear', C=0.001, gamma=0.0001, probability=True)
    elif classifier == 'KNN':
        ml_flow = KNeighborsClassifier(p=1, weights='distance', algorithm='auto',
        n_neighbors=15)
    elif classifier == 'Neural Network':
        ml_flow = MLPClassifier(alpha=0.1, solver='adam', hidden_layer_sizes=(50, 50, 50))
    elif classifier == 'Logistic Regression':
        ml_flow = LogisticRegression(C=0.1, penalty='l2', solver='lbfgs',
        multi_class='ovr')
    elif classifier == 'KMeans':
        ml_flow = KMeans(n_clusters=3, random_state=0)
    else:
        print("Invalid classifier argument, exiting..")
        sys.exit(0)

    return ml_flow


if __name__ == '__main__':
    main()
