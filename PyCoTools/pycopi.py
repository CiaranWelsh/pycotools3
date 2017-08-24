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


 $Author: Ciaran Welsh
 $Date: 12-09-2016 
 Time:  13:33

'''
import time
import threading
import Queue
import shutil
import numpy 
import pandas
import scipy
import os
from lxml import etree
import logging
import os
import subprocess
import re
import pickle
import PEAnalysis,Errors, Misc, _base, model
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap
import string
import itertools
from  multiprocessing import Process
import glob
import seaborn as sns
from copy import deepcopy
from subprocess import check_call
from collections import OrderedDict




LOG=logging.getLogger(__name__)
sns.set_context(context='poster',
                font_scale=3)

## TODO change pycopi to tasks

class CopasiMLParser():

    """
    Parse a copasi file into xml.etree.
    The copasiML is availbale as the copasiML attribute.

    args:
        copasi_file:
            A full path to a copasi file


    """
    def __init__(self,copasi_file):
        self.copasi_file=copasi_file
        if os.path.isfile(self.copasi_file)!=True:
            raise Errors.FileDoesNotExistError('{} is not a copasi file'.format(self.copasi_file))
        self.copasiMLTree=self._parse_copasiML()
        self.copasiML=self.copasiMLTree.getroot()
        self.xml = self.copasiMLTree.getroot()

        os.chdir(os.path.dirname(self.copasi_file))
            
    def _parse_copasiML(self):
        '''
        Parse xml doc with lxml 
        '''
        tree= etree.parse(self.copasi_file)
        return tree

    def write_copasi_file(self,copasi_filename, xml):
        '''
        write to file with lxml write function
        '''
        #first convert the copasiML to a root element tree
        root=etree.ElementTree(xml)
        root.write(copasi_filename)
        LOG.debug('model written to {}'.format(copasi_filename))


class Run(_base._ModelBase):
    """

    """
    def __init__(self, model, **kwargs):
        """

        :param model: instance of model.Model
        :param kwargs:
        """
        super(Run, self).__init__(model, **kwargs)

        self.default_properties = {'task': 'time_course',
                                   'mode': True,
                                   'max_time': None,
                                   'copasi_file': None,
                                   'sge_job_filename': None}

        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self.do_checks()

        ##TODO check whether scheduled parameter should be 'true' or '1' format

        if self.copasi_file == None:
            self.copasi_file = self.model.copasi_file

        if self.sge_job_filename == None:
            self.SGE_job_filename = os.path.join(os.getcwd(), 'SGEJobFile.sh')

        self.model = self.set_task()
        self.model.save()
        if self.mode == True:
            try:
                self.run()
            except Errors.CopasiError:
                self.run_linux()
        elif self.mode == 'SGE':
            self.submit_copasi_job_SGE()
        elif self.mode == 'multiprocess':
            self.multi_run()


    def __str__(self):
        return 'Run({})'.format(self.to_string())

    def multi_run(self):
        def run(x):
            if os.path.isfile(x) != True:
                raise Errors.FileDoesNotExistError('{} is not a file'.format(self.copasi_file))
            subprocess.Popen(['CopasiSE', self.copasi_file])
        Process(run(self.copasi_file))

    def set_task(self):
        """

        :return:
        """
        # print self.model
        task = self.task.replace('_', '')
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            i.attrib['scheduled'] = "false"  # set all to false
            if task == i.attrib['type'].lower():
                i.attrib['scheduled'] = "true"
        return self.model

    def run(self):
        '''
        Process the copasi file using CopasiSE
        '''
        args = ['CopasiSE', "{}".format(self.copasi_file)]
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        d = {}
        d['output'] = output
        d['error'] = err
        if err != '':
            try:
                self.run_linux()
            except:
                raise Errors.CopasiError('Failed with Copasi error: \n\n' + d['error'])
        return d['output']

    def run_linux(self):
        """
        Linux systems do not respond to the run function
        in the same way as windows. This ffunction
        uses basic os.system instead, which linux systems
        do respond to. This solution is less than elegant.
        Look into it further.
        :return:
        """
        ##TODO find better solution for running copasi files on linux
        os.system('CopasiSE "{}"'.format(self.copasi_file))

    def submit_copasi_job_SGE(self):
        '''
        Submit copasi file as job to SGE based job scheduler.
        '''
        with open(self.SGE_job_file, 'w') as f:
            f.write('#!/bin/bash\n#$ -V -cwd\nmodule add apps/COPASI/4.16.104-Linux-64bit\nCopasiSE {}'.format(
                self.copasi_file))
        ## -N option for job name
        os.system('qsub {} -N {} '.format(self.SGE_job_file, self.SGE_job_file))
        ## remove .sh file after used.
        os.remove(self.SGE_job_file)

    def do_checks(self):
        """
        Varify integrity of user input
        :return:
        """
        tasks = ['steady_state', 'time_course',
                 'scan', 'flux_mode', 'optimization',
                 'parameter_estimation', 'metabolic_control_analysis',
                 'lyapunov_exponents', 'time_scale_separation_analysis',
                 'sensitivities', 'moieties', 'cross_section',
                 'linear_noise_approximation']
        if self.task not in tasks:
            raise Errors.InputError('{} not in list of tasks. List of tasks are: {}'.format(self.task, tasks))



class Reports(_base._ModelBase):
    '''
    Creates reports in copasi output specification section.
    Use:
        -the report_type kwarg to specify which type of report you want to make
        -the metabolites and global_quantities kwargs to specify which parameters
        to include



    args:
        copasi_file:
            The copasi file you want to add a report too

    **kwargs:

        report_type:
            Which report to write. Options:
                profilelikleihood:
                    - for Pydentify, shouldn't need to manually touch this
                time_course:
                    -a table of time Vs concentrations. Included values are specified to the metabolites and//or global_quantities arguments
            parameter_estimation:
                    -a table of values from a parameter estimation and the residual sum of squares value for each run.


        metabolites:
            A list of valid model metabolites you want to include in the report. Default=All metabolites

        global_quantities;
            List of valid global quantities that you want to include in the report. Default=All global variables

        quantity_type:
            Either 'concentration' or 'particle_number'. Switch between having report output in either concentration of in particle_numbers.

        report_name:
            Name of the report. Default depends on kwarg report_type

        append:
            True or False. append to report. Default False

        confirm_overwrite:
            True or False.  Default= False

        save:
            either False,'overwrite' or 'duplicate'.
            false: don't write to file
            overwrite: overwrite copasi_file
            duplicate: write a new file named using the kwarg OutputML


        variable:
            When report_type is profilelikelihood, theta is the parameter of interest

    '''
    def __init__(self, model, **kwargs):
        super(Reports, self).__init__(model, **kwargs)

        self.default_properties = {'metabolites': self.model.metabolites,
                                 'global_quantities': self.model.global_quantities,
                                 'local_parameters': self.model.local_parameters,
                                 'quantity_type': 'concentration',
                                 'report_name': None,
                                 'append': False,
                                 'confirm_overwrite': False,
                                 'separator': '\t',
                                 'update_model': False,
                                 'report_type': 'parameter_estimation',
                                 'variable': self.model.metabolites[0], #only for profile_likelihood
                                 'directory': None,
                                 }
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self._do_checks()

        # for key in self.kwargs:
        #     if key not in self.allowed_properties:
        #         raise Errors.InputError('{} not in {}'.format(key, self.allowed_properties.keys()))
        # self.update_properties(self.allowed_properties)

        self.run()

    def _do_checks(self):
        """
        Varify integrity of user input
        :return:
        """

        if isinstance(self.metabolites,str):
            self.metabolites = [self.metabolites]
        if isinstance(self.global_quantities,str):
            self.global_quantities=[self.global_quantities]

        if isinstance(self.local_parameters, str):
            self.local_parameters = [self.local_parameters]

        if self.quantity_type not in ['concentration','particle_number']:
            raise Errors.InputError('{} not concentration or particle_number'.format(self.quantity_type))

        if self.append == True:
            self.append = str(1)
        else:
            self.append = str(0)

        if self.confirm_overwrite==True:
            self.confirm_overwrite=str(1)
        else:
            self.confirm_overwrite=str(0)


        self.report_types=[None,'profilelikelihood', 'profilelikelihood2',
                           'time_course','parameter_estimation', 'multi_parameter_estimation']
        assert self.report_type in self.report_types,'valid report types include {}'.format(self.report_types)

        quantity_types=['particle_numbers','concentration']
        assert self.quantity_type in quantity_types


        if self.report_name == None:
            if self.report_type == 'profilelikelihood':
                default_report_name='profilelikelihood.txt'
            elif self.kwargs.get('report_type')=='profilelikelihood2':
                default_report_name='profilelikelihood2.txt'

            elif self.report_type == 'time_course':
                default_report_name='time_course.txt'
            elif self.report_type =='parameter_estimation':
                default_report_name = 'parameter_estimation.txt'
            elif self.report_type == 'multi_parameter_estimation':
                default_report_name = 'multi_parameter_estimation.txt'
            self.report_name = default_report_name

        # self.__dict__ = Bool2Str(self.__dict__).convert_dct()



    def __str__(self):
        return 'Report({})'.format(self.to_string())

    def timecourse(self):
        '''
        creates a report to collect time course results.

        By default all species and all global quantities are used with
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the metabolites keyword or global quantities to the
        global quantities keyword
        '''
        #get existing report keys
        keys=[]
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name']=='Time-Course':
                self.model=self.remove_report('time_course')

        new_key='Report_30'
        while new_key  in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))

        ListOfReports = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports,
                                  'Report',
                                  attrib={'precision': '6',
                                          'separator': '\t',
                                          'name': 'Time-Course',
                                          'key':new_key,
                                          'taskType': 'Time-Course'})
        comment=etree.SubElement(report, 'Comment')
        comment=comment #get rid of annoying squiggly line above
        table=etree.SubElement(report, 'Table')
        table.attrib['printTitle']=str(1)
        #Objects for the report to report
        time=etree.SubElement(table, 'Object')
        #first element always time.
        time.attrib['cn']='CN=Root,Model={},Reference=Time'.format(self.model.name)

        '''
        generate more SubElements dynamically
        '''
        #for metabolites
        if self.metabolites != None:
            for i in self.metabolites:
                if self.quantity_type == 'concentration':
                    '''
                    A coapsi 'reference' for metabolite in report
                    looks like this:
                        "CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration"
                    '''
                    # cn= self.model.metabolites[i].reference
                    # print self.model.reference
                    cn = '{},{},{}'.format(self.model.reference,
                                               i.compartment.reference,
                                               i.transient_reference)
                elif self.quantity_type == 'particle_number':
                    cn = '{},{},{}'.format(self.model.reference,
                                                                     i.compartment.reference,
                                                                     i.reference)

            #add to xml
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn

        #for global quantities
        if self.global_quantities != None:
            for i in self.global_quantities:
                """
                A Copasi 'reference' for global_quantities in report
                looks like this:
                    cn="CN=Root,Model=New Model,Vector=Values[B2C],Reference=Value"
                """
                cn = '{},{}'.format(self.model.reference, i.transient_reference)
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn
        return self.model
    #
    def profile_likelihood(self):
        '''
        Create report of a parameter and best value for a parameter estimation
        for profile likelihoods
        '''
        #get existing report keys
        keys=[]
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name']=='profilelikelihood':
                self.remove_report('profilelikelihood')

        new_key='Report_31'
        while new_key in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes = {'precision': '6',
                             'separator': '\t',
                             'name': 'profilelikelihood',
                             'key': new_key,
                             'taskType': 'Scan'}

        ListOfReports=self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)

        comment=etree.SubElement(report,'Comment')
        table=etree.SubElement(report,'Table')
        table.attrib['printTitle']=str(1)
        if self.variable.name in [i.name for i in self.metabolites]:
            cn = '{},{}'.format( self.model.reference, self.variable.initial_reference)
        elif self.variable.name in [i.name for i in self.global_quantities]:
            cn = '{},{}'.format(self.model.reference, self.variable.initial_reference)
        elif self.variable.name in [i.name for i in self.local_parameters]:
            cn = '{},{}'.format(self.model.reference, self.variable.reference)
        etree.SubElement(table,'Object',attrib={'cn': cn})
        etree.SubElement(table,'Object',attrib={'cn': "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.model


    def parameter_estimation(self):
        '''
        Define a parameter estimation report and include the progression
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords.
        '''
        #get existing report keys
        keys=[]
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name']=='parameter_estimation':
                self.model.xml = self.remove_report('parameter_estimation')

        new_key='Report_32'
        while new_key  in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes={'precision': '6',
                           'separator': '\t',
                           'name': 'parameter_estimation',
                           'key': new_key,
                           'taskType': 'parameterFitting'}

        # print self.model, type(self.model)
        ListOfReports=self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        comment=etree.SubElement(report,'Comment')
        footer=etree.SubElement(report,'Footer')
        Object=etree.SubElement(footer,'Object')
        Object.attrib['cn']="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"
        Object=etree.SubElement(footer,'Object')
        Object.attrib['cn']="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"
        LOG.debug('Reports PE setup copasiML {}'.format(self.model.xml))
        return self.model

    def multi_parameter_estimation(self):
        '''
        Define a parameter estimation report and include the progression
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords.
        '''
        #get existing report keys
        keys=[]
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name']=='multi_parameter_estimation':
                self.model.xml=self.remove_report('multi_parameter_estimation')

        new_key='Report_32'
        while new_key  in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes={'precision': '6',
                           'separator': '\t',
                           'name': 'multi_parameter_estimation',
                           'key': new_key,
                           'taskType': 'parameterFitting'}

        ListOfReports=self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        comment=etree.SubElement(report,'Comment')
        table=etree.SubElement(report,'Table')
        table.attrib['printTitle']=str(1)
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"})
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.model



    def run(self):
        '''
        Execute code that builds the report defined by the kwargs
        '''
        if self.report_type == 'parameter_estimation':
            LOG.debug('created a \'parameter_estimation\' report')
            self.model = self.parameter_estimation()

        elif self.report_type  == 'multi_parameter_estimation':
            LOG.debug('created a \'parameter_estimation\' report')
            self.model =self.multi_parameter_estimation()

        elif self.report_type == 'profilelikelihood':
            self.model = self.profile_likelihood()
            LOG.debug('created a \'profile_likelihod\' type report')

        elif self.report_type == 'time_course':
            self.model = self.timecourse()
            LOG.debug('created a \'time_course\' type report')

        elif self.report_type == None:
            self.model = self.model
            LOG.debug('created a \'none\' type report')

        return self.model

    def remove_report(self,report_name):
        """

        remove report called report_name
        :param report_name:
        :return: PyCoTools.model.Model
        """
        assert report_name in self.report_types,'{} not a valid report type. These are valid report types: {}'.format(report_name,self.report_types)
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if report_name=='time_course':
                report_name='time-course'
            if i.attrib['name'].lower() == report_name.lower():
                i.getparent().remove(i)
        return self.model


    def clear_all_reports(self):
        """
        Having multile reports defined at once can be really annoying
        and give you unexpected results. Use this function to remove all reports
        before defining a new one to ensure you only have one active report any once.
        :return:
        """
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            for j in list(i):
                if 'target' in j.attrib.keys():
                    j.attrib['target']=''
        return self.model


class Bool2Str():
    """
    copasiML expects strings and we pythoners want to use python booleans not strings
    This class quickly converts between them
    """
    def __init__(self,dct):
        self.dct = dct
        if isinstance(self.dct,dict)!=True:
            raise Errors.InputError('Input must be dict')

        self.acceptable_kwargs = ['append','confirm_overwrite','update_model',
                                  'output_in_subtask','adjust_initial_conditions',
                                  'randomize_start_values','log10','scheduled','output_event']

    def convert(self,boolean):
        if boolean == True:
            return "true"
        elif boolean == False:
            return "false"
        else:
            raise Errors.InputError('Input should be boolean not {}'.format(isinstance(boolean)))

    def convert_dct(self):
        """

        ----
        return
        """
        for kwarg in self.dct.keys():
            if kwarg in self.acceptable_kwargs:
                if self.dct[kwarg]==True:
                    self.dct.update({kwarg:"true"})
                else:
                    self.dct.update({kwarg:"false"})
#
        return self.dct


class TimeCourse(_base._ModelBase):
    """

    Change the plotting functions of time course.
    Create new class. Like viz in ecell4 for visualizing
    the data. This will give more flexibility than what we presently have.
    The idea is that user will be able to enter x or y variable,
    or multiple such variables for the y axis to plot whatever they like.
    """

    def __init__(self, model, **kwargs):
        super(TimeCourse, self).__init__(model, **kwargs)

        default_report_name = os.path.join(os.path.dirname(self.model.copasi_file), 'TimeCourseData.txt')

        self.default_properties = {'intervals': 100,
                                   'step_size': 0.01,
                                   'end': 1,
                                   'start': 0,
                                   'update_model': False,
                                   # report variables
                                   'metabolites': self.model.metabolites,
                                   'global_quantities': self.model.global_quantities,
                                   'quantity_type': 'concentration',
                                   'report_name': default_report_name,
                                   'append': False,
                                   'confirm_overwrite': False,
                                   'method': 'deterministic',
                                   'output_event': False,
                                   'scheduled': True,
                                   'automatic_step_size': False,
                                   'start_in_steady_state': False,
                                   'integrate_reduced_model': False,
                                   'relative_tolerance': 1e-6,
                                   'absolute_tolerance': 1e-12,
                                   'max_internal_steps': 10000,
                                   'max_internal_step_size': 0,
                                   'subtype': 2,
                                   'use_random_seed': True,
                                   'random_seed': 1,
                                   'epsilon': 0.001,
                                   'lower_limit': 800,
                                   'upper_limit': 1000,
                                   'partitioning_interval': 1,
                                   'runge_kutta_step_size': 0.001,
                                   'run': True,
                                   'plot': False,
                                   'correct_headers':  True,
                                   'save': False}

        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self.do_checks()

        self.set_timecourse()
        self.set_report()

        self.run_task()
        self.correct_output_headers()

        if self.save:
            self.model.save()

    def correct_output_headers(self):
        """
        Copasi writes time courses with variables
        surrounded in square brackets (i.e. [A]).
        This method removes the square brackets
        :return:
        """
        if self.correct_headers:
            df = pandas.read_csv(self.report_name, sep='\t', index_col=0)
            df.columns = [re.findall('\[(.*)\]', i)[0] for i in df.keys()]
            os.remove(self.report_name)
            df.to_csv(self.report_name, sep='\t')

    def do_checks(self):
        """
        method for checking user input
        :return: void
        """
        method_list = ['deterministic',
                       'direct',
                       'gibson_bruck',
                       'tau_leap',
                       'adaptive_tau_leap',
                       'hybrid_runge_kutta',
                       'hybrid_lsoda',
                       'hybrid_rk45']
        if self.method not in method_list:
            raise Errors.InputError('{} is not a valid method. These are valid methods {}'.format(self.method, method_list))

        if os.path.isabs(self.report_name)!=True:
            self.report_name = os.path.join(os.path.dirname(self.model.copasi_file), self.report_name)

    def __str__(self):
        return "TimeCourse({})".format(self.to_string())

    def run_task(self):
        R = Run(self.model, task='time_course')
        return R.model

    def create_task(self):
        """
        Begin creating the segment of xml needed
        for a time course. Define task and problem
        definition. This section of xml is common to all
        methods

        Should look like this:

            <Task key="Task_15" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
              <Problem>
                <Parameter name="AutomaticStepSize" type="bool" value="0"/>
                <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
                <Parameter name="StepSize" type="float" value="0.01"/>
                <Parameter name="Duration" type="float" value="1"/>
                <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
                <Parameter name="OutputStartTime" type="float" value="0"/>
                <Parameter name="Output Event" type="bool" value="0"/>
                <Parameter name="Start in Steady State" type="bool" value="0"/>
              </Problem>

        :return: lxml.etree._Element
        """

        task = etree.Element('Task', attrib={'key': 'Task_15',
                                             'name': 'Time-Course',
                                             'type': 'timeCourse',
                                             'scheduled': 'false',
                                             'update_model': 'false'})
        problem = etree.SubElement(task, 'Problem')

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'AutomaticStepSize',
                                 'type': 'bool',
                                 'value': self.automatic_step_size})

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'StepNumber',
                                 'type': 'unsignedInteger',
                                 'value': str(self.intervals)})

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'StepSize',
                                 'type': 'float',
                                 'value': str(self.step_size)})

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'Duration',
                                 'type': 'float',
                                 'value': str(self.end)})

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'TimeSeriesRequested',
                                 'type': 'float',
                                 'value': '1'})

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'OutputStartTime',
                                 'type': 'float',
                                 'value': str(self.start)})

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'Output Event',
                                 'type': 'bool',
                                 'value': self.output_event})

        etree.SubElement(problem,
                         'Parameter',
                         attrib={'name': 'Start in Steady State',
                                 'type': 'bool',
                                 'value': self.start_in_steady_state})

        return task

    def set_timecourse(self):
        """
        Set method specific sections of xml. This
        is a method element after the problem element
        that looks like this:

        :return: lxml.etree._Element
        """
        if self.method == 'deterministic':
            timecourse = self.deterministic()
        elif self.method == 'gibson_bruck':
            timecourse = self.gibson_bruck()
        elif self.method == 'direct':
            timecourse = self.direct()
        elif self.method == 'tau_leap':
            timecourse = self.tau_leap()
        elif self.method == 'adaptive_tau_leap':
            timecourse = self.adaptive_tau_leap()
        elif self.method == 'hybrid_runge_kutta':
            timecourse = self.hybrid_runge_kutta()
        elif self.method == 'hybrid_lsoda':
            timecourse = self.hybrid_lsoda()
        elif self.method == 'hybrid_rk45':
            timecourse = self.hybrid_rk45()

        list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        for task in self.model.xml.find(list_of_tasks):
            if task.attrib['name'] == 'Time-Course':
                ##remove old time course
                task.getparent().remove(task)
        ## insert new time course
        self.model.xml.find(list_of_tasks).insert(1, timecourse)
        LOG.debug('Timecourse task element is:\n\n{}'.format(etree.tostring(timecourse, pretty_print=True) ))
        return self.model

    def deterministic(self):
        """
          <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
            <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
            <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
            <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
            <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
            <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
          </Method>
        :return:lxml.etree._Element
        """
        method = etree.Element('Method', attrib={'name': 'Deterministic (LSODA)',
                                                 'type':'Deterministic(LSODA)'})

        dct = {'name': 'Integrate Reduced Model',
               'type': 'bool',
               'value': self.integrate_reduced_model}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Relative Tolerance',
               'type': 'unsignedFloat',
               'value': str(self.relative_tolerance)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Absolute Tolerance',
               'type': 'unsignedFloat',
               'value': str(self.absolute_tolerance)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Max Internal Steps',
               'type': 'unsignedInteger',
               'value': str(self.max_internal_steps)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Max Internal Step Size',
               'type': 'unsignedFloat',
               'value': str(self.max_internal_step_size)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        task = self.create_task()
        task.append(method)
        return task

    def gibson_bruck(self):
        """
          <Method name="Stochastic (Gibson + Bruck)" type="DirectMethod">
            <Parameter name="Max Internal Steps" type="integer" value="1000000"/>
            <Parameter name="Subtype" type="unsignedInteger" value="2"/>
            <Parameter name="Use Random Seed" type="bool" value="0"/>
            <Parameter name="Random Seed" type="unsignedInteger" value="1"/>
          </Method>
        </Task>
        :return:
        """
        method = etree.Element('Method', attrib={'name': 'Stochastic (Gibson + Bruck)',
                                                 'type': 'DirectMethod'})

        dct = {'name': 'Max Internal Steps',
               'type': 'unsignedInteger',
               'value': str(self.max_internal_steps)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Subtype',
               'type': 'unsignedInteger',
               'value': str(self.subtype)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Use Random Seed',
               'type': 'bool',
               'value': self.use_random_seed}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Random Seed',
               'type': 'unsignedInteger',
               'value': str(self.random_seed)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        task = self.create_task()
        task.append(method)
        return task

    def direct(self):
        """
          <Method name="Stochastic (Direct method)" type="Stochastic">
            <Parameter name="Max Internal Steps" type="integer" value="1000000"/>
            <Parameter name="Use Random Seed" type="bool" value="0"/>
            <Parameter name="Random Seed" type="unsignedInteger" value="1"/>
          </Method>
        </Task>
        :return:
        """
        method = etree.Element('Method', attrib={'name': 'Stochastic (Direct method)',
                                                 'type': 'Stochastic'})

        dct = {'name': 'Max Internal Steps',
               'type': 'unsignedInteger',
               'value': str(self.max_internal_steps)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Use Random Seed',
               'type': 'bool',
               'value': self.use_random_seed}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Random Seed',
               'type': 'unsignedInteger',
               'value': str(self.random_seed)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        task = self.create_task()
        task.append(method)
        return task

    def tau_leap(self):
        """
          <Method name="Stochastic (τ-Leap)" type="TauLeap">
            <Parameter name="Epsilon" type="float" value="0.001"/>
            <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
            <Parameter name="Use Random Seed" type="bool" value="0"/>
            <Parameter name="Random Seed" type="unsignedInteger" value="1"/>
          </Method>
        </Task>
        :return:
        """
        method = etree.Element('Method', attrib={'name': 'Stochastic (τ-Leap)',
                                                 'type': 'TauLeap'})

        dct = {'name': 'Epsilon',
               'type': 'float',
               'value': self.epsilon}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Max Internal Steps',
               'type': 'unsignedInteger',
               'value': str(self.max_internal_steps)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Use Random Seed',
               'type': 'bool',
               'value': self.use_random_seed}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Random Seed',
               'type': 'unsignedInteger',
               'value': str(self.random_seed)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        task = self.create_task()
        task.append(method)
        return task

    def adaptive_tau_leap(self):
        """
          </Problem>
          <Method name="Stochastic (Adaptive SSA/τ-Leap)" type="AdaptiveSA">
            <Parameter name="Epsilon" type="float" value="0.03"/>
            <Parameter name="Max Internal Steps" type="integer" value="1000000"/>
            <Parameter name="Use Random Seed" type="bool" value="0"/>
            <Parameter name="Random Seed" type="unsignedInteger" value="1"/>
          </Method>
        </Task>
        :return:
        """
        method = etree.Element('Method', attrib={'name': 'Stochastic (Adaptive SSA/τ-Leap)',
                                                 'type': 'AdaptiveSA'})

        dct = {'name': 'Epsilon',
               'type': 'float',
               'value': self.epsilon}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Max Internal Steps',
               'type': 'unsignedInteger',
               'value': str(self.max_internal_steps)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Use Random Seed',
               'type': 'bool',
               'value': self.use_random_seed}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Random Seed',
               'type': 'unsignedInteger',
               'value': str(self.random_seed)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        task = self.create_task()
        task.append(method)
        return task

    def hybrid_runge_kutta(self):
        """

          <Method name="Hybrid (Runge-Kutta)" type="Hybrid">
            <Parameter name="Max Internal Steps" type="integer" value="1000000"/>
            <Parameter name="Lower Limit" type="float" value="800"/>
            <Parameter name="Upper Limit" type="float" value="1000"/>
            <Parameter name="Partitioning Interval" type="unsignedInteger" value="1"/>
            <Parameter name="Use Random Seed" type="bool" value="0"/>
            <Parameter name="Random Seed" type="unsignedInteger" value="1"/>
            <Parameter name="Runge Kutta Stepsize" type="float" value="0.001"/>
          </Method>
        </Task>
        :return:
        """
        method = etree.Element('Method', attrib={'name': 'Hybrid (Runge-Kutta)',
                                                 'type': 'Hybrid'})

        dct = {'name': 'Max Internal Steps',
               'type': 'unsignedInteger',
               'value': str(self.max_internal_steps)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Lower Limit',
               'type': 'float',
               'value': str(self.lower_limit)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Upper Limit',
               'type': 'float',
               'value': str(self.upper_limit) }
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Partitioning Interval',
               'type': 'unsignedInteger',
               'value': str(self.partitioning_interval)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Use Random Seed',
               'type': 'bool',
               'value': self.use_random_seed}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Random Seed',
               'type': 'unsignedInteger',
               'value': str(self.random_seed)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Runge-Kutta Stepsize',
               'type': 'float',
               'value': str(self.runge_kutta_step_size)}
        etree.SubElement(method, 'Parameter', attrib=dct)
        task = self.create_task()
        task.append(method)
        return task

    def hybrid_lsoda(self):
        """
      <Method name="Hybrid (LSODA)" type="Hybrid (LSODA)">
        <Parameter name="Max Internal Steps" type="integer" value="1000000"/>
        <Parameter name="Lower Limit" type="float" value="800"/>
        <Parameter name="Upper Limit" type="float" value="1000"/>
        <Parameter name="Partitioning Interval" type="unsignedInteger" value="1"/>
        <Parameter name="Use Random Seed" type="bool" value="0"/>
        <Parameter name="Random Seed" type="unsignedInteger" value="1"/>
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
        :return:
        """
        method = etree.Element('Method', attrib={'name': 'Hybrid (LSODA)',
                                                 'type': 'Hybrid (LSODA)'})
        dct = {'name': 'Max Internal Steps',
               'type': 'unsignedInteger',
               'value': str(self.max_internal_steps)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Lower Limit',
               'type': 'float',
               'value': str(self.lower_limit)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Upper Limit',
               'type': 'float',
               'value': str(self.upper_limit) }
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Partitioning Interval',
               'type': 'unsignedInteger',
               'value': str(self.partitioning_interval)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Use Random Seed',
               'type': 'bool',
               'value': self.use_random_seed}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Random Seed',
               'type': 'unsignedInteger',
               'value': str(self.random_seed)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Integrate Reduced Model',
               'type': 'bool',
               'value': self.integrate_reduced_model}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Relative Tolerance',
               'type': 'unsignedFloat',
               'value': str(self.relative_tolerance)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Absolute Tolerance',
               'type': 'unsignedFloat',
               'value': str(self.absolute_tolerance)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        dct = {'name': 'Max Internal Step Size',
               'type': 'unsignedFloat',
               'value': str(self.max_internal_step_size)}
        etree.SubElement(method, 'Parameter', attrib=dct)

        task = self.create_task()
        task.append(method)
        return task

    def hybrid_rk45(self):
        """
          <Method name="Hybrid (RK-45)" type="Hybrid (DSA-ODE45)">
            <Parameter name="Max Internal Steps" type="unsignedInteger" value="100000"/>
            <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
            <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-009"/>
            <Parameter name="Partitioning Strategy" type="string" value="User specified Partition"/>
            <ParameterGroup name="Deterministic Reactions">
            </ParameterGroup>
            <Parameter name="Use Random Seed" type="bool" value="0"/>
            <Parameter name="Random Seed" type="unsignedInteger" value="1"/>
          </Method>
        </Task>

        :return:
        """
        raise Errors.NotImplementedError('The hybrid-RK-45 method is not yet implemented')

    def set_report(self):
        """
        ser a time course report containing time
        and all species or global quantities defined by the user.

        :return: PyCoTools.model.Model
        """
        report_options = {'metabolites': self.metabolites,
                          'global_quantities': self.global_quantities,
                          'quantity_type': self.quantity_type,
                          'report_name': self.report_name,
                          'append': self.append,
                          'confirm_overwrite': self.confirm_overwrite,
                          'update_model': self.update_model,
                          'report_type': 'time_course'}
        ## create a time course report
        self.model = Reports(self.model, **report_options).model

        ## get the report key
        key = self.get_report_key()
        arg_dct = {'append': self.append,
                   'target': self.report_name,
                   'reference': key,
                   'confirmOverwrite': self.confirm_overwrite}

        query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        present = False
        for i in self.model.xml.xpath(query):
            for j in list(i):
                if 'append' and 'target' in j.attrib.keys():
                    present = True
                    j.attrib.update(arg_dct)
            if present == False:
                report = etree.Element('Report', attrib=arg_dct)
                i.insert(0, report)
        return self.model


    def get_report_key(self):
        '''
        cros reference the timecourse task with the newly created
        time course reort to get the key
        '''
        LOG.debug('getting report key')
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'] == 'Time-Course':
                key = i.attrib['key']
        assert key != None, 'have you ran the report_definition method?'
        return key

    # def run(self):
    #     '''
    #     run a time course. Use keyword argument:
    #         simulation_type='deterministic' #default
    #         SumulationType='stochastic' #still to be written
    #     '''
    #     if self.kwargs.get('simulation_type') == 'deterministic':
    #         self.copasiML = self.report_definition()
    #         self.copasiML = self.set_report()
    #         self.copasiML = self.set_deterministic()
    #         LOG.debug('setting up deterministic time course')
    #     elif self.kwargs.get('simulation_type') == 'stochastic':
    #         raise Errors.NotImplementedError(
    #             'There is space in this class to write code to Run a stochastic simulation but it is not yet written')
    #     ##
    #     #            # save to duplicate copasi file
    #     self.save()
    #     R = Run(self.copasi_file, task='time_course')
    #     LOG.debug('Time course ran')
    #     return R


