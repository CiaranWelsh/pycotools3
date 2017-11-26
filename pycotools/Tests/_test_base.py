#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:43:23 2017

@author: b3053674

This file provides a set of base classes for pycotools.Tests only.
It is not used in pycotools itself.


"""
import pycotools
import test_models#, test_data
import unittest
import glob
import os
import shutil 
import pandas


class _BaseTest(unittest.TestCase):
    """
    class for all tests to inherit from. 
        -> Take string model from TestModels and write to file
        -> Initiate model
    """
    def setUp(self, test_model='test_model1'):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.test_model = test_model
        tests = ['test_model1', 'kholodenko_model']
        if self.test_model not in tests:
            raise pycotools.Errors.InputError('{} not in {}'.format(self.test_model, test_models) )

        with open(self.copasi_file,'w') as f:
            if self.test_model=='test_model1':
                f.write(test_models.TestModels.get_model1())
            elif self.test_model=='kholodenko_model':
                f.write(test_models.TestModels.get_model2())
            
        # self.GMQ = pycotools.pycopi.GetModelQuantities(self.copasi_file)
        self.model = pycotools.model.Model(self.copasi_file)

    def tearDown(self):
        tear_down = False
        delete_dirs = True

        if tear_down:
            dire = os.path.dirname(self.copasi_file)
            subdirs = ['Boxplots', 'TimeCourseGraphs',
                       'ParameterEstimationPlots', 'test_mpe',
                       'EnsembleTimeCourse', 'Histograms',
                       'LinearRegression', 'MultipleParameterEstimationResults',
                       'PCA', 'Scatters', 'ProfileLikelihoods']
            if delete_dirs:
                for i in subdirs:
                    d = os.path.join(dire, i)
                    if os.path.isdir(d):
                        shutil.rmtree(d)

            for i in glob.glob(os.path.join(dire, '*.xlsx') ):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.cps') ):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.txt') ):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.csv') ):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.pickle')):
                dire, fle = os.path.split(i)
                ## keep until I know keep list is not needed.
                keep_list = []
                if fle not in keep_list:
                    os.remove(i)

# class _ParameterEstimationBase(_BaseTest):
#     """
#     Simulate 2 time courses. Add noise then use PE class
#     """
#     def setUp(self):
#         super(_ParameterEstimationBase, self).setUp()
#
#         self.parameter_estimation_options={
#                  'metabolites':self.GMQ.get_IC_cns().keys(),
#                  'global_quantities':self.GMQ.get_global_quantities().keys(),
#                  'append': True,
#                  'confirm_overwrite': True,
#                  'overwrite_config_file': True,
#                  'update_model': True,
#                  'randomize_start_values': True,
#                  'create_parameter_sets': True,
#                  'calculate_statistics': True,
#                  'method': 'GeneticAlgorithm',
#                  'number_of_generations': 10,
#                  'population_size': 10,
#                  'random_number_generator': 4,
#                  'seed': 0,
#                  'pf': 0.675,
#                  'iteration_limit': 1140,
#                  'tolerance': 0.1,
#                  'rho': 0.2,
#                  'scale': 100,
#                  'swarm_size': 500,
#                  'std_deviation': 0.0000004641,
#                  'number_of_iterations': 1516400000,
#                  'start_temperature': 100,
#                  'cooling_factor': 0.85498,
#                  'scheduled': True,
#                  'plot':True,
#                  'savefig': True,
#                  'run': False}
#
#
#
#
#         self.TC1 = pycotools.pycopi.TimeCourse(self.model, end=1000, step_size=100,
#                                               intervals=10, report_name='report1.txt')
#         self.TC2 = pycotools.pycopi.TimeCourse(self.model, end=1000, step_size=100,
#                                               intervals=10, report_name='report2.txt')
#
#         data1 = pycotools.Misc.add_noise(self.TC1['report_name'])
#         data2 = pycotools.Misc.add_noise(self.TC2['report_name'])
#
#         os.remove(self.TC1['report_name'])
#         os.remove(self.TC2['report_name'])
#
#         data1.to_csv(self.TC1['report_name'], sep='\t')
#         data2.to_csv(self.TC2['report_name'], sep='\t')
#
#         self.PE = pycotools.pycopi.ParameterEstimation(self.copasi_file,
#                                                        [self.TC1['report_name'],
#                                                         self.TC2['report_name']],
#                                                        **self.parameter_estimation_options)
#
#     def tearDown(self):
#         super(_ParameterEstimationBase, self).tearDown()
#         if os.path.isdir(self.PE['results_directory']):
#             shutil.rmtree(self.PE['results_directory'])


# class _MultiParameterEstimationBase(_BaseTest):
#     def setUp(self):
#         super(_MultiParameterEstimationBase, self).setUp()
#
#         ## do time course
#         self.TC=pycotools.pycopi.TimeCourse(self.copasi_file,step_size=100,plot=False,
#                                                intervals=50,end=5000)
#
#         ## add noise
#         noisy_data = pycotools.Misc.add_noise(self.TC.report_name)
#         os.remove(self.TC.report_name)
#         noisy_data.to_csv(self.TC.report_name, sep='\t')
#
#
#
#         self.options={'copy_number':2,
#                       'pe_number':2,
#                       'population_size':10,
#                       'number_of_generations':20,
#                       'randomize_start_values':True,
#                       'plot':False,
#                       'line_width':3,
#                       'lower_bound':0.1,
#                       'upper_bound':100,
#                       'metabolites':[],
#                       'global_quantities':[]}
#
#         self.RMPE=pycotools.pycopi.RunMultiplePEs(self.copasi_file,
#                                                   self.report_name,
#                                                   **self.options)
#         self.RMPE.write_config_template()
#         self.RMPE.setup()
#         self.RMPE.run()
#         self.data = self.wait_for_PEs()
#         self.RMPE.format_results()
# #
# #
#     def wait_for_PEs(self):
#         number_of_expected_PEs = 4
#         x=0
#
#         while x!=number_of_expected_PEs:
#             df_dct = {}
#             for f in os.listdir(self.RMPE['results_directory']):
#                 f = os.path.join(self.RMPE['results_directory'], f)
#                 try:
#                     df_dct[f] = pandas.read_csv(f, sep='\t', skiprows=1,header=None)
#                 except IOError:
#                     continue
#                 except pandas.io.common.EmptyDataError:
#                     continue
#             try:
#                 df = pandas.concat(df_dct)
#
#             except ValueError:
#                 continue
#             x = df.shape[0]
#
#         return df
#
#     def test(self):
#         pass
#
#     def tearDown(self):
#         super(_MultiParameterEstimationBase, self).tearDown()
#         if os.path.isdir(self.RMPE['results_directory']):
#             shutil.rmtree(self.RMPE['results_directory'])
#

if __name__=='__main__':
    unittest.main()




















