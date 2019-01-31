# -*- coding: utf-8 -*-

'''
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
 
'''
import pycotools3
import unittest
import os
import pandas
import re
from Tests import _test_base


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

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)

        self.PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                       self.TC1.report_name,
                                                       method='genetic_algorithm',
                                                       population_size=10,
                                                       number_of_generations=10,
                                                       report_name='PE_report_name')
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

    def test_report_name(self):
        print(self.PE.report_name)
        self.assertTrue(self.PE.report_name == 'PE_report_name')

    def test_config_file(self):
        """
        A test that PE writes the config file to the
        right place
        :return:
        """
        # self.PE.item_template
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
        new_xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml
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

        tasks = self.PE.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name'] == 'Parameter Estimation':
                self.assertEqual(i[-1].attrib['type'].lower(), self.PE.method.lower().replace('_', ''))

    def test_run(self):
        self.PE.write_config_file()
        self.model = self.PE.setup()
        self.PE.run()
        f = os.path.join(self.PE.results_directory, self.PE.report_name) + '_0.txt'
        self.assertTrue(os.path.isfile(f))

    def test_viz_param_est_parser(self):
        """
        test that viz.Parser correctly formats the
        parameter estimation data
        :return:
        """
        self.PE.write_config_file()
        self.model = self.PE.setup()
        self.PE.run()
        p = pycotools3.viz.Parse(self.PE)
        order = ['A', 'B', 'C', 'A2B', 'ADeg_k1', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ThisIsAssignment', 'RSS']
        df = p.from_multi_parameter_estimation(self.PE)
        self.assertListEqual(sorted(order), sorted(list(df.columns)))

    def test_viz_param_est_parser_len(self):
        """
        outputs only one row for parameter estimation
        results
        :return:
        """
        self.PE.write_config_file()
        self.model = self.PE.setup()
        self.PE.run()
        import time
        time.sleep(2)
        p = pycotools3.viz.Parse(self.PE)
        df = p.from_multi_parameter_estimation(self.PE)
        self.assertEqual(df.shape[0], 1)

    #
    def test_(self):
        if os.path.isfile(self.PE.config_filename):
            os.remove(self.PE.config_filename)
        self.PE.write_config_file()
        self.model = self.PE.setup()
        # self.model.open()


class ParameterEstimationConfigFileTests(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationConfigFileTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)

    def test_config_file_locals2(self):
        """

        :return:
        """
        PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                  self.TC1.report_name,
                                                  method='genetic_algorithm',
                                                  population_size=10,
                                                  number_of_generations=10,
                                                  report_name='PE_report_name.csv')
        item_template = PE.item_template
        boolean = False
        locs = ['(ADeg).k1', '(B2C).k2', '(C2A).k1']
        for i in locs:
            if i not in list(item_template.index):
                print(('{} not in template'.format(i)))
                boolean = True
        # self.assertFalse(boolean)

    def test_config_file_metabs1(self):
        """

        :return:
        """
        PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                  self.TC1.report_name,
                                                  method='genetic_algorithm',
                                                  population_size=10,
                                                  number_of_generations=10,
                                                  report_name='PE_report_name.csv')
        item_template = PE.item_template
        boolean = False
        locs = ['A', 'B', 'C']
        for i in locs:
            if i not in list(item_template.index):
                print(('{} not in template'.format(i)))
                boolean = True
        self.assertFalse(boolean)

    def test_config_file_metabs2(self):
        """

        :return:
        """
        PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                  self.TC1.report_name,
                                                  method='genetic_algorithm',
                                                  population_size=10,
                                                  number_of_generations=10,
                                                  report_name='PE_report_name.csv',
                                                  metabolites=[])
        item_template = PE.item_template
        boolean = False
        metabs = []
        for i in metabs:
            if i not in list(item_template.index):
                print(('{} not in template'.format(i)))
                boolean = True
        self.assertFalse(boolean)

    def test_config_file_metabs3(self):
        """

        :return:
        """
        PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                  self.TC1.report_name,
                                                  method='genetic_algorithm',
                                                  population_size=10,
                                                  number_of_generations=10,
                                                  report_name='PE_report_name.csv',
                                                  metabolites=['A'])
        item_template = PE.item_template
        boolean = False
        metabs = ['A']
        for i in metabs:
            if i not in list(item_template.index):
                print(('{} not in template'.format(i)))
                boolean = True
        self.assertFalse(boolean)

    def test_config_file_globs1(self):
        """

        :return:
        """
        PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                  self.TC1.report_name,
                                                  method='genetic_algorithm',
                                                  population_size=10,
                                                  number_of_generations=10,
                                                  report_name='PE_report_name.csv',
                                                  global_quantities=['A2B'])
        item_template = PE.item_template
        boolean = False
        globs = ['A2B']
        for i in globs:
            if i not in list(item_template.index):
                print(('{} not in template'.format(i)))
                boolean = True
        self.assertFalse(boolean)

    def test_config_file_globs2(self):
        """

        :return:
        """
        PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                  self.TC1.report_name,
                                                  method='genetic_algorithm',
                                                  population_size=10,
                                                  number_of_generations=10,
                                                  report_name='PE_report_name.csv',
                                                  )
        item_template = PE.item_template
        boolean = False
        globs = ['ThisIsAssignment', 'B2C', 'A2B']
        for i in globs:
            if i not in list(item_template.index):
                print(('{} not in template'.format(i)))
                boolean = True
        self.assertFalse(boolean)


class TwoParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(TwoParameterEstimationTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        self.model.set('metabolite', 'A', 150, match_field='name', change_field='concentration')

        self.TC2 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report2.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)
        data2 = pycotools3.misc.add_noise(self.TC2.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)
        os.remove(self.TC2.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')
        data2.to_csv(self.TC2.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)

    def test_setup_has_two_data_files(self):
        PE = pycotools3.tasks.ParameterEstimation(
            self.model, [self.TC1.report_name, self.TC2.report_name], method='genetic_algorithm',
            population_size=5, number_of_generations=20,
            metabolites=[], local_parameters=[], lower_bound=0.1,
            upper_bound=100)
        if os.path.isfile(PE.config_filename):
            os.remove(PE.config_filename)

        PE.write_config_file()
        PE.setup()

        query = '//*[@name="File Name"]'
        count = 0
        for i in PE.model.xml.xpath(query):
            count += 1
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()