class Scan(_base._ModelBase):
    """
    Interface to COPASI scan task
    """
    def __init__(self, model, **kwargs):
        super(Scan, self).__init__(model, **kwargs)

        default_report_name = os.path.split(self.model.copasi_file)[1][:-4] + '_PE_results.txt'
        self.default_properties = {'metabolites': self.model.metabolites,
                                   'global_quantities': self.model.global_quantities,
                                   'variable': self.model.metabolites[0],
                                   'quantity_type': 'concentration',
                                   'report_name': default_report_name,
                                   'append': False,
                                   'confirm_overwrite': False,
                                   'update_model': False,
                                   'subtask': 'parameter_estimation',
                                   'report_type': 'profilelikelihood',
                                   'output_in_subtask': False,
                                   'adjust_initial_conditions': False,
                                   'number_of_steps': 10,
                                   'maximum': 100,
                                   'minimum': 0.01,
                                   'log10': False,
                                   'distribution_type': 'normal',
                                   'scan_type': 'scan',
                                   # scan object specific (for scan and random_sampling scan_types)
                                   'scheduled': True,
                                   'save': False,
                                   'clear_scans': True,  # if true, will remove all scans present then add new scan
                                   'run_mode': False}

        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self.do_checks()

        ## conflicts with other classes in base
        ## class so just convert the scan log10 argument
        ## to numeric string here
        if self.log10 == False:
            self.log10 = str(0)
        else:
            self.log10 = str(1)


        self.model = self.define_report()


        if self.clear_scans == True:
            self.model = self.remove_scans()

        self.model = self.define_report()
        self.model = self.create_scan()
        self.model = self.set_scan_options()

        if self.save:
            self.model.save()

        self.run()

    def do_checks(self):
        """
        Varify integrity of user input
        :return:
        """
        subtasks = ['steady_state', 'time_course',
                    'metabolic_control_anlysis',
                    'lyapunov_exponents',
                    'optimiztion', 'parameter_estimation',
                    'sensitivities', 'linear_noise_approximation',
                    'cross_section', 'time_scale_separation_analysis']

        dist_types = ['normal', 'uniform', 'poisson', 'gamma']
        scan_types = ['scan', 'repeat', 'random_sampling']

        assert self.subtask in subtasks
        assert self.distribution_type in dist_types
        assert self.scan_type in scan_types

        # numericify the some keyword arguments
        self.subtask_numbers = [0, 1, 6, 7, 4, 5, 9, 12, 11, 8]
        self.subtask_numbers = dict(zip(subtasks, [str(i) for i in self.subtask_numbers]))
        for i, j in self.subtask_numbers.items():
            if i == self.subtask:
                self.subtask = j

        scan_type_numbers = [1, 0, 2]
        LOG.debug('kwargs[scan_type is: {}'.format(self.scan_type))
        for i in zip(scan_types, scan_type_numbers):
            LOG.debug('scan type to number tuple: {}'.format(i))
            if i[0] == self.scan_type:
                self.scan_type = str(i[1])

        dist_types_numbers = [0, 1, 2, 3]
        for i in zip(dist_types, dist_types_numbers):
            if i[0] == self.distribution_type:
                self.distribution_type = str(i[1])

    def define_report(self):
        """
        Use Report class to create report
        :return:
        """
        logging.debug('defining report')
        self.report_dict = {}
        self.report_dict['metabolites'] = self.metabolites
        self.report_dict['global_quantities'] = self.global_quantities
        self.report_dict['quantity_type'] = self.quantity_type
        self.report_dict['report_name'] = self.report_name
        self.report_dict['append'] = self.append
        self.report_dict['confirm_overwrite'] = self.confirm_overwrite
        self.report_dict['variable'] = self.variable
        self.report_dict['report_type'] = self.report_type
        R = Reports(self.model.copasi_file, **self.report_dict)
        return R.model

    def get_report_key(self):
        '''

        '''
        # ammend the time course option
        if self.report_type.lower() == 'time_course':
            self.report_type = 'time-course'
        key = None
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'].lower() == self.report_type.lower():
                key = i.attrib['key']
        if key == None:
            raise Errors.ReportDoesNotExistError('Report doesn\'t exist. Check to see if you have either defined the report manually or used the pycopi.Reports class')
        return key

    def create_scan(self):
        """
        metabolite cn:
            CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=InitialConcentration"/>

        :return:
        """
        # get cn value
        ## if variable is a metabolite
        if self.variable.name in [i.name for i in self.model.metabolites]:
            if self.quantity_type == 'concentration':
                cn = '{},{},{}'.format(self.model.reference,
                                       self.variable.compartment.reference,
                                       self.variable.initial_reference)

            elif self.quantity_type == 'particle_number':
                cn = '{},{},{}'.format(self.model.reference,
                                       self.variable.compartment.reference,
                                       self.variable.initial_particle_reference)

        elif self.variable.name in [i.name for i in self.model.global_quantities]:
            cn = '{},{}'.format(self.model.reference, self.variable.initial_reference)

        elif self.variable.name in [i.name for i in self.model.local_parameters]:
            cn = '{},{}'.format(self.model.reference, self.variable.initial_reference)

        number_of_steps_attrib = {'type': 'unsignedInteger',
                                  'name': 'Number of steps',
                                  'value': str(self.number_of_steps )}

        scan_item_attrib = {'type': 'cn',
                            'name': 'Object',
                            'value': cn}

        type_attrib = {'type': 'unsignedInteger',
                       'name': 'Type',
                       'value': self.scan_type}

        maximum_attrib = {'type': 'float',
                          'name': 'Maximum',
                          'value': str(self.maximum)}

        minimum_attrib = {'type': 'float',
                          'name': 'Minimum',
                          'value': str(self.minimum)}

        log_attrib = {'type': 'bool',
                      'name': 'log',
                      'value': self.log10}
        dist_type_attrib = {'type': 'unsignedInteger',
                            'name': 'Distribution type',
                            'value': self.distribution_type}

        scanItem_element = etree.Element('ParameterGroup', attrib={'name': 'ScanItem'})

        ## regular scan
        if self.scan_type == '1':
            etree.SubElement(scanItem_element, 'Parameter', attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=scan_item_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=type_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=maximum_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=minimum_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=log_attrib)

        ## repeat scan
        elif self.scan_type == '0':
            etree.SubElement(scanItem_element, 'Parameter', attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=type_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=scan_item_attrib)

        ## distribution scan
        elif self.scan_type == '2':
            etree.SubElement(scanItem_element, 'Parameter', attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=type_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=scan_item_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=minimum_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=maximum_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=log_attrib)
            etree.SubElement(scanItem_element, 'Parameter', attrib=dist_type_attrib)
        query = '//*[@name="ScanItems"]'
        # print etree.tostring(scanItem_element, pretty_print=True)
        for i in self.model.xml.xpath(query):
            i.append(scanItem_element)
        return self.model
    #
    def set_scan_options(self):
        report_attrib = {'append': self.append,
                         'target': self.report_name,
                         'reference': self.get_report_key(),
                         'confirmOverwrite': self.confirm_overwrite}

        subtask_attrib = {'type': 'unsignedInteger', 'name': 'Subtask', 'value': self.subtask}
        output_in_subtask_attrib = {'type': 'bool', 'name': 'Output in subtask',
                                    'value': self.kwargs['output_in_subtask']}
        adjust_initial_conditions_attrib = {'type': 'bool', 'name': 'Adjust initial conditions',
                                            'value': self.adjust_initial_conditions}
        scheduled_attrib = {'scheduled': self.scheduled, 'updateModel': self.update_model}

        R = etree.Element('Report', attrib=report_attrib)
        query = '//*[@name="Scan"]'
        '''
        If scan task already has a report element defined, modify it,
        otherwise create a new report element directly under the ScanTask
        element
        '''
        scan_task = self.model.xml.xpath(query)[0]
        if scan_task[0].tag == '{http://www.copasi.org/static/schema}Problem':
            scan_task.insert(0, R)
        elif scan_task[0].tag == '{http://www.copasi.org/static/schema}Report':
            scan_task[0].attrib.update(report_attrib)
        for i in self.model.xml.xpath(query):
            i.attrib.update(scheduled_attrib)
            for j in list(i):
                for k in list(j):
                    if k.attrib['name'] == 'Subtask':
                        k.attrib.update(subtask_attrib)
                    if k.attrib['name'] == 'Output in subtask':
                        k.attrib.update(output_in_subtask_attrib)
                    if k.attrib['name'] == 'Adjust initial conditions':
                        k.attrib.update(adjust_initial_conditions_attrib)
        return self.model

    def remove_scans(self):
        """
        Remove all scans that have been defined.

        :return:
        """
        query = '//*[@name="ScanItems"]'
        for i in self.model.xml.xpath(query):
            for j in list(i):
                i.remove(j)
        return self.model

    def run(self):
        R = Run(self.model, task='scan', mode=self.run)


