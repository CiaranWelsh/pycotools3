# -*-coding: utf-8 -*-
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


 $Author: Ciaran Welsh

Module that tests the operations of the _Base base test

"""
import site

site.addsitedir('/home/b3053674/Documents/pycotools')
import pandas
from pycotools import model, tasks, misc, viz
from pycotools.Tests import _test_base
import unittest
import os
import pickle
import numpy
import shutil
import glob
import time
from shutil import rmtree

class BuildAntimonyTestsCreateFromNew(unittest.TestCase):
    """
    A test case for building new copasi models with antimony.
    Files are deleted between test and build anew
    """
    def setUp(self):
        ## create model selection directory

        self.dire = os.path.join(os.path.dirname(__file__), 'AntimonyModels')
        if not os.path.isdir(self.dire):
            os.makedirs(self.dire)

        self.copasi_file1 = os.path.join(self.dire, 'negative_feedback.cps')
        self.copasi_file2 = os.path.join(self.dire, 'positive_feedback.cps')
        self.copasi_file3 = os.path.join(self.dire, 'feedforward.cps')

    def test_build(self):
        """
        Make copasi file from antimony
        :return:
        """
        with model.BuildAntimony(self.copasi_file1) as loader:
            self.mod1 = loader.load(
                """
                model model1
                    compartment cell = 1.0
                    var A in cell
                    var B in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kBProd = 0.3
                    kBDeg = 0.4
                    A = 0
                    B = 0

                    AProd: => A; cell*vAProd
                    ADeg: A =>; cell*kADeg*A*B
                    BProd: => B; cell*kBProd*A
                    BDeg: B => ; cell*kBDeg*B
                end
                """
            )
        self.assertTrue(os.path.isfile(self.copasi_file1))

    def test_exception(self):
        """
        Forget the trailing 'end' and ensure it produces an error
        :return:
        """
        exception_message = "Antimony: Error in model string, line 19:  syntax error, unexpected end of file, expecting '-' or '+' or => or '<'"
        try:
            with model.BuildAntimony(self.copasi_file2) as loader:
                self.mod2 = loader.load(
                    """
                    model model2
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
                    """
                )

        except Exception as E:
            self.assertEqual(E.message, exception_message)

    def tearDown(self):
        rmtree(self.dire)
        # path_list = [
        #     self.copasi_file1,
        #     self.copasi_file2,
        #     self.copasi_file3,
        #     self.TC.report_name
        # ]
        # [os.remove(i) for i in path_list]


class BuildAntimonyTestsWithoutRemovalBetweenTests(unittest.TestCase):
    """
    Test the case where a model already exists
    """
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

        assert os.path.isfile(self.copasi_file1)

    def tearDown(self):
        rmtree(self.dire)

    def test_build_model_to_file_path_which_already_exists(self):
        with model.BuildAntimony(self.copasi_file1) as loader:
            mod = loader.load(
                """
                model model1
                    compartment cell = 1.0
                    var A in cell
                    var C in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kCProd = 0.3
                    kCDeg = 0.4
                    vBasalAProd = 0.001
                    A = 0
                    C = 0

                    AProd: => A; cell*vAProd*B+vBasalAProd
                    ADeg: A =>; cell*kADeg*A
                    CProd: => C; cell*kCProd*A
                    CDeg: C => ; cell*kCDeg*C
                end
                """
            )

        self.assertNotIn('B', [i.name for i in mod.metabolites])



if __name__ == '__main__':
    unittest.main()

