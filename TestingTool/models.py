#################################################################################
# Django Test database model
#
# File: models.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: File specifying the database Test model fields
#
#################################################################################

from django.db import models


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    networkAttack = models.TextField()
    addAttackType = models.TextField()
    preprocessingType = models.TextField()
    classifier = models.TextField()
    adTraining = models.TextField()
    ensembleWeight = models.TextField()
    testNumber = models.TextField()
    results = models.TextField()
    submissionTime = models.TextField()


    # submissionTime = models.TextField()
    # targetClassifier = models.TextField()
    # networkAttack = models.TextField()
    # addAttackType = models.TextField()
    # results = models.TextField()
    # description = models.TextField()

