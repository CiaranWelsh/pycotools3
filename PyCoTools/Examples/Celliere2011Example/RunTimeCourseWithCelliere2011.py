# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas
import sys
import FilePaths

#instantiate FilePaths.KhodenkoExmaple to get necessary file paths
C=FilePaths.Celliere2011Example()

#run deterministic time course with kholodenko model
PyCoTools.pycopi.TimeCourse(C.celliere2011_model,ReportName=C.timecourse_report,End=4000,
                               Intervals=50,StepSize=80,Plot='true',SaveFig='true',
                               GlobalQuantities=None) #don't want global quantities right now





































