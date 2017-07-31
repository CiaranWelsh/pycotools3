#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:47:47 2017

@author: b3053674
"""

import site
#site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir(r'/home/b3053674/Documents/PyCoTools')
import PyCoTools
import os, glob
import numpy

#model = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko.cps'
#model2 = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko_1.cps'
#
#
#dire = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/MultipleParameterEstimationResults'
#
#pl_d='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.txt'
#pl_f='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.cps'
##
##
#
#results_d = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Test4'
#results_f = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/test1/ParameterFit1.txt'







import pandas
import os,glob
import site
#site.addsitedir(r'/home/b3053674/Documents/PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models

dire = r'/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial'
kholodenko_model = os.path.join(dire, 'kholodenko_model.cps')

def get_model(model_filename):
    TM = test_models.TestModels()
    kholodenko_string = TM.get_kholodenko_variant1()
    with open(model_filename, 'w') as f:
        f.write(kholodenko_string)
    return model_filename


m = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/MultipleParameterEstimationResults'

f = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/kholodenko_model_1.cps'
from PyCoTools.pycopi import *

#FormatPEData.format_folder(f, m)

#kholodenko = get_model(kholodenko_model)
#TC = PyCoTools.pycopi.TimeCourse(kholodenko, end=1000, step_size=100, intervals=10)
#RMPE = PyCoTools.pycopi.RunMultiplePEs(kholodenko, TC['report_name'], metabolites=[],
#                                       global_quantities=[], lower_bound=0.1, upper_bound=100, 
#                                       results_directory=m, copy_number=3, pe_number=3)

#RMPE.write_config_template()
#RMPE.setup()
#RMPE.format_results()

#    
##    
#
#kholodenko2 = os.path.join(dire, 'kholodenko_model_1.cps')
#
#
#pe_results = r'/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/MultipleParameterEstimationResults'
#
#
#F = PyCoTools.pycopi.FormatPEData(kholodenko2, pe_results, report_type='multi_parameter_estimation')
#F.format_folder(pe_results)
PyCoTools.pydentify.Plot(f, parameter_path=m, index=[0,1,2,3], 
                         )




























