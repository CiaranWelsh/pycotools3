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


## todo make sure viz works with new parameter estimation
## todo modify other class arguments if necessary to be like the parameter estimation class
## todo clean up repository of old and unused code, objects files etc
## todo remove Models folder
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
                'run_mode': False,
                'lower_bound': 0.05,
                'upper_bound': 36
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
        self.assertEqual(self.PE.config.datasets.validations.report3.mappings.C.object_type, 'Metabolite')

    def test_mappings1(self):
        self.assertEqual(self.PE.config.datasets.experiments.report1.mappings.A.model_object, 'A')

    def test_mappings3(self):
        self.assertEqual(
            self.PE.config.datasets.experiments.report2.
                mappings.B.model_object, 'B')

    def test_fit_items_A_lower_bound(self):
        expected = 15
        actual = self.PE.config.items.fit_items.A.lower_bound
        self.assertEqual(expected, actual)

    def test_fit_items_A_upper_bound(self):
        ## now I've broken the use of lower and upper bounds in
        ## individual fit items
        expected = 35
        actual = self.PE.config.items.fit_items.A.upper_bound
        self.assertEqual(expected, actual)

    def test_fit_items2(self):
        self.assertEqual(self.PE.config.items.fit_items.A.affected_experiments[0], 'report1')

    def test_fit_items3(self):
        expected = 0.05
        actual = self.PE.config.items.fit_items.B.lower_bound
        self.assertEqual(expected, actual)

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
        expected = ['model1']
        actual = self.config.experiments.report1.affected_models
        self.assertListEqual(expected, actual)

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

    def test_models_affected_experiments_property(self):
        expected = ['report1', 'report2']
        actual = self.config.models_affected_experiments['model1']
        self.assertListEqual(expected, actual)

    def test_models_affected_validation_experiments_property(self):
        expected = ['report3']
        actual = self.config.models_affected_validation_experiments['model1']
        self.assertListEqual(expected, actual)


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
        fname1 = os.path.join(os.path.dirname(__file__), 'report1.txt')
        fname2 = os.path.join(os.path.dirname(__file__), 'report2.txt')

        data1 = self.model.simulate(0, 1000, 100)
        data2 = self.model.simulate(0, 1000, 100)
        data1.to_csv(fname1, sep='\t')
        data2.to_csv(fname2, sep='\t')

        fname3 = os.path.join(os.path.dirname(__file__), 'report3.txt')
        df = pandas.read_csv(fname2, sep='\t')
        ## remove square brackets around species
        df = df.rename(columns={list(df.keys())[2]: list(df.keys())[2] + str('_indep')})
        df.to_csv(fname3, sep='\t', index=False)
        assert os.path.isfile(fname3)

        ## create some SS data for fitting
        ss_df = df.drop('Time', axis=1)
        ss_df = pandas.DataFrame(ss_df.iloc[0].transpose(), index=list(ss_df.keys())).transpose()
        fname4 = os.path.join(os.path.dirname(__file__), 'report4.txt')
        ss_df.to_csv(fname4, sep='\t', index=False)

        ## create some SS data with more than one experiment
        fname5 = os.path.join(os.path.dirname(__file__), 'report5.txt')
        s = 'A\tB\tC\n0.07\t0.06\t2.8\n\n0.09\t0.10\t2.9\n'
        with open(fname5, 'w') as f:
            f.write(s)

        self.report1 = fname1
        self.report2 = fname2
        self.report3 = fname3
        self.report4 = fname4
        self.report5 = fname5

        self.conf_dct = dict(
            models=dict(
                model1=dict(
                    copasi_file=self.model.copasi_file,
                    results_directory=os.path.join(self.model.root, 'ParameterEstimationResults'))
            ),
            datasets=dict(
                experiments=dict(
                    report1=dict(
                        filename=self.report1,
                    ),
                    report2=dict(
                        filename=self.report2
                    ),
                    ss=dict(
                        filename=self.report4
                    ),
                    ss_multi=dict(
                        filename=self.report5
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
                        affected_experiments=['report1', 'ss', 'ss_multi']
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
        # self.mod = self.PE.models['first'].model
        # print(self.mod)

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
        self.assertEqual(count, 5)

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
            os.path.join(os.path.dirname(__file__), 'report1.txt'), 'File Name')

    def test_experiment_number_of_columns(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('4', 'Number of Columns')

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
        self.assertEqual(5, count)

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
        mod = self.PE.models.model1.model
        query = '//*[@name="Experiment Set"]'
        count = 0
        for i in mod.xml.xpath(query):
            for j in i:
                count += 1
        self.assertEqual(5, count)

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
        self.assertEqual(5, count)

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

    def test_independent_variables_get_mapped(self):
        mod = self.PE.models['model1'].model
        query = '//*[@name="ss"]'
        actual = None
        expected = r'CN=Root,Model=TestModel1,Vector=Compartments[nuc],Vector=Metabolites[B],Reference=InitialConcentration'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'Object Map':
                    for k in j:
                        if k.attrib['name'] == '1':
                            for l in k:
                                if l.attrib['name'] == 'Object CN':
                                    actual = l.attrib['value']
        self.assertEqual(expected, actual)

    def test_affected_experiments_key(self):
        """
        Since changing the configuration to support experimental data files containing more than
        one experiment there has been a bug in the mapping of initial concentation of A. After digging,
        it turns out that the initial concentration of A makes use of the affected experiments feature which
        is causing the bug because of inconsisent experiment keys.
        Returns:

        """
        #  Could not find experiment for fit item 'CN=Root,Model=TestModel1,Vector=Compartments[nuc],
        #  Vector=Metabolites[A],Reference=InitialConcentration'.
        mod = self.PE.models['model1'].model
        query = '//*[@name="Affected Experiments"]'
        actual = None
        expected = 'Experiment_report1'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['value'] == 'Experiment_report1':
                    actual = 'Experiment_report1'
        self.assertEqual(expected, actual)


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
                create_parameter_sets=False,
                upper_bound=50,
                lower_bound=0.1,
            )
        )
        self.conf = ParameterEstimation.Config(**self.conf_dct)

        self.PE = pycotools3.tasks.ParameterEstimation(self.conf)

        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

    def test_load_model(self):
        self.assertIsInstance(self.PE.config.models.model1.model, pycotools3.model.Model)

    def test_output_directory_id(self):
        ## build the results directory gradually so that it works on windows and linus
        results_directory = os.path.join(os.path.dirname(__file__), 'Problem1')
        # results_directory = os.path.join(results_directory, 'res')
        results_directory = os.path.join(results_directory, 'Fit1')
        results_directory = os.path.join(results_directory, 'model1')
        results_directory = os.path.join(results_directory, 'ParameterEstimationData')
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

    def test_number_of_affected_experiments_is_correct(self):
        count = 0
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="Affected Experiments"]'):
            # print(i, i.attrib)
            for j in i:
                print(j, j.attrib)
                count += 1

        ## only 1 of 3 experiment datasets has affected_experiments
        self.assertEqual(2, count)

    def test_number_of_affected_validation_experiments_is_correct(self):
        count = 0
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="Affected Cross Validation Experiments"]'):
            for j in i:
                count += 1

        ## only 1 of 3 experiment datasets has affected_experiments
        self.assertEqual(1, count)

    def test_affected_experiments_for_global_quantity_A2B(self):
        experiment_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib['value'] == 'CN=Root,Model=TestModel1,Vector=Values[A2B],Reference=InitialValue':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Experiments':
                        for k in j:
                            experiment_keys.append(k.attrib['value'])

        self.assertListEqual([], experiment_keys)

    def test_affected_experiments_for_initial_value_A(self):
        ## line 2994
        ##4215 is the problem for this test
        ## and 4268
        experiment_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib[
                'value'] == 'CN=Root,Model=TestModel1,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=InitialConcentration':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Experiments':
                        for k in j:
                            experiment_keys.append(k.attrib['value'])

        self.assertListEqual(['Experiment_report1', 'Experiment_report4'], experiment_keys)

    def test_affected_validation_experiments_for_global_quantity_A2B(self):
        count = 0
        valiadtion_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib['value'] == 'CN=Root,Model=TestModel1,Vector=Values[A2B],Reference=InitialValue':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Cross Validation Experiments':
                        for k in j:
                            valiadtion_keys.append(k.attrib['value'])

        self.assertListEqual([], valiadtion_keys)

    def test_affected_validation_experiments_for_ic_B(self):
        valiadtion_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib[
                'value'] == 'CN=Root,Model=TestModel1,Vector=Compartments[nuc],Vector=Metabolites[B],Reference=InitialConcentration':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Cross Validation Experiments':
                        for k in j:
                            valiadtion_keys.append(k.attrib['value'])

        self.assertListEqual(['Experiment_report2'], valiadtion_keys)

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
        mod = self.PE.model_copies['model1'][3]
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
        mod = self.PE.model_copies['model1'][3]
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
        mod = self.PE.model_copies['model1'][3]
        expected_report_name = os.path.join(
            self.PE.results_directory['model1'], 'PEData3.txt')
        actual = ''
        query = '//*[@name="Scan"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.tag == 'Report':
                    actual = j.attrib['target']
        self.assertEqual(expected_report_name, actual)

    def test_run_mode_is_true(self):
        """
        false by default
        :return:
        """
        self.PE.config.settings.run_mode = True
        self.PE.run(self.PE.model_copies)

        expected = 4
        results_dir = self.PE.results_directory['model1']
        files = glob.glob(os.path.join(
            results_dir, '*.txt')
        )
        self.assertEqual(expected, len(files))

    def test_parse_pe_data(self):
        self.PE.config.settings.run_mode = True
        self.PE.run(self.PE.model_copies)

        data = pycotools3.viz.Parse(self.PE).data
        expected = 8
        self.assertEqual(expected, data['model1'].shape[0])

    def test_randomize_start_values(self):
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

    def test_upper_bound(self):
        mod = self.PE.config.models.model1.model
        query = '//*[@name="FitItem"]'
        ## note the 100 at the end is from constraint_items
        expected = ['50', '50', '50', '50', '50', '50', '50', '50', '100']
        actual = []
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'UpperBound':
                    actual.append(j.attrib['value'])
        self.assertListEqual(expected, actual)

    def test_lower_bound(self):
        mod = self.PE.config.models.model1.model
        query = '//*[@name="FitItem"]'
        ## note the 100 at the end is from constraint_items
        expected = ['0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1']
        actual = []
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'LowerBound':
                    actual.append(j.attrib['value'])
        self.assertListEqual(expected, actual)

    def test_model_value_start_value_resolves(self):
        mod = self.PE.config.models.model1.model
        query = '//*[@name="FitItem"]'
        ## note the 100 at the end is from constraint_items
        expected = ['1.0000001549282924', '1.0000001549282924', '1.0000001549282924', '4.0', '9.0', '0.1', '0.1', '0.1',
                    '9.0']
        actual = []
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'StartValue':
                    actual.append(j.attrib['value'])
        self.assertListEqual(expected, actual)


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
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 10)
            config = context.get_config()

        self.assertTrue(isinstance(config, ParameterEstimation.Config))

    def test_create_config_file(self):
        fname = os.path.join(os.path.dirname(__file__), 'config_file.yaml')
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a', filename=fname) as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 10)
            config = context.get_config()
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
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 10)
            config = context.get_config()

        self.assertTrue(os.path.isfile(fname))

    def test_create_config_file_with_prefix(self):
        ## means set_Default_fit_items_str isn't working properly
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('prefix', 'B')
            context.set('number_of_generations', 25)
            context.set('population_size', 10)
            config = context.get_config()
        expected = sorted(['B', 'B2C', 'B2C_0_k2'])
        actual = sorted(list(config.items.fit_items.keys()))
        self.assertListEqual(expected, actual)

    def test_settings_get_updated(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            context.set('prefix', 'B')
            config = context.get_config()
        expected = 'genetic_algorithm_sr'
        actual = config.settings.method
        self.assertEqual(expected, actual)

    def test_settings_get_updated2(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            context.set('prefix', 'B')
            config = context.get_config()
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
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            context.set('prefix', 'B')
            context.set('separator', ',')
            config = context.get_config()
        pe = ParameterEstimation(config)

        query = '//*[@name="Separator"]'
        actual = []
        for i in pe.config.models.test_model.model.xml.xpath(query):
            actual.append(i.attrib['value'])

        expected = [',', ',', ',', ',']
        self.assertListEqual(expected, actual)

    def test_context_set_lower_bound(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 254)
            context.set('population_size', 143)
            context.set('prefix', 'B')
            context.set('separator', ',')
            context.set('start_value', 5)
            context.set('lower_bound', 0.1)
            context.set('upper_bound', 10)
            # start value lower bound and upper bounds are not being copied over to config.items.fititems
            config = context.get_config()
        pe = ParameterEstimation(config)

        mod = pe.models.test_model.model
        l = []
        query = '//*[@name="FitItem"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'LowerBound':
                    l.append(j.attrib['value'])
        self.assertListEqual([0.1, 0.1, 0.1], [float(i) for i in l])

    def test_context_mappings_after_use_of_set(self):
        fname = os.path.join(os.path.dirname(__file__), 'timeseries.txt')
        data = self.model.simulate(0, 10, 11)
        data.to_csv(fname)

        with ParameterEstimation.Context(
                self.model.copasi_file, fname,
                context='s', parameters='a') as context:
            context.set('separator', ',')
            config = context.get_config()

        pe = ParameterEstimation(config)
        query = '//*[@name="Object Map"]'
        expected = 4
        count = 0
        for i in pe.models.test_model.model.xml.xpath(query):
            for j in i:
                count += 1
        self.assertEqual(expected, count)

    def test_default_mappings(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            config = context.get_config()
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
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            config = context.get_config()
        pe = ParameterEstimation(config)
        query = '//*[@name="Object Map"]'
        expected = 4
        actual = 0
        for i in pe.models.test_model.model.xml.xpath(query):
            actual += 1
        self.assertEqual(expected, actual)

    def test_setup_scan_pe_number(self):
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            context.set('copy_number', 3)
            context.set('pe_number', 2)
            config = context.get_config()
        pe = ParameterEstimation(config)

        mod = pe.model_copies['test_model'][1]
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
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            context.set('copy_number', 3)

            config = context.get_config()
        pe = ParameterEstimation(config)

        mod = pe.model_copies['test_model'][0]
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
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='a') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            context.set('copy_number', 3)

            config = context.get_config()
        pe = ParameterEstimation(config)
        mod = pe.model_copies['test_model'][1]
        expected_report_name = os.path.join(
            pe.results_directory['test_model'], 'PEData1.txt')
        actual = ''
        query = '//*[@name="Scan"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.tag == 'Report':
                    actual = j.attrib['target']
        self.assertEqual(expected_report_name, actual)

    def test_that_it_works(self):
        ##compartments not being added to report?
        with ParameterEstimation.Context(
                self.model.copasi_file,
                [self.TC1.report_name, self.TC2.report_name,
                 self.report3, self.report4],
                context='s', parameters='glm') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('number_of_generations', 25)
            context.set('population_size', 14)
            context.set('randomize_start_values', True)
            context.set('copy_number', 3)
            context.set('run_mode', True)
            config = context.get_config()

        pe = ParameterEstimation(config)
        data = pycotools3.viz.Parse(pe)
        self.assertEqual(3, data['test_model'].shape[0])


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
            context.set('method', 'genetic_algorithm_sr')
            context.set('population_size', 49)
            config = context.get_config()
        PE = ParameterEstimation(config)
        time.sleep(0.2)
        actual = self.get_population_size(PE.config.models.first.model.xml)
        self.assertEqual(str(49), actual)

    def test_two_models_second(self):
        with ParameterEstimation.Context(
                models=[self.mod1.copasi_file, self.mod2.copasi_file],
                experiments=self.experiment, context='s', parameters='g') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('population_size', 84)
            config = context.get_config()
        PE = ParameterEstimation(config)
        time.sleep(0.2)
        actual = self.get_population_size(PE.config.models.second.model.xml)
        self.assertEqual(str(84), actual)

    def test_two_models_experiments(self):
        with ParameterEstimation.Context(
                models=[self.mod1.copasi_file, self.mod2.copasi_file],
                experiments=self.experiment, context='s', parameters='g') as context:
            context.set('method', 'genetic_algorithm_sr')
            context.set('population_size', 84)
            config = context.get_config()
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
            context.set('method', 'genetic_algorithm_sr')
            context.set('population_size', 84)
            config = context.get_config()
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


class UseConfigMoreThanOnceTest(_test_base._BaseTest):
    """
    I noticed a bug where if you use a config object in
    a parameter estimation, modify it and then use it again,
    we get an error. This class reproduces this situation
    and tests for it
    """

    def setUp(self):
        super(UseConfigMoreThanOnceTest, self).setUp()

        self.fname = os.path.join(os.path.dirname(__file__), 'timecourse.txt')
        self.model.simulate(0, 10, 1, report_name=self.fname)

        self.conf_dct = dict(
            models=dict(
                test_model=dict(
                    copasi_file=self.model.copasi_file
                )
            ),
            datasets=dict(
                experiments=dict(
                    timecourse=dict(
                        filename=self.fname,
                    ),
                )
            ),
            items=dict(
                fit_items='g',
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
                create_parameter_sets=False,
                upper_bound=50,
                lower_bound=0.1,
                run_mode=True,
            )
        )
        self.config = ParameterEstimation.Config(**self.conf_dct)

    def test_runs_once(self):
        PE = ParameterEstimation(self.config)
        data = pycotools3.viz.Parse(PE)
        expected = 8
        actual = data['test_model'].shape[0]
        self.assertEqual(expected, actual)

    def test_runs_twice(self):
        PE = ParameterEstimation(self.config)
        PE = ParameterEstimation(self.config)
        data = pycotools3.viz.Parse(PE)
        expected = 8
        actual = data['test_model'].shape[0]
        self.assertEqual(expected, actual)

    def test_runs_twice_different_method(self):
        PE = ParameterEstimation(self.config)
        self.config.settings.method = 'hooke_jeeves'
        self.config.settings.iteration_limit = 10
        self.config.settings.tolerance = 1e-2
        PE = ParameterEstimation(self.config)
        data = pycotools3.viz.Parse(PE)
        expected = 8
        actual = data['test_model'].shape[0]
        self.assertEqual(expected, actual)

    def test_runs_with_context_manager(self):
        with ParameterEstimation.Context(
                self.model, self.fname, context='s', parameters='g') as context:
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 25)
            context.set('copy_number', 4)
            context.set('pe_number', 2)
            context.set('run_mode', True)
            config = context.get_config()
        pe = ParameterEstimation(config)
        data = pycotools3.viz.Parse(pe)
        expected = 8
        actual = data['test_model'].shape[0]
        self.assertEqual(expected, actual)

    def test_runs_first_without_then_with_context_manager(self):
        pe = ParameterEstimation(self.config)
        with ParameterEstimation.Context(
                self.model, self.fname, context='s', parameters='g') as context:
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 25)
            context.set('copy_number', 4)
            context.set('pe_number', 2)
            context.set('run_mode', True)
            config = context.get_config()
        pe = ParameterEstimation(config)
        data = pycotools3.viz.Parse(pe)
        expected = 8
        actual = data['test_model'].shape[0]
        self.assertEqual(expected, actual)


