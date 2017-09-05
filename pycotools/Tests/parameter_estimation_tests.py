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

import site
site.addsitedir('/home/b3053674/Documents/pycotools')
# site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
import pycotools
from pycotools.Tests import test_models
import unittest
import glob
import os
import shutil 
import pandas
from pycotools.Tests import _test_base


##TODO Test that local_parameters, metabolites and global quantity argument work


def parse_timecourse(self):
    """
    read time course data into pandas dataframe. Remove
    copasi generated square brackets around the variables
    :return: pandas.DataFrame
    """

    df = pandas.read_csv(self.cls_instance.report_name, sep='\t')
    headers = [re.findall('(Time)|\[(.*)\]', i)[0] for i in list(df.columns)]
    time = headers[0][0]
    headers = [i[1] for i in headers]
    headers[0] = time
    df.columns = headers
    return df


class ParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationTests, self).setUp()

        self.TC1 = pycotools.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        ## add some noise
        data1 = pycotools.misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        pycotools.misc.correct_copasi_timecourse_headers(self.TC1.report_name)



        self.PE = pycotools.tasks.ParameterEstimation(self.model,
                                                       self.TC1.report_name,
                                                       method='genetic_algorithm',
                                                       population_size=10,
                                                       number_of_generations=10,
                                                       report_name='PE_report_name.csv')
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

    def test_report_name(self):
        self.assertTrue(self.PE.report_name == os.path.join(os.path.dirname(self.model.copasi_file), self.PE.report_name))

    def test_config_file(self):
        """
        A test that PE writes the config file to the
        right place
        :return:
        """
        self.PE.write_config_file()
        self.assertTrue(os.path.isfile(self.PE.config_filename))



    def test_insert_fit_items(self):
        '''
        Tests that there are the same number of rows in the template file
        as there are fit items inserted into copasi
        '''
        self.PE.write_config_file()
        self.PE.model = self.PE.remove_all_fit_items()
        self.model = self.PE.insert_all_fit_items()
        self.model.save()
        new_xml = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml
        list_of_tasks = new_xml.find(self.list_of_tasks)
        ## [5][1][3] indexes the parameter estimation item list
        optimization_item_list = list_of_tasks[5][1][3]
        self.assertEqual(len(optimization_item_list), 9)


    def test_set_PE_method(self):
        '''
        test to see if method has been properly inserted into the copasi file
        '''
        self.PE.write_config_file()
        self.PE.setup()

        tasks=self.PE.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name']=='Parameter Estimation':
                self.assertEqual(i[-1].attrib['type'].lower(),self.PE.method.lower().replace('_',''))

    def test_run(self):
        self.PE.write_config_file()
        self.model = self.PE.setup()
        self.PE.run()
        self.assertTrue(os.path.isfile(self.PE.report_name))


    def test_viz_param_est_parser(self):
        """
        test that viz.Parser correctly formats the
        parameter estimation data
        :return:
        """
        self.PE.write_config_file()
        self.model = self.PE.setup()
        self.PE.run()
        p = pycotools.viz.Parse(self.PE)
        order = ['ThisIsAssignment','B2C','A2B',
                 '(ADeg).k1','(B2C).k2','(C2A).k1',
                 'B','A','C', 'RSS']
        df = p.parse_parameter_estmation()
        self.assertListEqual(order, list(df.columns))

    def test_viz_param_est_parser_len(self):
        """
        outputs only one row for parameter estimation
        results
        :return:
        """
        self.PE.write_config_file()
        self.model = self.PE.setup()
        self.PE.run()
        p = pycotools.viz.Parse(self.PE)
        df = p.parse_parameter_estmation()
        self.assertEqual(df.shape[0], 1)

if __name__=='__main__':
    unittest.main()