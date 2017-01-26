# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas


current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\GoldbetterExample'
copasi_file=r'Goldbeter1995_CircClock.cps'
goldbetter_model=os.path.join(current_directory,copasi_file)
report=os.path.join(current_directory,'TimeCourseOutput.txt')
#
TC=PyCoTools.pycopi.TimeCourse(goldbetter_model,ReportName=report,End=1000,
                               Intervals=50,StepSize=20,Plot='false')






































