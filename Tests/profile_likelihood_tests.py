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

from pycotools3 import viz, tasks, model
from Tests import _test_base
import unittest
import os
import glob


## todo update profile likelihood test model
class ProfileLikelihoodTests(_test_base._BaseTest):

    def setUp(self):
        super(ProfileLikelihoodTests, self).setUp()
        self.fname = os.path.join(os.path.dirname(__file__), 'timecourse.txt')
        self.data = self.model.simulate(0, 10, 1, report_name=self.fname)

        with tasks.ParameterEstimation.Context(
                self.model, self.fname, context='s', parameters='g'
        ) as context:
            context.set('method', 'hooke_jeeves')
            context.set('run_mode', True)
            context.set('randomize_start_values', True)
            context.set('update_model', False)
            context.set('iteration_limit', 5)
            config = context.get_config()
        self.pe = tasks.ParameterEstimation(config)
        data = viz.Parse(self.pe).data
        self.pe_mod = self.pe.models['test_model'].model
        self.pe_mod.insert_parameters(df=data, index=0, inplace=True)

    def test_run(self):
        """
        Returns:

        """
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'nl2sol')
            context.set('run_mode', True)
            context.set('pe_number', 12)
            config = context.get_config()
        pe = tasks.ParameterEstimation(config)
        expected = 12
        data = viz.Parse(pe)['A2B']
        print(data)
        actual = data.shape[0]
        self.assertEqual(expected, actual)

    def test_run_parallel(self):
        """
        Returns:

        """
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'nl2sol')
            context.set('run_mode', 'parallel')
            context.set('nproc', 2)
            context.set('pe_number', 12)
            config = context.get_config()
        pe = tasks.ParameterEstimation(config)
        import time
        time.sleep(5)
        expected = 12
        data = viz.Parse(pe)['A2B']
        actual = data.shape[0]
        self.assertEqual(expected, actual)

    def test_parse(self):
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'hooke_jeeves')
            context.set('tolerance', 1e-1)
            context.set('iteration_limit', 5)
            context.set('run_mode', True)
            context.set('pe_number', 10)
            config = context.get_config()
        pe = tasks.ParameterEstimation(config)
        data = viz.Parse(pe).data
        print(data)

    def test_get_best_parameter_set(self):
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'nl2sol')
            context.set('tolerance', 1e-1)
            context.set('iteration_limit', 5)
            context.set('run_mode', True)
            context.set('pe_number', 10)
            config = context.get_config()
        pl = tasks.ParameterEstimation(config)
        data = viz.Parse(pl).data
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl)
        print(p.get_best_original_parameter_set())

    def test_compute_x_even(self):
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'nl2sol')
            context.set('tolerance', 1e-1)
            context.set('iteration_limit', 5)
            context.set('run_mode', True)
            context.set('pe_number', 10)
            config = context.get_config()
        pl = tasks.ParameterEstimation(config)
        data = viz.Parse(pl).data
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl)
        print(p.compute_x())
        # p.plot1('A2B', best_rss=1.2)
        # print(p.plot(x='ADeg_k1'))

    def test_compute_x_odd(self):
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'nl2sol')
            context.set('tolerance', 1e-1)
            context.set('iteration_limit', 5)
            context.set('run_mode', True)
            context.set('pe_number', 10)
            config = context.get_config()
        pl = tasks.ParameterEstimation(config)
        data = viz.Parse(pl).data
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl)
        print(p.compute_x())
        # p.plot1('A2B', best_rss=1.2)
        # print(p.plot(x='ADeg_k1'))

    def test_compute_plot(self):
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'nl2sol')
            context.set('tolerance', 1e-1)
            context.set('iteration_limit', 5)
            context.set('run_mode', True)
            context.set('pe_number', 10)
            config = context.get_config()
        pl = tasks.ParameterEstimation(config)
        data = viz.Parse(pl).data
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl)
        print(p.compute_x())
        # p.plot1('A2B', best_rss=1.2)
        # print(p.plot(x='ADeg_k1'))

    def test(self):
        pass




if __name__ == '__main__':
    unittest.main()
