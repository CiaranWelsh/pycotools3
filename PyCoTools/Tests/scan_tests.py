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
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil 
import pandas
from PyCoTools.Tests import _test_base
import re



class ScanTests(_test_base._BaseTest):
    def setUp(self):
        super(ScanTests, self).setUp()
        
        self.scan_options={#report variables
                 'subtask':'parameter_estimation',
                 'report_type':'time_course',
                 'number_of_steps':10,
                 'maximum':300,
                 'minimum':45,
                 'log10':False,
                 'distribution_type':'normal',
                 'scan_type':'scan',
                 'variable':self.GMQ.get_IC_cns().keys()[0],
                 'scheduled':False,
                 'clear_scans':False,
                 'run':False,
                 'update_model':False,
                 'append':False}
#                                      

        
        
        

    def test_set_scan_options_scheduled(self):
        '''
        Test setting up the scan options: scheduled
        '''
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i.attrib['scheduled'],'false')
#
    def test_report_type_timecourse(self):
        '''
        Test setting up the scan options: scheduled
        '''
        self.scan_options.update({'report_type':'time_course'})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        for i in S.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name']=='time-course':
                self.assertEqual(self.scan_options['report_type'],i.attrib['name'])

    def test_report_type_pl(self):
        '''
        '''
        self.scan_options.update({'report_type':'profilelikelihood'})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        for i in S.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name']=='profilelikelihood':
                self.assertEqual(self.scan_options['report_type'],i.attrib['name'])

    def test_report_type_profilelikelihood(self):
        '''
        Test setting up the scan options: scheduled
        '''
        self.scan_options.update({'report_type':'parameter_estimation'})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        for i in S.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name']=='parameter_estimation':
                self.assertEqual(self.scan_options['report_type'],i.attrib['name'])

    def test_set_scan_options_update_model(self):
        '''
        Test setting up the scan for profile likelihood
        '''
        self.scan_options.update({'update_model':True})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i.attrib['updateModel'],'true')

    def test_set_scan_options_append(self):
        '''
        Test setting up the scan for profile likelihood
        '''
        self.scan_options.update({'append':True})

        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['append'],'true')
               
    def test_set_scan_options_confirm_overwrite(self):
        '''
        Test setting up the scan for profile likelihood
        '''
        self.scan_options.update({'confirm_overwrite':True})

        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['confirmOverwrite'],'true')
#       

    def test_set_up_scan_number_of_steps(self):
        self.scan_options['scan_type']='scan'
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Number of steps':
                        self.assertEqual(k.attrib['value'],str(self.scan_options['number_of_steps']))

    def test_set_up_scan_type(self):
#        print self.scan_options['scan_type']
        S=PyCoTools.pycopi.Scan(self.copasi_file,scan_type='scan')
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Type':
                        self.assertEqual(k.attrib['value'],S.kwargs.get('scan_type'))
#
    def test_set_up_repeat(self):
        self.scan_options['scan_type']='repeat'
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Type':
                        self.assertEqual(k.attrib['value'],S.kwargs.get('scan_type'))


    def test_set_up_random_sampling(self):
        self.scan_options['scan_type']='random_sampling'
        self.scan_options['distribution_type']='gamma'        
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Distribution type':
                        self.assertEqual(k.attrib['value'],S.kwargs.get('distribution_type'))




    def test_set_up_scan_variable_global(self):
        self.scan_options['scan_type']='scan'
        if len(self.GMQ.get_global_quantities().keys())==0:
            return 'no global quantities in your model. Test cannot be run'
        self.scan_options['variable']=self.GMQ.get_global_quantities().keys()[0]
        S=PyCoTools.pycopi.Scan(self.copasi_file,scan_type='scan',variable=self.GMQ.get_global_quantities_cns().keys()[0])
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Object':
                        match=re.findall('.*Values\[(.*)\]',k.attrib['value'])[0]
                        self.assertEqual(match,S.kwargs.get('variable'))
                        

    def test_set_up_scan_variable_metabolites(self):
        self.scan_options['scan_type']='scan'
        if len(self.GMQ.get_IC_cns().keys())==0:
            return 'no metabolites in your model. Test cannot be run'
        self.scan_options['variable']=self.GMQ.get_IC_cns().keys()[0]
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Object':
                        match=re.findall('.*Metabolites\[(.*)\]',k.attrib['value'])[0]
                        self.assertEqual(match,S.kwargs.get('variable'))


    def test_set_up_scan_variable_local_parameter(self):
        self.scan_options['scan_type']='scan'
        if len(self.GMQ.get_local_parameters())==0:
            return 'no reactions in your model. Test cannot be run'
        self.scan_options['variable']=self.GMQ.get_local_parameters().keys()[0]
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Object':
                        match=re.findall('.*Reactions\[(.*)\].*Parameter=(.*),',k.attrib['value'])[0]
                        match='({}).{}'.format(match[0],match[1])
                        self.assertEqual(match,S.kwargs.get('variable'))
















