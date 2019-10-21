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
        self.assertListEqual(expected, actual)


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
        expected = [2, 6]
        actual = list(data['test_model'].shape)
        self.assertListEqual(expected, actual)

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
        self.assertListEqual(expected, actual)


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



class WaterfallPlotTests(_test_base._BaseTest):
    def setUp(self):
        super(WaterfallPlotTests, self).setUp()

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

    # def test_boxplot_is_saved(self):
    #     """
    #     :return:
    #     """
    #     b = pycotools3.viz.Boxplots(self.pe, savefig=True, num_per_plot=2)
    #     self.assertEqual(len(glob.glob(b.results_directory['test_model'] + '/*')), 3)

    def test_waterfall_plot_is_created(self):
        wf = viz.WaterfallPlot(self.pe, savefig=True)
        res = wf.create_directory()

class PlotParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(PlotParameterEstimationTests, self).setUp()

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

    def test_create_directory(self):
        """

        :return:
        """
        pl = pycotools3.viz.PlotParameterEstimation(self.pe, savefig=False)

        dire = pl.create_directories()
        # for k, v in dire.items():
            # print(k, v)
            # self.assertTrue(os.path.isdir(v))

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
        # for i in pl.create_directories():
        #     self.assertEqual(len(glob.glob(pl.create_directories()[i] + '/*')), 6)

    # def test_plot2(self):
    #     """
    #     test y argument works
    #     :return:
    #     """
    #     pl = pycotools3.viz.PlotParameterEstimation(self.pe,
    #                                                 savefig=True,
    #                                                 show=False,
    #                                                 y=['A', 'B'])
    #     pl.plot()
        # for i in pl.create_directories():
        #     self.assertEqual(len(glob.glob(pl.create_directories()[i] + '/*')), 2)
#

# class PlotTimeCourseTests(_test_base._BaseTest):
#
#     def setUp(self):
#         super(PlotTimeCourseTests, self).setUp()
#         self.model = pycotools3.model.Model(self.copasi_file)
#         self.original_parameters = self.model.parameters
#
#         self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=10, step_size=0.1,
#                                                intervals=50, report_name='report1.txt')
#
#     def test_plot_tc(self):
#         T = pycotools3.viz.PlotTimeCourse(self.TC1, savefig=True)
#         self.assertEqual(len(glob.glob(T.results_directory + '/*')), 7)
#
#     def test_plot_tc(self):
#         T = pycotools3.viz.PlotTimeCourse(self.TC1, savefig=True, y=['A', 'B'], x='A', show=False)
#         self.assertEqual(len(glob.glob(T.results_directory + '/*')), 2)
#
#
# class EnsembleTimeCourseTests(_test_base._BaseTest):
#
#     def setUp(self):
#         super(EnsembleTimeCourseTests, self).setUp()
#         self.model = pycotools3.model.Model(self.copasi_file)
#         self.original_parameters = self.model.parameters
#
#
# class PlotPLTests(_test_base._BaseTest):
#     def setUp(self):
#         super(PlotPLTests, self).setUp()
#         self.model = pycotools3.model.Model(self.copasi_file)
#
#         ## simulate time course
#         tc = pycotools3.tasks.TimeCourse(self.model, end=1000, intervals=1000, step_size=1)
#
#         ## format time course for parameter estimation
#         pycotools3.misc.format_timecourse_data(tc.report_name)
#
#         ## get the paramete pickle filename
#         pe_data_file = os.path.join(self.model.root, 'test_profile_likleihood.pickle')
#
#         ##try and get data from parameter pickle.
#         ## if you can get the df, if not simulate the data
#         try:
#             PE = pycotools3.tasks.MultiParameterEstimation(
#                 self.model, tc.report_name, metabolites=[],
#                 lower_bound=0.1, upper_bound=100, method='genetic_algorithm',
#                 copy_number=1, pe_number=10, number_of_generations=1,
#                 population_size=1, overwrite_config_file=True,
#             )
#             PE.write_config_file()
#             PE._setup()
#             df = pandas.read_pickle(pe_data_file)
#         except IOError:
#             PE = pycotools3.tasks.MultiParameterEstimation(
#                 self.model, tc.report_name, metabolites=[],
#                 lower_bound=0.1, upper_bound=100, method='genetic_algorithm',
#                 copy_number=5, pe_number=10, number_of_generations=1,
#                 population_size=1, overwrite_config_file=True
#             )
#             PE.write_config_file()
#             PE._setup()
#             PE.run()
#             time.sleep(10)
#             p = pycotools3.viz.Parse(PE)
#
#             ##write pickle
#             p.data.to_pickle(pe_data_file)
#             df = pandas.read_pickle(pe_data_file)
#
#         ## try read the profile likelihood data
#         ## if fail with input error, simulate profile likelihood data
#         try:
#             self.PL = pycotools3.tasks.ProfileLikelihood(
#                 self.model, df=df, index=[0, 1],
#                 lower_bound_multiplier=1001,
#                 log10=True, run=False, tolerance=1e-1,
#                 iteration_limit=1
#             )
#             p = pycotools3.viz.Parse(self.PL)
#
#         except pycotools3.errors.InputError:
#             self.PL = pycotools3.tasks.ProfileLikelihood(
#                 self.model, df=df, index=[0, 1],
#                 lower_bound_multiplier=1001,
#                 log10=True, run='multiprocess', tolerance=1e-1,
#                 iteration_limit=1, intervals=4,
#             )
#             time.sleep(100)
#             p = pycotools3.viz.Parse(self.PL)
#
#     def test_parse(self):
#         p = pycotools3.viz.Parse(self.PL)
#         self.assertTrue(isinstance(p.data, pandas.core.frame.DataFrame))
#
#     def test_parse_pl_log_linear(self):
#         p = pycotools3.viz.Parse(self.PL)
#         linear_scale_value = p.data.loc['B2C']['RSS'].iloc[0]
#         log_scale = numpy.log10(linear_scale_value)
#         p2 = pycotools3.viz.Parse(self.PL, log10=True)
#
#         self.assertEqual(log_scale, p2.data.loc['B2C']['RSS'].iloc[0])
#

#


if __name__ == '__main__':
    unittest.main()
