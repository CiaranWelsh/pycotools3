# -*-coding: utf-8 -*-
"""
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
 $Author: Ciaran Welsh
Module that tests the operations of the _Base base test
"""
import pandas
import pycotools3
from pycotools3 import model, tasks, viz
from Tests import _test_base
import unittest
import os
import numpy
import glob
import time


class ParseDataTests(_test_base._BaseTest):
    def setUp(self):
        super(ParseDataTests, self).setUp()

        fname = os.path.join(os.path.dirname(__file__), 'report1.txt')
        data = self.model.simulate(0, 50, 1, report_name=fname)

        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, fname, context='s', parameters='g',
        ) as context:
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 2)
            context.set('number_of_generations', 5)
            context.set('copy_number', 2)
            context.set('pe_number', 2)
            context.set('randomize_start_values', True)
            context.set('lower_bound', 0.01)
            context.set('upper_bound', 10)
            context.set('run_mode', True)
            config = context.get_config()

        self.pe = pycotools3.tasks.ParameterEstimation(config)

    def test_parse_parameter_estimation_data(self):
        """
        :return:
        """
        data = viz.Parse(self.pe).data
        expected = [4, 6]
        actual = list(data['test_model'].shape)
        # self.assertListEqual(expected, actual)


class TruncateDataTests(_test_base._BaseTest):
    def setUp(self):
        super(TruncateDataTests, self).setUp()

        fname = os.path.join(os.path.dirname(__file__), 'report1.txt')
        data = self.model.simulate(0, 50, 1, report_name=fname)

        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, fname, context='s', parameters='g',
        ) as context:
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 2)
            context.set('number_of_generations', 5)
            context.set('copy_number', 2)
            context.set('pe_number', 2)
            context.set('run_mode', True)
            config = context.get_config()

        self.pe = pycotools3.tasks.ParameterEstimation(config)
        self.data = viz.Parse(self.pe).data

    def test_below_theta_truncate_mode_using_percentile(self):
        """
        :return:
        """
        data = viz.TruncateData(self.data, mode='percent', theta=50)
        expected = [4, 6]
        actual = list(data['test_model'].shape)
        # self.assertListEqual(expected, actual)

    def test_below_theta_truncate_mode_using_ranks(self):
        """
        :return:
        """
        data = viz.TruncateData(self.data, mode='ranks', theta=1)
        expected = [1, 6]
        actual = list(data['test_model'].shape)
        self.assertListEqual(expected, actual)

    def test_below_theta_truncate_mode_using_ranks(self):
        """
        :return:
        """
        ##get best rank returns a series, not a dataframe
        data = viz.TruncateData(self.data, mode='ranks', theta=1)
        expected = 6
        actual = data['test_model'].shape[0]
        self.assertEqual(expected, actual)

    def test_below_theta_truncate_mode_using_below(self):
        """
        :return:
        """
        ##get best rank returns a series, not a dataframe
        data = viz.TruncateData(self.data, mode='below_theta', theta=100)
        expected = [4, 6]
        actual = list(data['test_model'].shape)
        # self.assertListEqual(expected, actual)


class BoxPlotTests(_test_base._BaseTest):
    def setUp(self):
        super(BoxPlotTests, self).setUp()

        fname = os.path.join(os.path.dirname(__file__), 'report1.txt')
        data = self.model.simulate(0, 50, 1, report_name=fname)

        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, fname, context='s', parameters='g',
        ) as context:
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 2)
            context.set('number_of_generations', 5)
            context.set('copy_number', 2)
            context.set('pe_number', 2)
            context.set('run_mode', True)
            config = context.get_config()

        self.pe = pycotools3.tasks.ParameterEstimation(config)

    def test_boxplot_is_saved(self):
        """
        :return:
        """
        b = pycotools3.viz.Boxplots(self.pe, savefig=True, num_per_plot=2)
        # self.assertEqual(len(glob.glob(b.results_directory['test_model'] + '/*')), 3)

    def test_boxplot_is_saved2(self):
        """
        :return:
        """
        b = pycotools3.viz.Boxplots(self.pe, savefig=True, num_per_plot=2,
                                    log10=True)
        # self.assertEqual(len(glob.glob(b.results_directory['test_model'] + '/*')), 3)


class WaterFallPlotTests(_test_base._BaseTest):
    def setUp(self):
        super(WaterFallPlotTests, self).setUp()

        fname = os.path.join(os.path.dirname(__file__), 'report1.txt')
        data = self.model.simulate(0, 50, 1, report_name=fname)

        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, fname, context='s', parameters='g',
        ) as context:
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 2)
            context.set('number_of_generations', 5)
            context.set('copy_number', 2)
            context.set('pe_number', 2)
            context.set('run_mode', True)
            config = context.get_config()

        self.pe = pycotools3.tasks.ParameterEstimation(config)

    def test_waterfall_is_saved(self):
        """
        :return:
        """
        b = pycotools3.viz.WaterfallPlot(self.pe, savefig=True)
        self.assertEqual(len(glob.glob(b.results_directory['test_model'] + '/*')), 1)


class PlotParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(PlotParameterEstimationTests, self).setUp()

        fname = os.path.join(os.path.dirname(__file__), 'report1.txt')
        data = self.model.simulate(0, 50, 1, report_name=fname)
        ss_fname = os.path.join(os.path.dirname(__file__), 'ss.txt')
        df = pandas.DataFrame({'A': 5, 'B': 5, 'C': 5}, index=[0])
        df.to_csv(ss_fname, index=False, sep='\t')

        with pycotools3.tasks.ParameterEstimation.Context(
                self.model, [fname, ss_fname], context='s', parameters='g',
        ) as context:
            context.set('method', 'genetic_algorithm')
            context.set('population_size', 2)
            context.set('number_of_generations', 5)
            context.set('copy_number', 2)
            context.set('pe_number', 2)
            context.set('randomize_start_values', True)
            context.set('lower_bound', 0.01)
            context.set('upper_bound', 10)
            context.set('run_mode', True)
            config = context.get_config()

        self.pe = pycotools3.tasks.ParameterEstimation(config)
        self.mod = self.pe.models['test_model'].model


    def test_update_parameters(self):
        """

        :return:
        """
        pl = pycotools3.viz.PlotParameterEstimation(self.pe, savefig=False)
        model = pl.update_parameters()
        lo = '(ADeg).k1'
        met = 'A'
        gl = 'B2C'
        # self.assertNotEqual(self.original_parameters[lo].iloc[0], model.parameters[lo].iloc[0])
        # self.assertNotEqual(self.original_parameters[gl].iloc[0], model.parameters[gl].iloc[0])
        # self.assertNotEqual(self.original_parameters[met].iloc[0], model.parameters[met].iloc[0])

    def test_plot(self):
        """
        test plots are being generated in correct place
        :return:
        """
        pl = pycotools3.viz.PlotParameterEstimation(
            self.pe,
            savefig=True,
            show=False,
        )
        k = list(pl.results_directory.keys())[0]
        self.assertEqual(len(glob.glob(pl.results_directory[k] + '/*/*.png')), 10)

if __name__ == '__main__':
    unittest.main()
