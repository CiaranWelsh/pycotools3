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

class ReportsTests(unittest.TestCase):


    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, self.copasiML)

        self.timecourse_report_name=os.path.join(os.getcwd(),'cheese.txt')
        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)
            
        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
        self.report_options={#report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'QuantityType':'concentration',
                 'ReportName':'cheese.txt',
                 'Append': '1', 
                 'ConfirmOverwrite': '0',
                 'Save':'overwrite',
                 'ReportType':'profilelikelihood'}

        
        
    def tearDown(self):
        if os.path.isfile(self.copasi_file):
            os.remove(self.copasi_file)

        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)
            
        for i in glob.glob('*.jpeg'):
            os.remove(i)
        
        for i in glob.glob('*.txt'):
            os.remove(i)
            
        for i in glob.glob('*.xlsx'):
            os.remove(i)


    def test_timecourse_report(self):
        new_report_options={'ReportType':'time_course'}
        self.report_options.update(new_report_options)
        R=PyCoTools.pycopi.Reports(self.copasi_file,**self.report_options)
        l=[]
        for i in R.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            l.append(i.attrib['name'])
        self.assertTrue(self.report_options['ReportType'],l)
    
    def test_profile_likelihood_report(self):
        new_report_options={'ReportType':'profilelikelihood'}
        self.report_options.update(new_report_options)
        R=PyCoTools.pycopi.Reports(self.copasi_file,**self.report_options)
        l=[]
        for i in R.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            l.append(i.attrib['name'])
        self.assertTrue(self.report_options['ReportType'],l)


    def test_parameter_estimation_report(self):
        new_report_options = {'ReportType': 'parameter_estimation'}
        self.report_options.update(new_report_options)
        R = PyCoTools.pycopi.Reports(self.copasi_file, **self.report_options)
        l = []
        for i in R.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            l.append(i.attrib['name'])
        self.assertTrue(self.report_options['ReportType'], l)
        
if __name__=='__main__':
    unittest.main()