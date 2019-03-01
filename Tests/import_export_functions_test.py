# -*-coding: utf-8 -*-
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


 $Author: Ciaran Welsh

Module that tests the operations of the _Base base test

"""
from pycotools3 import model, tasks, misc, viz, errors
from Tests import _test_base
import unittest
import os
import glob
from shutil import rmtree


class TestSBMLFunctions(unittest.TestCase):
    def setUp(self):
        ## create model selection directory

        self.dire = os.path.join(os.path.dirname(__file__), 'AntimonyModels')
        if not os.path.isdir(self.dire):
            os.makedirs(self.dire)

        self.copasi_file1 = os.path.join(self.dire, 'negative_feedback.cps')

        with model.BuildAntimony(self.copasi_file1) as loader:
            self.mod = loader.load(
                """
                model model1
                    compartment cell = 1.0
                    var A in cell
                    var B in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kBProd = 0.3
                    kBDeg = 0.4
                    vBasalAProd = 0.001
                    A = 0
                    B = 0

                    AProd: => A; cell*vAProd*B+vBasalAProd
                    ADeg: A =>; cell*kADeg*A
                    BProd: => B; cell*kBProd*A
                    BDeg: B => ; cell*kBDeg*B
                end
                """
            )
        if not os.path.isfile(self.copasi_file1):
            raise errors.FileDoesNotExistError('Copasi File "{}" was not created in '
                                               'setting up the test case'.format(self.copasi_file1))

    def tearDown(self):
        """
        tests fail with :
         WindowsError: [Error 32] The process cannot access the file because it is being used by another process: 'D:\\pycotools3\\Tests\\AntimonyModels\\TimeCourseGraphs'
        If you try to delete directory here
        :return:
        """
        # rmtree(self.dire)

    def test_sbml_export(self):
        """

        :return:
        """
        sbml_filename = self.mod.to_sbml()
        self.assertTrue(os.path.isfile(sbml_filename))

    def test_sbml_import(self):
        ## create sbml file for import
        sbml_filename = self.mod.to_sbml()
        assert os.path.isfile(sbml_filename)

        ## remove the existing copasi file
        if os.path.isfile(self.copasi_file1):
            os.remove(self.copasi_file1)

        ## import sbml
        mod = model.ImportSBML(sbml_filename).model
        self.assertTrue(type(mod) == model.Model)

    def test_sbml_import_works(self):
        """
        Test that time course works after import
        :return:
        """
        ## create sbml file for import
        sbml_filename = self.mod.to_sbml()
        assert os.path.isfile(sbml_filename)

        ## remove the existing copasi file
        if os.path.isfile(self.copasi_file1):
            os.remove(self.copasi_file1)

        ## import sbml
        mod = model.ImportSBML(sbml_filename).model
        self.assertIsInstance(mod, model.Model)
        # TC = tasks.TimeCourse(mod, end=100, intervals=100, step_size=1)
        # plotted_time_course = viz.PlotTimeCourse(TC, savefig=True)
        # self.assertEqual(
        #     3,
        #     len(
        #         glob.glob(
        #             os.path.join(plotted_time_course.results_directory, '*')
        #         )
        #     )
        # )

if __name__ == '__main__':
    unittest.main()

