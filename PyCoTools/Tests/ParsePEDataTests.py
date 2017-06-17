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
import unittest
import os
import re
import pandas
import numpy
import scipy
import PyCoTools
import glob
import shutil
import TestModels
import lxml.etree as etree

MODEL_STRING = TestModels.TestModels.get_model1()

class ParsePETests(unittest.TestCase):
    
    
    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, self.copasiML)

        self.timecourse_report_name=os.path.join(os.getcwd(),'timecourse.txt')
        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)
            
        self.PE_report_name=os.path.join(os.path.dirname(self.copasi_file),'PEdata.txt')
        self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,StepSize=100,Plot='false',Intervals=50,End=5000,ReportName=self.timecourse_report_name)
        PyCoTools.pycopi.PruneCopasiHeaders(self.timecourse_report_name,replace='true')
        
        self.PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,
                                                        self.timecourse_report_name,
                                                        PopulationSize=6,
                                                        NumberOfGenerations=5,
                                                        RandomizeStartValues='true',
                                                        ReportName=self.PE_report_name,
                                                        Save='overwrite',Plot='false')
        self.PE.write_item_template()
        self.PE.set_up()
                                                        
        self.S=PyCoTools.pycopi.Scan(self.copasi_file,ScanType='repeat',
                                        ReportType='parameter_estimation',
                                        Run='true',NumberOfSteps=3,
                                        ReportName=self.PE_report_name,Scheduled='true')

#        self.PE.run()
        self.PE_dir=os.path.join(os.path.dirname(self.copasi_file),'PE_dir')
        if os.path.isdir(self.PE_dir)==False:
            os.mkdir(self.PE_dir)
        new_fle= os.path.join(self.PE_dir,os.path.split(self.PE_report_name)[1])
        shutil.copy(self.PE_report_name,new_fle)
        
        
        self.GEP=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
    
    
    def test_read_from_file(self):
        P=PyCoTools.PEAnalysis.ParsePEData(self.PE_report_name)
        self.assertEqual(P.data.shape[0],int(self.S.kwargs.get('NumberOfSteps')))
        
    def test_read_from_folder(self):
        P=PyCoTools.PEAnalysis.ParsePEData(self.PE_dir)
        self.assertEqual(P.data.shape[0],int(self.S.kwargs.get('NumberOfSteps')))
        
    def test_pickle1(self):
        '''
        When UsePickle set to false, the pickle path should be made and not used
        '''        
        P=PyCoTools.PEAnalysis.ParsePEData(self.PE_dir,UsePickle='false')
        self.assertTrue(os.path.isfile(P.pickle_path))
        

        
        
    def test_pickle2(self):
        '''
        When use pickle is set to true but there is no pickle path, 
        turn UsePickle back to false and write a pickle file
        '''        
        P=PyCoTools.PEAnalysis.ParsePEData(self.PE_dir,UsePickle='true')
        self.assertTrue(os.path.isfile(P.pickle_path))

    def test_pickle3(self):
        '''
        The pickle feature should be used this way. First use the parse class
        once then when you use it again you don't have to wait to read all the 
        data again
        '''        
        PyCoTools.PEAnalysis.ParsePEData(self.PE_dir,UsePickle='false',OverwritePickle='false')
        p2=PyCoTools.PEAnalysis.ParsePEData(self.PE_dir,UsePickle='true',OverwritePickle='false')
        self.assertTrue(p2.for_testing=='pickle_true_overwrite_false')


    def test_pickle4(self):
        '''
        The pickle feature should be used this way. First use the parse class
        once then when you use it again you don't have to wait to read all the 
        data again
        '''        
        PyCoTools.PEAnalysis.ParsePEData(self.PE_dir,UsePickle='false',OverwritePickle='false')
        p2=PyCoTools.PEAnalysis.ParsePEData(self.PE_dir,UsePickle='true',OverwritePickle='true')
        self.assertTrue(p2.for_testing=='pickle_true_overwrite_true')
        
    def test_log10_conversion(self):
        PEData=PyCoTools.PEAnalysis.ParsePEData(self.PE_dir,UsePickle='false',OverwritePickle='false')
        print PEData.log_data
        
        
        
    def tearDown(self):
        os.remove(self.copasi_file)
        os.remove(self.PE_report_name)
        shutil.rmtree(self.PE_dir)
        for i in glob.glob('*.pickle'):
            os.remove(i)
        os.remove(self.PE.kwargs['ConfigFilename'])
        os.remove(self.timecourse_report_name)

#==============================================================================


if __name__=='__main__':
#    current_dir= os.getcwd()    
#    new_dir= os.path.join(os.getcwd(),r'Tests\Pydentify2Tests')
#    os.chdir(new_dir)

    unittest.main()
    
























