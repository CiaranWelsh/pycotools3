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

class TimeCourseTests(unittest.TestCase):

    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, self.copasiML)

        self.timecourse_report_name=os.path.join(os.getcwd(),'cheese.txt')
        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)

        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)

        self.options={'Intervals':'10',
                 'StepSize':'100',
                 'End':'1000',
                 'RelativeTolerance':'1e-7',
                 'AbsoluteTolerance':'1e-11',
                 'MaxInternalSteps':'10100',
                 'Start':'0.0',
                 'UpdateModel':'false',
                 #report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'QuantityType':'concentration',
                 'ReportName':self.timecourse_report_name,
                 'Append': 'false',
                 'ConfirmOverwrite': 'false',
                 'SimulationType':'deterministic',
                 'OutputEvent':'false',
                 'Scheduled':'true',
                 'Save':'overwrite',
                 'OutputML':None,


                 #graph options
                 'Plot':'false'      ,
                 'LineWidth':2,
                 'LineColor':'k',
                 'MarkerColor':'r',
                 'LineStyle':'-',
                 'MarkerStyle':'o',
                 'AxisSize':15,
                 'FontSize':22,
                 'XTickRotation':0,
                 'TitleWrapSize':35,
                 'SaveFig':'false',
                 'ExtraTitle':None,
                 'DPI':125,
                 'MarkerSize':2,
                 }



    def tearDown(self):
        pass
        if os.path.isfile(self.copasi_file):
            os.remove(self.copasi_file)

        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)

        for i in glob.glob('*.jpeg'):
            os.remove(i)

        for i in glob.glob('*.txt'):
            os.remove(i)

    def test_report_setup(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        ListOfReports=TC.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        for i in ListOfReports:
            if i.attrib['name']=='Time-Course':
                boolean=True
        self.assertTrue(boolean)

    def test_scheduled(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
             self.assertEqual(i.attrib['scheduled'],TC.kwargs.get('Scheduled'))

    def test_update_model(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
#            print i.attrib,TC.kwargs['UpdateModel']
            self.assertEqual(i.attrib['updateModel'],TC.kwargs.get('UpdateModel'))




    def test_report_append(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['append'],TC.kwargs.get('Append'))

#
    def test_report_name(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        TC.copasiML=TC.set_report()
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['target'],TC.kwargs.get('ReportName'))
#
    def test_confirm_overwrite(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        TC.copasiML=TC.set_report()
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['confirmOverwrite'],TC.kwargs.get('ConfirmOverwrite'))


    def test_relative_tolerance(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Relative Tolerance':
                self.assertEqual(i.attrib['value'],self.options['RelativeTolerance'])#,


    def test_integrate_reduced_model(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Integrate Reduced Model':
                self.assertEqual(i.attrib['value'],str(0))

    def test_absolute_tolerance(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Absolute Tolerance':
                self.assertEqual(i.attrib['value'],self.options['AbsoluteTolerance'])

    def test_max_internal_steps(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='MaxInternalSteps':
                self.assertEqual(i.attrib['value'],self.options['MaxInternalSteps'])

    def test_step_number(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='StepNumber':
                self.assertEqual(i.attrib['value'],self.options['StepNumber'])
#
    def test_step_size(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='StepSize':
                self.assertEqual(i.attrib['value'],self.options['StepSize'])

    def test_duration(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Duration':
                self.assertEqual(i.attrib['value'],self.options['Duration'])

    def test_time_series_requested(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='TimeSeriesRequested':
                self.assertEqual(i.attrib['value'],'1')

    def test_output_start_time(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='OutputStartTime':
                self.assertEqual(i.attrib['value'],self.options['OutputStartTime'])

    def test_continue_on_simultaneous(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Continue on Simultaneous':
                self.assertEqual(i.attrib['value'],str(0))

    def test_output_event(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Output Event':
                self.assertEqual(i.attrib['value'],self.options['OutputEvent'])

    def test_data_production(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        data_file=os.path.join(os.getcwd(),TC.kwargs.get('ReportName'))
        self.assertTrue(os.path.isfile(data_file))

    def test_data_not_empty(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        data_file=os.path.join(os.getcwd(),TC.kwargs.get('ReportName'))
        data= pandas.read_csv(data_file,sep='\t')
        self.assertIsNot(data.shape,(0,0))
#        

            
if __name__=='__main__':
    unittest.main()