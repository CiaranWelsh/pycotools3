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
import site
# site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')

import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil 
import pandas
from PyCoTools.Tests import _test_base



class TimeCourseTests(_test_base._BaseTest):
    def setUp(self):
        super(TimeCourseTests, self).setUp()

    def test_deterministic1(self):
        TC = PyCoTools.pycopi.TimeCourse(self.model, end=1000,
                                         step_size=100,
                                         intervals=10)
        self.model = TC.set_deterministic()
        self.model.save(self.copasi_file, self.model.xml)
        model_for_test = PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in model_for_test.xpath(query):
            for j in list(i):
                self.assertTrue(j.attrib['name'] == 'Deterministic (LSODA)')

    def test_deterministic2(self):
        TC = PyCoTools.pycopi.TimeCourse(self.model, end=1000,
                                         step_size=100,
                                         intervals=10)
        self.model = TC.set_deterministic()
        self.model.save(self.copasi_file, self.model.xml)
        model_for_test = PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in model_for_test.xpath(query):
            for j in list(i):
                self.assertTrue(j.attrib['type'] == 'Deterministic(LSODA)')

    def test_deterministic3(self):
        TC = PyCoTools.pycopi.TimeCourse(self.model, end=1000,
                                         step_size=100,
                                         intervals=10)
        self.model = TC.set_deterministic()
        self.model.save(self.copasi_file, self.model.xml)
        model_for_test = PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in model_for_test.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name'] == 'Duration':
                        self.assertTrue(k.attrib['value'] == str(1000))

    def test_deterministic4(self):
        TC = PyCoTools.pycopi.TimeCourse(self.model, end=1000,
                                         step_size=100,
                                         intervals=10)
        self.model = TC.set_deterministic()
        self.model.save(self.copasi_file, self.model.xml)
        model_for_test = PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in model_for_test.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name'] == 'StepSize':
                        self.assertTrue(k.attrib['value'] == str(TC.step_size))

    def test_deterministic5(self):
        TC = PyCoTools.pycopi.TimeCourse(self.model, end=1000,
                                         step_size=100,
                                         intervals=10)
        self.model = TC.set_deterministic()
        self.model.save(self.copasi_file, self.model.xml)
        model_for_test = PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        for i in model_for_test.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name'] == 'Absolute Tolerance':
                        self.assertTrue(k.attrib['value'] == str(TC.absolute_tolerance))






                                            # os.system('CopasiUI {}'.format(self.copasi_file))
    # def test_report_setup(self):
    #     ListOfReports=self.TC.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
    #     for i in ListOfReports:
    #         if i.attrib['name']=='Time-Course':
    #             boolean=True
    #     self.assertTrue(boolean)


    # def test_scheduled(self):
    #     query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
    #     for i in self.TC.copasiML.xpath(query):
    #          self.assertEqual(i.attrib['scheduled'],self.TC['scheduled'])
    #
    # def test_update_model(self):
    #     query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
    #     for i in self.TC.copasiML.xpath(query):
    #         self.assertEqual(i.attrib['updateModel'],self.TC.kwargs.get('update_model'))
    #
    #
    #
    #
    # def test_report_append(self):
    #     query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
    #     for i in self.TC.copasiML.xpath(query):
    #         self.assertEqual(i[0].attrib['append'],self.TC['append'])
    #
    # def test_report_name(self):
    #     self.TC.copasiML=self.TC.set_report()
    #     query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
    #     for i in self.TC.copasiML.xpath(query):
    #         self.assertEqual(i[0].attrib['target'],self.TC.kwargs.get('report_name'))
    #
    #
    # def test_confirm_overwrite(self):
    #     self.TC.copasiML=self.TC.set_report()
    #     query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
    #     for i in self.TC.copasiML.xpath(query):
    #         self.assertEqual(i[0].attrib['confirmOverwrite'],self.TC.kwargs.get('confirm_overwrite'))
    #
    # def test_relative_tolerance(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='Relative tolerance':
    #             self.assertEqual(i.attrib['value'],self.TC['Relativetolerance'])#,
    #
    #
    # def test_integrate_reduced_model(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='Integrate Reduced model':
    #             self.assertEqual(i.attrib['value'],str(0))
    #
    # def test_absolute_tolerance(self):
    #     self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file)
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='Absolute tolerance':
    #             self.assertEqual(i.attrib['value'],self.TC['Absolutetolerance'])
    #
    # def test_max_internal_steps(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='MaxInternalSteps':
    #             self.assertEqual(i.attrib['value'],self.TC['MaxInternalSteps'])
    #
    # def test_step_number(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='StepNumber':
    #             self.assertEqual(i.attrib['value'],self.TC['StepNumber'])
    #
    # def test_step_size(self):
    #     self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file)
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='StepSize':
    #             self.assertEqual(i.attrib['value'],self.TC['step_size'])
    #
    # def test_duration(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='Duration':
    #             self.assertEqual(i.attrib['value'],self.TC['end'])
    #
    # def test_time_series_requested(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='TimeSeriesRequested':
    #             self.assertEqual(i.attrib['value'],'1')
    #
    # def test_output_start_time(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='OutputStartTime':
    #             self.assertEqual(i.attrib['value'],self.TC['start'])
    # def test_continue_on_simultaneous(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='Continue on Simultaneous':
    #             self.assertEqual(i.attrib['value'],str(0))
    #
    # def test_output_event(self):
    #     test_element= self.TC.copasiML[2][1]
    #     for i in list(test_element):
    #         if i.attrib['name']=='Output Event':
    #             self.assertEqual(i.attrib['value'],self.TC['output_event'])
    #
    # def test_data_production(self):
    #     data_file=os.path.join(os.getcwd(),self.TC.kwargs.get('report_name'))
    #     self.assertTrue(os.path.isfile(data_file))
    #
    # def test_data_not_empty(self):
    #     data_file=os.path.join(os.getcwd(),self.TC.kwargs.get('report_name'))
    #     data= pandas.read_csv(data_file,sep='\t')
    #     self.assertIsNot(data.shape,(0,0))

            
if __name__=='__main__':
    unittest.main()