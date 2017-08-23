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

import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
# site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil 
import pandas
from PyCoTools.Tests import _test_base


##TODO Test that local_parameters, metabolites and global quantity argument work

class ParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationTests, self).setUp()

        self.TC1 = PyCoTools.pycopi.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        ## add some noise
        data1 = PyCoTools.Misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        self.PE = PyCoTools.pycopi.ParameterEstimation(self.model,
                                                       self.TC1.report_name,
                                                       method='genetic_algorithm',
                                                       population_size=10,
                                                       number_of_generations=10)
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

    def test_config_file(self):
        """
        A test that PE writes the config file to the
        right place
        :return:
        """
        self.PE.write_config_file()
        self.assertTrue(os.path.isfile(self.PE.config_filename))



    def test_insert_fit_items(self):
        '''
        Tests that there are the same number of rows in the template file
        as there are fit items inserted into copasi
        '''
        self.PE.write_config_file()
        self.PE.model = self.PE.remove_all_fit_items()
        self.model = self.PE.insert_all_fit_items()
        self.model.save()
        new_xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
        list_of_tasks = new_xml.find(self.list_of_tasks)
        ## [5][1][3] indexes the parameter estimation item list
        optimization_item_list = list_of_tasks[5][1][3]
        self.assertEqual(len(optimization_item_list), 9)


    def test_set_PE_method(self):
        '''
        test to see if method has been properly inserted into the copasi file
        '''
        self.PE.write_config_file()
        self.PE.setup()

        tasks=self.PE.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name']=='Parameter Estimation':
                self.assertEqual(i[-1].attrib['type'].lower(),self.PE.method.lower().replace('_',''))

    def test_run(self):
        self.PE.write_config_file()
        self.model = self.PE.setup()
        self.model.open()
        '''
        not wrk:
        <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=New Model,Vector=Reactions[C2A],ParameterGroup=Parameters,Parameter=(C2A).k1,Reference=Value"/>
        <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=New Model,Vector=Reactions[B2C],ParameterGroup=Parameters,Parameter=k2,Reference=Value"/>
        work 
                    
        '''
        # self.model = self.run()
        # self.assertTrue(os.path.isfile(self.PE.report_name))

#     def test_set_PE_options(self):
#         self.PE.write_config_file()
#         self.PE.setup()
# #
#
#         # tasks=self.PE.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')
#         # for i in tasks:
#         #     if i.attrib['name']=='Parameter Estimation':
#                 # self.assertEqual(i.attrib['scheduled'],'true')
#
#         self.model.open()
#
#     def test_results_folder(self):
#         """
#
#         """
#         self.PE.write_config_file()
#         self.PE.setup()
#         self.PE.run()
#         self.assertTrue(os.path.isdir(self.PE['results_directory']) )
        
        
if __name__=='__main__':
    unittest.main()