class TestThatRemoveExperimentsWorksCorrectly(_test_base._BaseTest):
    def setUp(self):
        super(TestThatRemoveExperimentsWorksCorrectly, self).setUp()

        self.fname = os.path.join(os.path.dirname(__file__), 'timecourse.txt')
        self.model.simulate(0, 10, 1, report_name=self.fname)

        self.conf_dct = dict(
            models=dict(
                test_model=dict(
                    copasi_file=self.model.copasi_file
                )
            ),
            datasets=dict(
                experiments=dict(
                    data=dict(  ## Note that the name of this dataset is different to timecourse.txt
                        filename=self.fname,
                    ),
                )
            ),
            items=dict(
                fit_items='g',
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
                create_parameter_sets=False,
                upper_bound=50,
                lower_bound=0.1,
                run_mode=False,
            )
        )
        self.config = ParameterEstimation.Config(**self.conf_dct)

    def test_experiments_can_be_removed(self):
        query = '//*[@name="Experiment Set"]'
        pe = ParameterEstimation(self.config)
        pe._remove_all_experiments()
        expected = None
        actual = None
        for i in pe.models.test_model.model.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'data':
                    actual = True
        self.assertEqual(expected, actual)


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

        self.fname1 = os.path.join(os.path.dirname(__file__), 'dataset1.txt')
        self.fname2 = os.path.join(os.path.dirname(__file__), 'dataset2.txt')

        self.mod1.simulate(0, 9, 1, report_name=self.fname1)
        self.mod2.simulate(0, 9, 1, report_name=self.fname2)

        with ParameterEstimation.Context(
                [self.mod1, self.mod2], [self.fname1, self.fname2],
                context='s', parameters='g'
        ) as context:
            self.config = context.get_config()

        config_dct = dict(
            models=dict(
                first=dict(
                    copasi_file=self.mod1.copasi_file,
                ),
                second=dict(
                    copasi_file=self.mod2.copasi_file
                )
            ),
            datasets=dict(
                experiments=dict(
                    first_exp=dict(
                        filename=self.fname1
                    ),
                    second_exp=dict(
                        filename=self.fname2
                    )
                )
            ),
            items=dict(
                fit_items='g'
            ),
            settings=dict(
                working_directory=os.path.dirname(__file__)
            )
        )
        self.config = ParameterEstimation.Config(**config_dct)

    def test_experiments_obey_affected_models_list(self):
        self.config.datasets.experiments.first_exp.affected_models = ['first']
        self.config.datasets.experiments.second_exp.affected_models = ['second']
        pe = ParameterEstimation(self.config)
        query = '//*[@name="Experiment Set"]'
        experiment_names = []
        for i in pe.models.first.model.xml.xpath(query):
            for j in i:
                experiment_names.append(j.attrib['name'])

    def test_experiments_obey_affected_models_list_affected_experiments_in_fit_items(self):
        self.config.datasets.experiments.first_exp.affected_models = ['first']
        self.config.datasets.experiments.second_exp.affected_models = ['second']
        pe = ParameterEstimation(self.config)
        query = '//*[@name="FitItem"]'
        experiment_names = []
        for i in pe.models.first.model.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'Affected Experiments':
                    for k in j:
                        experiment_names.append(k.attrib['name'])
        self.assertNotIn('second', experiment_names)

    def test_fit_items_obey_affected_models(self):
        self.config.items.fit_items.k1.affected_models = 'first'
        self.config.items.fit_items.k2.affected_models = 'second'
        pe = ParameterEstimation(self.config)
        query = '//*[@name="FitItem"]'
        fit_items = []
        for i in pe.models.first.model.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'ObjectCN':
                    fit_items.append(j.attrib['value'])

        [self.assertTrue('[k2]' not in i) for i in fit_items]


