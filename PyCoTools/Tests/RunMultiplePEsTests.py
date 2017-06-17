# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
'''
 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.


Author:
    Ciaran Welsh
Date:
    12/03/2017

 Object:

'''

import PyCoTools
import unittest
import glob
import os
import numpy
import pandas
import time
import re
import shutil
import scipy
import TestModels
import lxml.etree as etree

MODEL_STRING = TestModels.TestModels.get_model1()


class RunMultiplePETests(unittest.TestCase):
    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, self.copasiML)

        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)

        self.timecourse_report1 = os.path.join(os.path.dirname(self.copasi_file),'TimeCourse1.txt')
        self.timecourse_report2 = os.path.join(os.path.dirname(self.copasi_file),'TimeCourse2.txt')

        self.TC1 = PyCoTools.pycopi.TimeCourse(self.copasi_file,
                                              End=1000,
                                              Intervals=10,
                                              StepSize=100,
                                              ReportName=self.timecourse_report1,
                                              Plot='false')

        self.TC2 = PyCoTools.pycopi.TimeCourse(self.copasi_file,
                                              End=1000,
                                              Intervals=10,
                                              StepSize=100,
                                              ReportName=self.timecourse_report2,
                                              Plot='false')
        self.experiment_files=[self.timecourse_report1, self.timecourse_report2]

        self.options = {'Run': 'multiprocess',
                       'OutputDir': None,
                       'CopyNumber': 1,
                       'NumberOfPEs': 3,
                       'ReportName': None,
                       'Metabolites': self.GMQ.get_metabolites().keys(),
                       'GlobalQuantities': self.GMQ.get_global_quantities().keys(),
                       'LocalParameters': self.GMQ.get_local_kinetic_parameters_cns().keys(),
                       'QuantityType': 'concentration',
                       'Append': 'false',
                       'SetReport': 'true',
                       'ConfirmOverwrite': 'false',
                       'ConfigFilename': None,
                       'OverwriteConfigFile': 'false',
                       'PruneHeaders': 'true',
                       'UpdateModel': 'false',
                       'RandomizeStartValues': 'true',
                       'CreateParameterSets': 'false',
                       'CalculateStatistics': 'false',
                       'UseTemplateStartValues': 'false',
                       'Method': 'GeneticAlgorithm',
                       'NumberOfGenerations': 200,
                       'PopulationSize': 50,
                       'RandomNumberGenerator': 1,
                       'Seed': 0,
                       'Pf': 0.475,
                       'IterationLimit': 50,
                       'Tolerance': 0.00001,
                       'Rho': 0.2,
                       'Scale': 10,
                       'SwarmSize': 50,
                       'StdDeviation': 0.000001,
                       'NumberOfIterations': 100000,
                       'StartTemperature': 1,
                       'CoolingFactor': 0.85,
                       'RowOrientation': ['true'] * len(self.experiment_files),
                       'ExperimentType': ['timecourse'] * len(self.experiment_files),
                       'FirstRow': [str(1)] * len(self.experiment_files),
                       'NormalizeWeightsPerExperiment': ['true'] * len(self.experiment_files),
                       'RowContainingNames': [str(1)] * len(self.experiment_files),
                       'Separator': ['\t'] * len(self.experiment_files),
                       'WeightMethod': ['mean_squared'] * len(self.experiment_files),
                       'Save': 'overwrite',
                       'Scheduled': 'false',
                       'Verbose': 'false',
                       'LowerBound': 0.000001,
                       'UpperBound': 1000000,
                       'Plot': 'false',
                       'FontSize': 22,
                       'AxisSize': 15,
                       'ExtraTitle': None,
                       'LineWidth': 3,
                       'Show': 'false',
                       'SaveFig': 'false',
                       'TitleWrapSize': 30,
                       'Ylimit': None,
                       'Xlimit': None,
                       'DPI': 125,
                       'XTickRotation': 35,
                       'DotSize': 4,
                       'LegendLoc': 'best'}


    def test_timecourse_prodution(self):
        """

        :return:
        """
        self.assertTrue(os.path.isfile(self.timecourse_report1))

    def test_default_parameters(self):
        RMPE = PyCoTools.pycopi.RunMultiplePEs(self.copasi_file,self.experiment_files,
                                               **self.options)
        RMPE.write_config_template()
        RMPE.set_up()
        RMPE.run()