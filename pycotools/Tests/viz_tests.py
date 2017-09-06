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

    def test_boxplot(self):
        """

        :return:
        """

        b= pycotools.viz.Boxplot(self.data, savefig=True,
                              results_directory=self.boxplot_dir,
                              num_per_plot=10, log10=True,
                              )
        self.assertTrue(isinstance(b.data, pandas.DataFrame))

    def test_truncate_data_mixin(self):
        """

        :return:
        """
        original_shape = self.data.shape
        new = pycotools.viz.TruncateDataMixin.truncate(self.data,
                                                       'percent',
                                                       x=50)
        self.assertEqual(new.shape[0], 30)

    def test_truncate_data_mixin2(self):
        """

        :return:
        """
        original_shape = self.data.shape
        new = pycotools.viz.TruncateDataMixin.truncate(self.data,
                                                       'below_x',
                                                       x=0.5)
        self.assertEqual(new.shape[0], 22)

    def test_rss_vs_iteration(self):

        b = pycotools.viz.RssVsIterations(
            self.data, savefig=True,
            results_directory=self.rss_vs_iteration)
        self.assertTrue(os.path.isdir(self.rss_vs_iteration))








































if __name__ == '__main__':
    unittest.main()

















