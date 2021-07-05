#################################################################################
# Django urls file
#
# File: urls.py
# Name: James Aiken
# Date: 25/03/2019
# Course: CSC4006 - Research and Development Project
# Desc: File containing url patterns corresponding to each page of the web
#       application
#
#################################################################################

from django.conf.urls import url, include
from . import views
from .models import Test

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('manual', views.manual, name='manual')
]
