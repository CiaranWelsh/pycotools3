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


raise NotImplementedError('This is currently not implemented but will eventually take '
                          'a statistical linear modelling approach to analysing '
                          'putative linear relationships between parameters '
                          'in a parameter estimation problem. ')



class TestLinearModel(unittest.TestCase):
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
        tasks

        ## format the time course data
        df = utils.format_timecourse_data(self.TC.report_name)

        ## write data to file
        df.to_csv(self.TC.report_name, sep='\t', index=False)

        self.MPE = tasks.MultiParameterEstimation(self.mod, self.TC.report_name,
                                                 method='genetic_algorithm',
                                                 population_size=25,
                                                 number_of_generations=50,
                                                 run_mode=True)
        self.MPE.write_config_file()
        self.MPE.setup()
        self.MPE.run()

    def tearDown(self):
        import shutil
        # shutil.rmtree(self.working_directory)

    def test(self):
        print viz.Parse(self.MPE)