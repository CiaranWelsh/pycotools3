#-*-coding: utf-8 -*-
"""

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


 $Author: Ciaran Welsh

Module that tests the operations of the _Base base test

"""

import site
site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
site.addsitedir('/home/b3053674/Documents/pycotools')
import pandas
import pycotools
from pycotools.Tests import _test_base
import unittest
import os
import pickle
import test_data
import numpy
import shutil
import glob

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
        self.model = pycotools.model.Model(self.copasi_file)

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
            pycotools.Tests.test_data.Paths().pe_results_pickle)

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

# class PlotParameterEstimationTests(_test_base._BaseTest):
#
#     def setUp(self):
#         super(PlotParameterEstimationTests, self).setUp()
#         self.model = pycotools.model.Model(self.copasi_file)
#         self.original_parameters = self.model.parameters
#
#         self.TC1 = pycotools.tasks.TimeCourse(self.model, end=50, step_size=10,
#                                          intervals=5, report_name='report1.txt')
#         pycotools.misc.add_noise(self.TC1.report_name)
#         self.TC2 = pycotools.tasks.TimeCourse(self.model, end=100, step_size=20,
#                                          intervals=5, report_name='report2.txt')
#         pycotools.misc.add_noise(self.TC1.report_name)
#         pycotools.misc.add_noise(self.TC2.report_name)
#
#         pycotools.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
#         pycotools.misc.correct_copasi_timecourse_headers(self.TC2.report_name)
#
#         self.PE = pycotools.tasks.ParameterEstimation(self.model,
#                                                  [self.TC1.report_name,
#                                                   self.TC2.report_name],
#                                                  method='genetic_algorithm',
#                                                  population_size=1,
#                                                  number_of_generations=1)
#         # # PE = pycotools.tasks.ParameterEstimation(model,
#         # #                                          TC1.report_name,
#         # #                                          method='particle_swarm',
#         # #                                          swarm_size=50,
#         # #                                          iteration_limit=1000)
#         if os.path.isfile(self.PE.config_filename):
#             os.remove(self.PE.config_filename)
#         self.PE.write_config_file()
#         self.PE.setup()
#         # # print model.local_parameters
#         self.PE.run()
#         # # PE.model.open()
#
#
#
#     def test_create_directory(self):
#         """
#
#         :return:
#         """
#         pl = pycotools.viz.PlotParameterEstimation(self.PE, savefig=False)
#
#         dire = pl.create_directories()
#         for i in dire:
#             self.assertTrue(os.path.isdir(dire[i]))
#
#     def test_update_parameters(self):
#         """
#
#         :return:
#         """
#         pl = pycotools.viz.PlotParameterEstimation(self.PE, savefig=False)
#         model = pl.update_parameters()
#         lo = '(ADeg).k1'
#         met = 'A'
#         gl = 'B2C'
#         self.assertNotEqual(self.original_parameters[lo].iloc[0], model.parameters[lo].iloc[0])
#         self.assertNotEqual(self.original_parameters[gl].iloc[0], model.parameters[gl].iloc[0])
#         self.assertNotEqual(self.original_parameters[met].iloc[0], model.parameters[met].iloc[0])
#
#
#     def test_plot(self):
#         """
#         test plots are being generated in correct place
#         :return:
#         """
#         pl = pycotools.viz.PlotParameterEstimation(self.PE,
#                                                    savefig=True,
#                                                    show=False)
#         pl.plot()
#         for i in pl.create_directories():
#             self.assertEqual(len(glob.glob(pl.create_directories()[i]+'/*')), 6)
#
#
#     def test_plot2(self):
#         """
#         test y argument works
#         :return:
#         """
#         pl = pycotools.viz.PlotParameterEstimation(self.PE,
#                                                    savefig=True,
#                                                    show=False,
#                                                    y=['A', 'B'])
#         pl.plot()
#         for i in pl.create_directories():
#             self.assertEqual(len(glob.glob(pl.create_directories()[i]+'/*')), 2)


class PlotTimeCourseTests(_test_base._BaseTest):

    def setUp(self):
        super(PlotTimeCourseTests, self).setUp()
        self.model = pycotools.model.Model(self.copasi_file)
        self.original_parameters = self.model.parameters

        self.TC1 = pycotools.tasks.TimeCourse(self.model, end=10, step_size=0.1,
                                         intervals=50, report_name='report1.txt')


    def test_plot_tc(self):
        T = pycotools.viz.PlotTimeCourse(self.TC1, savefig=True)
        self.assertEqual(len(glob.glob(T.results_directory+'/*')), 7)

    def test_plot_tc(self):
        T = pycotools.viz.PlotTimeCourse(self.TC1, savefig=True, y=['A', 'B'], x='A', show=True)
        self.assertEqual(len(glob.glob(T.results_directory+'/*')), 2)




if __name__ == '__main__':
    unittest.main()

















