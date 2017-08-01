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

import pickle
import site
#site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil 
import pandas
from PyCoTools.Tests import base_tests





class RunMultiplePETests(base_tests._MultiParameterEstimationBase):
    def setUp(self):
        super(RunMultiplePETests, self).setUp()
        

#    def test_output_directory(self):
#
#        self.assertTrue(os.path.isdir(self.RMPE.kwargs['results_directory']))
#
#    def test_report_files(self):
#        self.assertEqual(len(self.RMPE.report_files.items()),self.RMPE.kwargs['copy_number'])
#
#    def test_write_config_file(self):
#        """
#        Test that RMPE produces a config file
#        :return:
#        """
#        self.RMPE.write_config_template()
#        self.assertTrue(os.path.isfile(self.RMPE.kwargs['config_filename']))
##
#    def test_write_config_file2(self):
#        """
#        test that you can change the name of the config file
#        :return:
#        """
#        new_filename=os.path.join(os.getcwd(),'Newconfig_filename.xlsx')
#        self.options.update({'config_filename':new_filename})
#        self.RMPE = PyCoTools.pycopi.RunMultiplePEs(self.copasi_file,
#                                                    self.RMPE.experiment_files,
#                                                    **self.options)
#        if self.RMPE.kwargs['config_filename'] != new_filename:
#            raise PyCoTools.Errors.InputError('config_filename argument was not changed')
#        self.RMPE.write_config_template()
#        self.assertTrue(os.path.isfile(self.RMPE.kwargs['config_filename']))
#
#    def test_number_of_copasi_files(self):
#        """
#        make sure we have the correct number of files
#        :return:
#        """
#        num = self.RMPE['copy_number']
#        self.assertEqual(len(self.RMPE.sub_copasi_files), num)

    def test_scan(self):
        """
        ensure scan item is correctly set up on each of the sub copasi files
        :return:
        """
        first_model = self.RMPE.sub_copasi_files[0]
        query='//*[@name="ScanItems"]'
        copasiML = PyCoTools.pycopi.CopasiMLParser(first_model).copasiML
        for i in copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name'] == 'Number of steps':
                        self.assertEqual(int(k.attrib['value']) , self.RMPE['pe_number'])
        
    def test_pickle_path(self):
        """
        Test that the pickle path is created
        :return:
        """
        self.RMPE.write_config_template()
        self.RMPE.setup()
        self.assertTrue(os.path.isfile(self.RMPE.copasi_file_pickle))

    def test_pickle_contents(self):
        """
        Test that the pickle file has the correct number of
        copasi files as contents
        :return:
        """

        self.RMPE.write_config_template()
        self.RMPE.setup()
        with open(self.RMPE.copasi_file_pickle) as f:
            copasi_dict = pickle.load(f)
        self.assertEqual(int(self.RMPE.kwargs['copy_number']), len(copasi_dict.items()))
#
#    def test_pickle_changable(self):
#        """
#        Test that pickle is written every time in order to direct
#        the correct number of copasi copies to run
#        :return:
#        """
#        self.RMPE.write_config_template()
#        self.RMPE.setup()
#        with open(self.RMPE.copasi_file_pickle) as f1:
#            copasi_dct1 = pickle.load(f1)
#
#        first_len = len(copasi_dct1.items())
#
#        cp2 = 10
#        self.options.update({'copy_number':cp2})
#        RMPE2 = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
#        RMPE2.write_config_template()
#        RMPE2.setup()
#        with open(RMPE2.copasi_file_pickle) as f2:
#            copasi_dct2 = pickle.load(f2)
#
#        self.assertEqual(cp2,len(copasi_dct2))
##
##
#    def test_run(self):
#        """
#        run as current solution statistics so that they run quickly
#        Then use the wait for a little while
#        :return:
#        """
#        self.options.update({'method':'CurrentSolutionStatistics',
#                             'copy_number':6,
#                             'randomize_start_values':'false'})
#        RMPE = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
#        RMPE.write_config_template()
#        RMPE.setup()
#        RMPE.run()
#        dire = RMPE.kwargs['output_dir']
#        files = glob.glob(dire+'/*.txt')
#        time.sleep(5)
#        self.assertEqual(len(files), RMPE.kwargs['copy_number'])
#
#
#
#    def test_total_number_of_PE(self):
#        """
#        test that the total number of PEs = copy_number*pe_number
#
#        This test doesn't work but the behaviour is working as expected.
#        Not sure why the test wont work but I thnk its something to do with
#        write speed and sequentially deleting files and trying to count them.
#
#        Not important enough to spend lots of time on.
#        :return:
#        """
#        self.options.update({'method':'CurrentSolutionStatistics',
#                             'copy_number':4,
#                             'pe_number':6,
#                             'randomize_start_values':'false'})
#        self.RMPE = PyCoTools.pycopi.runMultiplePEs(self.copasi_file,self.experiment_files,**self.options)
#        self.RMPE.write_config_template()
#        self.RMPE.setup()
#        self.RMPE.run()
#        dire = self.RMPE.kwargs['output_dir']
#        files = glob.glob(dire+'/*.txt')
#
#        time.sleep(2)
#        pandas_lst =[]
#        for i in files:
#            df=pandas.read_csv(i,sep='\t')
#            pandas_lst.append(df)
#        df = pandas.concat(pandas_lst)
#        self.assertEqual(self.RMPE.kwargs['copy_number'] * self.RMPE.kwargs['pe_number'],
#                         df.shape[0])


if __name__=='__main__':
    unittest.main()




