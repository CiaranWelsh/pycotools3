#-*-coding: utf-8 -*-
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
from Tests import _test_base
import unittest
import os
import numpy
import glob
import time


class VizTests(_test_base._BaseTest):
    def setUp(self):
        """
        instead of generating data on the fly like
        I should do (for good testing practivce), I've pre-ran the parameter estimations
        and saved the data to pickle under the extra_data_for_tests
        file. Now I can read this pickle and not have to run the
        parameter estimations each time I run a test. I've also
        parsed the data into a pandas dataframe using viz.parse for ease

        Data can be transformed into log10 scale with a keyword argument
        to any of the plotting functions. This cannot be tested here since
        i've simulated the data prior to running the tests
        :return:
        """
        super(VizTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)

        self.boxplot_dir = os.path.join(os.path.dirname(
                                  self.model.copasi_file), 'Boxplots')

        self.histogram_dir = os.path.join(os.path.dirname(
                                  self.model.copasi_file), 'Histograms')

        self.scatter_dir = os.path.join(os.path.dirname(
                                  self.model.copasi_file), 'scatter_dirs')

        self.linregress_dir = os.path.join(os.path.dirname(
                                  self.model.copasi_file), 'LinearRegression')

        self.pca_dir = os.path.join(os.path.dirname(
                                  self.model.copasi_file), 'PCA')

        self.model_selection_dir = os.path.join(os.path.dirname(
                                  self.model.copasi_file), 'ModelSelection')

        self.ensemble_tc_dir = os.path.join(os.path.dirname(
                                  self.model.copasi_file), 'EnsembleTimeCourse')

        self.rss_vs_iteration = os.path.join(os.path.dirname(
            self.model.copasi_file), 'RssVsIteration')

        self.data = pandas.read_pickle(
            pycotools3.Tests.test_data.Paths().pe_results_pickle)

    def tearDown(self):
        dirs_to_delete = [self.boxplot_dir,
                          self.histogram_dir,
                          self.scatter_dir,
                          self.linregress_dir,
                          self.pca_dir,
                          self.model_selection_dir,
                          self.ensemble_tc_dir]
        for i in dirs_to_delete:
            if os.path.isdir(i):
                pass
                # shutil.rmtree(i)

class PlotParameterEstimationTests(_test_base._BaseTest):

    def setUp(self):
        super(PlotParameterEstimationTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)
        self.original_parameters = self.model.parameters

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=50, step_size=10,
                                               intervals=5, report_name='report1.txt')
        pycotools3.misc.add_noise(self.TC1.report_name)
        self.TC2 = pycotools3.tasks.TimeCourse(self.model, end=100, step_size=20,
                                               intervals=5, report_name='report2.txt')
        pycotools3.misc.add_noise(self.TC1.report_name)
        pycotools3.misc.add_noise(self.TC2.report_name)

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)

        self.PE = pycotools3.tasks.ParameterEstimation(self.model,
                                                       [self.TC1.report_name,
                                                  self.TC2.report_name],
                                                       method='genetic_algorithm',
                                                       population_size=1,
                                                       number_of_generations=1)
        # # PE = pycotools3.tasks.ParameterEstimation(model,
        # #                                          TC1.report_name,
        # #                                          method='particle_swarm',
        # #                                          swarm_size=50,
        # #                                          iteration_limit=1000)
        if os.path.isfile(self.PE.config_filename):
            os.remove(self.PE.config_filename)
        self.PE.write_config_file()
        self.PE.setup()
        # # print model.local_parameters
        self.PE.run()
        # # PE.model.open()



    def test_create_directory(self):
        """

        :return:
        """
        pl = pycotools3.viz.PlotParameterEstimation(self.PE, savefig=False)

        dire = pl.create_directories()
        for i in dire:
            self.assertTrue(os.path.isdir(dire[i]))

    def test_update_parameters(self):
        """

        :return:
        """
        pl = pycotools3.viz.PlotParameterEstimation(self.PE, savefig=False)
        model = pl.update_parameters()
        lo = '(ADeg).k1'
        met = 'A'
        gl = 'B2C'
        self.assertNotEqual(self.original_parameters[lo].iloc[0], model.parameters[lo].iloc[0])
        self.assertNotEqual(self.original_parameters[gl].iloc[0], model.parameters[gl].iloc[0])
        self.assertNotEqual(self.original_parameters[met].iloc[0], model.parameters[met].iloc[0])


    def test_plot(self):
        """
        test plots are being generated in correct place
        :return:
        """
        pl = pycotools3.viz.PlotParameterEstimation(self.PE,
                                                    savefig=True,
                                                    show=False)
        pl.plot()
        for i in pl.create_directories():
            self.assertEqual(len(glob.glob(pl.create_directories()[i]+'/*')), 6)


    def test_plot2(self):
        """
        test y argument works
        :return:
        """
        pl = pycotools3.viz.PlotParameterEstimation(self.PE,
                                                    savefig=True,
                                                    show=False,
                                                    y=['A', 'B'])
        pl.plot()
        for i in pl.create_directories():
            self.assertEqual(len(glob.glob(pl.create_directories()[i]+'/*')), 2)


