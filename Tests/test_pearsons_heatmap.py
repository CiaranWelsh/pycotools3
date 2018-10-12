# -*- coding: utf-8 -*-

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


Author:
    Ciaran Welsh
Date:
    12/03/2017

 Object:

"""
from pycotools import model, viz, tasks, misc
import unittest
import os

from Tests import _test_base


class PearsonsHeatMapTests(unittest.TestCase):
    def setUp(self):
        working_directory = os.path.dirname(__file__)

        copasi_file = os.path.join(working_directory, 'quick_start_model.cps')

        if os.path.isfile(copasi_file):
            os.remove(copasi_file)

        kf = 0.01
        kb = 0.1
        kcat = 0.05
        with model.Build(copasi_file) as m:
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

        michaelis_menten = model.Model(copasi_file)

        report = 'parameter_estimation_synthetic_data.txt'
        TC = tasks.TimeCourse(
            michaelis_menten, start=0, end=100, intervals=10, step_size=10, report_name=report
        )

        misc.correct_copasi_timecourse_headers(TC.report_name)

        fit1 = tasks.MultiParameterEstimation(
            michaelis_menten, TC.report_name, copy_number=2, pe_number=2,
            lower_bound=1e-3, upper_bound=5e3,
            results_directory='fit1',
            method='genetic_algorithm_sr', population_size=1, number_of_generations=1,
            overwrite_config_file=True
        )

        fit1.write_config_file()
        fit1.setup()
        fit1.run()
        self.fit1 = fit1
        self.model = michaelis_menten

        import time
        time.sleep(5)


    def test(self):
        P = viz.PearsonsCorrelation(self.fit1)
        print(P.pearsons)
        print(P.p_val)

if __name__ == '__main__':
    unittest.main()






















