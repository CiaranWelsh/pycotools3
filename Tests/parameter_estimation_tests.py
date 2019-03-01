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
from pycotools3.tasks import ParameterEstimation
from pycotools3.utils import DotDict
import glob
import time
from io import StringIO


# todo test model_value for start values are being resolved (there not)

def parse_timecourse(self):
    """
    read time course data into pandas dataframe. Remove
    copasi generated square brackets around the variables
    :return: pandas.DataFrame
    """
    time.sleep(0.1)
    df = pandas.read_csv(self.cls_instance.report_name, sep='\t')
    headers = [re.findall('(Time)|\[(.*)\]', i)[0] for i in list(df.columns)]
    time = headers[0][0]
    headers = [i[1] for i in headers]
    headers[0] = time
    df.columns = headers
    return df


class DotDictTests(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        from pycotools3.utils import DotDict
        dct = {'d': 4}
        dct = DotDict(dct)
        self.assertEqual(dct.d, 4)

    def test2(self):
        from pycotools3.utils import DotDict
        dct = {
            'd': {
                'c': 94
            }
        }
        dct = DotDict(dct, recursive=True)
        self.assertEqual(dct.d.c, 94)

    def test3(self):
        from pycotools3.utils import DotDict
        dct = {
            'd': {
                'c': {
                    'b': 7
                }
            }
        }
        dct = DotDict(dct, recursive=True)
        self.assertEqual(dct.d.c.b, 7)

    def test4(self):
        from pycotools3.utils import DotDict
        dct = {
            'd': {
                'c': {
                    'b': 7
                }
            }
        }
        dct = DotDict(dct, recursive=True)

        # self.assertEqual(dct.d.c.b, 7)


class ParameterEstimationTestsConfig(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationTestsConfig, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        self.TC2 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report2.txt')

        self.TC3 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report3.txt')

        self.TC4 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report4.txt')

        self.TC5 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report5.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)
        data2 = pycotools3.misc.add_noise(self.TC2.report_name)
        data3 = pycotools3.misc.add_noise(self.TC3.report_name)
        data4 = pycotools3.misc.add_noise(self.TC4.report_name)
        data5 = pycotools3.misc.add_noise(self.TC5.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)
        os.remove(self.TC2.report_name)
        os.remove(self.TC3.report_name)
        os.remove(self.TC4.report_name)
        os.remove(self.TC5.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')
        data2.to_csv(self.TC2.report_name, sep='\t')
        data3.to_csv(self.TC3.report_name, sep='\t')
        data4.to_csv(self.TC4.report_name, sep='\t')
        data5.to_csv(self.TC5.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC3.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC4.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC5.report_name)
        self.config = ParameterEstimation.Config(
            models={
                'model1': {
                    'copasi_file': self.model.copasi_file,
                },
            },
            datasets={
                'experiments': {
                    'report1': {
                        'filename': self.TC1.report_name,
                        'affected_models': 'all',
                        'mappings': {
                            'Time': {
                                'model_object': 'Time',
                                'role': 'time'
                            },
                            'A': {
                                'model_object': 'A',
                                'role': 'dependent',
                            },
                        }
                    },
                    'report2': {
                        'filename': self.TC2.report_name,
                        'separator': '\t'
                    }
                },
                'validations': {
                    'report3': {
                        'filename': self.TC3.report_name,
                        'affected_models': 'model1',

                    }
                }
            },
            items={
                'fit_items': {

                    'A': {
                        'lower_bound': 15,
                        'upper_bound': 35,
                        'affected_experiments': 'report1',
                        'affected_validation_experiments': 'report3',
                        'affected_models': 'all',
                        'start_value': 17.5
                    },
                    'B': {},
                    'C': {}
                },
                'constraint_items': {
                    'C': {
                        'upper_bound': 26,
                        'lower_bound': 16
                    }
                },
            },
            settings={
                'method': 'genetic_algorithm_sr',
                'population_size': 38,
                'number_of_generations': 100,
                'copy_number': 1,
                'pe_number': 1,
                'weight_method': 'value_scaling',
                'validation_weight': 4,
                'validation_threshold': 8.5,
                'working_directory': os.path.dirname(__file__),
                'run_mode': False

            }
        )
        self.PE = ParameterEstimation(self.config)

    def test_experiment_kw1(self):
        self.assertEqual(
            os.path.join(os.path.dirname(__file__), self.TC1.report_name),
            os.path.join(os.path.dirname(__file__), self.PE.config.datasets.experiments.report1.filename)
        )

    def test_experiment_kw2(self):
        self.assertEqual(self.PE.config.datasets.experiments.report1.separator, '\t')

    def test_experiment_kw3(self):
        self.assertEqual(self.PE.config.datasets.experiments.report2.separator, '\t')

    def test_experiment_kw4(self):
        self.assertEqual(self.PE.config.settings.weight_method, 'value_scaling')

    def test_validation_kw1(self):
        self.assertEqual(
            os.path.join(os.path.dirname(__file__), self.PE.config.datasets.validations.report3.filename),
            os.path.join(os.path.dirname(__file__), self.TC3.report_name)
        )

    def test_validation_kw2(self):
        self.assertEqual(self.PE.config.settings.validation_weight, 4)

    def test_validation_threshold(self):
        self.assertEqual(self.config.settings.validation_threshold, self.PE.config.settings.validation_threshold)

    def test_validation_weight(self):
        self.assertEqual(self.config.settings.validation_weight, self.PE.config.settings.validation_weight)

    def test_validation_mapppings1(self):
        # self.PE.config
        self.assertEqual(self.PE.config.datasets.validations.report3.mappings.C.object_type, 'Metabolite')

    def test_mappings1(self):
        self.assertEqual(self.PE.config.datasets.experiments.report1.mappings.A.model_object, 'A')

    def test_mappings3(self):
        self.assertEqual(
            self.PE.config.datasets.experiments.report2.
                mappings.B.model_object, 'B')

    def test_weight_method_updates(self):
        pass

    def test_fit_items1(self):
        self.assertEqual(self.PE.config.items.fit_items.A.lower_bound, 15)

    def test_fit_items2(self):
        self.assertEqual(self.PE.config.items.fit_items.A.affected_experiments[0], 'report1')

    def test_fit_items3(self):
        self.assertEqual(self.PE.config.items.fit_items.B.lower_bound, 1e-6)

    def test_constraint_items1(self):
        self.assertEqual(
            self.PE.config.items.constraint_items.C.lower_bound, 16
        )

    def test_settings1(self):
        self.assertEqual(self.PE.config.settings.method, 'genetic_algorithm_sr')

    def test_settings2(self):
        self.assertEqual(self.PE.config.settings.population_size, 38)

    def test_settings3(self):
        self.assertTrue(isinstance(self.PE.config.settings.run_mode, bool))

    def test_iteration(self):
        """
        tests that it is possible to iterate over a Conffig obj
        :return:
        """
        ## will error if cannot iter
        l = []
        for i in self.PE.config:
            l.append(i)
        expected = [
            'models',
            'datasets',
            'items',
            'settings',
        ]
        self.assertListEqual(sorted(expected), sorted(l))

    def test_affected_experiments_keyword_all_resolves1(self):
        """
        Ensure that the keyword 'all' is resolved for affected_experiments
        :return:
        """
        self.assertEqual(self.config.items.fit_items.A.affected_experiments[0], 'report1')

    def test_affected_experiments_keyword_all_resolves3(self):
        """
        Ensure that the keyword 'all' is resolved for affected_experiments
        :return:
        """
        self.assertEqual(self.config.items.fit_items.C.affected_validation_experiments[0],
                         'report3'
                         )

    def test_affected_experiments_keyword_all_resolves4(self):
        """
        Ensure that the keyword 'all' is resolved for affected_experiments
        :return:
        """
        self.assertListEqual(self.config.items.fit_items.C.affected_models,
                             ['model1']
                             )

    def test_affected_models_keyword_resolves_in_experiments(self):
        self.assertEqual(
            self.config.experiments.report1.affected_models,
            'model1'
        )

    def test_write_config_file(self):
        fname = os.path.join(os.path.dirname(__file__), 'config_file.yml')
        self.PE.config.to_yaml(fname)
        self.assertTrue(os.path.isfile(fname))

    def test_create_config_without_prefix_then_add_prefix(self):
        self.config.settings.prefix = 'B'
        self.config.configure()
        actual = list(self.config.items.fit_items.keys())
        expected = ['B']
        self.assertListEqual(expected, actual)

    def test_set(self):
        self.PE.config.set('method', 'simulated_annaeling')
        self.assertEqual('simulated_annaeling',
                         self.PE.config.settings.method)

    def test_set_all(self):
        self.PE.config.set('affected_models', 'fake_affected_model', recursive=True)
        self.assertEqual('fake_affected_model',
                         self.PE.config.datasets.experiments.report1.affected_models)

    def test_set_all_separators(self):
        self.PE.config.set('separator', ',', recursive=True)
        self.assertTrue(',', self.PE.config.experiments.report1.separator)


class ParameterEstimationConfigResolveSpecialArgsTests(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationConfigResolveSpecialArgsTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        self.config_dct = dict(
            models={
                'model1': {
                    'copasi_file': self.model.copasi_file,
                },
            },
            datasets={
                'experiments': {
                    'report1': {
                        'filename': self.TC1.report_name,
                    },
                },
            },

            settings=dict(
                working_directory=os.path.dirname(__file__)
            )
        )

    def test_number_of_fit_items_a(self):
        self.config_dct['items'] = dict(fit_items='a')
        PE = ParameterEstimation(ParameterEstimation.Config(**self.config_dct))

        expected = 10
        actual = len(PE.config.fit_items)
        self.assertEqual(expected, actual)

    def test_affected_models_a(self):
        self.config_dct['items'] = dict(fit_items='a')
        PE = ParameterEstimation(ParameterEstimation.Config(**self.config_dct))
        expected = ['model1']
        actual = PE.config.fit_items.A2B.affected_models
        self.assertEqual(expected, actual)

    def test_number_of_fit_items_g(self):
        self.config_dct['items'] = dict(fit_items='g')
        PE = ParameterEstimation(ParameterEstimation.Config(**self.config_dct))

        expected = 5
        actual = len(PE.config.fit_items)
        self.assertEqual(expected, actual)

    def test_affected_models_g(self):
        self.config_dct['items'] = dict(fit_items='g')
        PE = ParameterEstimation(ParameterEstimation.Config(**self.config_dct))
        expected = ['model1']
        actual = PE.config.fit_items.A2B.affected_models
        self.assertEqual(expected, actual)


class ExperimentMapperTests(_test_base._BaseTest):

    def setUp(self):
        super(ExperimentMapperTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report1.txt')
        self.TC2 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report2.txt')

        pycotools3.utils.format_timecourse_data(self.TC1.report_name)
        pycotools3.utils.format_timecourse_data(self.TC2.report_name)

        df = pandas.read_csv(self.TC2.report_name, sep='\t')
        ## remove square brackets around species
        df = df.rename(columns={list(df.keys())[2]: list(df.keys())[2] + str('_indep')})
        self.report3 = os.path.join(os.path.dirname(self.TC2.report_name), 'report3.txt')
        df.to_csv(self.report3, sep='\t', index=False)
        assert os.path.isfile(self.report3)

        ## create some SS data for fitting
        ss_df = df.drop('Time', axis=1)
        ss_df = pandas.DataFrame(ss_df.iloc[0].transpose(), index=list(ss_df.keys())).transpose()
        self.report4 = os.path.join(os.path.dirname(self.TC2.report_name), 'report4.txt')

        ss_df.to_csv(self.report4, sep='\t', index=False)

        self.conf_dct = dict(
            models=dict(
                model1=dict(
                    copasi_file=self.model.copasi_file,
                    results_directory=os.path.join(self.model.root, 'ParameterEstimationResults'))
            ),
            datasets=dict(
                experiments=dict(
                    report1=dict(
                        filename=self.TC1.report_name,
                    ),
                    report2=dict(
                        filename=self.TC2.report_name
                    ),
                    ss=dict(
                        filename=self.report4
                    )
                ),
                validations=dict(
                    report3=dict(
                        filename=self.report3
                    ),
                )
            ),
            items=dict(
                fit_items=dict(
                    A=dict(
                        affected_experiments=['report1', 'ss']
                    ),
                    B=dict(
                        affected_validation_experiments=['report3']
                    ),
                    C={},
                    A2B={},
                    B2C={},
                    B2C_0_k2={},
                    C2A_k1={},
                    ADeg_k1={},
                )
            ),
            settings=dict(
                method='genetic_algorithm_sr',
                population_size=10,
                number_of_generations=10,
                working_directory=os.path.dirname(__file__),
                weight_method='value_scaling',
                validation_weight=2.5,
                validation_threshold=9,
            )
        )
        self.conf = ParameterEstimation.Config(**self.conf_dct)
        self.PE = pycotools3.tasks.ParameterEstimation(self.conf)

        # print(self.TC1.report_name)

    def test_metabolite_entries(self):
        """
        test that A and B are estimated but not C
        :return:
        """
        bool = False
        for i in self.model.fit_item_order:
            if 'C' == i:
                bool = True
        self.assertFalse(bool)

    def test_global_quantity_entries(self):
        """
        :return:
        """
        bool = False
        for i in self.model.fit_item_order:
            if 'ADeg_k1' == i:
                bool = True
        self.assertFalse(bool)

    def test(self):
        self.PE._map_experiments()

    def test_correct_number_of_experiments(self):
        """
        Test that four  _experiments have been set up
        :return:
        """

        mod = self.PE.models['model1'].model
        count = 0
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                count += 1
        mod.open()
        self.assertEqual(count, 3)

    def test_correct_number_of_validation_experiments(self):
        """
        Test that four  _experiments have been set up
        :return:
        """

        mod = self.PE.models['model1'].model
        count = 0
        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report3':
                    count += 1

        self.assertEqual(count, 1)

    def test_validation_weight(self):
        """
        Test that 2 _experiments have been set up
        :return:
        """

        mod = self.PE.models['model1'].model

        ans = None

        query = '//*[@name="Validation Set"]'

        for j in mod.xml.xpath(query):
            for k in list(j):
                if k.attrib['name'] == 'Weight':
                    ans = k.attrib['value']
        self.assertEqual(ans, str(self.PE.config.settings.validation_weight))

    def test_validation_threshold(self):
        """
        Test that 2 _experiments have been set up
        :return:
        """

        mod = self.PE.models['model1'].model

        ans = None
        query = '//*[@name="Validation Set"]'

        for j in mod.xml.xpath(query):
            for k in list(j):
                if k.attrib['name'] == 'Threshold':
                    ans = k.attrib['value']
        self.assertEqual(ans, str(self.PE.config.settings.validation_threshold))

    def test_validation(self):
        """
        Test that 2 validation _experiments have been set up
        :return:
        """

        mod = self.PE.models['model1'].model

        count = 0
        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] not in ['Weight', 'Threshold']:
                    count += 1
        self.assertEqual(1, count)

    def experiment_checker_function(self, expected_value, attribute):

        mod = self.PE.config.models.model1.model
        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report1':
                    for k in j:
                        if k.attrib['name'] == attribute:
                            ans = k.attrib['value']
        self.assertEqual(expected_value, ans)

    def test_experiment_first_row(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('1', 'First Row')

    def test_experiment_weighting_method(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('3', 'Weight Method')

    def test_experiment_file_name(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function(
            os.path.join(
                os.path.dirname(__file__), 'report1.txt'), 'File Name')

    def test_experiment_number_of_columns(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('10', 'Number of Columns')

    def test_experiment_correct_reference1(self):
        """
        First row of experiment_0==1
        :return:
        """

        mod = self.PE.config.models.model1.model

        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report2':
                    for k in j:
                        if k.attrib['name'] == 'Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    ans = l[0].attrib['value']
        self.assertEqual(
            'CN=Root,Model=TestModel1,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration',
            ans
        )

    def test_experiment_correct_reference2(self):
        """
        First row of experiment_0==1
        :return:
        """

        mod = self.PE.config.models.model1.model
        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report1':
                    for k in j:
                        if k.attrib['name'] == 'Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    ans = l[0].attrib['value']
        self.assertEqual(
            'CN=Root,Model=TestModel1,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration',
            ans,
        )

    def test_validation_map1(self):
        """
        First row of experiment_0==1
        :return:
        """

        mod = self.PE.config.models.model1.model

        ans = None
        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report3':
                    for k in j:
                        if k.attrib['name'] == 'Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    ans = l[0].attrib['value']
        self.assertEqual(
            ans,
            'CN=Root,Model=TestModel1,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration'
        )

    def test_experiment_steady_state(self):
        """
        First row of experiment_0==1
        :return:
        """

        mod = self.PE.config.models.model1.model
        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'ss':
                    for k in j:
                        if k.attrib['name'] == 'Experiment Type':
                            ## code for steady state is '0'
                            ans = k.attrib['value']
        self.assertEqual(str(0), ans)

    def test_experiment_time_course(self):
        """
        First row of experiment_0==1
        :return:
        """

        mod = self.PE.config.models.model1.model

        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report1':
                    for k in j:
                        if k.attrib['name'] == 'Experiment Type':
                            ## code for steady state is '0'
                            ans = k.attrib['value']
        self.assertEqual(ans, str(1))

    def test_experiment_correct_number_of_object_maps(self):
        """
        First row of experiment_0==1
        :return:
        """

        mod = self.PE.config.models.model1.model

        count = 0
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'Object Map':
                        count += 1
        self.assertEqual(3, count)

    def test_experiment_correct_number_of_validation_obj_maps(self):
        """
        First row of experiment_0==1
        :return:
        """

        mod = self.PE.config.models.model1.model

        count = 0

        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'Object Map':
                        count += 1
        self.assertEqual(1, count)

    def test_get_experiment_keys(self):
        dct = self.PE._get_experiment_keys()
        self.assertEqual(dct['model1']['report1'], 'Experiment_report1')

    def test_get_validation_keys(self):
        dct = self.PE._get_validation_keys()
        self.assertEqual(dct['model1']['report3'], 'Experiment_report3')

    def test_create_correct_number_of_experiments(self):
        models = self.PE._map_experiments(validation=False)
        mod = models.model1.model
        query = '//*[@name="Experiment Set"]'
        count = 0
        for i in mod.xml.xpath(query):
            for j in i:
                print(j, j.attrib)
                count += 1
        mod.open()
        self.assertEqual(3, count)

    def test_fit_items_property(self):
        lst = ['A', 'B', 'C', 'A2B', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ADeg_k1']
        self.assertListEqual(sorted(lst), sorted(list(self.PE.config.items.fit_items.keys())))

    def test_create_correct_number_of_validation_experiments(self):
        models = self.PE._map_experiments(validation=True)
        mod = models.model1.model
        query = '//*[@name="Experiment Set"]'
        count = 0
        for i in mod.xml.xpath(query):
            for j in i:
                count += 1
        self.assertEqual(3, count)

    def test_remove_fit_item(self):
        self.PE

    def test_correct_number_of_fit_items(self):

        query = '//*[@name="FitItem"]'
        count = 0
        for i in self.PE.models.model1.model.xml.xpath(query):
            if i.attrib['name'] == 'FitItem':
                count += 1
        self.assertEqual(count, 8)

    def test_set_PE_method(self):

        mod = self.PE.models.model1.model

        query = '//*[@name="Parameter Estimation"]'
        ans = None
        for i in mod.xml.xpath(query):
            if i.tag == '{http://www.copasi.org/static/schema}Task':
                for j in i:
                    if j.tag == 'Method':
                        ans = j.attrib['name']
        self.assertEqual('Genetic Algorithm SR', ans)


class ParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        self.TC2 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report2.txt')

        self.TC3 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report3.txt')

        self.TC4 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report4.txt')

        self.TC5 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report5.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)
        data2 = pycotools3.misc.add_noise(self.TC2.report_name)
        data3 = pycotools3.misc.add_noise(self.TC3.report_name)
        data4 = pycotools3.misc.add_noise(self.TC4.report_name)
        data5 = pycotools3.misc.add_noise(self.TC5.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)
        os.remove(self.TC2.report_name)
        os.remove(self.TC3.report_name)
        os.remove(self.TC4.report_name)
        os.remove(self.TC5.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')
        data2.to_csv(self.TC2.report_name, sep='\t')
        data3.to_csv(self.TC3.report_name, sep='\t')
        data4.to_csv(self.TC4.report_name, sep='\t')
        data5.to_csv(self.TC5.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC3.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC4.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC5.report_name)

        self.conf_dct = dict(
            models=dict(
                model1=dict(
                    copasi_file=self.model.copasi_file
                )
            ),
            datasets=dict(
                experiments=dict(
                    report1=dict(
                        filename=self.TC1.report_name,
                    ),
                    report4=dict(
                        filename=self.TC4.report_name
                    ),
                    report5=dict(
                        filename=self.TC5.report_name
                    )
                ),
                validations=dict(
                    report2=dict(
                        filename=self.TC2.report_name
                    ),
                    report3=dict(
                        filename=self.TC3.report_name
                    )
                )
            ),
            items=dict(
                fit_items=dict(
                    A=dict(
                        affected_experiments=['report1', 'report4']
                    ),
                    B=dict(
                        affected_validation_experiments=['report2']
                    ),
                    C={},
                    A2B={},
                    B2C={},
                    B2C_0_k2={},
                    C2A_k1={},
                    ADeg_k1={},

                ),
                constraint_items=dict(
                    B2C=dict(
                        lower_bound=1e-1,
                        upper_bound=100
                    )
                )

            ),
            settings=dict(
                method='genetic_algorithm_sr',
                population_size=2,
                number_of_generations=2,
                working_directory=os.path.dirname(__file__),
                copy_number=4,
                pe_number=2,
                weight_method='value_scaling',
                validation_weight=2.5,
                validation_threshold=9,
                randomize_start_values=True,
                calculate_statistics=False,
                create_parameter_sets=False
            )
        )
        self.conf = ParameterEstimation.Config(**self.conf_dct)

        self.PE = pycotools3.tasks.ParameterEstimation(self.conf)

        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

    def test_load_model(self):
        self.assertIsInstance(self.PE.config.models.model1.model, pycotools3.model.Model)

    def test_output_directory_id(self):
        results_directory = os.path.join(os.path.dirname(__file__), 'Problem1/Fit1/model1/ParameterEstimationData')
        self.assertEqual(self.PE.results_directory['model1'], results_directory)

    def test_get_model_obj_from_strings(self):
        self.assertEqual(len(self.PE.get_model_objects_from_strings()), 9)

    def test_metabolites(self):
        metabs = ['A', 'B', 'C']
        self.assertListEqual(sorted(metabs), sorted(self.PE.metabolites))

    def test_global_quantities(self):
        glo = ['A2B', 'ADeg_k1', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ThisIsAssignment']
        self.assertListEqual(sorted(glo), sorted(self.PE.global_quantities))

    def test_local_parameter(self):
        loc = []
        self.assertListEqual(sorted(loc), sorted(self.PE.local_parameters))

    def test_report_arguments(self):
        dct = {
            'metabolites': ['A', 'B', 'C'],
            'global_quantities': sorted(['C2A_k1', 'A2B', 'ADeg_k1', 'ThisIsAssignment', 'B2C', 'B2C_0_k2']),
            'local_parameters': [],
            'quantity_type': 'concentration',
            'report_name': 'PEData.txt', 'append': False, 'confirm_overwrite': False,
            'report_type': 'multi_parameter_estimation'}
        report = self.PE._report_arguments
        for i in report:
            if isinstance(report[i], list):
                report[i] = sorted(report[i])

        self.assertEqual(report, dct)

    def test_define_report(self):
        models = self.PE._define_report()
        model = models['model1'].model
        for i in model.xml.xpath('//*[@name="Parameter Estimation"]'):
            if i.tag == '{http://www.copasi.org/static/schema}Task':
                for j in i:
                    if j.tag == '{http://www.copasi.org/static/schema}Report':
                        report = j.attrib['target']
        self.assertEqual(self.PE.config.settings.report_name, 'PEData.txt')

    def test_get_report_key(self):

        keys = self.PE._get_report_key()
        expected = {'model1': 'Report_32'}
        self.assertEqual(expected, keys)

    def test_get_experiment_keys1(self):

        experiment_keys = self.PE._get_experiment_keys()
        self.assertEqual(experiment_keys['model1']['report1'], 'Experiment_report1')

    def test_get_validation_keys1(self):
        experiment_keys = self.PE._get_validation_keys()
        self.assertEqual(experiment_keys['model1']['report2'], 'Experiment_report2')

    def test_get_experiment_keys2(self):
        experiment_keys = self.PE._get_experiment_keys()['model1']
        self.assertEqual(3, len(experiment_keys))

    # def test_write_config_file(self):
    #     """
    #     A test that PE writes the config file to the
    #     right place
    #     :return:
    #     """
    #     self.PE.write_config_file()
    #     self.assertTrue(os.path.isfile(self.PE.config_filename))

    def test_number_of_affected_experiments_is_correct(self):
        # self.PE.write_config_file()

        count = 0
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="Affected Experiments"]'):
            for j in i:
                count += 1

        ## only 1 of 3 experiment datasets has affected_experiments
        self.assertEqual(26, count)

    def test_number_of_affected_validation_experiments_is_correct(self):
        # self.PE.write_config_file()

        count = 0
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="Affected Cross Validation Experiments"]'):
            for j in i:
                count += 1

        ## only 1 of 3 experiment datasets has affected_experiments
        self.assertEqual(17, count)

    def test_affected_experiments_for_global_quantity_A2B(self):
        # self.PE.write_config_file()

        # self.PE.models.model1.model.open()
        count = 0
        experiment_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib['value'] == 'CN=Root,Model=TestModel1,Vector=Values[A2B],Reference=InitialValue':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Experiments':
                        for k in j:
                            experiment_keys.append(k.attrib['value'])

        self.assertListEqual(sorted(['Experiment_report1', 'Experiment_report4', 'Experiment_report5']),
                             sorted(experiment_keys))

    def test_affected_validation_experiments_for_global_quantity_A2B(self):
        # self.PE.write_config_file()

        # self.PE.models.model1.model.open()
        count = 0
        valiadtion_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib['value'] == 'CN=Root,Model=TestModel1,Vector=Values[A2B],Reference=InitialValue':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Cross Validation Experiments':
                        for k in j:
                            valiadtion_keys.append(k.attrib['value'])

        self.assertListEqual(sorted(['Experiment_report2', 'Experiment_report3']),
                             sorted(valiadtion_keys))

    def test_insert_fit_items(self):
        '''
        Tests that there are the same number of rows in the template file
        as there are fit items inserted into copasi
        '''

        mod = self.PE.models.model1.model
        list_of_tasks = mod.xml.find(self.list_of_tasks)
        ## [5][1][3] indexes the parameter estimation item list
        optimization_item_list = list_of_tasks[5][1][3]
        self.assertEqual(8, len(optimization_item_list))

    def test_constraint_items(self):
        mod = self.PE.models.model1.model
        list_of_tasks = mod.xml.find(self.list_of_tasks)
        ## [5][1][3] indexes the parameter estimation item list
        constraint_item_list = list_of_tasks[5][1][4]
        self.assertEqual(1, len(constraint_item_list))

    def test_set_PE_method(self):
        '''
        test to see if method has been properly inserted into the copasi file
        '''

        mod = self.PE.models.model1.model
        tasks = mod.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name'] == 'Parameter Estimation':
                self.assertEqual(i[-1].attrib['type'].lower(), self.PE.config.settings.method.lower().replace('_', ''))

    def test_that_error_on_line3539_is_raised(self):
        pass

    def test_copy_models(self):
        files = glob.glob(os.path.join(
            self.PE.models_dir['model1'], '*.cps'))
        self.assertEqual(self.PE.config.settings.copy_number, len(files))

    def test_setup_scan_pe_number(self):
        mod = self.PE.copied_models['model1'][3]
        query = '//*[@name="Scan"]'
        expected = 2
        actual = 0
        for i in mod.xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'ScanItems':
                        for l in k:
                            for m in l:
                                if m.attrib['name'] == 'Number of steps':
                                    actual = m.attrib['value']
        self.assertEqual(str(expected), str(actual))

    def test_setup_scan_type(self):
        """
        repeat task has type code '0'
        :return:
        """
        mod = self.PE.copied_models['model1'][3]
        query = '//*[@name="Scan"]'
        expected = str(0)
        actual = 0
        for i in mod.xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'ScanItems':
                        for l in k:
                            for m in l:
                                if m.attrib['name'] == 'Type':
                                    actual = m.attrib['value']
        self.assertEqual(expected, actual)

    def test_setup_scan_report_name(self):
        mod = self.PE.copied_models['model1'][3]
        expected_report_name = os.path.join(
            self.PE.results_directory['model1'], 'PEData3.txt')
        actual = ''
        query = '//*[@name="Scan"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.tag == 'Report':
                    actual = j.attrib['target']
        self.assertEqual(expected_report_name, actual)

    def test_run_mode_is_false(self):
        """
        false by default
        :return:
        """
        expected = 0
        results_dir = self.PE.results_directory['model1']
        files = glob.glob(os.path.join(
            results_dir, '*.txt')
        )
        self.assertEqual(expected, len(files))

    def test_run_mode_is_true(self):
        """
        false by default
        :return:
        """
        self.PE.config.settings.run_mode = True
        self.PE.run(self.PE.copied_models)

        expected = 4
        results_dir = self.PE.results_directory['model1']
        files = glob.glob(os.path.join(
            results_dir, '*.txt')
        )
        self.assertEqual(expected, len(files))

    def test_parse_pe_data(self):
        self.PE.config.settings.run_mode = True
        self.PE.run(self.PE.copied_models)

        data = pycotools3.viz.Parse(self.PE).data
        expected = 8
        self.assertEqual(expected, data['model1'].shape[0])

    def test_randomize_start_values(self):
        # self.PE.config.models.model1.model.open()
        query = '//*[@name="Randomize Start Values"]'
        expected = '1'
        actual = None
        for i in self.PE.config.models.model1.model.xml.xpath(query):
            if i.getparent().getparent().attrib['name'] == 'Parameter Estimation':
                actual = i.attrib['value']

        self.assertEqual(expected, actual)

    def test_calculate_statistics(self):
        query = '//*[@name="Calculate Statistics"]'
        expected = '0'
        actual = None
        for i in self.PE.config.models.model1.model.xml.xpath(query):
            if i.getparent().getparent().attrib['name'] == 'Parameter Estimation':
                actual = i.attrib['value']

        self.assertEqual(expected, actual)

    def test_create_parameter_sets(self):
        query = '//*[@name="Create Parameter Sets"]'
        expected = '0'
        actual = None
        for i in self.PE.config.models.model1.model.xml.xpath(query):
            if i.getparent().getparent().attrib['name'] == 'Parameter Estimation':
                actual = i.attrib['value']

        self.assertEqual(expected, actual)


class ParameterEstimationContextTests(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationContextTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report1.txt')
        self.TC2 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report2.txt')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)

        df = pandas.read_csv(self.TC2.report_name, sep='\t')
        ## remove square brackets around species
        df = df.rename(columns={list(df.keys())[2]: list(df.keys())[2] + str('_indep')})
        self.report3 = os.path.join(os.path.dirname(self.TC2.report_name), 'report3.txt')
        df.to_csv(self.report3, sep='\t', index=False)
        assert os.path.isfile(self.report3)

        ## create some SS data for fitting
        ss_df = df.drop('Time', axis=1)
        ss_df = pandas.DataFrame(ss_df.iloc[0].transpose(), index=list(ss_df.keys())).transpose()
        self.report4 = os.path.join(os.path.dirname(self.TC2.report_name), 'report4.txt')

        ss_df.to_csv(self.report4, sep='\t', index=False)

    def test_create_config(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4], context='s', parameters='a') as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 10
        self.assertTrue(isinstance(config, ParameterEstimation.Config))

    def test_create_config_file(self):
        fname = os.path.join(os.path.dirname(__file__), 'config_file.yaml')
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a', filename=fname) as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 10
        self.assertTrue(os.path.isfile(fname))

    def test_create_config_file_when_already_exists(self):
        fname = os.path.join(os.path.dirname(__file__), 'config_file.yaml')
        ##create fake file
        with open(fname, 'w') as f:
            f.write('fake file\n')

        assert os.path.isfile(fname)

        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a', filename=fname) as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 10

        self.assertTrue(os.path.isfile(fname))

    def test_create_config_file_with_prefix(self):
        ## means set_Default_fit_items_str isn't working properly
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 10
            config.settings.prefix = 'B'
        expected = sorted(['B', 'B2C', 'B2C_0_k2'])
        actual = sorted(list(config.items.fit_items.keys()))
        self.assertListEqual(expected, actual)

    def test_settings_get_updated(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 14
            config.settings.prefix = 'B'
        expected = 'genetic_algorithm_sr'
        actual = config.settings.method
        self.assertEqual(expected, actual)

    def test_settings_get_updated2(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 14
            config.settings.prefix = 'B'
        expected = 14
        actual = config.settings.population_size
        self.assertEqual(expected, actual)

    def test_get_config(self):
        context = ParameterEstimation.Context(
            self.model.copasi_file,
            [self.TC1.report_name, self.TC2.report_name,
             self.report3, self.report4],
            context='s', parameters='a')
        config = context.get_config()
        # print(config.toDict())
        self.assertTrue(isinstance(config, ParameterEstimation.Config))

    def test_context_set(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 14
            config.settings.prefix = 'B'
            config.set('separator', ',', recursive=True)
            pe = ParameterEstimation(config)

        query = '//*[@name="Separator"]'
        actual = []
        for i in pe.config.models.test_model.model.xml.xpath(query):
            actual.append(i.attrib['value'])

        expected = [',', ',', ',', ',']
        self.assertListEqual(expected, actual)



    # should i pull default args into a superclass of context and
    # config so they can booth inherit from and modify defaults

    def test_context_mappings_after_use_of_set(self):
        fname = os.path.join(os.path.dirname(__file__), 'timeseries.txt')
        data = self.model.simulate(0, 10, 11)
        data.to_csv(fname)

        with ParameterEstimation.Context(
                self.model.copasi_file, fname,
                context='s', parameters='a') as context:
            context.set('separator', ',')
            config = context.get_config()

        # print(config)

        # pe = ParameterEstimation(config)
        # pe.models.test_model.model.open()

        ## obj map is not being correctly configured. why?
        ## its because the config is not being set up correctly
        # print(pe.models.test_model.model.open())

        # query = '//*[@name="Separator"]'
        # actual = []
        # for i in pe.config.models.test_model.model.xml.xpath(query):
        #     actual.append(i.attrib['value'])
        #
        # expected = [',', ',', ',', ',']
        # self.assertListEqual(expected, actual)

    def test_default_mappings(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            config = context.get_config()
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.number_of_generations = 25
            config.settings.population_size = 14
        pe = ParameterEstimation(config)
        query = '//*[@name="Object Map"]'
        expected = 4
        actual = 0
        for i in pe.models.test_model.model.xml.xpath(query):
            actual += 1
        self.assertEqual(expected, actual)

    def test_default_mapping_when_using_set(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            config = context.get_config()
            config.set('method', 'genetic_algorithm_sr')
            config.set('number_of_generations', 25)
            config.set('population_size', 14)
        pe = ParameterEstimation(config)
        query = '//*[@name="Object Map"]'
        expected = 4
        actual = 0
        for i in pe.models.test_model.model.xml.xpath(query):
            actual += 1
        self.assertEqual(expected, actual)



class ParameterEstimationTestsWithDifferentModel(unittest.TestCase):
    def setUp(self):
        self.antimony_string = """
        model negative_feedback
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

        self.experimental_data = StringIO(
            """
            Time,A,B
             0, 0.000000, 0.000000
             1, 0.099932, 0.013181
             2, 0.199023, 0.046643
             3, 0.295526, 0.093275
             4, 0.387233, 0.147810
             5, 0.471935, 0.206160
             6, 0.547789, 0.265083
             7, 0.613554, 0.322023
             8, 0.668702, 0.375056
             9, 0.713393, 0.422852
            10, 0.748359, 0.464639
            """.strip()
        )

        self.df = pandas.read_csv(self.experimental_data, index_col=0)

        self.fname = os.path.join(os.path.dirname(__file__), 'experimental_data.csv')
        self.df.to_csv(self.fname)

        self.working_directory = os.path.abspath('')

        self.copasi_file = os.path.join(self.working_directory, 'negative_feedback.cps')

        with pycotools3.model.BuildAntimony(self.copasi_file) as loader:
            mod = loader.load(self.antimony_string)

        self.config_dct = dict(
            models=dict(
                model_name=dict(
                    copasi_file=self.copasi_file
                )
            ),
            datasets=dict(
                experiments=dict(
                    first_dataset=dict(
                        filename=self.fname,
                        separator=','
                    )
                )
            ),
            items=dict(
                fit_items=dict(
                    A={},
                    B={},
                )
            ),
            settings=dict(
                working_directory=self.working_directory
            )
        )

    def test_use_config_twice(self):
        """
        :return:
        """
        conf = ParameterEstimation.Config(**self.config_dct)
        ParameterEstimation(conf)
        conf.settings.run_mode = True
        PE = ParameterEstimation(conf)
        self.assertTrue(PE.config.settings.run_mode)

    def test_run(self):
        """

        I should go and figure out why run mode is
        being coerced into string from boolean
        :return:
        """
        conf = ParameterEstimation.Config(**self.config_dct)
        conf.settings.run_mode = True
        PE = ParameterEstimation(conf)
        fname = glob.glob(os.path.join(
            PE.results_directory['model_name'],
            '*.txt'
        ))[0]

        time.sleep(1)
        self.assertTrue(os.path.isfile(fname))


class ParameterEstimationTestsMoreThanOneModel(unittest.TestCase):
    def setUp(self):
        ant1 = """
        
        model first()
            compartment Cell = 1;
            
            R1: A => B ; Cell * k1 * A;
            R2: B => C ; Cell * k2 * B;
            R3: C => A ; Cell * k3 * C;
            
            k1 = 0.1;
            k2 = 0.1;
            k3 = 0.1;
            
            A = 100;
            B = 0;
            C = 0;
        end
        """

        ant2 = """
        
        model second()
            compartment Cell = 1;
            
            R1: A => B ; Cell * k1 * A;
            R2: B => C ; Cell * k2 * B;
            R3: B => A ; Cell * k3 * B;
            
            k1 = 0.1;
            k2 = 0.1;
            k3 = 0.1;
            
            A = 100;
            B = 0;
            C = 0;
        end
        """
        self.fname1 = os.path.join(os.path.dirname(__file__), 'first.cps')
        self.fname2 = os.path.join(os.path.dirname(__file__), 'second.cps')

        with pycotools3.model.BuildAntimony(self.fname1) as loader:
            self.mod1 = loader.load(ant1)

        with pycotools3.model.BuildAntimony(self.fname2) as loader:
            self.mod2 = loader.load(ant2)

        self.experiment = os.path.join(os.path.dirname(__file__), 'dataset.txt')

        self.mod1.simulate(0, 9, 1, report_name=self.experiment)
        time.sleep(0.2)

    def get_population_size(self, xml):
        query = '//*[@name="Population Size"]'
        value = False
        for i in xml.xpath(query):
            value = i.attrib['value']
        return value

    def test_two_models_first(self):
        with ParameterEstimation.Context(
                models=[self.mod1.copasi_file, self.mod2.copasi_file],
                experiments=self.experiment, context='s', parameters='g') as context:
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.population_size = 49
        PE = ParameterEstimation(config)

        time.sleep(0.2)
        actual = self.get_population_size(PE.config.models.first.model.xml)
        # PE.config.models.second.model.open()
        self.assertEqual(str(49), actual)

    def test_two_models_second(self):
        with ParameterEstimation.Context(
                models=[self.mod1.copasi_file, self.mod2.copasi_file],
                experiments=self.experiment, context='s', parameters='g') as context:
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.population_size = 84
        PE = ParameterEstimation(config)
        time.sleep(0.2)
        actual = self.get_population_size(PE.config.models.second.model.xml)
        self.assertEqual(str(84), actual)

    def test_two_models_experiments(self):
        with ParameterEstimation.Context(
                models=[self.mod1.copasi_file, self.mod2.copasi_file],
                experiments=self.experiment, context='s', parameters='g') as context:
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.population_size = 84
        PE = ParameterEstimation(config)
        query = '//*[@name="dataset"]'
        first = False
        second = False
        for i in PE.models.first.model.xml.xpath(query):
            if i.attrib['name'] == 'dataset':
                first = True
        for i in PE.models.second.model.xml.xpath(query):
            if i.attrib['name'] == 'dataset':
                second = True

        self.assertTrue(first is True and second is True)

    def test_two_models_fit_items(self):
        with ParameterEstimation.Context(
                models=[self.mod1.copasi_file, self.mod2.copasi_file],
                experiments=self.experiment, context='s', parameters='g') as context:
            config.settings.method = 'genetic_algorithm_sr'
            config.settings.population_size = 84
        PE = ParameterEstimation(config)
        query = '//*[@name="FitItem"]'
        import re
        first = []
        second = []
        for i in PE.models.first.model.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'ObjectCN':
                    cn_ref = j.attrib['value']
                    cn_ref = re.findall('.*\[(.*)\].*', cn_ref)
                    assert len(cn_ref) != 0
                    first.append(cn_ref[0])

        for i in PE.models.second.model.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'ObjectCN':
                    cn_ref = j.attrib['value']
                    cn_ref = re.findall('.*\[(.*)\].*', cn_ref)
                    assert len(cn_ref) != 0
                    second.append(cn_ref[0])

        self.assertListEqual(first, second)

    def tearDown(self):
        os.remove(self.experiment)
        os.remove(self.fname1)
        os.remove(self.fname2)


##todo use mocking for running tests.


if __name__ == '__main__':
    unittest.main()
