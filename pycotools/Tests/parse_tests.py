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
import site
site.addsitedir('/home/b3053674/Documents/pycotools')
from pycotools import tasks, model, utils, viz
import os, glob
import unittest




class TestParse(unittest.TestCase):
    def setUp(self):
        self.working_directory = os.path.join(os.path.dirname(__file__), 'viz_tests')
        if not os.path.isdir(self.working_directory):
            os.makedirs(self.working_directory)

        copasi_file = os.path.join(self.working_directory, 'test_model.cps')
        with model.BuildAntimony(copasi_file) as loader:
            self.mod = loader.load(
                """
                model negative_feedback
                    compartment cell = 1.0
                    var A in cell
                    var B in cell
                    var Signal in cell
                    var C in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kBProd = 0.3
                    kBDeg = 0.4
                    kCProd = 0.5
                    kCDeg = 0.6
                    A = 0
                    B = 0
                    C = 0
                    Signal = 10

                    AProd: $Signal => A; cell*vAProd*Signal
                    ADeg: A =>; cell*kADeg*A*B;
                    BProd: => B; cell*kBProd*A;
                    BDeg: B => ; cell*kBDeg*B;
                    CProd: => C ; cell*kCProd*B;
                    CDeg: C => ; cell*kCDeg*C
                end
                """
            )

        ## initialize empty dict to store TimeCourse objects
        self.TC = tasks.TimeCourse(
            self.mod, end=10, intervals=10, step_size=1,
            global_quantities=[], y=['A', 'B', 'C']
        )
        self.copy_number = 2
        self.pe_number = 4

        ## format the time course data
        df = utils.format_timecourse_data(self.TC.report_name)

        ## write data to file
        df.to_csv(self.TC.report_name, sep='\t', index=False)


    def tearDown(self):
        import shutil
        shutil.rmtree(self.working_directory)

    # def test_timecourse(self):
    #     data = viz.Parse(self.TC).data
    #     self.assertEqual(data.shape, (11, 5))
    #
    # def test_multi_parameter_estimation(self):
    #     MPE = tasks.MultiParameterEstimation(
    #         self.mod, self.TC.report_name,
    #         method='genetic_algorithm',
    #         population_size=5,
    #         number_of_generations=5,
    #         run_mode=True,
    #         copy_number=self.copy_number,
    #         pe_number=self.pe_number
    #     )
    #     MPE.write_config_file()
    #     MPE.setup()
    #     MPE.run()
    #     data = viz.Parse(MPE).data
    #     self.assertEqual(data.shape[0], self.copy_number*self.pe_number)
    #
    # def test_parameter_estimation(self):
    #     PE = tasks.ParameterEstimation(self.mod, self.TC.report_name,
    #                                    method='genetic_algorithm',
    #                                    population_size=5,
    #                                    number_of_generations=5,
    #                                    run_mode=True)
    #     PE.write_config_file()
    #     PE.setup()
    #     PE.run()
    #
    #     data = viz.Parse(PE).data
    #     self.assertEqual(data.shape[0], 1)
    #
    #
    # def test_from_folder_generated_with_multi_parameter_estimations(self):
    #     MPE = tasks.MultiParameterEstimation(
    #         self.mod, self.TC.report_name,
    #         method='genetic_algorithm',
    #         population_size=5,
    #         number_of_generations=5,
    #         run_mode=True,
    #         copy_number=self.copy_number,
    #         pe_number=self.pe_number
    #     )
    #     MPE.write_config_file()
    #     MPE.setup()
    #     MPE.run()
    #
    #     data = viz.Parse(MPE.results_directory, copasi_file=MPE.model.copasi_file).data
    #     self.assertEqual(data.shape[0], self.copy_number*self.pe_number)
    #
    #
    # def test_from_chaser_estimations(self):
    #     MPE = tasks.MultiParameterEstimation(
    #         self.mod, self.TC.report_name,
    #         method='genetic_algorithm',
    #         population_size=5,
    #         number_of_generations=5,
    #         run_mode=True,
    #         copy_number=self.copy_number,
    #         pe_number=self.pe_number
    #     )
    #     MPE.write_config_file()
    #     MPE.setup()
    #     MPE.run()
    #
    #     CPE = tasks.ChaserParameterEstimations(
    #         MPE, truncate_mode='ranks', theta=range(2),
    #         tolerance=1e-2, iteration_limit=5,
    #         run_mode=True
    #     )
    #
    #     data = viz.Parse(CPE).data
    #     self.assertEqual(data.shape[0], 2)



    def test_from_folder_generated_with_chaser_estimations(self):
        MPE = tasks.MultiParameterEstimation(
            self.mod, self.TC.report_name,
            method='genetic_algorithm',
            population_size=5,
            number_of_generations=5,
            run_mode=True,
            copy_number=self.copy_number,
            pe_number=self.pe_number
        )
        MPE.write_config_file()
        MPE.setup()
        MPE.run()

        CPE = tasks.ChaserParameterEstimations(
            MPE, truncate_mode='ranks', theta=list(range(2)),
            tolerance=1e-2, iteration_limit=5,
            run_mode=True
        )
        data = viz.Parse(CPE.results_directory, copasi_file=CPE.model.copasi_file).data
        print(data)
        self.assertEqual(data.shape[0], 2)















if __name__ == '__main__':
    unittest.main()

