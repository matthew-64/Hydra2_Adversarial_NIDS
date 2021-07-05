#################################################################################
# Django Form for Test database model
#
# File: forms.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: File specifying the Test Form corresponding to the Test databse model
#
# 
#################################################################################

from django import forms
from .models import Test


class TestForm(forms.ModelForm):

    networkAttack = forms.CharField()
    addAttackType = forms.CharField()
    preprocessingType = forms.CharField()
    # TODO; should this just be classifier?
    classifier = forms.CharField()
    adTraining = forms.CharField()
    ensembleWeight = forms.CharField()
    testNumber = forms.CharField()
    results = forms.CharField()
    submissionTime = forms.CharField()

    # What was here before:
    # testNumber = forms.CharField()
    # submissionTime = forms.CharField()
    # targetClassifier = forms.CharField()
    # networkAttack = forms.CharField()
    # addAttackType = forms.CharField()
    # results = forms.CharField()

    class Meta:
        model = Test
        fields = {
                "networkAttack",
                "addAttackType",
                "preprocessingType",
                "classifier",
                "adTraining",
                "ensembleWeight",
                "testNumber",
                "results",
                "submissionTime"}

        # fields = ('testNumber', 'submissionTime', 'targetClassifier', 'networkAttack',
        # 'addAttackType', 'results')
