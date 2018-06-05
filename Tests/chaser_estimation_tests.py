# -*- coding: utf-8 -*-
'''
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

'''

import pickle
import site
from pycotools import tasks, viz, misc, model, utils
import unittest
import os



class ChaserParameterEstimationTests(unittest.TestCase):

    def setUp(self):
        ## create model selection directory

        self.dire = os.path.join(os.path.dirname(__file__), 'ChaserEstimationTests')
        if not os.path.isdir(self.dire):
            os.makedirs(self.dire)

        self.copasi_file = os.path.join(self.dire, 'negative_feedback.cps')

        with model.BuildAntimony(self.copasi_file) as loader:
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

        self.TC1 = tasks.TimeCourse(self.mod, end=1000, step_size=100,
                                              intervals=10, report_name='report1.txt')

        utils.format_timecourse_data(self.TC1.report_name)
        ## add some noise
        data1 = misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        self.copy_number = 2
        self.pe_number = 3

        self.MPE = tasks.MultiParameterEstimation(
            self.mod,
            self.TC1.report_name,
            copy_number=self.copy_number,
            pe_number=self.pe_number,
            method='genetic_algorithm',
            population_size=10,
            number_of_generations=10,
            overwrite_config_file=True,
            results_directory='test_mpe',
            run_mode=True
        )

        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

        self.MPE.write_config_file()
        self.MPE.setup()
        self.MPE.run()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dire)

    def test_MPE_worked(self):
        data = viz.Parse(self.MPE).data
        self.assertEqual(data.shape[0], self.copy_number*self.pe_number)

    def test_pe_dict_is_created(self):
        """
        configuration is parallelized. This tests that the
        pe_dict containing cps files and sub parameter estimation
        is correctly created. 
        :return: 
        """
        CPE = tasks.ChaserParameterEstimations(self.MPE, truncate_mode='ranks',
                                               theta=list(range(2)), run_mode=False,
                                               tolerance=1e-1, iteration_limit=5)
        # print viz.Parse(CPE).data
        self.assertTrue(len(list(CPE.pe_dct.items())) == self.copy_number)

    def test_run_true(self):
        CPE = tasks.ChaserParameterEstimations(self.MPE, truncate_mode='ranks',
                                               theta=list(range(2)), run_mode=True,
                                               tolerance=1e-1, iteration_limit=5)
        results = viz.Parse(CPE).data
        self.assertEqual(results.shape[0], 2)

    # def test_run_parallel(self):
    #     CPE = tasks.ChaserParameterEstimations(self.MPE, truncate_mode='ranks',
    #                                            theta=range(2), run_mode='parallel',
    #                                            tolerance=1e-1, iteration_limit=5)
    #     ## sleep long enough for subprocesses to run the estimations
    #     time.sleep(10)
    #     results = viz.Parse(CPE).data
    #     self.assertEqual(results.shape[0], 2)


    def test_parameters(self):
        """
        make sure that new parameter sets are being inserted into the
        model before running the estimation
        :return:
        """

        CPE = tasks.ChaserParameterEstimations(self.MPE, truncate_mode='ranks',
                                               theta=list(range(2)), run_mode=True,
                                               tolerance=1e-1, iteration_limit=5)

        ## get parameters that were estimated in MPE
        pe_data = viz.Parse(self.MPE).data

        ## get keys to ordered dict
        keys = list(CPE.pe_dct.keys())

        ## key 0 should have best parameter set from MPE
        zero = CPE.pe_dct[keys[0]]


        pe_data0 = pe_data.iloc[0]

        model_params = zero.model.parameters

        pe_data.drop('RSS', inplace=True, axis=1)
        
        for i in list(pe_data.keys()):
            self.assertAlmostEqual(float(model_params[i]), float(pe_data0[i]))


















if __name__ == '__main__':
    unittest.main()























































