#-*-coding: utf-8 -*-
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
from pycotools import model, tasks, misc, viz
from Tests import _test_base
import unittest
import os
import glob


class ModelSelectionTests(unittest.TestCase):
    def setUp(self):
        ## create model selection directory

        self.dire = os.path.join(os.path.dirname(__file__), 'model_selection')
        if not os.path.isdir(self.dire):
            os.makedirs(self.dire)

        self.copasi_file1 = os.path.join(self.dire, 'negative_feedback.cps')
        self.copasi_file2 = os.path.join(self.dire, 'positive_feedback.cps')
        self.copasi_file3 = os.path.join(self.dire, 'feedforward.cps')

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
                end
                """
            )

        with model.BuildAntimony(self.copasi_file3) as loader:
            self.mod3 = loader.load(
                """
                model model3
                    compartment cell = 1.0
                    var A in cell
                    var B in cell
                    var C in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kBProd = 0.3
                    kBDeg = 0.4
                    kCDeg = 0.5
                    kCProd = 0.6
                    A = 0
                    B = 0
                    C = 0

                    AProd: => A; cell*vAProd
                    ADeg: A =>; cell*kADeg*A
                    BProd: => B; cell*kBProd*A
                    BDeg: B => ; cell*kBDeg*B
                    CProd: => C; cell*kCProd*A*B
                    CDeg: C => ; cell*kCDeg*C
                end
                """
            )

        self.TC = self.simulate_data()

        self.MMF = self.configure_model_selection()

    def tearDown(self):
        pass
        # path_list = [
        #     self.copasi_file1,
        #     self.copasi_file2,
        #     self.copasi_file3,
        #     self.TC.report_name
        # ]
        # [os.remove(i) for i in path_list]

    def simulate_data(self):
        """
        simulate some data from model1
        :return:
        """
        TC = tasks.TimeCourse(self.mod1, end=100, steps=10, intervals=10)
        misc.format_timecourse_data(TC.report_name)
        return TC

    def configure_model_selection(self):
        MMF = tasks.MultiModelFit(self.dire,
                                  method='genetic_algorithm',
                                  population_size=30,
                                  number_of_generations=100,
                                  copy_number=1,
                                  pe_number=3,
                                  run_mode=True,
                                  overwrite_config_file=True,
                                  lower_bound=1e-2,
                                  upper_bound=1e2)
        MMF.write_config_file()
        MMF.setup()
        MMF.run()
        return MMF

    def test_plot_violin(self):
        MS = viz.ModelSelection(self.MMF, savefig=True)
        files = glob.glob(os.path.join(MS.results_directory), '*')
        ## make sure 3 files are written, one for each model selection criteria and one for the csv file
        self.assertEqual(len(files), 4)
































if __name__ == '__main__':
    unittest.main()

