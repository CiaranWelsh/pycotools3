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
    19-08-2017
 '''

import pycotools3
import unittest
import os
from Tests import _test_base


class RunTests(_test_base._BaseTest):
    def setUp(self):
        super(RunTests, self).setUp()

    def test_scheduled_time_course(self):
        """
        Turn off all tasks. Then turn on time course.
        :return:
        """
        R = pycotools3.tasks.Run(self.model, task='time_course')
        ## configure time course but set run to False
        TC = pycotools3.tasks.TimeCourse(self.model, end=1000, intervals=1000,
                                         step_size=1, run=False)
        model = R.set_task()
        model.save()
        new_model = pycotools3.tasks.CopasiMLParser(self.copasi_file).copasiML
        # os.system('CopasiUI {}'.format(self.copasi_file))
        for i in new_model.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            if i.attrib['name'] == 'Time-Course':
                self.assertEqual(i.attrib['scheduled'], 'true')

    def test_timecourse_runs(self):
        """
        Test that a time course can be run using the
        Run class
        :return:
        """
        TC = pycotools3.tasks.TimeCourse(self.model, end=1000, intervals=1000,
                                         step_size=1, run=True,
                                         report_name='timecourse.csv')

        self.assertTrue(os.path.isfile(TC.report_name))

    def test_scheduled_parameter_estimation(self):
        """
        Turn off all tasks. Then turn on time course.
        :return:
        """
        R = pycotools3.tasks.Run(self.model, task='time_course')
        ## configure time course but set run to False
        TC = pycotools3.tasks.TimeCourse(self.model, end=1000, intervals=1000,
                                         step_size=1, run=False)
        model = R.set_task()
        model.save()
        new_model = pycotools3.tasks.CopasiMLParser(self.copasi_file).copasiML
        # os.system('CopasiUI {}'.format(self.copasi_file))
        for i in new_model.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            if i.attrib['name'] == 'parameter_estimation':
                self.assertEqual(i.attrib['scheduled'], 'true')

    def test_parameter_estimation_runs(self):
        """

        :return:
        """
        copy_number = 3
        df = self.model.simulate(0, 10, 1)
        fname = os.path.join(os.path.dirname(__file__), 'data.csv')
        df.to_csv(fname)
        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, fname, context='s', parameters='g') as context:
            context.set('separator', ',')
            context.set('run_mode', True)
            context.set('copy_number', copy_number)
            context.set('pe_number', 1)
            context.set('randomize_start_values', True)
            context.set('method', 'nl2sol')
            context.set('lower_bound', 1e-1)
            context.set('upper_bound', 1e1)
            config = context.get_config()

        pe = pycotools3.tasks.ParameterEstimation(config)

        import time
        done = False
        while not done:
            data = pycotools3.viz.Parse(pe).data['test_model']
            if data.shape[0] == copy_number:
                done = True
            time.sleep(5)
        self.assertEqual(data.shape[0], copy_number)

    def test_parameter_estimation_runs_parallel(self):
        """

        :return:
        """
        copy_number = 20
        df = self.model.simulate(0, 10, 1)
        fname = os.path.join(os.path.dirname(__file__),
                             'data.csv')
        df.to_csv(fname)
        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, fname, context='s', parameters='g') as context:
            context.set('separator', ',')
            context.set('run_mode', 'parallel')
            context.set('copy_number', copy_number)
            context.set('pe_number', 1)
            context.set('nproc', 3)
            context.set('randomize_start_values', True)
            context.set('method', 'nl2sol')
            context.set('lower_bound', 1e-1)
            context.set('upper_bound', 1e1)
            config = context.get_config()

        pe = pycotools3.tasks.ParameterEstimation(config)

        import time
        done = False
        while not done:
            data = pycotools3.viz.Parse(pe).data['test_model']
            if data.shape[0] == copy_number:
                done = True
            time.sleep(5)
        self.assertEqual(data.shape[0], copy_number)

    def test_sheduled_parameter_estimation(self):
        """
        Test that the executable box is checked
        :return: outputs warning because task isn't defined. This is okay
        """
        R = pycotools3.tasks.Run(self.model, task='parameter_estimation')
        self.model = R.model
        self.model.save()
        new_xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml
        for i in new_xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            if i.attrib['name'] == 'Parameter Estimation':
                self.assertTrue(i.attrib['scheduled'] == 'true')

    def test_sheduled_scan(self):
        """
        Test that the executable box is checked
        :return:outputs warning because task isn't defined. This is okay
        """
        R = pycotools3.tasks.Run(self.model, task='scan')
        self.model = R.model
        self.model.save()
        new_xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml
        for i in new_xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            if i.attrib['name'] == 'Scan':
                self.assertTrue(i.attrib['scheduled'] == 'true')


if __name__ == '__main__':
    unittest.main()
