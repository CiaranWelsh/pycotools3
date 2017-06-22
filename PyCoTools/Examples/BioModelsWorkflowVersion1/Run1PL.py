# -*- coding: utf-8 -*-
"""

 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 

run a profile likelihood
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
TC=PyCoTools.pycopi.TimeCourse(f,End=100,StepSize=1,Intervals=100,plot='true',
                               report_name=time_course_report,savefig='true')


#get some parameter estimation data 
PE=PyCoTools.pycopi.ParameterEstimation(f,time_course_report)

PE.write_item_template() #write the default template (estimation of all parameters)
PE.set_up()              # Automatic Parameter estimation setup   
PE.run()                #run the Parameter estimation 
#

'''
Output from parameter estimation is stored in default variable in the kwargs dict. 
You can change the default by giving a 'report_name' argument to the ParameterEstimation
class
'''
PyCoTools.pydentify2.ProfileLikelihood(f,parameter_path=PE.kwargs['report_name'],
                                       index=0,run='slow')





















