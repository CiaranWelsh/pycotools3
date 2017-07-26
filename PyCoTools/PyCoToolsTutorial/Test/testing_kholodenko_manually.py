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


dire = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/MultipleParameterEstimationResults'

pl_d='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.txt'
pl_f='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.cps'
#
#
#
#
#PyCoTools.pycopi.Reports(model, report_type='multi_parameter_estimation')
#
#
#
#os.system('CopasiUI {}'.format(model))







#PyCoTools.pydentify.FormatPLData(pl_f, pl_d).format


#P = PyCoTools.pydentify.Plot(model, parameter_path = dire, rss=0.1)#, index=0)#, mode='one', plot_index = 0, plot_parameter='(dephosphorylation of MAPK-PP).V9')
#
#PyCoTools.pycopi.Reports(model, report_type='profilelikelihood2', variable='A')
##
#os.system('CopasiUI {}'.format(model))
#S=PyCoTools.pycopi.Scan(model, scan_type='scan', variable='A')


#os.system('CopasiUI {}'.format(model))

#PL = PyCoTools.pydentify.ProfileLikelihood(model, run='slow', index=-1, iteration_limit=25, 
#                                           number_of_steps = 10,
#                                           tolerance = 1e-3)

#PyCoTools.pydentify.Plot(model, rss=0.01, index=-1, mode='one',
#                         plot_index=-1, plot_parameter='(MAPKKK activation).K1',
#                         log10=True)

#f=r'/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/-1/B.cps'
#import subprocess
#
#def run(copasi_file):
#    '''
#    Process the copasi file using CopasiSE
#    Must be Copasi version 16
#    
#    '''
#    args=['CopasiSE',"{}".format(copasi_file)] 
#    p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
#    output,err= p.communicate()
#    d={}
#    d['output']=output
#    d['error']=err
#    if err!='':
#       raise PyCoTools.Errors.CopasiError('Failed with Copasi error: \n\n'+d['error'])
#    return d['output']
#
#run(f)
#

#
TC = PyCoTools.pycopi.TimeCourse(model, end = 1000, step_size=1, intervals=1000,
                            plot=False)

#print TC['report_name']
#
PyCoTools.Misc.add_noise(TC['report_name'])
####
RMPE = PyCoTools.pycopi.RunMultiplePEs(model, TC.kwargs['report_name'], copy_number = 4,
                                       pe_number = 25, population_size = 20, 
                                       number_of_generations=20, results_directory = 'test1')
#
#RMPE.write_config_template()
RMPE.setup()
RMPE.run()
#RMPE.format_results()
#PE = PyCoTools.pycopi.ParameterEstimation(model, TC.kwargs['report_name'],
#                                          method = 'GeneticAlgorithm',
#                                          population_size=20,
#                                          number_of_generations=20,
#                                          plot=True)
#
##PE.write_config_template()
#PE.setup()
#PE.run()
#print PE.format_results()

#GMQ=PyCoTools.pycopi.GetModelQuantities(model)
#print GMQ.get_fit_item_order()


#
#pe_data ='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko_PE_results.txt'
#
#
#I=PyCoTools.pycopi.InsertParameters(model, parameter_path=pe_data, index=0)
#print I.parameters.transpose().sort_index()
#
#
#os.system('CopasiUI {}'.format(model))
#















