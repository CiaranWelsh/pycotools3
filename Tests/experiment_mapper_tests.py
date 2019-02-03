# -*- coding: utf-8 -*-
'''
 This file is part of pycotools3.

 pycotools3 is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools3 is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools3.  If not, see <http://www.gnu.org/licenses/>.


Author:
    Ciaran Welsh
Date:
    12/03/2017

 Object:
'''


import pycotools3
import unittest
import os
import pandas
from Tests import _test_base

class ExperimentMapperTests(_test_base._BaseTest):
    def setUp(self):
        super(ExperimentMapperTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report1.txt')
        self.TC2 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report2.txt')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)

        df = pandas.read_csv(self.TC2.report_name, sep='\t')
        ## remove square brackets around species
        df = df.rename(columns={list(df.keys())[2]: list(df.keys())[2]+str('_indep')})
        self.report3 = os.path.join(os.path.dirname(self.TC2.report_name), 'report3.txt')
        df.to_csv(self.report3, sep='\t', index=False)
        assert os.path.isfile(self.report3)

        ## create some SS data for fitting
        ss_df = df.drop('Time', axis=1)
        ss_df = pandas.DataFrame(ss_df.iloc[0].transpose(), index=list(ss_df.keys())).transpose()
        self.report4= os.path.join(os.path.dirname(self.TC2.report_name), 'report4.txt')
        ss_df.to_csv(self.report4, sep='\t', index=False)

        self.E = pycotools3.tasks.ExperimentMapper(self.model,
                                                   [self.TC1.report_name,
                                                    self.TC2.report_name,
                                                    self.report3,
                                                    self.report4],
                                                   experiment_type=['timecourse', 'timecourse',
                                                                    'timecourse', 'steadystate'],
                                                   validation=[False, True, True, False],
                                                   validation_weight=2,
                                                   validation_thershold=6
                                                   )
        self.model = self.E.model
        self.model.save()
        self.new_cps = pycotools3.tasks.CopasiMLParser(self.model.copasi_file)
        self.new_xml = self.new_cps.xml
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

    def test_experiment(self):
        """
        Test that four  experiments have been set up
        :return:
        """
        count = 0
        query = '//*[@name="Experiment Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                count += 1
        self.assertEqual(count, 2)

    def test_validation_weight(self):
        """
        Test that 2 experiments have been set up
        :return:
        """

        query = '//*[@name="Validation Set"]'

        for j in self.new_xml.xpath(query):
            for k in list(j):
                if k.attrib['name'] == 'Weight':
                    self.assertEqual(k.attrib['value'], str(self.E.validation_weight))


    def test_validation_threshold(self):
        """
        Test that 2 experiments have been set up
        :return:
        """

        query = '//*[@name="Validation Set"]'

        for j in self.new_xml.xpath(query):
            for k in list(j):
                if k.attrib['name'] == 'Threshold':
                    self.assertEqual(k.attrib['value'], str(self.E.validation_threshold))

    def test_validation(self):
        """
        Test that 2 validation experiments have been set up
        :return:
        """
        count = 0
        query = '//*[@name="Validation Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                ## new validation experiments are under a parameter group tag, under Validation Set
                if j.tag == '{http://www.copasi.org/static/schema}ParameterGroup':
                    count += 1
        self.assertEqual(count, 2)

    def test_experiment2(self):
        """
        First row of experiment_0==1
        :return:
        """

        query = '//*[@name="Experiment Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'Experiment_0':
                    for k in j:
                        if k.attrib['name'] =='First Row':
                            self.assertEqual(k.attrib['value'], '1')

    def test_experiment3(self):
        """
        First row of experiment_0==1
        :return:
        """

        query = '//*[@name="Experiment Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'Experiment_3':
                    for k in j:
                        if k.attrib['name'] =='Weight Method':
                            self.assertEqual(k.attrib['value'], '1')

    def test_experiment4(self):
        """
        First row of experiment_0==1
        :return:
        """

        query = '//*[@name="Experiment Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'Experiment_0':
                    for k in j:
                        if k.attrib['name'] =='Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    self.assertEqual('CN=Root,Model=New_Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration',
                                                     l[0].attrib['value'])

    def test_experiment5(self):
        """
        First row of experiment_0==1
        :return:
        """

        query = '//*[@name="Experiment Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'Experiment_3':
                    for k in j:
                        if k.attrib['name'] =='Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    self.assertEqual('CN=Root,Model=New_Model,Vector=Compartments[nuc],Vector=Metabolites[B],Reference=InitialConcentration',
                                                     l[0].attrib['value'])

    def test_experiment6(self):
        """
        First row of experiment_0==1
        :return:
        """

        query = '//*[@name="Experiment Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'Experiment_3':
                    for k in j:
                        if k.attrib['name'] == 'Experiment Type':
                            ## code for steady state is '0'
                            self.assertEqual(k.attrib['value'], str('0'))

                def test_experiment7(self):
                    """
                    First row of experiment_0==1
                    :return:
                    """
                    query = '//*[@name="Experiment Set"]'
                    for i in self.new_xml.xpath(query):
                        for j in i:
                            if j.attrib['name'] == 'Experiment_0':
                                for k in j:
                                    if k.attrib['name'] == 'Experiment Type':
                                        ## code for steady state is '0'
                                        self.assertEqual(k.attrib['value'], str(1))


    def test_experiment7(self):
        """
        First row of experiment_0==1
        :return:
        """
        count = 0

        query = '//*[@name="Experiment Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'Object Map':
                        count += 1
        self.assertEqual(count, 2)

    def test_experiment8(self):
        """
        First row of experiment_0==1
        :return:
        """
        count = 0

        query = '//*[@name="Validation Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'Object Map':
                        count += 1
        self.assertEqual(count, 2)

    def test_experiment9(self):
        """
        First row of experiment_0==1
        :return:
        """
        count = 0

        query = '//*[@name="Validation Set"]'
        for i in self.new_xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'Object Map':
                        count += 1
        self.assertEqual(count, 2)

if __name__=='__main__':
    unittest.main()