class ExperimentMapper(_base._ModelBase):
    """
    Class for mapping variables from file to cps



    This is what the xml should look like after using this class:
         <Task key="Task_19" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
          <Report reference="Report_12" target="" append="1" confirmOverwrite="1"/>
          <Problem>
            <Parameter name="Maximize" type="bool" value="0"/>
            <Parameter name="Randomize Start Values" type="bool" value="0"/>
            <Parameter name="Calculate Statistics" type="bool" value="1"/>
            <ParameterGroup name="OptimizationItemList">
            </ParameterGroup>
            <ParameterGroup name="OptimizationConstraintList">
            </ParameterGroup>
            <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
            <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
            <Parameter name="Create Parameter Sets" type="bool" value="0"/>
            <ParameterGroup name="Experiment Set">
              <ParameterGroup name="Experiment">
                <Parameter name="Data is Row Oriented" type="bool" value="1"/>
                <Parameter name="Experiment Type" type="unsignedInteger" value="1"/>
                <Parameter name="File Name" type="file" value="TimeCourseData.csv"/>
                <Parameter name="First Row" type="unsignedInteger" value="1"/>
                <Parameter name="Key" type="key" value="Experiment_1"/>
                <Parameter name="Last Row" type="unsignedInteger" value="12"/>
                <Parameter name="Normalize Weights per Experiment" type="bool" value="1"/>
                <Parameter name="Number of Columns" type="unsignedInteger" value="7"/>
                <ParameterGroup name="Object Map">
                  <ParameterGroup name="0">
                    <Parameter name="Role" type="unsignedInteger" value="3"/>
                  </ParameterGroup>
                  <ParameterGroup name="1">
                    <Parameter name="Object CN" type="cn" value="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[B],Reference=Concentration"/>
                    <Parameter name="Role" type="unsignedInteger" value="2"/>
                  </ParameterGroup>
                  <ParameterGroup name="2">
                    <Parameter name="Object CN" type="cn" value="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=InitialConcentration"/>
                    <Parameter name="Role" type="unsignedInteger" value="1"/>
                  </ParameterGroup>
                  <ParameterGroup name="3">
                    <Parameter name="Role" type="unsignedInteger" value="0"/>
                  </ParameterGroup>
                  <ParameterGroup name="4">
                    <Parameter name="Role" type="unsignedInteger" value="0"/>
                  </ParameterGroup>
                  <ParameterGroup name="5">
                    <Parameter name="Role" type="unsignedInteger" value="0"/>
                  </ParameterGroup>
                  <ParameterGroup name="6">
                    <Parameter name="Role" type="unsignedInteger" value="0"/>
                  </ParameterGroup>
                </ParameterGroup>
                <Parameter name="Row containing Names" type="unsignedInteger" value="1"/>
                <Parameter name="Separator" type="string" value="&#x09;"/>
                <Parameter name="Weight Method" type="unsignedInteger" value="1"/>
              </ParameterGroup>
            </ParameterGroup>
            <ParameterGroup name="Validation Set">
              <Parameter name="Threshold" type="unsignedInteger" value="5"/>
              <Parameter name="Weight" type="unsignedFloat" value="1"/>
            </ParameterGroup>
          </Problem>
    """
    def __init__(self, model, experiment_files, **kwargs):
        super(ExperimentMapper, self).__init__(model, **kwargs)
        self.experiment_files = experiment_files
        if isinstance(self.experiment_files, list) !=True:
            self.experiment_files = [self.experiment_files]


        self.default_properties={'type': 'experiment', #or 'validation_data
                                 'row_orientation': [True]*len(self.experiment_files),
                                 'experiment_type': ['timecourse']*len(self.experiment_files),
                                 'first_row': [1]*len(self.experiment_files),
                                 'normalize_weights_per_experiment': [True]*len(self.experiment_files),
                                 'row_containing_names': [1]*len(self.experiment_files),
                                 'separator': ['\t']*len(self.experiment_files),
                                 'weight_method': ['mean_squared']*len(self.experiment_files),
                                 'threshold': [5]*len(self.experiment_files),
                                 'weight': [1]*len(self.experiment_files) ,
                                 'save': False}

        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self.do_checks()


        #run the experiment mapper
        self.model = self.map_experiments()

        if self.save:
            self.model.save()


    def do_checks(self):
        """

        """
        data_types = ['experiment', 'validation']
        if self.type not in data_types:
            raise Errors.InputError('{} not in {}'.format(self.type, data_types))

        for i in range(len(self.experiment_files)):
            if os.path.isabs(self.experiment_files[i])!=True:
                self.experiment_files[i] = os.path.abspath(self.experiment_files[i])

        weight_method_string = ['mean','mean_squared','stardard_deviation','value_scaling']
        weight_method_numbers = [str(i) for i in [1,2,3,4] ]
        weight_method_dict = dict(zip(weight_method_string, weight_method_numbers))
        self.weight_method = [weight_method_dict[i] for i in self.weight_method  ]


        experiment_type_string = ['steadystate','timecourse']
        experiment_type_numbers = [str(i) for i in [0, 1]]
        experiment_type_dict = dict(zip(experiment_type_string, experiment_type_numbers))
        self.experiment_type = [experiment_type_dict[i] for i in self.experiment_type]

        l=[]
        assert isinstance(self.row_orientation, list)
        for i in self.row_orientation:
            assert i in [True,False]
            if i == True:
                l.append(str(1))
            else:
                l.append(str(0))
        self.row_orientation = l

        assert isinstance(self.first_row, list)
        l=[]
        for i in self.first_row:
            assert i!=0
            assert i!=str(0)
            l.append(str(i))
        self.first_row = l

        l=[]
        assert isinstance(self.normalize_weights_per_experiment, list)
        for i in self.normalize_weights_per_experiment:
            assert i in [True,False],'{} should be true or false'.format(i)
            if i == True:
                l.append(str(1))
            else:
                l.append(str(0))
        self.normalize_weights_per_experiment = l

        l=[]
        assert isinstance(self.row_orientation, list)
        for i in self.row_orientation:
            l.append(str(i))
        self.row_orientation=l

        l=[]
        assert isinstance(self.row_containing_names,list)
        for i in self.row_containing_names:
            l.append(str(i))
        self.row_containing_names = l


        assert isinstance(self.separator,list)
        for i in self.separator:
            assert isinstance(i,str),'separator should be given asa python list'

    def __str__(self):
        return 'ExperimentMapper({})'.format(self.to_string())

    @property
    def experiments(self):
        existing_experiment_list=[]
        if self.type == 'experiment':
            query = '//*[@name="Experiment Set"]'
        elif self.type == 'validation':
            query = '//*[@name="Validation Set"]'


        for i in self.model.xml.xpath(query):
            for j in list(i):
                existing_experiment_list.append(j)
        return existing_experiment_list

    def create_experiment(self, index):
        '''
        Adds a single experiment set to the parameter estimation task
        exp_file is an experiment filename with exactly matching headers (independent variablies need '_indep' appended to the end)
        since this method is intended to be used in a loop in another function to
        deal with all experiment sets, the second argument 'i' is the index for the current experiment

        i is the exeriment_file index
        '''
        assert isinstance(index, int)
        data=pandas.read_csv(self.experiment_files[index], sep=self.separator[index])
        #get observables from data. Must be exact match
        obs = list(data.columns)
        num_rows = str(data.shape[0])
        num_columns = str(data.shape[1]) #plus 1 to account for 0 indexed

        #if exp_file is in the same directory as copasi_file only use relative path
        if os.path.dirname(
                self.model.copasi_file) == os.path.dirname(
                    self.experiment_files[index]):
            exp = os.path.split(self.experiment_files[index])[1]
        else:
            exp = self.experiment_files[index]

        self.key='Experiment_{}'.format(index)

        #necessary XML attributes
        Exp=etree.Element('ParameterGroup', attrib={'name': self.key})
        # Exp = etree.Element('ParameterGroup', attrib={'name': self.experiment_files[index]})

        row_orientation = {'type': 'bool',
                         'name': 'Data is Row Oriented',
                         'value': self.row_orientation[index]}

        experiment_type = {'type': 'unsignedInteger',
                         'name': 'Experiment Type',
                         'value': self.experiment_type[index]}

        ExpFile = {'type': 'file',
                   'name': 'File Name',
                   'value': exp}

        first_row = {'type': 'unsignedInteger',
                     'name': 'First Row',
                     'value': str(self.first_row[index])}

        Key = {'type': 'key',
               'name': 'Key',
               'value': self.key}

        LastRow = {'type': 'unsignedInteger',
                   'name': 'Last Row',
                   'value': str(int(num_rows)+1)} #add 1 to account for 0 indexed python

        normalize_weights_per_experiment = {'type': 'bool',
                                            'name': 'Normalize Weights per Experiment',
                                            'value': self.normalize_weights_per_experiment[index]}

        NumberOfColumns = {'type': 'unsignedInteger',
                           'name': 'Number of Columns',
                           'value': num_columns}

        ObjectMap = {'name': 'Object Map'}

        row_containing_names = {'type': 'unsignedInteger',
                                'name': 'Row containing Names',
                                'value': str(self.row_containing_names[index])}

        separator = {'type': 'string',
                     'name': 'separator',
                     'value': self.separator[index]}

        weight_method = {'type': 'unsignedInteger',
                         'name': 'Weight Method',
                         'value': self.weight_method[index]}

        etree.SubElement(Exp, 'Parameter', attrib=row_orientation)
        etree.SubElement(Exp, 'Parameter', attrib=experiment_type)
        etree.SubElement(Exp, 'Parameter', attrib=ExpFile)
        etree.SubElement(Exp, 'Parameter', attrib=first_row)
        etree.SubElement(Exp, 'Parameter', attrib=Key)
        etree.SubElement(Exp, 'Parameter', attrib=LastRow)
        etree.SubElement(Exp, 'Parameter', attrib=normalize_weights_per_experiment)
        etree.SubElement(Exp, 'Parameter', attrib=NumberOfColumns)
        ## Map looks out of place but this order must be maintained
        Map = etree.SubElement(Exp, 'ParameterGroup', attrib=ObjectMap)
        etree.SubElement(Exp, 'Parameter', attrib=row_containing_names)
        etree.SubElement(Exp, 'Parameter', attrib=separator)
        etree.SubElement(Exp, 'Parameter', attrib=weight_method)

        #define object role attributes
        time_role = {'type': 'unsignedInteger',
                    'name': 'Role',
                    'value': '3'}

        dependent_variable_role = {'type': 'unsignedInteger',
                                 'name': 'Role',
                                 'value': '2'}

        independent_variable_role = {'type': 'unsignedInteger',
                                   'name': 'Role',
                                   'value': '1'}

        ignored_role = {'type': 'unsignedInteger',
                               'name': 'Role',
                               'value': '0'}

        for i in range(int(num_columns)):
            map_group=etree.SubElement(Map, 'ParameterGroup', attrib={'name': (str(i))})
            if self.experiment_type[index]==str(1): #when Experiment type is set to time course it should be 1
                ## first column is time
                if i == 0:
                    etree.SubElement(map_group, 'Parameter', attrib=time_role)
                else:
                    # LOG.warning(obs[i][:-6])
                    ## map independent variables
                    if obs[i][-6:] == '_indep':
                        if obs[i][:-6] in [j.name for j in self.model.metabolites]:
                            metab = [j for j in self.model.metabolites if j.name == obs[i][:-6]][0]
                            cn = '{},{},{}'.format(self.model.reference,
                                                   metab.compartment.reference,
                                                   metab.initial_reference)
                            independent_ICs = {'type': 'cn',
                                               'name': 'Object CN',
                                               'value': cn}
                            etree.SubElement(map_group, 'Parameter', attrib=independent_ICs)

                        elif obs[i][:-6] in [j.name for j in self.model.global_quantities]:
                            glob = [j for j in self.model.global_quantities if j.name == obs[i]][0]
                            cn = '{},{}'.format(self.model.reference,
                                                glob.initial_reference)

                            independent_globs = {'type': 'cn',
                                                 'name': 'Object CN',
                                                 'value': cn}

                            etree.SubElement(map_group,
                                             'Parameter',
                                             attrib=independent_globs)
                        else:
                            etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
                            LOG.warning('{} not found. Set to ignore'.format(obs[i]))
                        etree.SubElement(map_group, 'Parameter', attrib=independent_variable_role)

                    ## now do dependent variables
                    elif obs[i][:-6] != '_indep':
                        ## metabolites
                        if obs[i] in [j.name for j in self.model.metabolites]:
                            metab = [j for j in self.model.metabolites if j.name == obs[i]][0]
                            cn = '{},{},{}'.format(self.model.reference,
                                                   metab.compartment.reference,
                                                   metab.transient_reference)

                            dependent_ICs = {'type': 'cn',
                                             'name': 'Object CN',
                                             'value': cn}

                            etree.SubElement(map_group, 'Parameter', attrib=dependent_ICs)

                        ## global quantities
                        elif obs[i] in [j.name for j in self.model.global_quantities]:
                            glob = [j for j in self.model.global_quantities if j.name == obs[i]][0]
                            cn = '{},{}'.format(self.model.reference,
                                                glob.transient_reference)
                            dependent_globs = {'type': 'cn',
                                               'name': 'Object CN',
                                               'value': cn}
                            etree.SubElement(map_group,
                                             'Parameter',
                                             attrib=dependent_globs)
                        ## remember that local parameters are not mapped to experimental
                        ## data
                        else:
                            etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
                            LOG.warning('{} not found. Set to ignore'.format(obs[i]))
                        ## map for time course dependent variable
                        etree.SubElement(map_group, 'Parameter', attrib=dependent_variable_role)

            ## and now for steady state data
            else:

                ## do independent variables first
                if obs[i][-6:]=='_indep':

                    ## for metabolites
                    if obs[i][:-6] in [j.name for j in self.model.metabolites]:
                        metab = [j for j in self.model.metabolites if j.name == obs[i][:-6]][0]
                        cn = '{},{},{}'.format(self.model.reference,
                                               metab.compartment.reference,
                                               metab.initial_reference)

                        independent_ICs = {'type': 'cn',
                                           'name': 'Object CN',
                                           'value': cn}
                        x = etree.SubElement(map_group, 'Parameter', attrib=independent_ICs)

                    ## now for global quantities
                    elif obs[i][:-6] in [j.name for j in self.model.global_quantities]:
                        glob = [j for j in self.model.global_quantities if j.name == obs[i]][0]
                        cn = '{},{}'.format(self.model.reference,
                                            glob.initial_reference)

                        independent_globs = {'type': 'cn',
                                             'name': 'Object CN',
                                             'value': cn}

                        etree.SubElement(map_group,
                                         'Parameter',
                                         attrib=independent_globs)
                    ## local parameters are never mapped
                    else:
                        etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
                        LOG.warning('{} not found. Set to ignore'.format(obs[i]))
                    etree.SubElement(map_group, 'Parameter', attrib=independent_variable_role)


                elif obs[i][-6:] != '_indep':
                    ## for metabolites
                    if obs[i] in [j.name for j in self.model.metabolites]:
                        metab = [j for j in self.model.metabolites if j.name == obs[i]][0]
                        cn = '{},{},{}'.format(self.model.reference,
                                               metab.compartment.reference,
                                               metab.transient_reference)
                        independent_ICs = {'type': 'cn',
                                           'name': 'Object CN',
                                           'value': cn}
                        etree.SubElement(map_group, 'Parameter', attrib=independent_ICs)

                    ## now for global quantities
                    elif obs[i] in [j.name for j in self.model.global_quantities]:
                        glob = [j for j in self.model.global_quantities if j.name == obs[i]][0]
                        cn = '{},{}'.format(self.model.reference,
                                            glob.transient_reference)

                        independent_globs = {'type': 'cn',
                                             'name': 'Object CN',
                                             'value': cn}

                        etree.SubElement(map_group,
                                         'Parameter',
                                         attrib=independent_globs)
                    ## local parameters are never mapped
                    else:
                        etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
                        LOG.warning('{} not found. Set to ignore'.format(obs[i]))
                    etree.SubElement(map_group, 'Parameter', attrib=dependent_variable_role)
        return Exp

    def remove_experiment(self,experiment_name):
        '''
        name attribute of experiment. usually Experiment_1 or something
        '''
        if self.type == 'experiment':
            query = '//*[@name="Experiment Set"]'
        elif self.type == 'validation':
            query = '//*[@name="Validation Set"]'
        for i in self.model.xml.xpath(query):
            for j in list(i):
                if j.attrib['name'] == experiment_name:
                    j.getparent().remove(j)
        return self.model

    def remove_all_experiments(self):

        for i in self.experiments:
            experiment_name = i.attrib['name']
            self.remove_experiment(experiment_name)
        return self.model

    def add_experiment_set(self,experiment_element):
        """
        Map a single experiment set
        :param experiment_element:
        :return:
        """
        if self.type == 'experiment':
            query = '//*[@name="Experiment Set"]'
        elif self.type == 'validation':
            query = '//*[@name="Validation Set"]'
            raise Errors.NotImplementedError('Validation data sets are currently not supported')

        for j in self.model.xml.xpath(query):
            j.insert(0, experiment_element)
        return self.model


    def map_experiments(self):
        """
        map all experiment sets
        :return:
        """
        self.remove_all_experiments()
        LOG.debug('Removing all pre-existing experiments from copasi mapping interface')
        for i in range(len(self.experiment_files)):
            Experiment = self.create_experiment(i)
            LOG.debug('Mapping experiment {}'.format(self.experiment_files[i]))
            self.model = self.add_experiment_set(Experiment)
            # self.save() ## Note sure whether this save is needed. Keep commented until you're sure
        return self.model

