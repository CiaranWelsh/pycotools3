# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 21:44:50 2016

@author: b3053674
"""

import PyCoTools
import os



f=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\BIOMD0000000021\Leloup1999_CircClock.cps'

wd=os.path.dirname(f)
os.chdir(wd)
time_course_report=os.path.join(wd,'timecourse.txt')

#TC=PyCoTools.pycopi.TimeCourse(f,End=100,StepSize=1,Intervals=100,Plot='true',
#                               ReportName=time_course_report,SaveFig='true')



PE=PyCoTools.pycopi.ParameterEstimation(f,time_course_report)

#PE.write_item_template()
#PE.set_up()
#PE.run()
#

#import pandas
#df= pandas.DataFrame(pandas.DataFrame.from_csv(PE.kwargs.get('ReportName'),sep='\t').iloc[-1]).transpose()

PyCoTools.pydentify2.ProfileLikelihood(f,ParameterPath=PE.kwargs.get('ReportName'),
                                       Index=0,Run='slow')





















