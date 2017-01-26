# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 21:44:50 2016

@author: b3053674
"""

import PyCoTools
import os


'''
Change variable 'f' to the full path to your own model
'''
f=r'.\Leloup1999_CircClock.cps'

wd=os.path.dirname(f)
os.chdir(wd)
time_course_report=os.path.join(wd,'timecourse.txt')

#first create a time course to get some fake data for parameter estimation
TC=PyCoTools.pycopi.TimeCourse(f,End=100,StepSize=1,Intervals=100,Plot='true',
                               ReportName=time_course_report,SaveFig='true')


#get some parameter estimation data 
PE=PyCoTools.pycopi.ParameterEstimation(f,time_course_report)

PE.write_item_template() #write the default template (estimation of all parameters)
PE.set_up()              # Automatic Parameter estimation setup   
PE.run()                #Run the Parameter estimation 
#

'''
Output from parameter estimation is stored in default variable in the kwargs dict. 
You can change the default by giving a 'ReportName' argument to the ParameterEstimation
class
'''
PyCoTools.pydentify2.ProfileLikelihood(f,ParameterPath=PE.kwargs['ReportName'],
                                       Index=0,Run='slow')





