class PlotTimeCourseTests(_test_base._BaseTest):

    def setUp(self):
        super(PlotTimeCourseTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)
        self.original_parameters = self.model.parameters

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=10, step_size=0.1,
                                               intervals=50, report_name='report1.txt')


    def test_plot_tc(self):
        T = pycotools3.viz.PlotTimeCourse(self.TC1, savefig=True)
        self.assertEqual(len(glob.glob(T.results_directory+'/*')), 7)

    def test_plot_tc(self):
        T = pycotools3.viz.PlotTimeCourse(self.TC1, savefig=True, y=['A', 'B'], x='A', show=False)
        self.assertEqual(len(glob.glob(T.results_directory+'/*')), 2)


class BoxPlotTests(_test_base._BaseTest):
    def setUp(self):
        super(BoxPlotTests, self).setUp()


        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=50, step_size=10,
                                               intervals=5, report_name='report1.txt')
        pycotools3.misc.add_noise(self.TC1.report_name)
        self.TC2 = pycotools3.tasks.TimeCourse(self.model, end=100, step_size=20,
                                               intervals=5, report_name='report2.txt')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)

        self.MPE = pycotools3.tasks.MultiParameterEstimation(self.model,
                                                             [self.TC1.report_name,
                                                        self.TC2.report_name],
                                                             copy_number=2,
                                                             pe_number=2,
                                                             method='genetic_algorithm',
                                                             population_size=1,
                                                             number_of_generations=1)
        # if os.path.isfile(self.MPE.config_filename):
        #     os.remove(self.MPE.config_filename)
        self.MPE.write_config_file()
        self.MPE.setup()
        self.MPE.run()

    def test_boxplot_is_saved(self):
        """

        :return:
        """
        b = pycotools3.viz.Boxplots(self.MPE, savefig=True, num_per_plot=3)
        self.assertEqual(len(glob.glob(b.results_directory+'/*')), 3)

    def test_amount_of_data(self):
        """

        :return:
        """
        b = pycotools3.viz.Boxplots(self.MPE, savefig=True, num_per_plot=3)
        self.assertEqual(b.data.shape[0], 4)



class EnsembleTimeCourseTests(_test_base._BaseTest):

    def setUp(self):
        super(EnsembleTimeCourseTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)
        self.original_parameters = self.model.parameters


class PlotPLTests(_test_base._BaseTest):
    def setUp(self):
        super(PlotPLTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)

        ## simulate time course
        tc = pycotools3.tasks.TimeCourse(self.model, end=1000, intervals=1000, step_size=1)

        ## format time course for parameter estimation
        pycotools3.misc.format_timecourse_data(tc.report_name)

        ## get the paramete pickle filename
        pe_data_file = os.path.join(self.model.root, 'test_profile_likleihood.pickle')

        ##try and get data from parameter pickle.
        ## if you can get the df, if not simulate the data
        try:
            PE = pycotools3.tasks.MultiParameterEstimation(
                self.model, tc.report_name, metabolites=[],
                lower_bound=0.1, upper_bound=100, method='genetic_algorithm',
                copy_number=1, pe_number=10, number_of_generations=1,
                population_size=1, overwrite_config_file=True,
            )
            PE.write_config_file()
            PE.setup()
            df = pandas.read_pickle(pe_data_file)
        except IOError:
            PE = pycotools3.tasks.MultiParameterEstimation(
                self.model, tc.report_name, metabolites=[],
                lower_bound=0.1, upper_bound=100, method='genetic_algorithm',
                copy_number=5, pe_number=10, number_of_generations=1,
                population_size=1, overwrite_config_file=True
            )
            PE.write_config_file()
            PE.setup()
            PE.run()
            time.sleep(10)
            p = pycotools3.viz.Parse(PE)

            ##write pickle
            p.data.to_pickle(pe_data_file)
            df = pandas.read_pickle(pe_data_file)

        ## try read the profile likelihood data
        ## if fail with input error, simulate profile likelihood data
        try:
            self.PL = pycotools3.tasks.ProfileLikelihood(
                self.model, df=df, index=[0, 1],
                lower_bound_multiplier=1001,
                log10=True, run=False, tolerance=1e-1,
                iteration_limit=1
            )
            p = pycotools3.viz.Parse(self.PL)

        except pycotools3.errors.InputError:
            self.PL = pycotools3.tasks.ProfileLikelihood(
                self.model, df=df, index=[0, 1],
                lower_bound_multiplier=1001,
                log10=True, run='multiprocess', tolerance=1e-1,
                iteration_limit=1, intervals=4,
            )
            time.sleep(100)
            p = pycotools3.viz.Parse(self.PL)

    def test_parse(self):
        p = pycotools3.viz.Parse(self.PL)
        self.assertTrue(isinstance(p.data, pandas.core.frame.DataFrame))

    def test_parse_pl_log_linear(self):
        p = pycotools3.viz.Parse(self.PL)
        linear_scale_value = p.data.loc['B2C']['RSS'].iloc[0]
        log_scale = numpy.log10(linear_scale_value)
        p2 = pycotools3.viz.Parse(self.PL, log10=True)

        self.assertEqual(log_scale, p2.data.loc['B2C']['RSS'].iloc[0])

#


if __name__ == '__main__':
    unittest.main()

















