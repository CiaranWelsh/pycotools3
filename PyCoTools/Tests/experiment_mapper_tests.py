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
site.addsitedir(r'C:\Users\Ciaran\Documents\PyCoTools')
# site.addsitedir(r'/home/b3053674/Documents/PyCoTools')

import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil
import pandas
from PyCoTools.Tests import _test_base
import re
from lxml import etree

class ExperimentMapperTests(_test_base._BaseTest):
    def setUp(self):
        super(ExperimentMapperTests, self).setUp()

        self.TC1 = PyCoTools.pycopi.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report1.txt')
        self.TC2 = PyCoTools.pycopi.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report2.txt')

        df = pandas.read_csv(self.TC2.report_name, sep='\t')
        ## remove square brackets around species
        df = df.rename(columns={df.keys()[2]: df.keys()[2]+str('_indep')})
        self.report3 = os.path.join(os.path.dirname(self.TC2.report_name), 'report3.txt')
        df.to_csv(self.report3, sep='\t', index=False)
        assert os.path.isfile(self.report3)

        ## create some SS data for fitting
        ss_df = df.drop('Time', axis=1)
        ss_df = pandas.DataFrame(ss_df.iloc[0].transpose(), index=ss_df.keys()).transpose()
        self.report4= os.path.join(os.path.dirname(self.TC2.report_name), 'report4.txt')
        ss_df.to_csv(self.report4, sep='\t', index=False)

        self.E = PyCoTools.pycopi.ExperimentMapper(self.model,
                                                   [self.TC1.report_name,
                                                    self.TC2.report_name,
                                                    self.report3,
                                                    self.report4],
                                                   experiment_type=['timecourse', 'timecourse',
                                                                    'timecourse', 'steadystate'])
        self.model = self.E.model
        self.model.save()
        self.new_xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        self.model.open()

    def test_experiment(self):
        """
        Test that four  experiments have been set up
        :return:
        """

        list_of_tasks = self.new_xml.find(self.list_of_tasks)
        parameter_estimation = list_of_tasks[5]
        assert parameter_estimation.attrib['name'] == 'Parameter Estimation'
        problem = parameter_estimation[1]
        # print problem[3].attrib
        experiment_set = problem[8]
        assert experiment_set.attrib['name'] == 'Experiment Set'
        count = 0
        for i in experiment_set:
            count += 1
        self.assertEqual(count, 4)


if __name__=='__main__':
    unittest.main()