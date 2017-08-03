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

    def test_total_number_of_PE(self):
        """
        test that the total number of PEs = copy_number*pe_number
        :return:
        """
        self.assertEqual(self.data.shape[0], self.RMPE['copy_number']*self.RMPE['pe_number'] )


if __name__=='__main__':
    unittest.main()




