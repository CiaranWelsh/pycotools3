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
import re
import TestModels
import lxml.etree as etree

MODEL_STRING = TestModels.TestModels.get_model1()

class TimeCourseTests(unittest.TestCase):

    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, self.copasiML)
     

class ScanTests(unittest.TestCase):
    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        PyCoTools.pycopi.CopasiMLParser.write_copasi_file(self.copasi_file, self.copasiML)
            

        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
            
        self.scan_options={#report variables
                 'SubTask':'parameter_estimation',
                 'ReportType':'time_course',
                 'NumberOfSteps':10,
                 'Maximum':300,
                 'Minimum':45,
                 'Log':'false',
                 'DistributionType':'normal',
                 'ScanType':'scan',
                 #scan object specific (for scan and random_sampling ScanTypes)
                 'Variable':self.GMQ.get_metabolites().keys()[0],
                 'Scheduled':'false',
                 'Save':'overwrite',
                 'ClearScans':'false',#if true, will remove all scans present then add new scan
                 'Run':'false'}
                                  
    def test_set_scan_options_scheduled(self):
        '''
        Test setting up the scan options: Scheduled
        '''
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i.attrib['scheduled'],self.scan_options.get('Scheduled'))

    def test_report_type_timecourse(self):
        '''
        Test setting up the scan options: Scheduled
        '''
        self.scan_options.update({'ReportType':'time_course'})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name']=='time-course':
                self.assertEqual(self.scan_options['ReportType'],i.attrib['name'])

    def test_report_type_pl(self):
        '''
        '''
        self.scan_options.update({'ReportType':'profilelikelihood'})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name']=='profilelikelihood':
                self.assertEqual(self.scan_options['ReportType'],i.attrib['name'])

    def test_report_type_profilelikelihood(self):
        '''
        Test setting up the scan options: Scheduled
        '''
        self.scan_options.update({'ReportType':'parameter_estimation'})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name']=='parameter_estimation':
                self.assertEqual(self.scan_options['ReportType'],i.attrib['name'])

    def test_set_scan_options_update_model(self):
        '''
        Test setting up the scan for profile likelihood
        '''
        self.scan_options.update({'UpdateModel':'true'})
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i.attrib['updateModel'],self.scan_options.get('UpdateModel'))

    def test_set_scan_options_append(self):
        '''
        Test setting up the scan for profile likelihood
        '''
        self.scan_options.update({'Append':'true'})

        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['append'],self.scan_options.get('Append'))
               
    def test_set_scan_options_confirm_overwrite(self):
        '''
        Test setting up the scan for profile likelihood
        '''
        self.scan_options.update({'ConfirmOverwrite':'true'})

        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="Scan"]'
        for i in S.copasiML.xpath(query):
            self.assertEqual(i[0].attrib['confirmOverwrite'],self.scan_options.get('ConfirmOverwrite'))
       

    def test_set_up_scan_number_of_steps(self):
        self.scan_options['ScanType']='scan'
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Number of steps':
                        self.assertEqual(k.attrib['value'],str(self.scan_options['NumberOfSteps']))

    def test_set_up_scan_type(self):
#        print self.scan_options['ScanType']
        S=PyCoTools.pycopi.Scan(self.copasi_file,ScanType='scan')
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Type':
                        self.assertEqual(k.attrib['value'],S.kwargs.get('ScanType'))

    def test_set_up_repeat(self):
        self.scan_options['ScanType']='repeat'
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Type':
                        self.assertEqual(k.attrib['value'],S.kwargs.get('ScanType'))


    def test_set_up_random_sampling(self):
        self.scan_options['ScanType']='random_sampling'
        self.scan_options['DistributionType']='gamma'        
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Distribution type':
                        self.assertEqual(k.attrib['value'],S.kwargs.get('DistributionType'))




    def test_set_up_scan_variable_global(self):
        self.scan_options['ScanType']='scan'
        if len(self.GMQ.get_global_quantities().keys())==0:
            return 'no global quantities in your model. Test cannot be run'
        self.scan_options['Variable']=self.GMQ.get_global_quantities().keys()[0]
        S=PyCoTools.pycopi.Scan(self.copasi_file,ScanType='scan',Variable=self.GMQ.get_global_quantities_cns().keys()[0])
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Object':
                        match=re.findall('.*Values\[(.*)\]',k.attrib['value'])[0]
                        self.assertEqual(match,S.kwargs.get('Variable'))
                        

    def test_set_up_scan_variable_metabolites(self):
        self.scan_options['ScanType']='scan'
        if len(self.GMQ.get_metabolites().keys())==0:
            return 'no metabolites in your model. Test cannot be run'
        self.scan_options['Variable']=self.GMQ.get_metabolites().keys()[0]
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Object':
                        match=re.findall('.*Metabolites\[(.*)\]',k.attrib['value'])[0]
                        self.assertEqual(match,S.kwargs.get('Variable'))


    def test_set_up_scan_variable_local_parameter(self):
        self.scan_options['ScanType']='scan'
        if len(self.GMQ.get_local_parameters())==0:
            return 'no reactions in your model. Test cannot be run'
        self.scan_options['Variable']=self.GMQ.get_local_parameters().keys()[0]
        S=PyCoTools.pycopi.Scan(self.copasi_file,**self.scan_options)
        query='//*[@name="ScanItems"]'
        for i in S.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Object':
                        match=re.findall('.*Reactions\[(.*)\].*Parameter=(.*),',k.attrib['value'])[0]
                        match='({}).{}'.format(match[0],match[1])
                        self.assertEqual(match,S.kwargs.get('Variable'))

    def tearDown(self):
        if os.path.isfile(self.copasi_file):
            os.remove(self.copasi_file)

            
        for i in glob.glob('*.jpeg'):
            os.remove(i)
        
        for i in glob.glob('*.txt'):
            os.remove(i)
            
        for i in glob.glob('*.xlsx'):
            os.remove(i)




        
if __name__=='__main__':
    unittest.main()