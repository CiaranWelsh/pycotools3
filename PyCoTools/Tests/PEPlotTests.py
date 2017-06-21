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


class ParameterEstimationPlotsTests(unittest.TestCase):
    
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
            
        self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,StepSize=100,Plot='false',Intervals=50,End=5000,ReportName=self.timecourse_report_name)
        self.TC2=PyCoTools.pycopi.TimeCourse(self.copasi_file,StepSize=100,Plot='false',Intervals=60,End=6000,ReportName=self.timecourse_report_name2)
        
        self.time_course_reports=[self.timecourse_report_name,self.timecourse_report_name2]
        for i in self.time_course_reports:
            PyCoTools.pycopi.PruneCopasiHeaders(i,replace='true')
        
        self.PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,self.time_course_reports,
                                                   NumberOfGenerations=1,
                                                   PopulationSize=1,
                                                   ReportName=self.PE_report_name,
                                                   Plot='false')
        self.PE.write_item_template()
        self.PE.set_up()
        self.PE.run()
    
    def test_PE_data_being_produced(self):
        self.assertTrue( os.path.isfile(self.PE_report_name))
        
        
    def test_len_exp_files(self):
        '''
        make sure PEdataPlot is recognizing all necessary experimetnal files
        '''
        PL= PyCoTools.PEAnalysis.PlotPEData(self.copasi_file,self.time_course_reports,
                                           self.PE_report_name,
                                           Plot='false')
        self.assertEqual(len( PL.experiment_files),len(self.time_course_reports))


    def test_parse_experimental_files1(self):
        '''
        
        '''
        PL= PyCoTools.PEAnalysis.PlotPEData(self.copasi_file,self.time_course_reports,
                                           self.PE_report_name,
                                           Plot='false')
        df1=pandas.read_csv(self.time_course_reports[0],sep='\t')
        key1= PL.experiment_data.keys()[0]
        self.assertEqual(df1.all().all(),PL.experiment_data[key1].all().all())

    def test_parse_experimental_files2(self):
        '''
        '''
        PL= PyCoTools.PEAnalysis.PlotPEData(self.copasi_file,self.time_course_reports,
                                           self.PE_report_name,
                                           Plot='false')
        df1=pandas.read_csv(self.time_course_reports[1],sep='\t')
        key1= PL.experiment_data.keys()[1]
        self.assertEqual(df1.all().all(),PL.experiment_data[key1].all().all())
        
        
    def test_prune_parameters(self):
        PL= PyCoTools.PEAnalysis.PlotPEData(self.copasi_file,self.time_course_reports,
                                           self.PE_report_name,
                                           Plot='false')
        PyCoTools.pycopi.PruneCopasiHeaders(self.PE_report_name,replace='true')
        est_parameters=pandas.DataFrame.from_csv(self.PE_report_name,sep='\t')
        self.assertEqual(est_parameters.all().all(),PL.parameters.all().all())
        
    def test_insert_parameters(self):
        PL= PyCoTools.PEAnalysis.PlotPEData(self.copasi_file,self.time_course_reports,
                                           self.PE_report_name,
                                           Plot='false')
        ICP=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
        for i in PL.parameters.keys():
            for j in ICP.get_all_model_variables().keys():
                if i==j:
                    if ICP.get_all_model_variables()[i]['type']=='Species':
                        model_val=ICP.get_all_model_variables()[i]['concentration']
                    else:
                        model_val=ICP.get_all_model_variables()[i]['value']
                    self.assertAlmostEqual( float(PL.parameters[i]),float(model_val))
                    
                    
    def test_plot(self):
        PL= PyCoTools.PEAnalysis.PlotPEData(self.copasi_file,self.time_course_reports,
                                           self.PE_report_name,
                                           Plot='true',SaveFig='true')
        os.chdir(PL.kwargs['OutputDirectory'])
        len_files=0
        for i in glob.glob('*'):
            len_files+=1
        os.chdir('..')
        if os.path.isdir(PL.kwargs['OutputDirectory']):
            shutil.rmtree(PL.kwargs['OutputDirectory'])
        self.assertEqual(len_files,PL.parameters.shape[1]-1)#, minus 1 for RSS
        
        
        
    def tearDown(self):
        if os.path.isfile(self.copasi_file):
            os.remove(self.copasi_file)
    
        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)
            
        if os.path.isfile(self.PE_report_name):
            os.remove(self.PE_report_name)
            

            
#        for i in glob.glob('*.jpeg'):
#            os.remove(i)
#        
#        for i in glob.glob('*.txt'):
#            os.remove(i)
#            
#        for i in glob.glob('*.xlsx'):
#            os.remove(i)
            
            
            
if __name__=='__main__':
    unittest.main()