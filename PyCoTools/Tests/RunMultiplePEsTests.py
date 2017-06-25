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
import pickle
import re
import shutil
import scipy
import Testmodels
import lxml.etree as etree
import shutil
import logging
<<<<<<< HEAD

LOG = logging.getLogger()


=======
import pickle
import time
<<<<<<< HEAD
>>>>>>> origin/CopasiVersion19
MODEL_STRING = TestModels.TestModels.get_model1()
LOG = logging.getLogger(__name__)
=======
MODEL_STRING = Testmodels.Testmodels.get_model1()
LOG = logging.getlog10ger(__name__)
>>>>>>> 7759ebc9c3b0729eee95d01e8a6cddf4a1d82926

class runMultiplePESetUp(unittest.TestCase):
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
                                              report_name=self.timecourse_report1,
                                              plot='false')

        self.TC2 = PyCoTools.pycopi.TimeCourse(self.copasi_file,
                                              End=1000,
                                              Intervals=10,
                                              StepSize=100,
                                              report_name=self.timecourse_report2,
                                              plot='false')
        self.experiment_files=[self.timecourse_report1, self.timecourse_report2]

<<<<<<< HEAD
        self.options = {'Run': 'multiprocess',
                       'OutputDir': None,
                       'CopyNumber': 0,
                       'NumberOfPEs': 3,
                       'ReportName': None,
                       'Metabolites': self.GMQ.get_metabolites().keys(),
                       'GlobalQuantities': self.GMQ.get_global_quantities().keys(),
=======
        self.options = {'run': 'multiprocess',
                       'output_dir': None,
                       'copy_number': 2,
                       'pe_number': 3,
                       'report_name': None,
                       'metabolites': self.GMQ.get_metabolites().keys(),
                       'global_quantities': self.GMQ.get_global_quantities().keys(),
>>>>>>> 7759ebc9c3b0729eee95d01e8a6cddf4a1d82926
                       'LocalParameters': self.GMQ.get_local_kinetic_parameters_cns().keys(),
                       'quantity_type': 'concentration',
                       'append': 'false',
                       'SetReport': 'true',
                       'confirm_overwrite': 'false',
                       'config_filename': None,
                       'overwrite_config_file': 'false',
                       'prune_headers': 'true',
                       'update_model': 'false',
                       'randomize_start_values': 'true',
                       'create_parameter_sets': 'false',
                       'calculate_statistics': 'false',
                       'use_config_start_values': 'false',
                       'method': 'GeneticAlgorithm',
                       'number_of_generations': 200,
                       'population_size': 50,
                       'random_number_generator': 1,
                       'seed': 0,
                       'pf': 0.475,
                       'iteration_limit': 50,
                       'tolerance': 0.00001,
                       'rho': 0.2,
                       'scale': 10,
                       'swarm_size': 50,
                       'std_deviation': 0.000001,
                       'number_of_iterations': 100000,
                       'start_temperature': 1,
                       'cooling_factor': 0.85,
                       'row_orientation': ['true'] * len(self.experiment_files),
                       'experiment_type': ['timecourse'] * len(self.experiment_files),
                       'first_row': [str(1)] * len(self.experiment_files),
                       'normalize_weights_per_experiment': ['true'] * len(self.experiment_files),
                       'row_containing_names': [str(1)] * len(self.experiment_files),
                       'separator': ['\t'] * len(self.experiment_files),
                       'Weightmethod': ['mean_squared'] * len(self.experiment_files),
                       'save': 'overwrite',
                       'scheduled': 'false',
                       'Verbose': 'false',
                       'lower_bound': 0.000001,
                       'upper_bound': 1000000,
                       'plot': 'false',
                       'font_size': 22,
                       'axis_size': 15,
                       'extra_title': None,
                       'line_width': 3,
                       'show': 'false',
                       'savefig': 'false',
                       'title_wrap_size': 30,
                       'ylimit': None,
                       'xlimit': None,
                       'dpi': 125,
                       'xtick_rotation': 35,
                       'marker_size': 4,
                       'legend_loc': 'best'}

        self.RMPE = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,
                                                    **self.options)

<<<<<<< HEAD

    # def tearDown(self):
    #     shutil.rmtree(self.RMPE.kwargs['OutputDir'])
    #     os.remove(self.copasi_file)
=======
#
    def tearDown(self):
<<<<<<< HEAD
        pass
        ##  not yet
        # os.remove(self.copasi_file)
        # for i in glob.glob('*.txt'):
        #     os.remove(i)
        #
        # for i in glob.glob('*.xlsx'):
        #     os.remove(i)
>>>>>>> origin/CopasiVersion19

        # for i in glob.glob('*.cps'):
        #     os.remove(i)
        #
        # for i in glob.glob('*.pickle'):
        #     os.remove(i)

        shutil.rmtree(self.RMPE.kwargs['OutputDir'])
=======
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
        # shutil.rmtree(self.RMPE.kwargs['output_dir'])