class TestModelBuildWithOOInterface(unittest.TestCase):
    def setUp(self):
        ## Choose a working directory for model
        working_directory = os.path.abspath('')
        copasi_file = os.path.join(working_directory, 'MichaelisMenten.cps')

        if os.path.isfile(copasi_file):
            os.remove(copasi_file)

        kf = 0.01
        kb = 0.1
        kcat = 0.05
        with pycotools3.model.Build(copasi_file) as m:
            m.name = 'Michaelis-Menten'
            m.add('compartment', name='Cell')

            m.add('metabolite', name='P', concentration=0)
            m.add('metabolite', name='S', concentration=30)
            m.add('metabolite', name='E', concentration=10)
            m.add('metabolite', name='ES', concentration=0)

            m.add('reaction', name='S bind E', expression='S + E -> ES', rate_law='kf*S*E',
                  parameter_values={'kf': kf})

            m.add('reaction', name='S unbind E', expression='ES -> S + E', rate_law='kb*ES',
                  parameter_values={'kb': kb})

            m.add('reaction', name='ES produce P', expression='ES -> P + E', rate_law='kcat*ES',
                  parameter_values={'kcat': kcat})

        self.mm = pycotools3.model.Model(copasi_file)
        self.fname = os.path.join(working_directory, 'data.txt')
        self.mm.simulate(0, 10, 11, report_name=self.fname)

    def test(self):
        with ParameterEstimation.Context(
                self.mm.copasi_file, self.fname,
                context='s', parameters='l') as context:
            context.randomize_start_values = True
            context.lower_bound = 0.01
            context.upper_bound = 100
            context.run_mode = True
            config = context.get_config()
        PE = ParameterEstimation(config)
        self.assertIsInstance(PE, ParameterEstimation)

    ##todo use mocking for running tests.


