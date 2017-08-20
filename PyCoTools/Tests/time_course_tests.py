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
    19-08-2017
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
from lxml import etree


class DeterministicTimeCourseTests(_test_base._BaseTest):
    def setUp(self):
        super(DeterministicTimeCourseTests, self).setUp()
        self.TC = PyCoTools.pycopi.TimeCourse(self.model, end=1000,
                                              step_size=100, intervals=10,
                                              max_internal_steps=50000)
        self.timecourse = self.TC.model#self.TC.set_timecourse()
        self.timecourse.save()
        self.new_model = PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        self.list_of_reports = '{http://www.copasi.org/static/schema}ListOfReports'

    def test_report_definition(self):
        for i in self.new_model.find(self.list_of_reports):
            if i.attrib['name'] == 'Time-Course':
                self.assertTrue(i.attrib['name'] == 'Time-Course')

    def test_deterministic_options1(self):
        """

        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                self.assertTrue(i[2].attrib['name'] == 'Deterministic (LSODA)' )

    def test_deterministic_options2(self):
        """

        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in list(i[1]):
                    if j.attrib['name'] == 'Relative Tolerance':
                        self.assertTrue(j.attrib['value'] == str(self.TC.relative_tolerance ))

    def test_deterministic_options3(self):
        """

        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in list(i[1]):
                    if j.attrib['name'] == 'Max Internal Steps':
                        self.assertTrue(j.attrib['value'] == str(self.TC.max_internal_steps))


    def test_deterministic_writes_data(self):
        """
        Check that the data containing data is actually produced
        :return:
        """
        self.assertTrue(os.path.isfile(self.TC.report_name )  )

if __name__=='__main__':
    unittest.main()