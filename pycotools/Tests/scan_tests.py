# -*- coding: utf-8 -*-
'''
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
'''


import site
# site.addsitedir(r'C:\Users\Ciaran\Documents\pycotools')
site.addsitedir(r'/home/b3053674/Documents/pycotools')

import pycotools
# from pycotools.pycotoolsTutorial import test_models
import unittest
import glob
import os
import shutil
import pandas
from pycotools.Tests import _test_base
import re


class ScanTests(_test_base._BaseTest):
    def setUp(self):
        super(ScanTests, self).setUp()
        self.scan = pycotools.tasks.Scan(self.model,
                                          report_type='parameter_estimation',
                                          subtask='time_course',
                                          number_of_steps=17,
                                          )

    def test_report_definition(self):
        """
        Test that report has been properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        reports = new_model.find('{http://www.copasi.org/static/schema}ListOfReports')
        check = False
        for report in reports:
            if report.attrib['name'] == 'parameter_estimation':
                check = True
        self.assertTrue(check)

    def test_scan1(self):
        """
        Test that report has been properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        tasks = new_model.find('{http://www.copasi.org/static/schema}ListOfTasks')
        scan_task = tasks[2]

        # new_model.open()
        for i in scan_task:
            for j in list(i):
                if j.attrib['name'] == 'Subtask':
                    ## get which subtask is defined
                    sub = {k: v for k, v in self.scan.subtask_numbers.items() if v==j.attrib['value']}
                    self.assertEqual(sub.values()[0], self.scan.subtask)

    def test_scan2(self):
        """
        Test scan item properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        tasks = new_model.find('{http://www.copasi.org/static/schema}ListOfTasks')
        scan_task = tasks[2]
        for i in scan_task[1]:
            if i.attrib['name'] == 'ScanItems':
                for j in i:
                    for k in j:
                        if k.attrib['name'] == 'Type':
                            self.assertEqual(self.scan.scan_type, k.attrib['value'])

class RepeatScanTests(_test_base._BaseTest):
    def setUp(self):
        super(RepeatScanTests, self).setUp()
        self.scan = pycotools.tasks.Scan(self.model,
                                          report_type='profilelikelihood',
                                          subtask='time_course',
                                          scan_type='repeat',
                                          number_of_steps=6)

    def test_report_definition(self):
        """
        Test that report has been properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        reports = new_model.find('{http://www.copasi.org/static/schema}ListOfReports')
        check = False
        for report in reports:
            if report.attrib['name'] == 'profilelikelihood':
                check = True
        self.assertTrue(check)

    def test_scan1(self):
        """
        Test that report has been properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        tasks = new_model.find('{http://www.copasi.org/static/schema}ListOfTasks')
        scan_task = tasks[2]

        # new_model.open()
        for i in scan_task:
            for j in list(i):
                if j.attrib['name'] == 'Subtask':
                    ## get which subtask is defined
                    sub = {k: v for k, v in self.scan.subtask_numbers.items() if v == j.attrib['value']}
                    self.assertEqual(sub.values()[0], self.scan.subtask)

    def test_scan_if_repeat(self):
        """
        Test that repeat task is properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        tasks = new_model.find('{http://www.copasi.org/static/schema}ListOfTasks')
        scan_task = tasks[2]
        for i in scan_task[1]:
            if i.attrib['name'] == 'ScanItems':
                for j in i:
                    for k in j:
                        if k.attrib['name'] == 'Type':
                            self.assertEqual(self.scan.scan_type, k.attrib['value'])

class RandomDistributionScanTests(_test_base._BaseTest):
    def setUp(self):
        super(RandomDistributionScanTests, self).setUp()
        self.scan = pycotools.tasks.Scan(self.model,
                                          report_type='time_course',
                                          subtask='lyapunov_exponents',
                                          scan_type='random_sampling',
                                          number_of_steps=6)

    def test_report_definition(self):
        """
        Test that report has been properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        reports = new_model.find('{http://www.copasi.org/static/schema}ListOfReports')
        check = False
        for report in reports:
            if report.attrib['name'] == 'Time-Course':
                check = True
        self.assertTrue(check)

    def test_scan1(self):
        """
        Test that report has been properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        tasks = new_model.find('{http://www.copasi.org/static/schema}ListOfTasks')
        scan_task = tasks[2]

        # new_model.open()
        for i in scan_task:
            for j in list(i):
                if j.attrib['name'] == 'Subtask':
                    ## get which subtask is defined
                    sub = {k: v for k, v in self.scan.subtask_numbers.items() if
                           v == j.attrib['value']}
                    self.assertEqual(sub.values()[0], self.scan.subtask)

    def test_scan_is_random_dist(self):
        """
        Test that repeat task is properly defined
        :return:
        """
        self.model = self.scan.model
        self.model.save()
        new_model = pycotools.tasks.CopasiMLParser(self.copasi_file).xml
        tasks = new_model.find('{http://www.copasi.org/static/schema}ListOfTasks')
        scan_task = tasks[2]
        for i in scan_task[1]:
            if i.attrib['name'] == 'ScanItems':
                for j in i:
                    for k in j:
                        if k.attrib['name'] == 'Type':
                            self.assertEqual(self.scan.scan_type, k.attrib['value'])



        
if __name__=='__main__':
    unittest.main()