class CrossValidationContextTests(_test_base._BaseTest):
    def setUp(self):
        super(CrossValidationContextTests, self).setUp()

        self.ant = self.ant.replace('ADeg: A => ; nuc*ADeg_k1*A;', '')
        self.ant = self.ant.replace('ADeg_k1 = 0.1;', '')
        self.model = pycotools3.model.loada(self.ant, copasi_file=self.copasi_file)

        self.tc_fname1 = os.path.join(os.path.dirname(__file__), 'timecourse1.txt')
        self.tc_fname2 = os.path.join(os.path.dirname(__file__), 'timecourse2.txt')
        self.ss_fname1 = os.path.join(os.path.dirname(__file__), 'steady_state1.txt')
        self.ss_fname2 = os.path.join(os.path.dirname(__file__), 'steady_state2.txt')

        self.model.simulate(0, 5, 0.1, report_name=self.tc_fname1)
        self.model.simulate(0, 10, 0.5, report_name=self.tc_fname2)
        dct1 = {
            'A': 0.07,
            'B': 0.06,
            'C': 2.8
        }
        dct2 = {
            'A': 846,
            'B': 697,
            'C': 739
        }
        self.ss1 = pandas.DataFrame(dct1, index=[0])
        self.ss1.to_csv(self.ss_fname1, sep='\t', index=False)
        self.ss2 = pandas.DataFrame(dct2, index=[0])
        self.ss2.to_csv(self.ss_fname2, sep='\t', index=False)
        self.experiments = [self.tc_fname1, self.tc_fname2,
                            self.ss_fname1, self.ss_fname2]

        self.expected_experiments = {
            '4_0': ('timecourse1', 'timecourse2', 'steady_state1', 'steady_state2'),
            '3_0': ('timecourse1', 'timecourse2', 'steady_state1'),
            '3_1': ('timecourse1', 'timecourse2', 'steady_state2'),
            '3_2': ('timecourse1', 'steady_state1', 'steady_state2'),
            '3_3': ('timecourse2', 'steady_state1', 'steady_state2')}
        self.expected_validations = {
            '4_0': [],
            '3_0': ['steady_state2'],
            '3_1': ['steady_state1'],
            '3_2': ['timecourse2'],
            '3_3': ['timecourse1']}

    def test_simple(self):
        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, self.experiments, context='cv', parameters='gm'
        ) as context:
            context.set('randomize_start_values', True)
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 20)
            context.set('number_of_generations', 50)
            context.set('swarm_size', 100)
            context.set('iteration_limit', 2000)
            context.set('copy_number', 3)
            context.set('validation_threshold', 500)
            context.set('cross_validation_depth', 1)
            context.set('run_mode', True)
            context.set('lower_bound', 1e-3)
            context.set('upper_bound', 1e2)
            config = context.get_config()

        pe = ParameterEstimation(config)
        data = pycotools3.viz.Parse(pe).concat()
        self.assertLess(data.loc['3_0', 0]['RSS'], data.loc['3_1', 0]['RSS'])


