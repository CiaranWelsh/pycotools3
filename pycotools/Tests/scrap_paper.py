# -*- coding: utf-8 -*-
'''
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
'''


import site
site.addsitedir(r'C:\Users\Ciaran\Documents\pycotools')
site.addsitedir(r'/home/b3053674/Documents/pycotools')

import pycotools
from pycotools.Tests import test_models
import unittest
import glob
import os
import shutil
import pandas
from pycotools.Tests import _test_base
import re
from lxml import etree
from mixin import Mixin, mixin

import contextlib


dire = r'C:\Users\Ciaran\Documents\pycotools\pycotools\Tests'
dire = r'/home/b3053674/Documents/pycotools/pycotools/Tests/'

f = os.path.join(dire, 'test_model.cps')


model = pycotools.model.Model(f)
TIMECOURSE = False
PARAMETER_ESTIMATION = False
MULTI_PARAMETER_ESTIMATION = False
SCAN = False
PROFILE_LIKELIHOOD = True


if TIMECOURSE:
    TC1 = pycotools.tasks.TimeCourse(model, end=1000, step_size=100,
                                          intervals=10, report_name='report1.txt')

    T = pycotools.viz.PlotTimeCourse(TC1, savefig=True)
    print T.plot()

if SCAN:
    ##configure time course
    # model = pycotools.tasks.TimeCourse(
    #     model,
    #     end=1000,
    #     intervals=1000,
    #     step_size=1
    # ).model

    # ##configure and run scan
    S = pycotools.tasks.Scan(model, scan_type='scan',
                             subtask='time_course', run=True)
    print S.model.open()


if PARAMETER_ESTIMATION:
    TC1 = pycotools.tasks.TimeCourse(model, end=50, step_size=10,
                                          intervals=5, report_name='report1.txt')
    pycotools.misc.add_noise(TC1.report_name)
    TC2 = pycotools.tasks.TimeCourse(model, end=100, step_size=20,
                                     intervals=5, report_name='report2.txt')
    pycotools.misc.add_noise(TC1.report_name)
    pycotools.misc.add_noise(TC2.report_name)

    pycotools.misc.correct_copasi_timecourse_headers(TC1.report_name)
    pycotools.misc.correct_copasi_timecourse_headers(TC2.report_name)



    PE = pycotools.tasks.ParameterEstimation(model,
                                             [TC1.report_name],
                                             method='genetic_algorithm',
                                             population_size=1,
                                             number_of_generations=1)
    # # PE = pycotools.tasks.ParameterEstimation(model,
    # #                                          TC1.report_name,
    # #                                          method='particle_swarm',
    # #                                          swarm_size=50,
    # #                                          iteration_limit=1000)
    if os.path.isfile(PE.config_filename):
        os.remove(PE.config_filename)
    PE.write_config_file()
    PE.setup()
    # # print model.local_parameters
    PE.run()
    # # PE.model.open()
    pl = pycotools.viz.PlotParameterEstimation(PE, savefig=True)
    print pl.savefig


if MULTI_PARAMETER_ESTIMATION:
    TC1 = pycotools.tasks.TimeCourse(model, end=50, step_size=10,
                                          intervals=5, report_name='report1.txt')
    pycotools.misc.add_noise(TC1.report_name)
    TC2 = pycotools.tasks.TimeCourse(model, end=100, step_size=20,
                                     intervals=5, report_name='report2.txt')

    pycotools.misc.correct_copasi_timecourse_headers(TC1.report_name)
    pycotools.misc.correct_copasi_timecourse_headers(TC2.report_name)



    MPE = pycotools.tasks.MultiParameterEstimation(model,
                                                   [TC1.report_name,
                                                    TC2.report_name],
                                                   copy_number=6,
                                                   pe_number=20,
                                                   method='genetic_algorithm',
                                                   population_size=1,
                                                   number_of_generations=1)
    # # PE = pycotools.tasks.ParameterEstimation(model,
    # #                                          TC1.report_name,
    # #                                          method='particle_swarm',
    # #                                          swarm_size=50,
    # #                                          iteration_limit=1000)
    MPE.write_config_file()
    MPE.setup()
    # # print model.local_parameters
    # MPE.run()
    # pycotools.viz.Parse(MPE)
    # pycotools.viz.Boxplot(MPE, savefig=True, show=True)
    # pycotools.viz.RssVsIterations(MPE, savefig=True, show=True)
    # pycotools.viz.Pca(MPE, savefig=True, show=True, by='iterations')
    # pycotools.viz.Histograms(MPE, savefig=True, show=True)
    # pycotools.viz.Scatters(MPE, savefig=True, show=False,
    #                        x=['RSS', 'A'], linestyle='o')
    # pycotools.viz.LinearRegression(MPE, savefig=True, show=True)
    pycotools.viz.EnsembleTimeCourse(MPE, savefig=True, show=True,
                                     theta=5, check_as_you_plot=False)

    # # PE.model.open()
    # pl = pycotools.viz.PlotParameterEstimation(MPE, savefig=True)
    # print pl.savefig

# pycotools.misc.correct_copasi_timecourse_headers(TC1.report_name)
# ## add some noise
# data1 = pycotools.misc.add_noise(TC1.report_name)
#
# ## remove the data
# os.remove(TC1.report_name)
#
# ## rewrite the data with noise
# data1.to_csv(TC1.report_name, sep='\t')

# MPE = pycotools.tasks.ParameterEstimation(
#     model,
#     TC1.report_name,
#     copy_number=3,
#     pe_number=8,
#     method='genetic_algorithm',
#     population_size=10,
#     number_of_generations=10,
#     results_directory='test_mpe')
#
# MPE.write_config_file()
# MPE.setup()
# MPE.run()

# p = pycotools.viz.Parse(MPE)
# print p.parse_multi_parameter_estimation()




if PROFILE_LIKELIHOOD:
    f = '/home/b3053674/Documents/pycotools/pycotools/Tests/ProfileLikelihoods/0/A.cps'
    model = pycotools.model.Model(f)
    s = pycotools.tasks.Scan(model, scan_type='scan', variable='A')
    s.model.open()










































