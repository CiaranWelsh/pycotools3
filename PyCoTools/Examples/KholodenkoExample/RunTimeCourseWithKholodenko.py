# -*- coding: utf-8 -*-
'''
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
run a time course
 '''
import PyCoTools
import os
import pandas
import sys
from FilePaths import KholodenkoExample

#instantiate FilePaths.KhodenkoExmaple to get necessary file paths
K=KholodenkoExample()

#run deterministic time course with kholodenko model
PyCoTools.pycopi.TimeCourse(K.kholodenko_model,report_name=K.timecourse_report,End=1000,
                               Intervals=50,StepSize=20,metabolites=['Mek1-P','Mek1'],
                                                                    Markercolor='b',plot='true')
#                               )#,plot='true',savefig='true')





































