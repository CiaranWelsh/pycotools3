# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas
import sys
from FilePaths import KholodenkoExample

#instantiate FilePaths.KhodenkoExmaple to get necessary file paths
K=KholodenkoExample()

#run deterministic time course with kholodenko model
PyCoTools.pycopi.TimeCourse(K.kholodenko_model,ReportName=K.timecourse_report,End=1000,
                               Intervals=50,StepSize=20,Metabolites=['Mek1-P','Mek1'])
#                               )#,Plot='true',SaveFig='true')





































