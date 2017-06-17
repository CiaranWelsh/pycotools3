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
 
'''

import PyCoTools
import unittest
import glob
import os
import numpy
import pandas
import time
import re
import shutil 
import scipy
import TestModels
import lxml.etree as etree

MODEL_STRING = TestModels.TestModels.get_model1()






class ParameterEstimationTests(unittest.TestCase):

    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, self.copasiML)

        self.timecourse_report_name=os.path.join(os.path.dirname(self.copasi_file),'vilarTimeCourse.txt')
        self.timecourse_report_name2=os.path.join(os.path.dirname(self.copasi_file),'vilarTimeCourse2.txt')

        self.PE_report_name=os.path.join(os.path.dirname(self.copasi_file),'VilarPEData.txt')

        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)
            
        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
            
        self.parameter_estimation_options={#report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'QuantityType':'concentration',
                 'ReportName':os.path.join(os.path.dirname(self.copasi_file),'PE_testing.txt'),
                 'Append': 'true', 
                 'ConfirmOverwrite': 'true',
                 'ConfigFilename':os.path.join(os.path.dirname(self.copasi_file),'ItemTemplate.xlsx'),
                 'OverwriteConfigFile':'true',
                 #
                 'UpdateModel':'true',
                 'RandomizeStartValues':'true',
                 'CreateParameterSets':'false',
                 'CalculateStatistics':'true',
                 #method options
                 'Method':'ScatterSearch',
                 #'DifferentialEvolution',
                 'NumberOfGenerations':64,
                 'PopulationSize':10,
                 'RandomNumberGenerator':4,
                 'Seed':0,
                 'Pf':0.675,
                 'IterationLimit':1140,
                 'Tolerance':0.1,
                 'Rho':0.2,
                 'Scale':100,
                 'SwarmSize':500,
                 'StdDeviation':0.0000004641,
                 'NumberOfIterations':1516400000,
                 'StartTemperature':100,
                 'CoolingFactor':0.85498,
                 #experiment definition options
                 'Save':'overwrite',   
                 'Scheduled':'true'
                 }
        self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,StepSize=100,Plot='false',Intervals=50,End=5000,ReportName=self.timecourse_report_name)
        self.TC2=PyCoTools.pycopi.TimeCourse(self.copasi_file,StepSize=100,Plot='false',Intervals=60,End=6000,ReportName=self.timecourse_report_name2)
        
        self.time_course_reports=[self.timecourse_report_name,self.timecourse_report_name2]
        for i in self.time_course_reports:
            PyCoTools.pycopi.PruneCopasiHeaders(i,replace='true')
   
#

    def test_write_item_template(self):
        '''
        testthat the item file template is written
        '''
        PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,
                                                        self.time_course_reports,
                                                        PopulationSize=2,
                                                        NumberOfGenerations=2,
                                                        RandomizeStartValues='false',
                                                        ReportName=self.PE_report_name,
                                                        Save='overwrite')
        PE.write_item_template()
        self.assertTrue(os.path.isfile(PE.kwargs.get('ConfigFilename')))
#        
    def test_insert_fit_items(self):
        '''
        Tests that there are the same number of rows in the template file 
        as there are fit items inserted into copasi
        '''
        PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,
                                                        self.time_course_reports,
                                                        PopulationSize=2,
                                                        NumberOfGenerations=2,
                                                        RandomizeStartValues='false',
                                                        ReportName=self.PE_report_name,
                                                        Save='overwrite')
        PE.write_config_template()
        PE.copasiML=PE.remove_all_fit_items()
        PE.copasiML= PE.insert_all_fit_items()
        num_fit_items= PE.read_item_template().shape[0]
        self.assertEqual(num_fit_items, len(PE.get_fit_items()))

    def test_set_PE_method(self):
        '''
        test to see if method has been properly inserted into the copasi file
        '''
        PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,
                                                    self.timecourse_report_name,
                                                    **self.parameter_estimation_options)
        PE.write_item_template()
        PE.set_up()
        
        tasks=PE.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name']=='Parameter Estimation':
                self.assertEqual(i[-1].attrib['type'].lower(),self.parameter_estimation_options['Method'].lower())

    def test_set_PE_options(self):
        PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,
                                                    self.timecourse_report_name,
                                                    **self.parameter_estimation_options)
        PE.write_item_template()
        PE.set_up()

        tasks=PE.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name']=='Parameter Estimation':
                self.assertEqual(i.attrib['scheduled'],self.parameter_estimation_options['Scheduled'])


    def tearDown(self):
        # if os.path.isfile(self.copasi_file):
        #     os.remove(self.copasi_file)

        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)
            
        for i in glob.glob('*.jpeg'):
            os.remove(i)
        
        for i in glob.glob('*.txt'):
            os.remove(i)
            
        for i in glob.glob('*.xlsx'):
            os.remove(i)
#        os.remove(i for i in self.time_course_reports if os.path.isfile(i))







        
if __name__=='__main__':
    unittest.main()