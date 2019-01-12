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
import pycotools
import unittest
import os
from Tests import _test_base


class ScanTests(_test_base._BaseTest):
    def setUp(self):
        super(ScanTests, self).setUp()
        self.scan = pycotools.tasks.Scan(self.model,
                                          report_type='parameter_estimation',
                                          subtask='time_course',
                                          number_of_steps=17)

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
                    sub = {k: v for k, v in list(self.scan.subtask_numbers.items()) if v==j.attrib['value']}
                    self.assertEqual(list(sub.values())[0], self.scan.subtask)

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


    def test_clear_all_scans(self):
        """

        :return:
        """
        self.scan = pycotools.tasks.Scan(self.model,
                                          report_type='parameter_estimation',
                                          subtask='time_course',
                                          number_of_steps=18, clear_scans=False)
        self.scan.model = self.scan.remove_scans()
        # print model
        query = '//*[@name="ScanItem"]'
        scans = []
        self.assertListEqual(self.scan.model.xml.xpath(query), [])



class ScanVizTests(_test_base._BaseTest):
    def setUp(self):
        super(ScanVizTests, self).setUp()
        ## setup time course. Don't run
        self.model = pycotools.tasks.TimeCourse(
            self.model, end=1000, step_size=100, intervals=10,
            run=False
        ).model

        ##setup scan for time course
        self.scan = pycotools.tasks.Scan(self.model,
                                         report_type='time_course',
                                         variable='A',
                                         subtask='time_course',
                                         number_of_steps=10,
                                         run_mode=True,
                                         report_name=os.path.join(
                                             os.path.dirname(
                                                 self.model.copasi_file),
                                             'scan_time_course.csv')
                                         )
        '''
        not yet implemented plotting scan features. 
        TODO finish
        '''
    #
    # def test_parser_in_viz(self):
    #     """
    #
    #     :return:
    #     """
    #     if not os.path.isfile(self.scan.report_name):
    #         raise Exception
    #     p = pycotools.viz.Parse(self.scan)
    #
    #     print self.scan.number_of_steps
        # print p.parse_scan()
        # self.model.open()
        # import pandas
        # import numpy
        # names = ['a', 'b', 'c']
        # df = pandas.DataFrame([1,2,3,numpy.nan, 4,5,6,numpy.nan, 7, 8,9])
        # print df



            # def test_parser_in_viz2(self):
            #     """
            #
            #     :return:
            #     """
            #     p = pycotools.viz.Parse(self.TC)
            #     df = p.parse_timecourse()
            #     boolean = True
            #     ## set boolean to false if square brackets still in timecourse
            #     for i in list(df.columns):
            #         if '[' in i:
            #             boolean = False
            #     self.assertTrue(boolean)


class RepeatScanTests(_test_base._BaseTest):
    def setUp(self):
        super(RepeatScanTests, self).setUp()
        self.scan = pycotools.tasks.Scan(self.model,
                                          report_type='profile_likelihood',
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
            if report.attrib['name'] == 'profile_likelihood':
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
                    sub = {k: v for k, v in list(self.scan.subtask_numbers.items()) if v == j.attrib['value']}
                    self.assertEqual(list(sub.values())[0], self.scan.subtask)

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
                    sub = {k: v for k, v in list(self.scan.subtask_numbers.items()) if
                           v == j.attrib['value']}
                    self.assertEqual(list(sub.values())[0], self.scan.subtask)

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