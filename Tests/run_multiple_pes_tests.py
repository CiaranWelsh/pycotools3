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
import pycotools
from pycotools.retrying import retry
from Tests import test_models
import unittest
import os
import pandas
from Tests import _test_base



class MultiParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(MultiParameterEstimationTests, self).setUp()

        self.TC1 = pycotools.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        pycotools.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        ## add some noise
        data1 = pycotools.misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        self.MPE = pycotools.tasks.MultiParameterEstimation(
            self.model,
            self.TC1.report_name,
            copy_number=4,
            pe_number=8,
            method='genetic_algorithm',
            population_size=20,
            number_of_generations=20,
            overwrite_config_file=True,
            results_directory='test_mpe')
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

        self.MPE.write_config_file()
        self.MPE.setup()

    def test_output_directory(self):
        self.assertTrue(os.path.isdir(self.MPE.results_directory))

    def test_write_config_file(self):
        """
        Test that RMPE produces a config file
        :return:
        """
        self.MPE.write_config_file()
        self.assertTrue(os.path.isfile(self.MPE.config_filename))

    def test_number_of_copasi_files(self):
        """
        make sure we have the correct number of files
        :return:
        """
        num = self.MPE.copy_number
        self.assertEqual(len(self.MPE.models), num)

    def test_scan(self):
        """
        ensure scan item is correctly set up on each of the sub copasi files
        :return:
        """
        first_model = self.MPE.models[0]
        query='//*[@name="ScanItems"]'
        for i in first_model.xml.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name'] == 'Number of steps':
                        self.assertEqual(int(k.attrib['value']), self.MPE.pe_number)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def test_total_number_of_PE(self):
        """
        test that the total number of PEs = copy_number*pe_number
        :return:
        """
        x = self.MPE.copy_number*self.MPE.pe_number
        self.MPE.run()
        df_dct = {}
        for f in os.listdir(self.MPE.results_directory):
            f = os.path.join(self.MPE.results_directory, f)
            df_dct[f] = pandas.read_csv(f, sep='\t', skiprows=1, header=None)
        df = pandas.concat(df_dct)
        self.assertTrue(df.shape[0] == x)

    def test_viz_parser(self):
        """

        :return:
        """
        self.MPE.run()
        P = pycotools.viz.Parse(self.MPE)
        self.assertTrue(isinstance(P.data, pandas.core.frame.DataFrame))

    def test_usage_of_start_value(self):
        """
        Start values can be given to the start_value
        argument.

        :return:
        """
        self.MPE.run()
        p = pycotools.viz.Parse(self.MPE)
        PE = pycotools.tasks.ParameterEstimation(
            self.model, self.TC1.report_name,
            method='genetic_algorithm',
            population_size=20,
            number_of_generations=20,
            start_value=p.data.iloc[0],
            overwrite_config_file=True,
        )
        PE.write_config_file()
        PE.setup()

        ## No time to finish the test but opening
        ## the model shows that parameter have been inserted
        ## into the ParameterEstimation start values option
        # print p
        # PE.model.open()



if __name__=='__main__':
    unittest.main()




