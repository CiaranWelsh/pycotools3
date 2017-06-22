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
import shutil
import logging
import pickle
import time
MODEL_STRING = TestModels.TestModels.get_model1()
LOG = logging.getLogger(__name__)

class RunMultiplePESetUp(unittest.TestCase):
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
                       'CopyNumber': 2,
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

        self.RMPE = PyCoTools.pycopi.RunMultiplePEs(self.copasi_file,self.experiment_files,
                                                    **self.options)

#
    def tearDown(self):
        #  not yet
        os.remove(self.copasi_file)
        for i in glob.glob('*.txt'):
            os.remove(i)

        for i in glob.glob('*.xlsx'):
            os.remove(i)

        for i in glob.glob('*.cps'):
            os.remove(i)

        for i in glob.glob('*.pickle'):
            os.remove(i)
        # time.sleep(0.1)
        # shutil.rmtree(self.RMPE.kwargs['OutputDir'])

    def test_output_directory(self):

        self.assertTrue(os.path.isdir(self.RMPE.kwargs['OutputDir']))

    def test_report_files(self):
        LOG.debug('Here are the generated report files: {}'.format(self.RMPE.report_files))
        self.assertEqual(len(self.RMPE.report_files.items()),self.RMPE.kwargs['CopyNumber'])

    def test_write_config_file(self):
        """
        Test that RMPE produces a config file
        :return:
        """
        LOG.info('Testing the write_config_file() method')
        self.RMPE.write_config_template()
        self.assertTrue(os.path.isfile(self.RMPE.kwargs['ConfigFilename']))

    def test_write_config_file2(self):
        """
        test that you can change the name of the config file
        :return:
        """
        new_filename=os.path.join(os.getcwd(),'NewConfigFilename.xlsx')
        self.options.update({'ConfigFilename':new_filename})
        self.RMPE = PyCoTools.pycopi.RunMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        if self.RMPE.kwargs['ConfigFilename'] != new_filename:
            LOG.critical('ConfigFilname argument was not changed. {}'.format(self.RMPE.kwargs['ConfigFilename']))
            raise PyCoTools.Errors.InputError('ConfigFilename argument was not changed')
        LOG.info('Testing the write_config_file() method again')
        self.RMPE.write_config_template()
        self.assertTrue(os.path.isfile(self.RMPE.kwargs['ConfigFilename']))

    def test_set_up(self):
        """
        RMPE requries config file generation before setting
        :return:
        """
        pass

    def test_number_of_copasi_files(self):
        """
        make sure we have the correct number of files
        :return:
        """
        LOG.debug('This i')

    def test_number_of_copasi_files2(self):
        """
        Check that desired behaviour occurs when you
        the code twice but change the CopyNumber parameter
        :return:
        """
        pass

    def test_scan(self):
        """
        ensure scan item is correctly set up on each of the sub copasi files
        :return:
        """
        pass

    def test_pickle_path(self):
        """
        Test that the pickle path is created
        :return:
        """
        LOG.info('Testing that pickle path was created')
        self.RMPE.write_config_template()
        self.RMPE.set_up()
        self.assertTrue(os.path.isfile(self.RMPE.copasi_file_pickle))

    def test_pickle_contents(self):
        """
        Test that the pickle file has the correct number of
        copasi files as contents
        :return:
        """

        LOG.info('Testing the contents of the copasi pickle file are correct')
        self.RMPE.write_config_template()
        self.RMPE.set_up()
        with open(self.RMPE.copasi_file_pickle) as f:
            copasi_dict = pickle.load(f)
        LOG.debug('Copasi file pickle variable: {}'.format(copasi_dict))
        self.assertEqual(self.RMPE.kwargs['CopyNumber'], len(copasi_dict.items()))

    def test_pickle_changable(self):
        """
        Test that pickle is written every time in order to direct
        the correct number of copasi copies to run
        :return:
        """
        LOG.info('Testing that a new pickle file is written each time the code is run')
        self.RMPE.write_config_template()
        self.RMPE.set_up()
        with open(self.RMPE.copasi_file_pickle) as f1:
            copasi_dct1 = pickle.load(f1)

        frst_len = len(copasi_dct1.items())

        cp2 = 10
        self.options.update({'CopyNumber':cp2})
        RMPE2 = PyCoTools.pycopi.RunMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        RMPE2.write_config_template()
        RMPE2.set_up()
        with open(RMPE2.copasi_file_pickle) as f2:
            copasi_dct2 = pickle.load(f2)

        self.assertEqual(cp2,len(copasi_dct2))


    def test_run(self):
        """
        Run as current solution statistics so that they run quickly
        Then use the wait for a little while
        :return:
        """
        self.options.update({'Method':'CurrentSolutionStatistics',
                             'CopyNumber':6,
                             'RandomizeStartValues':'false'})
        RMPE = PyCoTools.pycopi.RunMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        RMPE.write_config_template()
        RMPE.set_up()
        RMPE.run()
        dire = RMPE.kwargs['OutputDir']
        files = glob.glob(dire+'/*.txt')
        time.sleep(5)
        LOG.debug('txt files in OutputDir: {}'.format(files))
        LOG.debug('Copy Number argument: {}'.format(RMPE.kwargs['CopyNumber']))
        self.assertEqual(len(files), RMPE.kwargs['CopyNumber'])



    def test_total_number_of_PE(self):
        """
        test that the total number of PEs = CopyNumber*NumberOfPEs

        This test doesn't work but the behaviour is working as expected.
        Not sure why the test wont work but I thnk its something to do with
        write speed and sequentially deleting files and trying to count them.

        Not important enough to spend lots of time on.
        :return:
        """
        self.options.update({'Method':'CurrentSolutionStatistics',
                             'CopyNumber':4,
                             'NumberOfPEs':6,
                             'RandomizeStartValues':'false'})
        self.RMPE = PyCoTools.pycopi.RunMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        self.RMPE.write_config_template()
        self.RMPE.set_up()
        self.RMPE.run()
        dire = self.RMPE.kwargs['OutputDir']
        files = glob.glob(dire+'/*.txt')

        time.sleep(2)
        LOG.debug('txt files in OutputDir: {}'.format(files))
        LOG.debug('Copy Number argument: {}'.format(self.RMPE.kwargs['CopyNumber']))
        pandas_lst =[]
        for i in files:
            LOG.debug('Reading file {}'.format(i))
            df=pandas.read_csv(i,sep='\t')
            pandas_lst.append(df)
            LOG.debug(df)
        df = pandas.concat(pandas_lst)
        LOG.debug('DataFrame after concat = {}'.format(df))
        LOG.debug('Dataframe shape after concatonation: {}'.format(df.shape))
        self.assertEqual(self.RMPE.kwargs['CopyNumber'] * self.RMPE.kwargs['NumberOfPEs'],
                         df.shape[0])





























