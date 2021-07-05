#################################################################################
# Django views model for the Hydra Web Application
#
# File: views.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: Django views script to handle http requests from the web application
#       This class handles user test submission
#
#
# Usage: Methods are called based on a web page http request.  The index method
#        handles test submission and laucnhes the TestManager package main.py
#
#################################################################################

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from subprocess import Popen, PIPE, STDOUT

from .models import Test
from .forms import TestForm

import time
import os


#################################################################################
# index()
#
# Function to handle requests in relation to the page 'index'
# Handles GET and POST requests, then returns a render of the web page
#
# Args:
#    request: http request to be handled
#
def index(request):

    if request.method == 'GET':
        form = TestForm()
        tests = Test.objects.all()

        args = {'form': form, 'tests': tests}
        return render(request, 'testmanager/home.html', args)
    elif request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            dir = os.getcwd() + "/App/TestManager/"
            form.save()

            network_attack = form.cleaned_data["networkAttack"]
            ad_attack = form.cleaned_data["addAttackType"]
            preprocessing = form.cleaned_data["preprocessingType"]
            classifier = form.cleaned_data["classifier"]
            ad_training = form.cleaned_data["adTraining"]
            ensmeble_weight = form.cleaned_data["ensembleWeight"]

            # What existed before
            sub_time = form.cleaned_data['submissionTime']
            # target_classifier = form.cleaned_data['targetClassifier']
            # network_attack = form.cleaned_data['networkAttack']
            # adversarial_attack = form.cleaned_data['addAttackType']
            # results = form.cleaned_data['results']

            test = Test.objects.all().last()
            test.description = test_description(test.addAttackType)
            test.save()

            # Test manager executed

            # TODO: Lets just test the printed inputs in a different main
            # cmd = "sudo python3 {}main.py '{}' '{}' '{}'".format(str(dir),
            #        str(target_classifier), str(network_attack), str(adversarial_attack))

            cmd = "sudo python3 {}main.py {} {} {} {} {} {} {}".format(
                    str(dir),
                    network_attack,
                    ad_attack,
                    preprocessing,
                    classifier,
                    ad_training,
                    ensmeble_weight,
                    form.cleaned_data)

            Popen(['gnome-terminal', '-e', cmd], stdout=PIPE)

            results_dir = dir + "test_results/results.txt"
            open(results_dir,"w")

            while(test_result(results_dir) == '-1'):
                time.sleep(5)

            test = Test.objects.all().last()
            test.results = test_result(results_dir)
            test.save()

            return redirect('index')

        args = {'form': form, 'submissionTime':submissionTime}

        return render(request, 'testmanager/home.html', args)


#################################################################################
# test_result(dir)
#
# Checks if the test has been completed by reading the file from dir
#
# Args:
#    dir: file to check results
#
def test_result(dir):

    if os.path.isfile(dir):
        result = open(dir,"r")

        line = result.readline()
        if line == "":
            return '-1'
        else:
            return line
    else:
        return '-1'


#################################################################################
# test_description(attack)
#
# Generates a string based on the adversarial attack (used in html tooltips)
#
# Args:
#    attack: string of adversarial attack name
#
# Returns:
#    String of attack description
#
def test_description(attack):
    if "Evasion: Stealth" == attack:
        return "An evasion attack which performs stealth SYN floods with perturbed \
        slow packet rates of 20pps, increased payload sizes of 90 bytes and forged \
        bidirectional traffic to give the appearance of legitimate communications."
    elif "Evasion: Rate" == attack:
        return "An evasion attack which performs SYN floods with a low and slow \
        packet rate of approximately 20pps."
    elif "Evasion: Payload" == attack:
        return "An evasion attack which performs SYN floods with perturbed payload\
        sizes, with a payload of 90 bytes."
    elif "Evasion: Pairflow" == attack:
        return "An evasion attack with performs SYN floods with forged bidrectional\
        traffic to give the appearance of legitimate communications"
    elif "Evasion: Rate+Payload" == attack:
        return "An evasion attack which performs SYN floods with a low and slow \
        packet rate of approximately 20pps and a perturbed payload size of 90 bytes"
    elif "Evasion: Rate+Pairflow" == attack:
        return "An evasion attack which performs stealth SYN floods with perturbed \
        packet rates of 20pps and forged bidirectional traffic to give the appearance \
        of legitimate communications."
    elif "Evasion: Payload+Pairflow" == attack:
        return "An evasion attack which performs stealth SYN floods with perturbed \
        packet payload sizes of 90 bytes and forged bidirectional traffic to give \
        the appearance of legitimate communications."
    else:
        return "No attack description"


#################################################################################
# manual(request)
#
# Handles http GET request for 'manual page'
#
# Returns:
#    render of the manual html page
#
def manual(request):

    if request.method == 'GET':
        return render(request, 'testmanager/manual.html', {})
