# -*- coding: utf-8 -*-
"""
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
"""
from pycotools3 import *
import unittest
import os
import pandas

class TestClassVariables(unittest.TestCase):

    def setUp(self):
        self.directory = os.path.join(os.path.dirname(__file__), 'SensitivityTests')
        os.makedirs(self.directory) if not os.path.isdir(self.directory) else None
        self.cps_file = os.path.join(self.directory, 'test_model.cps')

        self.antimony_string = """
            model test_model()
                R1: A => B; kAtoB*A
                R2: B => C; kBtoC*B
                
                kAtoB = 0.1
                kBtoC = 0.1
                A = 1000
                B = 0
                C = 0 
            end
            """

        with model.BuildAntimony(self.cps_file) as loader:
            self.mod = loader.load(antimony_str=self.antimony_string)

        assert isinstance(self.mod, model.Model)

        ##  add reaction using oo interfce to get a local parameter in
        self.mod.add_reaction('R3', 'C -> D', 'k*C')
        self.mod.save()
        self.s = tasks.Sensitivities(self.mod)


    def tearDown(self):
        import shutil
        # shutil.rmtree(self.directory)

    def test_subtasks(self):
        self.assertEqual(len(self.s.subtasks), 6)

    def test_evaluation_cause(self):
        self.assertEqual(len(self.s.evaluation_cause), 9)

    def test_evaluation_effect(self):
        self.assertEqual(len(self.s.evaluation_effect), 6)

    def test_steady_state_cause(self):
        self.assertEqual(len(self.s.steady_state_cause), 5)

    def test_steady_state_effect(self):
        self.assertEqual(len(self.s.steady_state_effect), 11)

    def test_time_series_cause(self):
        self.assertEqual(len(self.s.time_series_cause), 6)

    def test_time_series_effect(self):
        print((self.s.time_series_effect))
        self.assertEqual(len(self.s.time_series_effect), 11)

    def test_parameter_estimation_effect(self):
        self.assertEqual(len(self.s.parameter_estimation_effect), 1)

    def test_parameter_estimation_cause(self):
        self.assertEqual(len(self.s.parameter_estimation_cause), 6)

    def test_optimization_effect(self):
        self.assertEqual(len(self.s.optimization_effect), 1)

    def test_optimisation_cause(self):
        self.assertEqual(len(self.s.optimization_cause), 6)

    def cross_section_cause(self):
        self.assertEqual(len(self.s.cross_section_cause), 1)

    def cross_section_effect(self):
        self.assertEqual(len(self.s.cross_section_effect), 6)



class TestSensitivities(unittest.TestCase):

    def setUp(self):
        self.directory = os.path.join(os.path.dirname(__file__), 'SensitivityTests')
        os.makedirs(self.directory) if not os.path.isdir(self.directory) else None
        self.cps_file = os.path.join(self.directory, 'test_model.cps')
        self.antimony_string = """
            model test_model()
                R1: A => B; kAtoB*A
                R2: B => C; kBtoC*B

                kAtoB = 0.1
                kBtoC = 0.1
                A = 1000
                B = 0
                C = 0 
            end
            """

        with model.BuildAntimony(self.cps_file) as loader:
            self.mod = loader.load(antimony_str=self.antimony_string)

        assert isinstance(self.mod, model.Model)

        ##  add reaction using oo interfce to get a local parameter in
        self.mod.add_reaction('R3', 'C -> D', 'k*C')
        self.mod.save()

        self.report_name = os.path.join(self.directory, 'sensitivity_report.txt')

    def tearDown(self):
        os.remove(self.report_name) if os.path.isfile(self.report_name) else None

    def test_report(self):
        s = tasks.Sensitivities(self.mod)
        query = '//*[@name="sensitivity"]'
        sensitivity_report = s.model.xml.xpath(query)
        assert sensitivity_report != []
        # self.assertEqual(sensitivity_report[0].name, 'sensitivity')

    def test_get_task(self):
        s = tasks.Sensitivities(self.mod)
        self.assertEqual(s.task.attrib['name'], 'Sensitivities')

    def test_set_subtask(self):
        s = tasks.Sensitivities(self.mod, subtask='cross_section',
                                effect='single_object')
        task = s.set_subtask()
        self.assertEqual(task[1][0].attrib['value'], '5')

    def test_create_sensitivity_task_key(self):
        s = tasks.Sensitivities(self.mod)
        self.assertEqual(s.sensitivity_task_key(), 'Task_23')

    def test_run(self):
        s = tasks.Sensitivities(self.mod, report_name=self.report_name,
                                run=True)
        self.assertTrue(os.path.isfile(s.report_name))

    def test_get_report_key(self):
        s = tasks.Sensitivities(self.mod)
        self.assertEqual(s.get_report_key(), 'Report_31')

    def test_process_data(self):
        s = tasks.Sensitivities(self.mod, report_name=self.report_name, run=True)
        self.assertTrue(isinstance(s.sensitivities, pandas.DataFrame))

class TestFIM(unittest.TestCase):

    def setUp(self):
        self.directory = os.path.join(os.path.dirname(__file__), 'SensitivityTests')
        os.makedirs(self.directory) if not os.path.isdir(self.directory) else None
        self.cps_file = os.path.join(self.directory, 'test_model.cps')
        self.antimony_string = """
            model test_model()
                R1: A => B; kAtoB*A
                R2: B => C; kBtoC*B

                kAtoB = 0.1
                kBtoC = 0.1
                A = 1000
                B = 0
                C = 0 
            end
            """

        with model.BuildAntimony(self.cps_file) as loader:
            self.mod = loader.load(antimony_str=self.antimony_string)

        assert isinstance(self.mod, model.Model)

        ##  add reaction using oo interfce to get a local parameter in
        self.mod.add_reaction('R3', 'C -> D', 'k*C')
        self.mod.save()

        self.report_name = os.path.join(self.directory, 'sensitivity_report.txt')

    def test_sensitivities_runs(self):
        s = tasks.FIM(self.mod)
        self.assertTrue(isinstance(s.sensitivities, pandas.DataFrame))

    def test_matrix_multiply(self):
        s = tasks.FIM(self.mod)#
        self.assertTrue(s.fim.shape[0], s.fim.shape[1])


if __name__ == '__main__':
    unittest.main()