#
#MODEL_STRING = Testmodels.Testmodels.get_model1()
#
#class TimeCourseTests(unittest.TestCase):
#
#    def setUp(self):
#        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
#        S.copasiML = etree.fromstring(MODEL_STRING)
#        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, S.copasiML)
#     
#
#class ScanTests(unittest.TestCase):
#    def setUp(self):
#        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
#        S.copasiML = etree.fromstring(MODEL_STRING)
#        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, S.copasiML)
#            
#
#        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#            
#        self.scan_options={#report variables
#                 'subtask':'parameter_estimation',
#                 'report_type':'time_course',
#                 'number_of_steps':10,
#                 'maximum':300,
#                 'minimum':45,
#                 'log10':'false',
#                 'distribution_type':'normal',
#                 'scan_type':'scan',
#                 #scan object specific (for scan and random_sampling scan_types)
#                 'variable':self.GMQ.get_metabolites().keys()[0],
#                 'scheduled':'false',
#                 'save':'overwrite',
#                 'clear_scans':'false',#if true, will remove all scans present then add new scan
#                 'run':'false'}
#                                  
#    def test_set_scan_options_scheduled(self):
#        '''
#        Test setting up the scan options: scheduled
#        '''
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="Scan"]'
#        for i in S.copasiML.xpath(query):
#            self.assertEqual(i.attrib['scheduled'],self.scan_options.get('scheduled'))
#
#    def test_report_type_timecourse(self):
#        '''
#        Test setting up the scan options: scheduled
#        '''
#        self.scan_options.update({'report_type':'time_course'})
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        for i in S.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
#            if i.attrib['name']=='time-course':
#                self.assertEqual(self.scan_options['report_type'],i.attrib['name'])
#
#    def test_report_type_pl(self):
#        '''
#        '''
#        self.scan_options.update({'report_type':'profilelikelihood'})
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        for i in S.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
#            if i.attrib['name']=='profilelikelihood':
#                self.assertEqual(self.scan_options['report_type'],i.attrib['name'])
#
#    def test_report_type_profilelikelihood(self):
#        '''
#        Test setting up the scan options: scheduled
#        '''
#        self.scan_options.update({'report_type':'parameter_estimation'})
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        for i in S.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
#            if i.attrib['name']=='parameter_estimation':
#                self.assertEqual(self.scan_options['report_type'],i.attrib['name'])
#
#    def test_set_scan_options_update_model(self):
#        '''
#        Test setting up the scan for profile likelihood
#        '''
#        self.scan_options.update({'update_model':'true'})
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="Scan"]'
#        for i in S.copasiML.xpath(query):
#            self.assertEqual(i.attrib['updatemodel'],self.scan_options.get('update_model'))
#
#    def test_set_scan_options_append(self):
#        '''
#        Test setting up the scan for profile likelihood
#        '''
#        self.scan_options.update({'append':'true'})
#
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="Scan"]'
#        for i in S.copasiML.xpath(query):
#            self.assertEqual(i[0].attrib['append'],self.scan_options.get('append'))
#               
#    def test_set_scan_options_confirm_overwrite(self):
#        '''
#        Test setting up the scan for profile likelihood
#        '''
#        self.scan_options.update({'confirm_overwrite':'true'})
#
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="Scan"]'
#        for i in S.copasiML.xpath(query):
#            self.assertEqual(i[0].attrib['confirmOverwrite'],self.scan_options.get('confirm_overwrite'))
#       
#
#    def test_set_up_scan_number_of_steps(self):
#        self.scan_options['scan_type']='scan'
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="ScanItems"]'
#        for i in S.copasiML.xpath(query):
#            for j in list(i):
#                for k in list(j):
#                    if k.attrib['name']=='Number of steps':
#                        self.assertEqual(k.attrib['value'],str(self.scan_options['number_of_steps']))
#
#    def test_set_up_scan_type(self):
##        print self.scan_options['scan_type']
#        S=PyCoTools.pycopi.Scan(self.copasi_file,scan_type='scan')
#        query='//*[@name="ScanItems"]'
#        for i in S.copasiML.xpath(query):
#            for j in list(i):
#                for k in list(j):
#                    if k.attrib['name']=='Type':
#                        self.assertEqual(k.attrib['value'],S.kwargs.get('scan_type'))
#
#    def test_set_up_repeat(self):
#        self.scan_options['scan_type']='repeat'
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="ScanItems"]'
#        for i in S.copasiML.xpath(query):
#            for j in list(i):
#                for k in list(j):
#                    if k.attrib['name']=='Type':
#                        self.assertEqual(k.attrib['value'],S.kwargs.get('scan_type'))
#
#
#    def test_set_up_random_sampling(self):
#        self.scan_options['scan_type']='random_sampling'
#        self.scan_options['distribution_type']='gamma'        
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="ScanItems"]'
#        for i in S.copasiML.xpath(query):
#            for j in list(i):
#                for k in list(j):
#                    if k.attrib['name']=='Distribution type':
#                        self.assertEqual(k.attrib['value'],S.kwargs.get('distribution_type'))
#
#
#
#
#    def test_set_up_scan_variable_global(self):
#        self.scan_options['scan_type']='scan'
#        if len(self.GMQ.get_global_quantities().keys())==0:
#            return 'no global quantities in your model. Test cannot be run'
#        self.scan_options['variable']=self.GMQ.get_global_quantities().keys()[0]
#        S=PyCoTools.pycopi.Scan(self.copasi_file,scan_type='scan',variable=self.GMQ.get_global_quantities_cns().keys()[0])
#        query='//*[@name="ScanItems"]'
#        for i in S.copasiML.xpath(query):
#            for j in list(i):
#                for k in list(j):
#                    if k.attrib['name']=='Object':
#                        match=re.findall('.*Values\[(.*)\]',k.attrib['value'])[0]
#                        self.assertEqual(match,S.kwargs.get('variable'))
#                        
#
#    def test_set_up_scan_variable_metabolites(self):
#        self.scan_options['scan_type']='scan'
#        if len(self.GMQ.get_metabolites().keys())==0:
#            return 'no metabolites in your model. Test cannot be run'
#        self.scan_options['variable']=self.GMQ.get_metabolites().keys()[0]
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="ScanItems"]'
#        for i in S.copasiML.xpath(query):
#            for j in list(i):
#                for k in list(j):
#                    if k.attrib['name']=='Object':
#                        match=re.findall('.*metabolites\[(.*)\]',k.attrib['value'])[0]
#                        self.assertEqual(match,S.kwargs.get('variable'))
#
#
#    def test_set_up_scan_variable_local_parameter(self):
#        self.scan_options['scan_type']='scan'
#        if len(self.GMQ.get_local_parameters())==0:
#            return 'no reactions in your model. Test cannot be run'
#        self.scan_options['variable']=self.GMQ.get_local_parameters().keys()[0]
#        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
#        query='//*[@name="ScanItems"]'
#        for i in S.copasiML.xpath(query):
#            for j in list(i):
#                for k in list(j):
#                    if k.attrib['name']=='Object':
#                        match=re.findall('.*Reactions\[(.*)\].*Parameter=(.*),',k.attrib['value'])[0]
#                        match='({}).{}'.format(match[0],match[1])
#                        self.assertEqual(match,S.kwargs.get('variable'))
#
#    def tearDown(self):
#        if os.path.isfile(self.copasi_file):
#            os.remove(self.copasi_file)
#
#            
#        for i in glob.glob('*.jpeg'):
#            os.remove(i)
#        
#        for i in glob.glob('*.txt'):
#            os.remove(i)
#            
#        for i in glob.glob('*.xlsx'):
#            os.remove(i)
#



        
if __name__=='__main__':
    unittest.main()