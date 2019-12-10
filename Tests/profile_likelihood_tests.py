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
            config = context.get_config()
        self.pe = tasks.ParameterEstimation(config)
        data = viz.Parse(self.pe).data
        self.rss = data.loc[0, 'RSS']
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
        data = viz.Parse(pe).data['A2B']
        expected = (10, 5)
        actual = data.shape
        self.assertEqual(expected, actual)

    def test_compute_x(self):
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
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl, 1.2)
        x = p.compute_x()
        expected = (10, 5)
        actual = x.shape
        self.assertEqual(expected, actual)

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
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl, 1.2)
        print(p.compute_x())
        # p.plot1('A2B', best_rss=1.2)
        # print(p.plot(x='ADeg_k1'))

    def test_get_experiment_filenames(self):
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
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl, 1.2)
        actual = p.get_experiment_files()
        expected = {'timecourse': self.fname}
        self.assertEqual(expected, actual)

    def test_dof(self):
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
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl, 1.2)
        expected = 4
        actual = p.dof()
        self.assertEqual(expected, actual)

    def test_num_data_points(self):
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
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl, 1.2)
        expected = 99
        actual = p.num_data_points()
        self.assertEqual(expected, actual)

    def test_compute_plot3(self):
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
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl, self.rss)
        filename = os.path.join(os.path.dirname(__file__), 'plt.png')
        p.plot(x='all', y='C2A_k1', ncol=2,
               savefig=False, filename=filename)
        self.assertTrue(os.path.isfile(filename))


## todo update profile likelihood test model
class ProfileLikelihoodTests(unittest.TestCase):

    def setUp(self):
        super(ProfileLikelihoodTests, self).setUp()
        ant_str = """
        model new_model
            R1: A -> B ; _k1*A;
            R2: B -> A; k2*B;
            R3: C -> D; _k3*C*B;
            R4: D -> C; k4*D;
            
            A = 100;
            B = 0;
            _k1=0.1;
            k2 = 0.01
            _k3 = 0.01
            k4 = 1
        end
        """
        self.copasi_file = os.path.join(os.path.dirname(__file__), 'test_model.cps')
        self.model = model.loada(ant_str, self.copasi_file)
        self.fname = os.path.join(os.path.dirname(__file__), 'timecourse.txt')
        self.data = self.model.simulate(0, 10, 1, report_name=self.fname)

        with tasks.ParameterEstimation.Context(
                self.model, self.fname, context='s', parameters='g'
        ) as context:
            context.set('method', 'hooke_jeeves')
            context.set('run_mode', True)
            context.set('prefix', '_')
            context.set('randomize_start_values', True)
            config = context.get_config()
        self.pe = tasks.ParameterEstimation(config)
        data = viz.Parse(self.pe).data['test_model']
        self.rss = data.loc[0, 'RSS']
        self.pe_mod = self.pe.models['test_model'].model
        self.pe_mod.insert_parameters(df=data, index=0, inplace=True)

    def test_plotcl(self):
        with tasks.ParameterEstimation.Context(
                self.pe_mod, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'hooke_jeeves')
            context.set('run_mode', True)
            context.set('pe_number', 10)
            context.set('prefix', '_')
            context.set('nproc', 5)
            config = context.get_config()
        pl = tasks.ParameterEstimation(config)
        p = viz.PlotProfileLikelihoods(self.pe_mod, pl, self.rss)
        filename = os.path.join(os.path.dirname(__file__), 'plt.png')
        p.plot(x='all', y='RSS', ncol=2,
               filename=None)
        self.assertTrue(os.path.isfile(filename))


if __name__ == '__main__':
    unittest.main()