>>>>>>> 7759ebc9c3b0729eee95d01e8a6cddf4a1d82926

    def test_output_directory(self):

        self.assertTrue(os.path.isdir(self.RMPE.kwargs['output_dir']))

<<<<<<< HEAD
    def test_results_copy_copasi_pickle(self):
        with open(self.RMPE.copasi_file_pickle) as f:
            c = pickle.load(f)
        LOG.debug('pickle copasi file is: {}'.format(c))

        self.assertEqual(len(c.items()),self.RMPE.kwargs['CopyNumber'])

    # def test_results_number_of_PEs(self):
    #     df_list = []
    #     for i in glob.glob(self.RMPE.kwargs['OutputDir']):
    #         print pandas.read_csv(i,sep='\t')
        #     df_list.append(pandas.read_csv(i,sep='\t'))
        # df = pandas.concat(df_list)
        # num = self.RMPE.kwargs['CopyNumber'] * self.RMPE.kwargs['NumberOfPEs']
        # print df
        # self.assertEqual(df.shape[0],num)
=======
    def test_report_files(self):
        LOG.debug('Here are the generated report files: {}'.format(self.RMPE.report_files))
        self.assertEqual(len(self.RMPE.report_files.items()),self.RMPE.kwargs['copy_number'])

    def test_write_config_file(self):
        """
        Test that RMPE produces a config file
        :return:
        """
        LOG.info('Testing the write_config_file() method')
        self.RMPE.write_config_template()
        self.assertTrue(os.path.isfile(self.RMPE.kwargs['config_filename']))

    def test_write_config_file2(self):
        """
        test that you can change the name of the config file
        :return:
        """
        new_filename=os.path.join(os.getcwd(),'Newconfig_filename.xlsx')
        self.options.update({'config_filename':new_filename})
        self.RMPE = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        if self.RMPE.kwargs['config_filename'] != new_filename:
            LOG.critical('ConfigFilname argument was not changed. {}'.format(self.RMPE.kwargs['config_filename']))
            raise PyCoTools.Errors.InputError('config_filename argument was not changed')
        LOG.info('Testing the write_config_file() method again')
        self.RMPE.write_config_template()
        self.assertTrue(os.path.isfile(self.RMPE.kwargs['config_filename']))

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
        the code twice but change the copy_number parameter
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
        self.assertEqual(self.RMPE.kwargs['copy_number'], len(copasi_dict.items()))

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
        self.options.update({'copy_number':cp2})
        RMPE2 = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        RMPE2.write_config_template()
        RMPE2.set_up()
        with open(RMPE2.copasi_file_pickle) as f2:
            copasi_dct2 = pickle.load(f2)

        self.assertEqual(cp2,len(copasi_dct2))


    def test_run(self):
        """
        run as current solution statistics so that they run quickly
        Then use the wait for a little while
        :return:
        """
        self.options.update({'method':'CurrentSolutionStatistics',
                             'copy_number':6,
                             'randomize_start_values':'false'})
        RMPE = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        RMPE.write_config_template()
        RMPE.set_up()
        RMPE.run()
        dire = RMPE.kwargs['output_dir']
        files = glob.glob(dire+'/*.txt')
        time.sleep(5)
        LOG.debug('txt files in output_dir: {}'.format(files))
        LOG.debug('Copy Number argument: {}'.format(RMPE.kwargs['copy_number']))
        self.assertEqual(len(files), RMPE.kwargs['copy_number'])



    def test_total_number_of_PE(self):
        """
        test that the total number of PEs = copy_number*pe_number

        This test doesn't work but the behaviour is working as expected.
        Not sure why the test wont work but I thnk its something to do with
        write speed and sequentially deleting files and trying to count them.

        Not important enough to spend lots of time on.
        :return:
        """
        self.options.update({'method':'CurrentSolutionStatistics',
                             'copy_number':4,
                             'pe_number':6,
                             'randomize_start_values':'false'})
        self.RMPE = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
        self.RMPE.write_config_template()
        self.RMPE.set_up()
        self.RMPE.run()
        dire = self.RMPE.kwargs['output_dir']
        files = glob.glob(dire+'/*.txt')

        time.sleep(2)
        LOG.debug('txt files in output_dir: {}'.format(files))
        LOG.debug('Copy Number argument: {}'.format(self.RMPE.kwargs['copy_number']))
        pandas_lst =[]
        for i in files:
            LOG.debug('Reading file {}'.format(i))
            df=pandas.read_csv(i,sep='\t')
            pandas_lst.append(df)
            LOG.debug(df)
        df = pandas.concat(pandas_lst)
        LOG.debug('DataFrame after concat = {}'.format(df))
        LOG.debug('Dataframe shape after concatonation: {}'.format(df.shape))
        self.assertEqual(self.RMPE.kwargs['copy_number'] * self.RMPE.kwargs['pe_number'],
                         df.shape[0])





























>>>>>>> origin/CopasiVersion19
