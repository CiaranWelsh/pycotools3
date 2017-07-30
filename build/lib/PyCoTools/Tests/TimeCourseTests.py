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
import Testmodels
import lxml.etree as etree

MODEL_STRING = Testmodels.Testmodels.get_model1()

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
                 'Relativetolerance':'1e-7',
                 'Absolutetolerance':'1e-11',
                 'MaxInternalSteps':'10100',
                 'Start':'0.0',
                 'update_model':'false',
                 #report variables
                 'metabolites':self.GMQ.get_metabolites().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'quantity_type':'concentration',
                 'report_name':self.timecourse_report_name,
                 'append': 'false',
                 'confirm_overwrite': 'false',
                 'SimulationType':'deterministic',
                 'OutputEvent':'false',
                 'scheduled':'true',
                 'save':'overwrite',
                 'OutputML':None,


                 #graph options
                 'plot':'false'      ,
                 'line_width':2,
                 'Linecolor':'k',
                 'Markercolor':'r',
                 'LineStyle':'-',
                 'MarkerStyle':'o',
                 'axis_size':15,
                 'font_size':22,
                 'xtick_rotation':0,
                 'title_wrap_size':35,
                 'savefig':'false',
                 'extra_title':None,
                 'dpi':125,
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
             self.assertEqual(i.attrib['scheduled'],TC.kwargs.get('scheduled'))

    def test_update_model(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
#            print i.attrib,TC.kwargs['update_model']
            self.assertEqual(i.attrib['updatemodel'],TC.kwargs.get('update_model'))




    def test_report_append(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['append'],TC.kwargs.get('append'))

#
    def test_report_name(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        TC.copasiML=TC.set_report()
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['target'],TC.kwargs.get('report_name'))
#
    def test_confirm_overwrite(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        TC.copasiML=TC.set_report()
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in TC.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['confirmOverwrite'],TC.kwargs.get('confirm_overwrite'))


    def test_relative_tolerance(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Relative tolerance':
                self.assertEqual(i.attrib['value'],self.options['Relativetolerance'])#,


    def test_integrate_reduced_model(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Integrate Reduced model':
                self.assertEqual(i.attrib['value'],str(0))

    def test_absolute_tolerance(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        test_element= TC.copasiML[2][1]
        for i in list(test_element):
            if i.attrib['name']=='Absolute tolerance':
                self.assertEqual(i.attrib['value'],self.options['Absolutetolerance'])

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
        data_file=os.path.join(os.getcwd(),TC.kwargs.get('report_name'))
        self.assertTrue(os.path.isfile(data_file))

    def test_data_not_empty(self):
        TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,**self.options)
        data_file=os.path.join(os.getcwd(),TC.kwargs.get('report_name'))
        data= pandas.read_csv(data_file,sep='\t')
        self.assertIsNot(data.shape,(0,0))
#        

            
if __name__=='__main__':
    unittest.main()