class PhaseSpaceDep(TimeCourse):
    '''
    Use TimeCourse to get data and replot all n choose 2 combinations
    of phase space plot
    '''
    def __init__(self,copasi_file,**kwargs):
        super(PhaseSpace,self).__init__(copasi_file,**kwargs)
        LOG.debug('plotting all combinations of phase space plot')
        self.new_options={'plot':False}
        self.kwargs.update(self.new_options)
        self.species_data=self.isolate_species()
        self.combinations=self.get_combinations()

        if self.kwargs.get('savefig')==True:
            self.phase_dir=self.make_phase_dir()
            os.chdir(self.phase_dir)

        self.plot_all_phase()

        os.chdir(os.path.dirname(self.copasi_file))


    def isolate_species(self):
        '''
        Isolate the species from the time course data
        '''
        metabs= self.GMQ.get_IC_cns().keys()
        for i in metabs:
            if i not in self.data.keys():
                raise Errors.IncompatibleStringError(' {} is an incompatible string that is not supported by PyCoTools. Please modify the string and rerun')
        return self.data[metabs]

    def get_combinations(self):
        return list(itertools.combinations(self.species_data.keys(),2))

    def make_phase_dir(self):
        dire=os.path.join(os.path.dirname(self.copasi_file),'Phaseplots')
        if os.path.isdir(dire)==False:
            os.mkdir(dire)
        return dire


    def plot1phase(self,x,y):
        if x  not in self.species_data.keys():
            raise Errors.InputError('{} is not in your model species: {}'.format(x,self.species_data.keys()))

        if y  not in self.species_data.keys():
            raise Errors.InputError('{} is not in your model species: {}'.format(y,self.species_data.keys()))

        x_data=self.species_data[x]
        y_data=self.species_data[y]
        plt.figure()
        ax = plt.subplot(111)
        plt.plot(x_data,y_data,linewidth=self.kwargs.get('line_width'),
                    color=self.kwargs.get('line_color'),
                    linestyle=self.kwargs.get('line_style'),
                    marker='o',markerfacecolor=self.kwargs.get('marker_color'),
                    markersize=self.kwargs.get('marker_size'))

        plt.title('\n'.join(wrap('{} Vs {} Phase plot'.format(x,y),self.kwargs.get('title_wrap_size'))),fontsize=self.kwargs.get('font_size'))
        try:
            plt.ylabel(y+'({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('font_size'))
            plt.xlabel(x+'({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('font_size'))
        except UnicodeEncodeError:
            plt.ylabel(y+'({})'.format('micromol'),fontsize=self.kwargs.get('font_size'))
            plt.xlabel(x+'({})'.format('micromol'),fontsize=self.kwargs.get('font_size'))


        #pretty stuff
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)

            #xtick rotation
        plt.xticks(rotation=self.kwargs.get('xtick_rotation'))

        #options for changing the plot axis
        if self.kwargs.get('ylimit')!=None:
            ax.set_ylim(self.kwargs.get('ylimit'))
        if self.kwargs.get('xlimit')!=None:
            ax.set_xlim(self.kwargs.get('xlimit'))
        if self.kwargs.get('show')==True:
            plt.show()

        def replace_non_ascii(st):
            for j in st:
                if j  not in string.ascii_letters+string.digits+'_-[]':
                    st=re.sub('\{}'.format(j),'__',st)
            return st

        y_new=replace_non_ascii(y)
        x_new=replace_non_ascii(x)
        name='{}_Vs_{}_Phaseplot'.format(x_new,y_new)

        if self.kwargs.get('savefig')==True:
            if self.kwargs.get('extra_title') !=None:
                plt.savefig(name+'_'+self.kwargs.get('extra_title')+'.png',bbox_inches='tight',format='png',dpi=self.kwargs.get('dpi'))
            else:
                plt.savefig(name+'_'+'.png',format='png',bbox_inches='tight',dpi=self.kwargs.get('dpi'))
    def plot_all_phase(self):
        for i in self.combinations:
            self.plot1phase(i[0],i[1])


class FormatPEData():
    def __init__(self,copasi_file,report_name, report_type='parameter_estimation'):
        self.copasi_file = copasi_file
        self.report_type = report_type
        self.GMQ = GetModelQuantities(self.copasi_file)
        self.report_name = report_name

        available_report_types = ['parameter_estimation','multi_parameter_estimation']
        if self.report_type not in available_report_types:
            raise Errors.InputError('{} not in {}'.format(self.report_type,available_report_types))

#        if os.path.isdir(self.report_name):
#            for i in os.listdir(self.report_name):

#        if os.path.isfile(self.report_name)!=True:
#            raise Errors.InputError('file {} does not exist'.format(self.report_name))

        if self.report_type=='parameter_estimation':
            try:
                self.format = self.format_results()
            except IOError:
                raise Errors.FileIsEmptyError('{} is empty and therefore cannot be read by pandas. Make sure you have waited until there is data in the parameter estimation file before formatting parameter estimation output')
            except pandas.parser.CParserError:
                raise Errors.InputError('Pandas cannot read data file. Ensure you are using report_type=\'multi_parameter_estimation\' for multiple parameter estimation classes')
        elif self.report_type=='multi_parameter_estimation':
            try:
                self.format = self.format_multi_results()
            except IOError:
                raise Errors.FileIsEmptyError('{} is empty and therefore cannot be read by pandas. Make sure you have waited until there is data in the parameter estimation file before formatting parameter estimation output')


    def format_results(self):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :return:
        """
        data = pandas.read_csv(self.report_name, sep='\t', header=None)
        data = data.drop(data.columns[0], axis=1)
        LOG.debug('Shape of estimated parameters: {}'.format(data.shape))
        width = data.shape[1]
        ## remove the extra bracket
        data[width] = data[width].str[1:]
#        num = data.shape[0]
        names = self.GMQ.get_fit_item_order()+['RSS']
        data.columns = names
        os.remove(self.report_name)
        data.to_csv(self.report_name,sep='\t',index=False)
        return data

    def format_multi_results(self):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :return:
        """
        try:
            data = pandas.read_csv(self.report_name, sep='\t', header=None, skiprows=[0])
        except:
            LOG.warning('No Columns to parse from file. {} is empty. Returned None'.format(self.report_name))
            return None
        bracket_columns = data[data.columns[[0,-2]]]
        if bracket_columns.iloc[0].iloc[0] != '(':
            data = pandas.read_csv(self.report_name, sep='\t')
            return data
        else:
            data = data.drop(data.columns[[0,-2]], axis=1)
            data.columns = range(data.shape[1])
            LOG.debug('Shape of estimated parameters: {}'.format(data.shape))
            ### parameter of interest has been removed.
            names = self.GMQ.get_fit_item_order()+['RSS']
            if self.GMQ.get_fit_item_order() == []:
                raise Errors.SomethingWentHorriblyWrongError('Parameter Estimation task is empty')
            if len(names) != data.shape[1]:
                raise Errors.SomethingWentHorriblyWrongError('length of parameter estimation data does not equal number of parameters estimated')

            if os.path.isfile(self.report_name):
                os.remove(self.report_name)
            data.columns = names
            data.to_csv(self.report_name, sep='\t', index=False)
            return self.report_name

    @staticmethod
    def format_folder(copasi_file, folder, report_type='multi_parameter_estimation'):
        """
        Format entire folder of similar PE data files
        """
        for i in glob.glob(os.path.join(folder, '*.txt')):
            FormatPEData(copasi_file, i, report_type=report_type)


class ParameterEstimation(_base._ModelBase):
    '''
    Set up and run a parameter estimation in copasi. Since each parameter estimation
    problem is different, this process cannot be done in a single line of code.
    Instead the user should initialize an instance of the ParameterEstimation
    class with all the relevant keyword arguments. Subsequently use the
    write_item_template() method and modify the resulting xlsx in your copasi file
    directory. save the file then close and run the setup()() method to define your
    optimization problem. When run is set to True, the parameter estimation will
    automatically run in CopasiSE. If plot is also set to True, a plot comparing
    experimental and simulated profiles are produced. Profiles are saved
    to file with savefig=True

    args:

        copasi_file:
            The file path for the copasi file you want to perform parameter estimation on

        experiment_files:
            Either a single experiment file path or a list of experiment file paths

    **Kwargs:

        metabolites:
            Which metabolites (ICs) to include in parameter esitmation. Default = all of them.

        global_quantities:
            Which global values to include in the parameter estimation. Default= all

        quantity_type:
            either 'concentration' or particle numbers

        report_name:
            name of the output report

        append:
            append to report or not,True or False

        confirm_overwrite:
            True or False, overwrite report or not

        config_filename:
            Filename for the parameter estimation config file

        overwrite_config_file:,
            True or False, overwrite the config file each time program is run

        update_model:
            Update model parameters after parameter estimation

        randomize_start_values:
            True or False. Check the randomize start values box or not. Default True

        create_parameter_sets:
            True or False. Check the create parameter sets box or not. Default False

        calculate_statistics':str(1),
            True or False. Check the calcualte statistics box or not. Default False

        method:
            Name of one of the copasi parameter estimation algorithms. Valid arguments:
            ['CurrentSolutionStatistics','DifferentialEvolution','EvolutionaryStrategySR','EvolutionaryProgram',
             'HookeJeeves','LevenbergMarquardt','NelderMead','ParticleSwarm','Praxis',
             'RandomSearch','ScatterSearch','SimulatedAnnealing','SteepestDescent',
             'TruncatedNewton','GeneticAlgorithm','GeneticAlgorithmSR'],
             Default=GeneticAlgorithm

        number_of_generations:
            A parameter for parameter estimation algorithms. Default=200

        population_size:
            A parameter for parameter estimation algorithms. Default=50

        random_number_generator:
            A parameter for parameter estimation algorithms. Default=1

        seed:
            A parameter for parameter estimation algorithms. Default=0

        pf:
            A parameter for parameter estimation algorithms. Default=0.475

        iteration_limit:
            A parameter for parameter estimation algorithms. Default=50

        tolerance:
            A parameter for parameter estimation algorithms. Default=0.00001

        rho;
            A parameter for parameter estimation algorithms. Default=0.2

        scale:
            A parameter for parameter estimation algorithms. Default=10

        swarm_size:
            A parameter for parameter estimation algorithms. Default=50

        std_deviation:
            A parameter for parameter estimation algorithms. Default=0.000001

        number_of_iterations:
            A parameter for parameter estimation algorithms. Default=100000

        start_temperature:
            A parameter for parameter estimation algorithms. Default=1

        cooling_factor:
            A parameter for parameter estimation algorithms. Default=0.85

        row_orientation:
            1 means data is row oriented, 0 means its column oriented

        experiment_type:
            List with the same number elements as you have experiment files. Each element
            is either 'timecourse' or 'steady_state' and describes the type of
            data at that element in the experiment_files argument

        first_row:
            List with the same number elements as you have experiment files. Each element
            is the starting line for data as an integer. Default is a list of 1's and this
            rarely needs to be changed.

        normalize_weights_per_experiment':[True]*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is True or False and correlates to ticking the
            normalize wieghts per experiment box in the copasi gui. Default [true]*len(experiments)

        row_containing_names:
            List with the same number elements as you have experiment files. Each element
            is an integer value corresponding to the row in the data containing names. The default
            is 1 for all experiment files [1]*len(experiment_files)


        separator':['\t']*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is the separator used in the data files. Defaults to a tab (\\t) for all files
            though commas are also common

        weight_method':['mean_squared']*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is a list of the name of the normalization algorithm to use for that data set.
            This should probably be the same for each experiment file and defaults to mean_squared.
            Options are: ['mean','mean_squared','stardard_deviation','value_scaling']

        save:
            One of False,'duplicate' or 'overwrite'. If duplicate, use the name in
            the keyword argument OutputML to save the file.


        prune_headers:
            Copasi uses references to distinguish between variable types. The report
            output usually contains these references in variable names. True removes
            the references while False leaves them in.
        scheduled':False
            True or False. Check the box called 'executable' in the top right hand
            corner of the Copasi GUI. This tells Copasi to shedule a parameter estimation
            task when using CopasiSE. This should be True of you are running a parameter
            estimation from the parameter estimation task via the pycopi but False when you
            want to set up a repeat item in the scan task with the parameter estimation subtask

        use_config_start_values:
            Default set to False. Determines whether the starting parameters
            from within the fitItemTemplate.xlsx are use for starting values
            in the parameter estimation or not

        lower_bound:
            Value of the default lower bound for the FitItemTemplate. Default 0.000001

        upper_bound:
            Value of default upper bound for FitItemTemplate. Default=1000000

#        run:
#            run the parameter estimation using CopasiSE. When running via the parameter
#            estimation task, the output is a matrix of function evaluation progression over
#            time. When running via the scan's repeat task, output is lines of parameter
#            estimation runs

        plot:
            Whether to plot result or not. Defualt=True

        font_size:
            Control graph label font size

        axis_size:
            Control graph axis font size

        extra_title:
            When savefig=True, given the saved
            file an extra label in the file path

        line_width:
            Control graph line_width

        marker_size:
            How big to plot the dots on the graph

        savefig:
            save graphs to file labelled after the index


        title_wrap_size:
            When graph titles are long, how many characters to have per
            line before word wrap. Default=30.

        show:
            When not using iPython, use show=True to display graphs

        ylimit: default==None, restrict amount of data shown on y axis.
        Useful for honing in on small confidence intervals

        xlimit: default==None, restrict amount of data shown on x axis.
        Useful for honing in on small confidence intervals

        dpi:
            How big saved figure should be. Default=125

        xtick_rotation:
            How many degrees to rotate the x tick labels
            of the output. Useful if you have very small or large
            numbers that overlay when plotting.


    '''

    def __init__(self, model, experiment_files, **kwargs):
        super(ParameterEstimation, self).__init__(model, **kwargs)
        self.experiment_files = experiment_files
        if isinstance(self.experiment_files, list) !=True:
            self.experiment_files = [self.experiment_files]

        default_report_name = os.path.join(os.path.dirname(self.model.copasi_file), 'PEData.txt')
        config_file = os.path.join(os.path.dirname(self.model.copasi_file), 'config_file.csv')

        self.default_properties = {'metabolites': self.model.metabolites,
                                   'global_quantities': self.model.global_quantities,
                                   'local_parameters': self.model.local_parameters,
                                   'quantity_type': 'concentration',
                                   'report_name': default_report_name,
                                   'append': False,
                                   'confirm_overwrite': False,
                                   'config_filename': config_file,
                                   'overwrite_config_file': False,
                                   'prune_headers': True,
                                   'update_model': False,
                                   'randomize_start_values': True,
                                   'create_parameter_sets': False,
                                   'calculate_statistics': False,
                                   'use_config_start_values': False,
                                   # method options
                                   'method': 'genetic_algorithm',
                                   # 'DifferentialEvolution',
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
                                   # experiment definition options
                                   # need to include options for defining multiple experimental files at once
                                   'row_orientation': [True] * len(self.experiment_files),
                                   'experiment_type': ['timecourse'] * len(self.experiment_files),
                                   'first_row': [str(1)] * len(self.experiment_files),
                                   'normalize_weights_per_experiment': [True] * len(self.experiment_files),
                                   'row_containing_names': [str(1)] * len(self.experiment_files),
                                   'separator': ['\t'] * len(self.experiment_files),
                                   'weight_method': ['mean_squared'] * len(self.experiment_files),
                                   'scheduled': False,
                                   'lower_bound': 0.000001,
                                   'upper_bound': 1000000,
                                   'start_value': 0.1,
                                   'save':False}


        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self.do_checks()

        self._convert_numeric_arguments_to_string()

        if self.save:
            self.model.save()

    def __str__(self):
        return "ParameterEstimation({})".format(self.to_string())

    def do_checks(self):
        """
        Validate integrity of user input
        :return:
        """
        ## ensure experiment files exist
        for fle in self.experiment_files:
            if os.path.isfile(fle)!=True:
                raise Errors.InputError('{} does not exist'.format(fle))

        ## ensure method exists
        self.method_list = ['current_solution_statistics', 'differential_evolution',
                            'evolutionary_strategy_sr', 'evolutionary_program',
                            'hooke_jeeves', 'levenberg_marquardt', 'nelder_mead',
                            'particle_swarm', 'praxis', 'random_search', 'scatter_search',
                            'simulated_annealing', 'steepest_descent', 'truncated_newton',
                            'genetic_algorithm', 'genetic_algorithm_sr']
        if self.method not in self.method_list:
            raise Errors.InputError(
                '{} not a valid method. These are valid methods: {}'.format(self.method, self.method_list))

        ## Do not randomize start values if using current solution statistics
        if self.kwargs['method'] == 'current_solution_statistics':
            if self.randomize_start_values == True:
                raise Errors.InputError(
                    'Cannot run current solution statistics with \'randomize_start_values\' set to \'true\'.')

        ## ensure metabolties are a list (even if only 1 element)
        if isinstance(self.metabolites, list) != True:
            self.metabolites = [self.metabolites]

        ## ensure global_quantities are a list (even if only 1 element)
        if isinstance(self.global_quantities, list) != True:
            self.global_quantities = [self.global_quantities]

        # ensure local_parameters are a list (even if only 1 element)
        if isinstance(self.local_parameters, list) != True:
            self.local_parameters = [self.local_parameters]

        ## ensure arguments to local parameters exist
        for i in [j.name for j in self.local_parameters]:
            if i not in [j.name for j in self.model.local_parameters]:
                raise Errors.InputError(
                    '{} not a local parameter. These are your local parameters: {}'.format(
                        i, self.model.local_parameters) )

        ## ensure arguments to metabolites exist
        for i in [j.name for j in self.metabolites]:
            if i not in [j.name for j in self.model.metabolites]:
                raise Errors.InputError(
                    '{} not a local parameter. These are your local parameters: {}'.format(
                        i,self.model.metabolites) )

        ## ensure arguments to global_quantities exist
        for i in [j.name for j in self.global_quantities]:
            if i not in [j.name for j in self.model.global_quantities]:
                raise Errors.InputError(
                    '{} not a local parameter. These are your local parameters: {}'.format(
                        i,self.model.global_quantities) )

        if self.use_config_start_values not in [True, False]:
            raise Errors.InputError(
                ''' Argument to the use_config_start_values must be \'True\' or \'False\' not {}'''.format(
                    self.use_config_start_values))

    @property
    def _experiment_mapper_args(self):
        """
        method to construct a dictionary to pass to ExperimentMapper
        :return:
        """
        kwargs_experiment={}
        kwargs_experiment['row_orientation'] = self.row_orientation
        kwargs_experiment['experiment_type'] = self.experiment_type
        kwargs_experiment['first_row'] = self.first_row
        kwargs_experiment['normalize_weights_per_experiment'] = self.normalize_weights_per_experiment
        kwargs_experiment['row_containing_names'] = self.row_containing_names
        kwargs_experiment['separator'] = self.separator
        kwargs_experiment['weight_method'] = self.weight_method
        return kwargs_experiment

    def setup(self):
        """
        Setup a parameter estimation
        :return:
        """
        EM=ExperimentMapper(self.model, self.experiment_files, **self._experiment_mapper_args)
        self.model = EM.model
        self.model=self.define_report()
        self.model=self.remove_all_fit_items()
        self.model=self.set_PE_method()
        self.model=self.set_PE_options()
        self.model=self.insert_all_fit_items()
        assert self.model != None
        return self.model

    def _select_method(self):
        """
        #determine which method to use
        :return: tuple. (str, str), (method_name, method_type)
        """
        if self.method == 'current_solution_statistics'.lower():
            method_name='Current Solution Statistics'
            method_type='CurrentSolutionStatistics'

        if self.method == 'differential_evolution'.lower():
            method_name='Differential Evolution'
            method_type='DifferentialEvolution'

        if self.method == 'evolutionary_strategy_sr'.lower():
            method_name='Evolution Strategy (SRES)'
            method_type='EvolutionaryStrategySR'

        if self.method == 'evolutionary_program'.lower():
            method_name='Evolutionary Programming'
            method_type='EvolutionaryProgram'

        if self.method == 'hooke_jeeves'.lower():
            method_name='Hooke &amp; Jeeves'
            method_type='HookeJeeves'

        if self.method == 'levenberg_marquardt'.lower():
            method_name='Levenberg - Marquardt'
            method_type='LevenbergMarquardt'

        if self.method == 'nelder_mead'.lower():
            method_name='Nelder - Mead'
            method_type='NelderMead'

        if self.method == 'particle_swarm'.lower():
            method_name='Particle Swarm'
            method_type='ParticleSwarm'

        if self.method == 'praxis'.lower():
            method_name='Praxis'
            method_type='Praxis'

        if self.method == 'random_search'.lower():
            method_name='Random Search'
            method_type='RandomSearch'

        if self.method == 'simulated_nnealing'.lower():
            method_name='Simulated Annealing'
            method_type='SimulatedAnnealing'

        if self.method == 'steepest_descent'.lower():
            method_name='Steepest Descent'
            method_type='SteepestDescent'

        if self.method == 'truncated_newton'.lower():
            method_name='Truncated Newton'
            method_type='TruncatedNewton'

        if self.method == 'scatter_search'.lower():
            method_name='Scatter Search'
            method_type='ScatterSearch'

        if self.method == 'genetic_algorithm'.lower():
            method_name='Genetic Algorithm'
            method_type='GeneticAlgorithm'

        if self.method == 'genetic_algorithm_sr'.lower():
            method_name='Genetic Algorithm SR'
            method_type='GeneticAlgorithmSR'

        return method_name, method_type

    def _convert_numeric_arguments_to_string(self):
        """
        xml requires all numbers to be strings.
        This method makes this conversion
        :return: void
        """
        self.number_of_generations=str(self.number_of_generations)
        self.population_size=str(self.population_size)
        self.random_number_generator=str(self.random_number_generator)
        self.seed=str(self.seed)
        self.pf=str(self.pf)
        self.iteration_limit=str(self.iteration_limit)
        self.tolerance=str(self.tolerance)
        self.rho=str(self.rho)
        self.scale=str(self.scale)
        self.swarm_size =str(self.swarm_size)
        self.std_deviation =str(self.std_deviation)
        self.number_of_iterations =str(self.number_of_iterations)
        self.start_temperature =str(self.start_temperature)
        self.cooling_factor =str(self.cooling_factor)
        self.lower_bound =str( self.lower_bound)
        self.start_value =str( self.start_value)
        self.upper_bound = str( self.upper_bound)

    @property
    def _report_arguments(self):
        """
        collect report specific arguments in a dict
        :return: dict
        """
        #report specific arguments
        report_dict={}
        report_dict['metabolites']=self.metabolites
        report_dict['global_quantities']=self.global_quantities
        report_dict['local_parameters']=self.local_parameters
        report_dict['quantity_type']=self.quantity_type
        report_dict['report_name']=self.report_name
        report_dict['append']=self.append
        report_dict['confirm_overwrite']=self.confirm_overwrite
        report_dict['report_type']='parameter_estimation'
        return report_dict

    def define_report(self):
        """
        create parameter estimation report
        for result collection
        :return: PyCoTools.model.Model
        """
        return Reports(self.model, **self._report_arguments).model

    def get_report_key(self):
        """
        After creating the report to collect
        results, this method gets the corresponding key
        There is probably a more efficient way to do this
        but this works...
        :return:
        """
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'].lower() == 'parameter_estimation':
                key = i.attrib['key']
        assert key != None
        return key



        # '''
        # PlotPEDataKwargs plotting specific kwargs
        # '''
        # self.PlotPEDataKwargs={}
        # self.PlotPEDataKwargs['line_width']=self.kwargs.get('line_width')
        # self.PlotPEDataKwargs['font_size']=self.kwargs.get('font_size')
        # self.PlotPEDataKwargs['axis_size']=self.kwargs.get('axis_size')
        # self.PlotPEDataKwargs['extra_title']=self.kwargs.get('extra_title')
        # self.PlotPEDataKwargs['show']=self.kwargs.get('show')
        # self.PlotPEDataKwargs['savefig']=self.kwargs.get('savefig')
        # self.PlotPEDataKwargs['title_wrap_size']=self.kwargs.get('title_wrap_size')
        # self.PlotPEDataKwargs['ylimit']=self.kwargs.get('ylimit')
        # self.PlotPEDataKwargs['xlimit']=self.kwargs.get('xlimit')
        # self.PlotPEDataKwargs['dpi']=self.kwargs.get('dpi')
        # self.PlotPEDataKwargs['xtick_rotation']=self.kwargs.get('xtick_rotation')
        # self.PlotPEDataKwargs['marker_size']=self.kwargs.get('marker_size')
        # self.PlotPEDataKwargs['legend_loc']=self.kwargs.get('legend_loc')
        # self.PlotPEDataKwargs['prune_headers']=self.kwargs.get('prune_headers')
        # self.PlotPEDataKwargs['separator']=self.kwargs.get('separator')
        # self.PlotPEDataKwargs['results_directory']=self.kwargs.get('results_directory')



    # def run(self):
    #     if self.plot==False:
    #         LOG.debug('running ParameterEstimation. Data reported to file: {}'.format(self.report_name))
    #         self.model = Run(self.model, task='parameter_estimation')
    #         self.format_results()
    #         return self.model
    #     else:
    #         ##Run with 'mode' set to false just unchecks the executable boxes.
    #         self.model = Run(self.model,task='parameter_estimation',mode=False)
    #         ## Now run with check_call
    #         os.system('CopasiSE "{}"'.format(self.model.copasi_file))
    #         self.format_results()
    #         self.plot()
    #         return self.model

    def format_results(self):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :return:
        """
        FormatPEData(self.model, self.report_name, report_type='parameter_estimation')

    @property
    def _fit_items(self):
        """
        Get existing fit items
        :return: dict
        """
        d={}
        query='//*[@name="FitItem"]'
        for i in self.model.xml.xpath(query):
            for j in list(i):
                if j.attrib['name']=='ObjectCN':
                    match=re.findall('Reference=(.*)',j.attrib['value'])[0]

                    if match=='Value':
                        match2=re.findall('Reactions\[(.*)\].*Parameter=(.*),', j.attrib['value'])
                        if match2!=[]:
                            match2='({}).{}'.format(match2[0][0],match2[0][1])

                    elif match=='InitialValue':
                        match2=re.findall('Values\[(.*)\]', j.attrib['value'])
                        if match2!=[]:
                            match2=match2[0]
                    elif match=='InitialConcentration':

                        match2=re.findall('Metabolites\[(.*)\]',j.attrib['value'])
                        if match2!=[]:
                            match2=match2[0]
                    if match2!=[]:
                        d[match2]=j.attrib
        return d

    def remove_fit_item(self,item):
        """
        Remove item from parameter estimation
        :param item:
        :return: PyCoTools.model.Model
        """
        all_items= self._fit_items.keys()
        query='//*[@name="FitItem"]'
        assert item in all_items,'{} is not a fit item. These are the fit items: {}'.format(item,all_items)
        item=self._fit_items[item]
        for i in self.model.xml.xpath(query):
            for j in list(i):
                if j.attrib['name']=='ObjectCN':
                    #locate references
                    #remove local parameters from PE task
                    match=re.findall('Reference=(.*)',j.attrib['value'])[0]
                    if match=='Value':
                        pattern='Reactions\[(.*)\].*Parameter=(.*),Reference=(.*)'
                        match2_copasiML=re.findall(pattern, j.attrib['value'])
                        if match2_copasiML!=[]:
                            match2_item=re.findall(pattern, item['value'])
                            if match2_item!=[]:
                                if match2_item==match2_copasiML:
                                    i.getparent().remove(i)

                    #rempve global parameters from PE task
                    elif match=='InitialValue':
                        pattern='Values\[(.*)\].*Reference=(.*)'
                        match2_copasiML=re.findall(pattern, j.attrib['value'])
                        if match2_copasiML!=[]:
                            match2_item=re.findall(pattern,item['value'])
                            if match2_item==match2_copasiML:
                                i.getparent().remove(i)

                    #remove IC parameters from PE task
                    elif match=='InitialConcentration' or match=='InitialParticleNumber':
                        pattern='Metabolites\[(.*)\],Reference=(.*)'
                        match2_copasiML=re.findall(pattern,j.attrib['value'])
                        if match2_copasiML!=[]:
                            if match2_copasiML[0][1]=='InitialConcentration' or match2_copasiML[0][1]=='InitialParticleNumber':
                                match2_item=re.findall(pattern,item['value'])
                                if match2_item!=[]:
                                    if match2_item==match2_copasiML:
                                        i.getparent().remove(i)
                    else:
                        raise TypeError('Parameter {} is not a local parameter, initial concentration parameter or a global parameter.initial_value'.format(match2_item))
        return self.model


    def remove_all_fit_items(self):
        """
        Iterate over all fit items and remove them
        from the parameter estimation task
        :return: PyCoTools.model.Model
        """
        for i in self._fit_items:
            self.model = self.remove_fit_item(i)
        return self.model


    def write_config_file(self):
        """
        write a parameter estimation config file to
        self.config_filename.
        :return: str. Path to config file
        """
        if (os.path.isfile(self.config_filename) == False) or (self.overwrite_config_file == True):
            self.item_template.to_csv(self.config_filename)
            LOG.debug(  'writing config template. {} set to {} and {} is {}'.format('overwrite_config_file',self.kwargs.get('overwrite_config_file'),'config_filename',self.kwargs.get('config_filename')))
        return self.config_filename

    def read_config_file(self):
        """

        :return:
        """
        if os.path.isfile(self.config_filename) != True:
            raise Errors.InputError('ConfigFile does not exist. run \'write_config_file\' method and modify it how you like then run the setup()  method again.')
        df = pandas.read_csv(self.config_filename)
        parameter_names = list(df[df.columns[0]])

        model_parameters = self.model.all_variable_names
        for parameter in parameter_names:
            if parameter not in model_parameters:
                raise Errors.InputError('{} not in {}\n\n Ensure you are using the correct PE config file!'.format(parameter, model_parameters))
        return df

    @property
    def item_template(self):
        """
        Collect information about the model in order to
        create a config file template.
        :return: pandas.DataFrame
        """

        local_params= self.model.local_parameters
        global_params = self.model.global_quantities
        metabolites = self.model.metabolites

        for i,item in enumerate(local_params):
            if item.global_name not in [j.global_name for j in self.local_parameters]:
                del local_params[i]

        for i,item in enumerate(global_params):
            if item.name not in [j.name for j in self.global_quantities]:
                del global_params[i]


        for i,item in enumerate(metabolites):
            if item.name not in [j.name for j in self.metabolites]:
                del metabolites[i]

        df_list_local=[]
        df_list_global=[]
        df_list_metabolites=[]
        for item in local_params:
            df_list_local.append(item.to_df() )

        for item in global_params:
            df_list_global.append(item.to_df())

        for item in metabolites:
            df_list_metabolites.append(item.to_df())

        metab = pandas.concat(df_list_metabolites, axis=1).transpose()
        lo = pandas.concat(df_list_local, axis=1).transpose()
        print lo
        gl = pandas.concat(df_list_global, axis=1).transpose()

        gl = gl.rename(columns={'value': 'start_value'})
        lo = lo.rename(columns={'value': 'start_value'})
        metab.drop('compartment', inplace=True, axis=1)
        metab = metab.rename(columns={'value': 'start_value'})

        if self.quantity_type == 'concentration':
            metab.drop('particle_number', axis=1, inplace=True)
            metab = metab.rename(columns={'concentration': 'start_value'})
        elif self.quantity_type == 'particle_number':
            metab.drop('concentration', axis=1, inplace=True)
            metab = metab.rename(columns={'particle_number': 'start_value'})

        gl = gl[['name', 'start_value']]
        lo = lo[['global_name', 'start_value']]
        lo = lo.rename(columns={'global_name': 'name'})
        metab = metab[['name', 'start_value']]
        df = pandas.concat([gl, lo, metab], axis=0)
        df = df.set_index('name')
        df['lower_bound']=[self.lower_bound]*df.shape[0]
        df['upper_bound']=[self.upper_bound]*df.shape[0]

        return df


    def add_fit_item(self,item):
        """
        Add fit item to model
        :param item: a row from the config template as pandas series
        :return: PyCoTools.model.Model
        """
        ##TODO check whether the new version of add_fit_item is doing what it is supposed to be doing
        ## figure out what type of variable item is and assign to component
        if item['name'] in [i.name for i in self.metabolites]:
            component = [i for i in self.metabolites if i.name == item['name']][0]

        elif item['name'] in [i.global_name for i in self.local_parameters]:
            component = [i for i in self.local_parameters if i.global_name == item['name']][0]

        elif item['name'] in [i.name for i in self.global_quantities]:
            component = [i for i in self.global_quantities if i.name == item['name']][0]
        else:
            raise Errors.SomethingWentHorriblyWrongError('{} not a metabolite, local_parameter or global_quantity'.format(item['name']))

        #initialize new element
        new_element=etree.Element('ParameterGroup', attrib={'name': 'FitItem'})
        all_items= self.read_config_file()
        # assert item in list(all_items['name']), '{} is not in your ItemTemplate. You item template contains: {}'.format(item, list(all_items.index))
        # item= all_items.loc[item]

        ##TODO include affected Cross Validation Experiments
        ##TODO include Affected Experiment options
        subA1={'name': 'Affected Cross Validation Experiments'}
        subA2={'name': 'Affected Experiments'}
        subA3={'type': 'cn',  'name': 'LowerBound',  'value': str(item['lower_bound'])}
        if self.use_config_start_values == True:
            subA5={'type': 'float',  'name': 'StartValue',  'value': str(item['start_value'])}

        subA6={'type': 'cn',  'name': 'UpperBound',  'value': str(item['upper_bound'])}
        etree.SubElement(new_element, 'ParameterGroup', attrib=subA1)
        etree.SubElement(new_element, 'ParameterGroup', attrib=subA2)
        etree.SubElement(new_element, 'Parameter',  attrib=subA3)

        if self.use_config_start_values == True:
            etree.SubElement(new_element, 'Parameter', attrib=subA5)
        etree.SubElement(new_element, 'Parameter', attrib=subA6)

        #for IC parameters
        if isinstance(component, model.Metabolite):
            if self.quantity_type == 'concentration':
                subA4={'type': 'cn',  'name': 'ObjectCN',  'value': '{},{},{}'.format(self.model.reference,
                                                                                      component.compartment.reference,
                                                                                      component.initial_reference) }
            else:
                subA4={'type': 'cn',  'name': 'ObjectCN',  'value': '{},{},{}'.format(self.model.reference,
                                                                                      component.compartment.reference,
                                                                                      component.initial_particle_reference)}

        elif isinstance(component, model.LocalParameter):
            subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{}'.format(self.model.reference,
                                                                               component.reference) }

        elif isinstance(component, model.GlobalQuantity):
            subA4={'type': 'cn',  'name': 'ObjectCN',  'value': '{},{}'.format(self.model.reference,
                                                                               component.initial_reference) }

        else:
            raise Errors.InputError('{} is not a valid parameter for estimation'.format(list(item)))

        ## add element
        etree.SubElement(new_element, 'Parameter', attrib=subA4)

        ##insert fit item

        list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        parameter_est = self.model.xml.find(list_of_tasks)[5]
        problem = parameter_est[1]
        ## TODO add support for OptimizationConstraintList --> problem[4]
        assert problem.tag == '{http://www.copasi.org/static/schema}Problem'
        optimization_item_list = problem[3]
        assert optimization_item_list.attrib.values()[0] == 'OptimizationItemList'
        optimization_item_list.append(new_element)
        return self.model

    def insert_all_fit_items(self):
        """
        insert all fit items defined in config file
        into the model
        :return:
        """
        for row in range(self.read_config_file().shape[0]):
            assert row != 'nan'
            ## feed each item from the config file into add_fit_item
            self.model = self.add_fit_item(self.read_config_file().iloc[row])
        return self.model


    def set_PE_method(self):
        '''
        Choose PE algorithm and set algorithm specific parameters
        '''
        #Build xml for method.
        method_name, method_type = self._select_method()
        method_params={'name':method_name, 'type':method_type}
        method_element=etree.Element('Method',attrib=method_params)

        #list of attribute dictionaries
        #Evolutionary strategy parametery
        number_of_generations={'type': 'unsignedInteger', 'name': 'Number of Generations', 'value': self.number_of_generations}
        population_size={'type': 'unsignedInteger', 'name': 'Population Size', 'value': self.population_size}
        random_number_generator={'type': 'unsignedInteger', 'name': 'Random Number Generator', 'value': self.random_number_generator}
        seed={'type': 'unsignedInteger', 'name': 'Seed', 'value': self.seed}
        pf={'type': 'float', 'name': 'Pf', 'value': self.pf}
        #local method parameters
        iteration_limit={'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.iteration_limit}
        tolerance={'type': 'float', 'name': 'Tolerance', 'value': self.tolerance}
        rho = {'type': 'float', 'name': 'Rho', 'value': self.rho}
        scale = {'type': 'unsignedFloat', 'name': 'Scale', 'value': self.scale}
        #Particle Swarm parmeters
        swarm_size = {'type': 'unsignedInteger', 'name': 'Swarm Size', 'value': self.swarm_size}
        std_deviation = {'type': 'unsignedFloat', 'name': 'Std. Deviation', 'value': self.std_deviation}
        #Random Search parameters
        number_of_iterations = {'type': 'unsignedInteger', 'name': 'Number of Iterations', 'value': self.number_of_iterations}
        #Simulated Annealing parameters
        start_temperature = {'type': 'unsignedFloat', 'name': 'Start Temperature', 'value': self.start_temperature}
        cooling_factor = {'type': 'unsignedFloat', 'name': 'Cooling Factor', 'value': self.cooling_factor}


        #build the appropiate xML, with method at root (for now)
        if self.method == 'current_solution_statistics':
            pass #no additional parameter elements required

        if self.method=='differential_evolution'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method=='evolutionary_strategy_sr'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
            etree.SubElement(method_element, 'Parameter', attrib=pf)

        if self.method=='evolutionary_program'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method=='hooke_jeeves'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=rho)

        if self.method=='levenberg_marquardt'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
#
        if self.method=='nelder_mead'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
            etree.SubElement(method_element,'Parameter',attrib=scale)

        if self.method=='particle_swarm'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=swarm_size)
            etree.SubElement(method_element,'Parameter',attrib=std_deviation)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)

        if self.method=='praxis'.lower():
            etree.SubElement(method_element,'Parameter',attrib=tolerance)

        if self.method=='random_search'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_iterations)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)

        if self.method=='simulated_annealing'.lower():
            etree.SubElement(method_element,'Parameter',attrib=start_temperature)
            etree.SubElement(method_element,'Parameter',attrib=cooling_factor)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)
#
        if self.method=='steepest_descent'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
#
        if self.method=='truncated_newton'.lower():
            #required no additonal paraemters
            pass
#
        if self.method=='scatter_search'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_iterations)


        if self.method=='genetic_algorithm'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_generations)
            etree.SubElement(method_element,'Parameter',attrib=population_size)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)

        if self.method=='genetic_algorithm_sr'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_generations)
            etree.SubElement(method_element,'Parameter',attrib=population_size)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)
            etree.SubElement(method_element,'Parameter',attrib=pf)


        tasks=self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')

        method= tasks[5][-1]
        parent=method.getparent()
        parent.remove(method)
        parent.insert(2,method_element)
        return self.model

    def set_PE_options(self):
        """
        Set parameter estimation sepcific arguments
        :return: PyCoTools.model.Model
        """


        scheluled_attrib={'scheduled': self.scheduled,
                          'updateModel': self.update_model}

        report_attrib={'append': self.append,
                       'reference': self.get_report_key(),
                       'target': self.report_name,
                       'confirmOverwrite': self.confirm_overwrite}


        randomize_start_values={'type': 'bool',
                                'name': 'Randomize Start Values',
                                'value': self.randomize_start_values}

        calculate_stats={'type': 'bool', 'name': 'Calculate Statistics', 'value': self.calculate_statistics}
        create_parameter_sets={'type': 'bool', 'name': 'Create Parameter Sets', 'value': self.create_parameter_sets}

        query='//*[@name="Parameter Estimation"]' and '//*[@type="parameterFitting"]'
        for i in self.model.xml.xpath(query):
            i.attrib.update(scheluled_attrib)
            for j in list(i):
                if self.report_name != None:
                    if 'append' in j.attrib.keys():
                        j.attrib.update(report_attrib)
                if list(j)!=[]:
                    for k in list(j):
                        if k.attrib['name']=='Randomize Start Values':
                            k.attrib.update(randomize_start_values)
                        elif k.attrib['name']=='Calculate Statistics':
                            k.attrib.update(calculate_stats)
                        elif k.attrib['name']=='Create Parameter Sets':
                            k.attrib.update(create_parameter_sets)
        return self.model

    def run(self):
        """
        Run the parameter estimation using the Run class
        :return:
        """
        Run(self.model, mode= False, task='parameter_estimation')




    # def plot(self):
    #     self.PL=PEAnalysis.PlotPEData(self.copasi_file,self.experiment_files,self.kwargs.get('report_name'),
    #                     **self.PlotPEDataKwargs)




class MultiParameterEstimation(ParameterEstimation):
    '''

    '''
    ##TODO Merge ParameterEstimation and Multi into one class.
    def __init__(self, model, experiment_files,**kwargs):
        super(MultiParameterEstimation, self).__init__(model, experiment_files, **kwargs)

        self.default_properties.update({'copy_number': 1,
                                 'pe_number':1,
                                 'run_mode': 'multiprocess',
                                 'results_directory':os.path.join(os.path.dirname(self.model.copasi_file),'MultipleParameterEstimationResults'),
                                 'copasi_file_pickle': os.path.join(os.path.dirname(self.model.copasi_file), 'copasi_paths.pickle')
                                 })

        ## cannot use self.check_integrity as as inherit from
        ## parameter estimation and add new arguments not in the
        ## base class.
        # for property in self.kwargs:
        #     print property
            # if property not in self.default_properties.keys()
        # self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.do_checks()




        self._create_output_directory()
        self.report_files=self.enumerate_PE_output()
        self.output_in_subtask = True

    def __str__(self):
        return 'MultiParameterEstimation({})'.format(self.to_string())

    def check_integrity(self, allowed, given):
        """
        Method to raise an error when a wrong
        kwarg is passed to a subclass
        :param: allowed. List of allowed kwargs
        :param: given. List of kwargs given by user or default
        :return: 0
        """
        for key in given:
            if key not in allowed:
                raise Errors.InputError('{} not in {}'.format(key, allowed))

    def do_checks(self):
        """

        :return:
        """
        pass

    def format_results(self):
        """
        Copasi output does not have headers. This function
        gives PE data output headers
        :return: list. Path to report files
        """
        try:
            cps_keys = self.sub_copasi_files.keys()
        except AttributeError:
            self.setup()
            cps_keys = self.sub_copasi_files.keys()
        report_keys = self.report_files.keys()
        for i in range(len(self.report_files)):
            try:
                FormatPEData(self.sub_copasi_files[cps_keys[i]], self.report_files[report_keys[i]],
                         report_type='multi_parameter_estimation')
            except Errors.InputError:
                LOG.warning('{} is empty. Cannot parse. Skipping this file'.format(self.report_files[report_keys[i]]))
                continue
        return self.report_files

    def setup(self):
        """
        Analogous to the set_up method of the ParameterEstimation class but this time
        setup both the PE and Scan tasks
        :return:
        """

        EM = ExperimentMapper(self.model, self.experiment_files, **self._experiment_mapper_args)
        self.model = EM.model
        self.model = self.define_report()
        self.model = self.remove_all_fit_items()
        self.model = self.set_PE_method()
        self.model = self.set_PE_options()
        self.model = self.insert_all_fit_items()
        assert self.model != None
        ## need to save before copy
        self.model.save()
        ## TODO modify copy copasi to write copasi. Since the change, we can simply write multiple coapsi files rather than copying
        self.sub_copasi_files=self.copy_copasi()
        self._setup_scan()
        return self.model

    def run(self):
        """

        :return:
        """
        ##load cps from pickle in case run not being use straignt after set_up
        if self.run == 'SGE':
            try:
                check_call('qhost')
            except Errors.NotImplementedError:
                LOG.warning('Attempting to run in SGE mode but SGE specific commands are unavailable. Switching to \'multiprocess\' mode')
                self.run = 'multiprocess'
        if os.path.isfile(self.copasi_file_pickle):
            with open(self.copasi_file_pickle) as f:
                self.sub_copasi_files=pickle.load(f)
        for i in self.sub_copasi_files:
            LOG.info('running model: {}'.format(i))
            Run(self.sub_copasi_files[i], mode=self.run_mode ,task='scan')

    def copy_copasi(self):
        '''
        Copy copasi files m times to run separetly on a single
        computer

        returns:
            dict[model_number]=cps_file
        '''
        LOG.debug('Copying copasi file {} times'.format(self.copy_number))
        sub_copasi_files_dct={}
        copasi_path,copasi_filename=os.path.split(self.model.copasi_file)
        for i in range(1,self.copy_number):
            new_cps=os.path.join(copasi_path,copasi_filename[:-4]+'_{}.cps'.format(str(i)))
            shutil.copy(self.copasi_file,new_cps)
            sub_copasi_files_dct[i]= new_cps
        sub_copasi_files_dct[0]=self.model.copasi_file

        with open(self.copasi_file_pickle,'w')as f:
            pickle.dump(sub_copasi_files_dct,f)

        return sub_copasi_files_dct

    ##void
    def _setup_scan(self):
        '''
        Set up n repeat items with number_of_steps repeats of parameter estimation
        Set run to false as we want to use the multiprocess mode of the run class
        to process all m files at once in CopasiSE

        Remember scan needs iterating over because each file needs an unique report
        name
        '''

        q=Queue.Queue()
        for num in range(self.copy_number):
            LOG.debug('setting up scan for model : {}'.format(self.sub_copasi_files[num]))
            t=threading.Thread(target=self._setup1scan,
                               args =  (q, self.sub_copasi_files[num] , self.report_files[num])  )
            t.daemon=True
            t.start()
            time.sleep(0.1)

        s=q.get()
        ## Since this is being executed in parallel sometimes
        ## we get process clashes. Not sure exactly whats going on
        ## but introducing a small delay seems to fix
        time.sleep(0.1)
        return 0



    ## void
    def _setup1scan(self,q,cps,report):
        '''

        '''
#        LOG.info('setting up scan for model number {}'.format(num))
        start=time.time()
        q.put(Scan(cps,
             scan_type='repeat',
             number_of_steps=self.pe_number,
             subtask='parameter_estimation',
             report_type='multi_parameter_estimation',
             report_name=report,
             run_mode=False,
             append = self.append,
             confirm_overwrite = self.confirm_overwrite,
             output_in_subtask = self.output_in_subtask,
             save=True) )
        LOG.debug('Setup Took {} seconds'.format(time.time() - start))
#
    ##void
    def _do_checks(self):
        '''

        '''
        run_arg_list=['multiprocess','SGE']
        if self.run_mode not in run_arg_list:
            raise Errors.InputError('run needs to be one of {}'.format(run_arg_list))

        if isinstance(self.copy_number,int)!=True:
            raise Errors.InputError('copy_number argument is of type int')

        if isinstance(self.kwargs['pe_number'],int)!=True:
            raise Errors.InputError('pe_number argument is of type int')

        if self.results_directory==None:
            self.results_directory = 'MultipleParameterEsimationAnalysis'
        self.results_directory = os.path.abspath(self.results_directory)


    def _create_output_directory(self):
        '''

        '''
        LOG.debug('creating a directory for analysis in : \n\n{}'.format(self.results_directory))
        if os.path.isdir(self.results_directory)!=True:
            os.mkdir(self.results_directory)
#


    def enumerate_PE_output(self):
        '''
        Create a filename for each file to collect PE results

        Returns:
            dct['model_copy_number]=enumerated_report_name
        '''
        LOG.debug('Enumerating PE report files')
        dct={}
        dire,fle=os.path.split(self.report_name)
        for i in range(self.copy_number):
            new_file=os.path.join(self.results_directory,
                                  fle[:-4]+'{}.txt'.format(str(i)))
            dct[i]=new_file
        return dct


class MultiModelFit():
    '''
    Coordinate a systematic multi model fitting parameter estimation and
    compare results using AIC/BIC.

    Usage:
        1):
            Setup a new folder containing all models that you would like to fit
            and all data you would like to fit to the model. Do not have any
            other text or csv files in this folder as python will try and setup
            fits for them. Data files must have 'Time' in the left column
            and each subsequent column must be titled with a variable name mapping
            to a model entity exactly (watch out for trailing spaces). It is
            reccommended to supply a plain text file detailing the common
            component between the models and what is different between each model.
            This however should not be saved as a .txt file or python will
            try and map it to the models. Just save the 'ReadMe' without an extention
            to avoid this problem.

                i.e.:
                    ./project_dir
                        --Exp data 1
                        --Exp data n
                        --model1.cps
                        --model2.cps

        2):
            Instantiate instance of the MultimodelFit class with all relevant
            keywords. Relevant keywords are described in the ParameterEstimation
            or runMultiplePEs classes. As non-optional arguments this takes the absolute path
            to the project directory that you created in step 1.
            Python automatically creates subdirectories  for each model in your
            model selection problem and maps all data files in the main directory
            to each of the models.
        3):
            Use the write_item_template() method to create a spreadsheet containing
            your a config file with it instructions. By default, all ICs and all kinetic (global or local)
            parameters are included. Delete entries that you would like to keep fixed. Do not
            modify the last columns which contain xml code for that variable.
        4):
            Once each model folder has a config file specific for that model
            use the setup()() method. Then open one of the child copasi files
            in order to check that things are configured how you'd like them before
            using the run() method.


        **kwargs:
            copy_number:
                Default = 1. This is how many times to copy a copasi file before
                running the parameter estimation on each model.
            pe_number:
                Default = 3. How many parameter estimations to perform in one model.
                i.e. a repeat scan task is automatically configured.

            All other kwargs are described in runMultiplePEs or ParameterEstimation
    '''
    def __init__(self,project_config,**kwargs):
        self.project_dir=project_config
#        self.config_filename=config_filename
        self.do_checks()
        self.cps_files,self.exp_files=self.read_fit_config()

#        if self.config_filename==None:
#            self.config_filename=os.path.join(self.project_dir,'PEConfigFile.xlsx')

        options={'run':'multiprocess',
                 'copy_number':1,
                 'pe_number':3,
                 'report_name':None,
                 'results_directory':None,
                 ##default parameters for ParameterEstimation
                 'method':'GeneticAlgorithm',
                 'plot':False,
                 'quantity_type':'concentration',
                 'append': False,
                 'confirm_overwrite': False,
                 'config_filename':'PEConfigFile.xlsx',
                 'overwrite_config_file':False,
                 'prune_headers':True,
                 'update_model':False,
                 'randomize_start_values':True,
                 'create_parameter_sets':False,
                 'calculate_statistics':False,
                 'use_config_start_values':False,
                 #method options
                 #'DifferentialEvolution',
                 'number_of_generations':200,
                 'population_size':50,
                 'random_number_generator':1,
                 'seed':0,
                 'pf':0.475,
                 'iteration_limit':50,
                 'tolerance':0.0001,
                 'rho':0.2,
                 'scale':10,
                 'swarm_size':50,
                 'std_deviation':0.000001,
                 'number_of_iterations':100000,
                 'start_temperature':1,
                 'cooling_factor':0.85,
                 #experiment definition options
                 #need to include options for defining multiple experimental files at once
                 'row_orientation':[True]*len(self.exp_files),
                 'experiment_type':['timecourse']*len(self.exp_files),
                 'first_row':[str(1)]*len(self.exp_files),
                 'normalize_weights_per_experiment':[True]*len(self.exp_files),
                 'row_containing_names':[str(1)]*len(self.exp_files),
                 'separator':['\t']*len(self.exp_files),
                 'weight_method':['mean_squared']*len(self.exp_files),
                 'save':'overwrite',
                 'scheduled':False,
                 'lower_bound':0.000001,
                 'upper_bound':1000000}

        for key in kwargs.keys():
            if key not in options.keys():
                raise Errors.InputError('{} is not a keyword argument for MultiModelFit'.format(key))
        options.update( kwargs)
        self.kwargs=options


        self.sub_cps_dirs=self.create_workspace()
        self.RMPE_dct=self.instantiate_run_multi_PEs_class()
        self.results_folder_dct=self.get_output_directories()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value

    def instantiate_run_multi_PEs_class(self):
        '''
        pass correct arguments to the runMultiplePEs class in order
        to instantiate a runMultiplePEs instance for each model.

        Reutrns:
            dict[model_filename]=runMultiplePEs_instance
        '''
        LOG.debug('instantiating an instance of runMultiplePEs for each model')
        dct={}

        for cps_dir in self.sub_cps_dirs:
            os.chdir(cps_dir)
            if os.path.isabs(self.kwargs['config_filename']):
                self.kwargs['config_filename']=os.path.split(self.kwargs['config_filename'])[1]
            dct[self.sub_cps_dirs[cps_dir]]=MultiParameterEstimation(self.sub_cps_dirs[cps_dir],
                                                           self.exp_files,**self.kwargs)

        LOG.debug('Each instance of MultiParameterEstimation is being held in a dct:\n{}'.format(dct))
        return dct

    def get_output_directories(self):
        '''
        Returns the location of the parameter estimation output files
        produced from the analysis.
        '''
        LOG.debug('getting output directories')
        output_dct={}
        for RMPE in self.RMPE_dct:
            LOG.debug('output directory for model \n{}:'.format(RMPE))
            LOG.debug('\t\t'+self.RMPE_dct[RMPE].kwargs['results_directory'])
            output_dct[RMPE]=self.RMPE_dct[RMPE].kwargs['results_directory']
        return output_dct

    #void
    def write_config_file(self):
        '''
        A class to write a config file template for each
        model in the analysis. Calls the corresponding
        write_config_file from the runMultiplePEs class
        ===returns===
        list of config files
        '''
        conf_list=[]
        for RMPE in self.RMPE_dct:
            f = self.RMPE_dct[RMPE].write_config_file()
            conf_list.append(f)
        return conf_list

    def setup(self):
        '''
        A user interface class which calls the corresponding
        method (setup) from the runMultiplePEs class per model.
        Perform the ParameterEstimation.setup() method on each model.

        '''
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].setup()

    def set_up_dep(self):
        '''
        A user interface class which calls the corresponding
        method (set_up) from the runMultiplePEs class per model.
        Perform the ParameterEstimation.set_up() method on each model.

        '''
        LOG.warning('The set_up method is deprecated. Use setup() method instead')
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].set_up()


    def run(self):
        '''
        A user interface class which calls the corresponding
        method (run) from the runMultiplePEs class per model.
        Perform the ParameterEstimation.run() method on each model.
        '''
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].run()


    def do_checks(self):
        '''
        Function to check the integrity of the input given by user
        '''
        pass


    def create_workspace(self):
        '''
        Creates a workspace from cps and experiment files in self.project_dir

        i.e.
            --project_dir
            ----model1_dir
            ------model1.cps
            ------exp_data.txt
            ----model2_dir
            ------model2.cps
            ------exp_data.txt

        returns:
            Dictionary[cps_filename]=DirectoryForCpsAnalysis
        '''
        LOG.info('Creating workspace from project_dir')
        LOG.debug('Creating Workspace from files in: \n{}'.format(self.project_dir))
        ## Create entire working directory for analysis
        self.wd=self.project_dir

        LOG.debug('New Working directory is:\n{}'.format(self.wd))
        if os.path.isdir(self.wd)!=True:
            LOG.debug('{} doesn\' already exist. Creating {}'.format(self.wd,self.wd))
            os.mkdir(self.wd)
        os.chdir(self.project_dir)
        LOG.debug('changing directory to project_dir: \n({}) to read relevent .cps and exp files'.format(self.wd))
        LOG.debug('Creating a directory in working directory for each of the model files')

        cps_dirs={}

        for cps in self.cps_files:
            cps_abs=os.path.abspath(cps)
            cps_filename=os.path.split(cps_abs)[1]
            sub_cps_dir=os.path.join(self.wd,cps_filename[:-4])
            if os.path.isdir(sub_cps_dir)!=True:
                os.mkdir(sub_cps_dir)
            sub_cps_abs=os.path.join(sub_cps_dir,cps_filename)
            shutil.copy(cps_abs,sub_cps_abs)
            if os.path.isfile(sub_cps_abs)!=True:
                raise Exception ('Error in copying copasi file to sub directories')
            cps_dirs[sub_cps_dir]=sub_cps_abs
        LOG.info('Workspace created')
        return cps_dirs
#

    def read_fit_config(self):
        '''
        The recommed way to use this class:
            Put all .cps files you want to fit in a folder with meaningful names (pref with no spaces)
            Put all data files for fitting in the same folder.
                Make sure all data files have left most column as Time (with consistent units)
                and all other columns corresponding exactly (no trailing white spaces) to model variables.
                Any independent variables should have the '_indep' suffix
        This function will read this multifit config and produce a directory tree for subsequent analysis
        '''
        LOG.debug('Reading fit configuration')
        if self.project_dir==None:
            raise Errors.InputError('Cannot read multifit confuration as no Project kwarg is provided')
        ##make sure we're in the right directory
        os.chdir(self.project_dir)
        cps_list=[]
        LOG.debug('These are the cps files in your fit config:')
        for cps_file in glob.glob('*.cps'):
            LOG.debug('''{}'''.format(cps_file))
            cps_list.append(cps_file)

        LOG.debug('These are the experiment files in your fit config:')
        exp_list=[]
        exp_file_types=('*.csv','*.txt')
        for typ in exp_file_types:
            for exp_file in glob.glob(typ):
                LOG.debug('''{}'''.format(exp_file))
                exp_list.append(os.path.abspath(exp_file))

        if cps_list==[]:
            raise Errors.InputError('No cps files in your project')
        if exp_list==[]:
            raise Errors.InputError('No experiment files in your project')
        return cps_list,exp_list


    def format_data(self):
        """
        Method for giving appropiate headers to parameter estimation data
        """
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].format_results()


class InsertParameters():
    '''
    Insert parameters from a file, dictionary or a pandas dataframe into a copasi
    file.

    Positional Arguments:

        copasi_file:
            The copasi file you want to enter parameters into

    **Kwargs
        index:
            index of parameter estimation run to input into the copasi file.
            The index is ordered by rank of best fit, with 0 being the best.
            Default=0

        quantity_type:
            Either 'particle_number' or 'concentration'. Default='concentration'

        report_name;
            Unused. Delete?

        save:
            either False,'overwrite' or 'duplicate',default=overwrite

        parameter_dict:
            A python dictionary with keys correponding to parameters in the model
            and values the parameters (dict[parameter_name]=parameter value).
            Default=None

        df:
            A pandas dataframe with parameters being column names matching
            parameters in your model and RSS values and rows being individual
            parameter estimationruns. In this case, ensure you have set the
            index parameter to the index you want to use. Dataframes are
            automatically sorted by the RSS column.

        parameter_path:
            Full path to a parameter estimation file ('.txt','.xls','.xlsx' or
            '.csv') or a folder containing parameter estimation files.

    '''
    def __init__(self,copasi_file,**kwargs):
        '''
        coapsi_file = file you want to insert
        kwargs:
            index: If not specified default to -1
                    can be int or list of ints
        '''
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
        self.GMQ=GetModelQuantities(self.copasi_file)

        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt'
        options={#report variables
                 'metabolites':self.GMQ.get_IC_cns().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'quantity_type':'concentration',
                 'report_name':default_report_name,
                 'save':'overwrite',
                 'index':0,
                 'parameter_dict':None,
                 'df':None,
                 'parameter_path':None,
                 }

        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for InsertParameters'.format(i)
        options.update( kwargs)
        self.kwargs=options
        self.kwargs = Bool2Str(self.kwargs).convert_dct()

        LOG.debug('These are kwargs {}'.format(self.kwargs))

#        assert os.path.exists(self.parameter_path),'{} doesn\'t exist'.format(self.parameter_path)
        assert self.kwargs.get('quantity_type') in ['concentration','particle_numbers']
        if self.kwargs.get('parameter_dict') != None:
            if isinstance(self.kwargs.get('parameter_dict'),dict)!=True:
                raise Errors.InputError('Argument to \'parameter_dict\' keyword needs to be of type dict')
            for i in self.kwargs.get('parameter_dict').keys():
                if i not in self.GMQ.get_all_model_variables().keys():
                    raise Errors.InputError('Parameter \'{}\' is not in your model. \n\nThese are in your model:\n{}'.format(i,sorted(self.GMQ.get_all_model_variables().keys())))

        if self.kwargs.get('parameter_dict')==None and self.kwargs.get('parameter_path')==None and self.kwargs.get('df') is None:
            raise Errors.InputError('You need to give at least one of parameter_dict,parameter_path or df keyword arguments')

        assert isinstance(self.kwargs.get('index'),int)


        #make sure user gives the right number of arguments
        num=0
        if self.kwargs.get('parameter_dict')!=None:
            num+=1
        if self.kwargs.get('df') is not None:
            num+=1
        if self.kwargs.get('parameter_path')!=None:
            num+=1
        if num!=1:
            raise Errors.InputError('You need to supply exactly one of parameter_dict,parameter_path or df keyord argument. You cannot give two or three.')

        self.parameters=self.get_parameters()
        self.parameters= self.replace_gl_and_lt()
#        self.insert_locals()
        self.insert_all()
        #change

    def check_parameter_consistancy(self,df):
        '''
        raise an error if no parameters in the PE header match
        parameters in model

        args:
            df:
                containing parameters to compare with parameters
                in the model
        '''
        model_parameter_names= set(self.GMQ.get_all_model_variables().keys())
        input_parameter_names= set(list(df.keys()))
        intersection=list( model_parameter_names.intersection(input_parameter_names))
        if intersection==[]:
            raise Errors.ParameterInputError('''The parameters in your parameter estimation data are not in your model.\
Please check the headers of your PE data are consistent with your model parameter names.''' )

    def get_parameters(self):
        '''
        Get parameters depending on the type of input.
        Converge on a pandas dataframe.
        Columns = parameters, rows = parameter sets

        Use check parameter consistency to see
        whether headers have been pruned or not. If not try pruning them
        '''
        if self.kwargs.get('parameter_dict')!=None:
            assert isinstance(self.kwargs.get('parameter_dict'),dict),'The parameter_dict argument takes a Python dictionary'
            for i in self.kwargs.get('parameter_dict'):
                assert i in self.GMQ.get_all_model_variables().keys(),'{} is not a parameter. These are your parameters:{}'.format(i,self.GMQ.get_all_model_variables().keys())
            return pandas.DataFrame(self.kwargs.get('parameter_dict'),index=[0])

        if self.kwargs.get('parameter_path')!=None:
            PED=PEAnalysis.ParsePEData(self.kwargs.get('parameter_path'))
            if isinstance(self.kwargs.get('index'),int):
                return pandas.DataFrame(PED.data.iloc[self.kwargs.get('index')]).transpose()
            else:
                return PED.data.iloc[self.kwargs.get('index')]
        if self.kwargs.get('df') is not None:
            df= pandas.DataFrame(self.kwargs.get('df').iloc[self.kwargs.get('index')]).transpose()
            self.check_parameter_consistancy(df)
        # except Errors.ParameterInputError:
        #     df=PruneCopasiHeaders(df).prune()
        #     self.check_parameter_consistancy(df)
        return df

    def insert_locals(self):
        '''

        '''
        ## get local parameters
        local=sorted(self.GMQ.get_local_kinetic_parameters_cns().keys())
        ## remove local parameters from complete list depending on whether
        ## user wants to insert anything for that parameter or not
        local= [i for i in self.parameters if i in local]
        LOG.debug('Local parameters being inserted into model: {}'.format(local))
        ## create a dict[parameter]=reactiontype dict to help
        ## navidate the xml
        local_dct={}
        for full_param in local:
            local_dct[full_param]={}
            k,v = re.findall(  '\((.*)\)\.(.*)', full_param ) [0]
            local_dct[full_param][k] = v

        LOG.debug('Constructing a dict of reaction:parameter for local parameters: {}'.format(local_dct))

        ## Iterate over all local parameters that we want to insert
        ## Identify the list of reactions ,match for the current reaction
        ## bore into that reaction to locate the locally defined rate constant
        ## match with the parameter then insert the str(float(*.)) representation
        ## of the parameter value into the value attribute for the constant
        ## element
        for key in local_dct:
            for reaction_name, parameter_name in local_dct[key].items():
                for element_tags in self.copasiML.iter():
                    if  element_tags.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                        for reaction in element_tags:
                            if reaction.attrib['name'] == reaction_name:
                                for reaction_element in reaction:
                                    if reaction_element.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                                        for constant_xml in reaction_element:
                                            if constant_xml.attrib['name'] == parameter_name:
                                                constant_xml.attrib['value'] = str(float(self.parameters['({}).{}'.format(reaction_name,parameter_name)]))
        return self.copasiML

    def assemble_state_values(self):
        """

        """
        LOG.debug('States:\t {}'.format( self.GMQ.get_state_template()))
        state_values = []
        count = 0
        for state in self.GMQ.get_state_template():
            #LOG.debug('assembling parameter {} out of {}'.format(count,len(self.GMQ.get_state_template())))
            count+=1
            model = re.findall('(Model)_',state)
            metab = re.findall('Metabolite',state)
            mod_value = re.findall('ModelValue',state)
            compartment = re.findall('Compartment',state)
            if model !=[]:
                LOG.debug('State {} is model'.format(state))
                assert metab == []
                assert mod_value == []
                assert compartment ==[]
                state_values.append(str(0))
                LOG.debug('Added 0 for first parameter in sequence')
            elif metab !=[]:
                LOG.debug('State {} is metab'.format(state))
                assert model == []
                assert mod_value == []
                assert compartment == []
                metab_name= self.GMQ.get_metabolites_object_reference()[state]
#                    print self.parameters[metab_name]
                metab =  self.GMQ.get_IC_cns()[metab_name]
                comp_vol = self.GMQ.get_IC_cns()[metab_name]['compartment_volume']

                metab_val = self.GMQ.get_IC_cns()[metab_name]['value']
                #LOG.debug('Metab dict for {}, \n\n{}'.format(state,self.GMQ.get_IC_cns()[metab_name]))

                if metab_name in self.parameters:
                    metab_val =  self.GMQ.convert_molar_to_particles(float(self.parameters[metab_name]),
                                                          self.GMQ.get_quantity_units(),
                                                          float(comp_vol))
                state_values.append(str(float(metab_val)))

            elif mod_value !=[]:
                LOG.debug('State {} is Global variable'.format(state))

                assert model == []
                assert metab == []
                assert compartment == []
                mod_value_name = self.GMQ.get_global_object_reference()[state]
                mod_value_value = self.GMQ.get_global_quantities()[mod_value_name]
                if mod_value_name in self.parameters.keys():
                    mod_value_value=str(float(self.parameters[mod_value_name]))
                state_values.append(mod_value_value)

            elif compartment != []:
                '''
                Warning: A potential bug may exist where if some metabolites are
                calculated before the compartment is changed then other after, 
                we'll get metabolites with inconsident volumes. This will be 
                rare as I don't generally estimate the compartment volumes 
                but if you are then this could be a problem. 
                '''
                assert model ==[]
                assert metab == []
                assert mod_value == []
                compartment_name = self.GMQ.get_compartment_object_reference()[state]
                compartment_value = self.GMQ.get_compartments()[compartment_name]['value']
                if compartment_name in self.parameters.keys():
                    compartment_value = str(float(self.parameters[compartment_name]))
                state_values.append(compartment_value)

#        if len(state_values)!=len(self.GMQ.get_state_template()):
#            raise Exception('For some reason the number of state values does not equal the number of global + IC parameters in yoru model')
        return state_values

    def insert_ICs(self):
        IC=self.GMQ.get_IC_cns()
        for i in IC:
            query='//*[@cn="{}"]'.format( self.GMQ.get_IC_cns()[i]['cn'])
            for j in self.copasiML.xpath(query):
                if i in self.parameters.keys() and j.attrib['simulationType']=='reactions':
                    if self.kwargs.get('quantity_type')=='concentration':
                        particles=self.GMQ.convert_molar_to_particles(float(self.parameters[i]),self.GMQ.get_quantity_units(),float(IC[i]['compartment_volume']))#,self.GMQ.get_volume_unit())
##                        particles=self.parameters[i]
                    elif self.kwargs.get('quantity_type')=='particle_numbers':
                        particles=self.parameters[i]
                    j.attrib['value']=str(float(particles))
        return self.copasiML
    
    def insert_global_and_ICs(self):
        """
        
        """
        def reduce_str(y,z):
            return '{} {}'.format(y,z)
        values=reduce(reduce_str,self.assemble_state_values())
        query = '//*[@type="initialState"]'
        for i in self.copasiML.xpath(query):
            i.text = values
        return self.copasiML
                    
    def insert_global(self):
        glob= self.GMQ.get_global_quantities_cns().keys()
        for i in glob:
            query='//*[@cn="{}"]'.format( self.GMQ.get_global_quantities_cns()[i]['cn'])
            for j in self.copasiML.xpath(query):
                if i in self.parameters.keys() and j.attrib['SimulationType']!='assignment':
                    j.attrib['value']=str(float(self.parameters[i]))
        return self.copasiML




    def insert_fit_items(self):
        '''
        insert parameters into fit items
        '''
        copasiML=self.copasiML
        query="//*[@name='OptimizationItemList']"
        ICs_and_global=None
        reaction=None
        parameter=None
        for i in copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='ObjectCN':
                        pattern1='Vector=(?!Reactions).*\[(.*)\]'#match global and IC parameters but not local
                        search1= re.findall(pattern1,k.attrib['value'])
                        
                        if search1 !=[]:
                            ICs_and_global=search1[0]
                    if k.attrib['name']=='StartValue':
                        if ICs_and_global !=None:
                            if ICs_and_global in self.parameters.keys():
                                k.attrib['value']=str(float(self.parameters[ICs_and_global]))
                    #now again for local parameters
                    if k.attrib['name']=='ObjectCN':
                        pattern2='Vector=Reactions\[(.*)\].*Parameter=(.*),'
                        search2= re.findall(pattern2,k.attrib['value'])

                        if search2!=[]:
                            reaction,parameter= search2[0]
                            local= '({}).{}'.format(reaction,parameter)
                    if k.attrib['name']=='StartValue':
                        if reaction != None and parameter !=None:
                            if local in self.parameters.keys():
                                k.attrib['value']=str(float(self.parameters[local]))
                            else:
                                continue
        return self.copasiML

        


    def replace_gl_and_lt(self):
        '''
        replace greater than and less than symbols for xML purposes
        '''
        l=[]
        for i in self.parameters.keys():
            i= i.replace('<','\<')
            i=i.replace('>','\>')
            l.append(i)
        self.parameters.columns=pandas.Index(l)
        return self.parameters
            
        
    def insert_all(self):
        self.copasiML=self.insert_locals()
        self.copasiML = self.insert_global_and_ICs()
        self.copasiML=self.insert_fit_items()
        self.save()
        
    def save(self):
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML


class HighThroughputFit():
    """
    The aim of this class is to build a way
    of fitting high throughput data sets to
    a single abstract model.

    The reason this class is being built is
    to model microarray data with an abstract
    model of transcription. In principle this
    idea can be extended to other models and data
    
    Just an idea t the moment. not implemented
    """

    def __init__(self,abstract_model_file):
        self.abstract_model_file = abstract_model_file


if __name__=='__main__':
    pass
#    execfile('/home/b3053674/Documents/Models/2017/08_Aug/PyCoToolsTests/RunPEs.py')
        #    execfile('/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/testing_kholodenko_manually.py')
