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
site.addsitedir('/home/b3053674/Documents/pycotools')
site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
from pycotools import tasks, viz, misc, model
from pycotools.retrying import retry
from pycotools.Tests import test_models
import unittest
import glob
import os
import shutil
import pandas
from pycotools.Tests import _test_base
import time




class ChaserParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(ChaserParameterEstimationTests, self).setUp()

        self.TC1 = tasks.TimeCourse(self.model, end=1000, step_size=100,
                                              intervals=10, report_name='report1.txt')

        misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        ## add some noise
        data1 = misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        self.MPE = tasks.MultiParameterEstimation(
            self.model,
            self.TC1.report_name,
            copy_number=4,
            pe_number=8,
            method='genetic_algorithm',
            population_size=10,
            number_of_generations=10,
            overwrite_config_file=True,
            results_directory='test_mpe')

        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

        self.MPE.write_config_file()
        self.MPE.setup()
        self.MPE.run()
        time.sleep(5)


    # def test_from_pe_data_str(self):
    #     """
    #     instantiate with argument to model and pe_data.
    #
    #     pe_data is string
    #     :return:
    #     """
    #     bool = True
    #     try:
    #         C = tasks.ChaserParameterEstimations(model=self.model, pe_data=self.MPE.results_directory)
    #     except:
    #         bool = False
    #
    #     self.assertTrue(bool)
    #
    # def test_from_pe_data_pandas_df(self):
    #     """
    #     instantiate with argument to model and pe_data.
    #
    #     pe_data is pandas dataframe
    #     :return:
    #     """
    #     self.model.save()
    #     data = viz.Parse(self.MPE.results_directory, copasi_file=self.model.copasi_file).data
    #
    #     bool = True
    #     try:
    #         C = tasks.ChaserParameterEstimations(model=self.model, pe_data=data)
    #     except:
    #         bool = False
    #
    #     self.assertTrue(bool)
    #
    # def test_from_mpe(self):
    #     bool = True
    #     try:
    #         C = tasks.ChaserParameterEstimations(self.MPE)
    #     except:
    #         bool = False
    #
    #     self.assertTrue(bool)

    def test(self):
        CPE = tasks.ChaserParameterEstimations(self.MPE, truncate_mode='ranks',
                                               theta=range(3), run_mode=True,
                                               tolerance=1e-1, iteration_limit=5)
        CPE.setup()

        CPE.run()















if __name__ == '__main__':
    unittest.main()























































