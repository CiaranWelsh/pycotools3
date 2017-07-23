#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:47:47 2017

@author: b3053674
"""

import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
import PyCoTools
import os, glob


model = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko.cps'



TC = PyCoTools.pycopi.TimeCourse(model, end = 1000, step_size=1, intervals=1000,
                            plot=False)

PE = PyCoTools.pycopi.ParameterEstimation(model, TC.kwargs['report_name'],
                                          method = 'GeneticAlgorithm',
                                          population_size=20,
                                          number_of_generations=20)

#PE.write_config_template()
PE.setup()
PE.run()
#print PE.format_results()

#GMQ=PyCoTools.pycopi.GetModelQuantities(model)
#print GMQ.get_fit_item_order()



pe_data ='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko_PE_results.txt'


I=PyCoTools.pycopi.InsertParameters(model, parameter_path=pe_data, index=0)
print I.parameters.transpose().sort_index()


os.system('CopasiUI {}'.format(model))
