class ParameterEstimationTestsWithDifferentTypesOfDataSet(_test_base._BaseTest):
    """
    Sometimes we want to show copasi data files that have individual repeats
    rather than the average. These repeats are separated by a blank
    line. Test that ParameterEstimation is flexible enough to
    support both.
    """

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

        self.data1 = "A,B,C\n5,10,15\n\n\n"""

        self.data2 = "A,B,C\n5,10,15\n\n4,11,14\n\n6,9,16"

        self.data3 = "Time,A,B,C\n" \
                     "0,5,10,15\n" \
                     "1,6,11,16\n" \
                     "2,7,12,17\n" \
                     "\n" \
                     "0,8,12,16\n" \
                     "1,9,12,17\n" \
                     "2,10,13,18\n" \
                     "\n" \
                     "0,5,10,15\n" \
                     "1,6,11,16\n" \
                     "2,7,12,17\n"

        fname1 = os.path.join(os.path.dirname(__file__), 'first.cps')
        self.mod1 = pycotools3.model.loada(ant1, fname1)

        self.fname1 = os.path.join(os.path.dirname(__file__), 'dataset1.txt')
        self.fname2 = os.path.join(os.path.dirname(__file__), 'dataset2.txt')
        self.fname3 = os.path.join(os.path.dirname(__file__), 'dataset3.txt')

        with open(self.fname1, 'w') as f:
            f.write(self.data1)
        with open(self.fname2, 'w') as f:
            f.write(self.data2)
        with open(self.fname3, 'w') as f:
            f.write(self.data3)

        with ParameterEstimation.Context(
                self.mod1, [self.fname1, self.fname2, self.fname3],
                context='s', parameters='g') as context:
            context.set('separator', ',')
            self.config = context.get_config()

        self.pe = ParameterEstimation(self.config)

    # def tearDown(self):
    #     os.remove(self.fname1)
    #     os.remove(self.fname2)
    #     os.remove(self.fname3)

    def test_line_numbers_accurate_in_multi_experiment_file(self):
        actual_end = None
        actual_start = None
        mod = self.pe.config.models['first'].model
        for i in mod.xml.xpath("//*[@name='dataset2_MultiExperiment1']"):
            for j in list(i):
                if j.attrib['name'] == 'First Row':
                    actual_start = int(j.attrib['value'])
                elif j.attrib['name'] == 'Last Row':
                    actual_end = int(j.attrib['value'])
        expected_start = 4
        expected_end = 4
        # ans = [(1, 2), (4, 4), (6, 6)]
        self.assertEqual((expected_start, expected_end), (actual_start, actual_end))

    def test_line_numbers_accurate_in_multi_experiment_file2(self):
        actual_end = None
        actual_start = None
        mod = self.pe.config.models['first'].model
        for i in mod.xml.xpath("//*[@name='dataset2_MultiExperiment1']"):
            for j in list(i):
                if j.attrib['name'] == 'First Row':
                    actual_start = int(j.attrib['value'])
                elif j.attrib['name'] == 'Last Row':
                    actual_end = int(j.attrib['value'])
        expected_start = 4
        expected_end = 4
        # ans = [(1, 2), (4, 4), (6, 6)]
        self.assertEqual((expected_start, expected_end), (actual_start, actual_end))

    def test_file_data_file3(self):
        expected = (10, 12)

        actual_start = None
        actual_end = None

        mod = self.pe.config.models['first'].model
        for i in mod.xml.xpath("//*[@name='dataset3_MultiExperiment2']"):
            for j in list(i):
                if j.attrib['name'] == 'First Row':
                    actual_start = int(j.attrib['value'])
                elif j.attrib['name'] == 'Last Row':
                    actual_end = int(j.attrib['value'])
        self.assertEqual(expected, (actual_start, actual_end))


