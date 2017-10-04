# -*- coding: utf-8 -*-
"""
 This file is part of pycotools.

 pycotools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools.  If not, see <http://www.gnu.org/licenses/>.


Author:
    Ciaran Welsh
Date:
    12/03/2017

 Object:

"""

import pickle
import site

# site.addsitedir('/home/b3053674/Documents/pycotools')
# site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
site.addsitedir('/home/b3053674/Documents/pycotools')

import pycotools
from pycotools.Tests import test_models
import unittest
import glob
import os
import shutil
import pandas
from pycotools.Tests import _test_base
import subprocess


class ReportsTests(_test_base._BaseTest):
    """
    Should be able to accept model from file or an xml parsed
    model
    """

    def setUp(self):
        super(ReportsTests, self).setUp()

    def test_time_course_report_exists(self):
        R = pycotools.tasks.Reports(self.model, quantity_type='concentration')
        self.model = R.timecourse()
        self.model.save(self.copasi_file)
        model_for_test = pycotools.tasks.CopasiMLParser(self.copasi_file).copasiML
        ListOfReports = model_for_test .find('{http://www.copasi.org/static/schema}ListOfReports')
        for report in ListOfReports:
            if report.attrib['name'] == 'Time-Course':
                timecourse_report_element = report
        self.assertTrue(timecourse_report_element.attrib['name'], 'Time-Course')

    def test_time_course_correct_elements(self):
        R = pycotools.tasks.Reports(self.model, quantity_type='concentration')
        self.model = R.timecourse()
        self.model.save(self.copasi_file)
        model_for_test = pycotools.tasks.CopasiMLParser(self.copasi_file).copasiML
        ListOfReports = model_for_test.find('{http://www.copasi.org/static/schema}ListOfReports')
        for report in ListOfReports:
            if report.attrib['name'] == 'Time-Course':
                timecourse_report_element = report
        lst = []
        for i in timecourse_report_element:
            for j in list(i):
                lst.append(j.attrib['cn'])

        ## test the contents of a few of the table entries
        self.assertTrue('Reference=Time' in lst[0])
        self.assertTrue('Vector=Metabolites[B]' in lst[1])
        self.assertTrue('Vector=Values[B2C]' in lst[5])


        '''
        TODO
        I should also runn a time course and test for the data contents
        Will do this after the time course task is ready
        '''
    def test_profile_likelihood_exists(self):
        R = pycotools.tasks.Reports(self.model, quantity_type='concentration')
        self.model = R.profile_likelihood()
        self.model.save(self.copasi_file)
        model_for_test = pycotools.tasks.CopasiMLParser(self.copasi_file).copasiML
        ListOfReports = model_for_test.find('{http://www.copasi.org/static/schema}ListOfReports')
        for report in ListOfReports:
            if report.attrib['name'] == 'profilelikelihood':
                profile_likelihood_report_element = report
        self.assertTrue(profile_likelihood_report_element .attrib['name'], 'profilelikelihood')



    def test_parameter_estimation_exists(self):
        R = pycotools.tasks.Reports(self.model, quantity_type='concentration',
                                     report_type='parameter_estimation')
        self.model = R.model
        self.model.save()
        model_for_test = pycotools.tasks.CopasiMLParser(self.copasi_file).copasiML

        ListOfReports = model_for_test.find('{http://www.copasi.org/static/schema}ListOfReports')
        for report in ListOfReports:
            if report.attrib['name'] == 'parameter_estimation':
                parameter_estimation_report_element = report
        self.assertTrue(parameter_estimation_report_element.attrib['name'], 'parameter_estimation')



    def test_multi_parameter_estimation_exists(self):
        R = pycotools.tasks.Reports(self.model, quantity_type='concentration')
        self.model = R.multi_parameter_estimation()
        self.model.save(self.copasi_file)
        model_for_test = pycotools.tasks.CopasiMLParser(self.copasi_file).copasiML
        ListOfReports = model_for_test.find('{http://www.copasi.org/static/schema}ListOfReports')
        for report in ListOfReports:
            if report.attrib['name'] == 'multi_parameter_estimation':
                multi_parameter_estimation_report_element = report
        self.assertTrue(multi_parameter_estimation_report_element.attrib['name'], 'multi_parameter_estimation')












if __name__=='__main__':
    unittest.main()