class DuplicateForEachExperimentTests(_test_base._BaseTest):
    """
    Sometimes we want to show copasi data files that have individual repeats
    rather than the average. These repeats are separated by a blank
    line. Test that ParameterEstimation is flexible enough to
    support both.
    """

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

        self.data1 = "A,B,C\n5,10,15\n\n\n"""

        self.data2 = "A,B,C\n5,10,15\n\n4,11,14\n\n6,9,16"

        self.data3 = "Time,A,B,C\n" \
                     "0,5,10,15\n" \
                     "1,6,11,16\n" \
                     "2,7,12,17\n" \
                     "\n" \
                     "0,8,12,16\n" \
                     "1,9,12,17\n" \
                     "2,10,13,18\n" \
                     "\n" \
                     "0,5,10,15\n" \
                     "1,6,11,16\n" \
                     "2,7,12,17\n"

        fname1 = os.path.join(os.path.dirname(__file__), 'first.cps')

        with pycotools3.model.BuildAntimony(fname1) as loader:
            self.mod1 = loader.load(ant1)

        self.fname1 = os.path.join(os.path.dirname(__file__), 'dataset1.txt')
        self.fname2 = os.path.join(os.path.dirname(__file__), 'dataset2.txt')
        self.fname3 = os.path.join(os.path.dirname(__file__), 'dataset3.txt')

        with open(self.fname1, 'w') as f:
            f.write(self.data1)
        with open(self.fname2, 'w') as f:
            f.write(self.data2)
        with open(self.fname3, 'w') as f:
            f.write(self.data3)

        with ParameterEstimation.Context(
                self.mod1, [self.fname1, self.fname2, self.fname3],
                context='s', parameters='g') as context:
            context.set('separator', ',')
            self.config = context.get_config()

        self.pe = ParameterEstimation(self.config)

    # def test(self):
    #     self.pe.duplicate_for_every_experiment(
    #         self.pe.models['first'].model,
    #         'A',
    #     )


#


if __name__ == '__main__':
    unittest.main()
