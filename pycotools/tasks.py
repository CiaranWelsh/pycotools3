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
import viz,errors, misc, _base, model
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap
import string
import itertools
from  multiprocessing import Process, cpu_count
import glob
import seaborn as sns
from copy import deepcopy
from subprocess import check_call
from collections import OrderedDict
from mixin import Mixin, mixin

## TODO use generators when iterating over a function with another function. i.e. plotting


LOG=logging.getLogger(__name__)
sns.set_context(context='poster',
                font_scale=3)

## TODO change pycopi to tasks


class GetModelVariableFromStringMixin(Mixin):
    @staticmethod
    def get_variable_from_string(m, v):
        """
        Use model entity name to get the
        pycotools variable
        :param m:
            :py:class:`model`

        :param v:
            `str` variable in model

        :return:
            variable as a model component
        """
        if not isinstance(m, model.Model):
            raise errors.InputError('expected model.Model but got "{}" instance'.format(
                type(m)
            ))
        if not isinstance(v, str):
            raise errors.InputError('variable_name should be a string')
        ## allow a user to input a string not pycotools.model class
        if isinstance(v, str):
            if v in [i.name for i in m.metabolites]:
                v = m.get('metabolite', v, by='name')

            elif v in [i.name for i in m.compartments]:
                v = m.get('compartments', v, by='name')

            elif v in [i.name for i in m.global_quantities]:
                v = m.get('global_quantity', v, by='name')

            elif v in [i.global_name for i in m.local_parameters]:
                v = m.get('local_parameter', v, by='global_name')

            else:
                assignments = m.get(
                    'local_parameter', 'assignment', by='simulation_type'
                )
                raise errors.InputError('Variable "{}" is not in model. '
                                        'These are your model variables: '
                                        '{} and these are local_parameters '
                                        'with global_quantities assigned '
                                        'to them: "{}"'.format(v, m.all_variable_names,
                                                             [i.global_name for i in assignments]))
        assert isinstance(v, str) != True
        return v

class UpdatePropertiesMixin(Mixin):

    def update_properties(self, kwargs):
        """
        method for updating properties from kwargs

        :param kwargs: dict of options for subclass
        :return: void
        """
        for k in kwargs:
            try:
                getattr(self, k)
                setattr(self, k, kwargs[k])
            except AttributeError:
                setattr(self, k, kwargs[k])

class Bool2Numeric(Mixin):
    """
    CopasiML uses 1's and 0's for True or False in some
    but not all places. When one of these options
    is required by the user and is specified as bool,
    this class converts them into 1's or 0's.

    Use this method in early on in constructor for
    all subclasses where this applies.
    """
    @staticmethod
    def convert_bool_to_numeric(dct):
        """
        :param:
            `dict`.  __dict__ or kwargs or options

        :return:
            `dict` with certain boolean args as 1's and 0's
        """
        lst = ['append',
               'confirm_overwrite',
               'output_event',
               'scheduled',
               'automatic_step_size',
               'start_in_steady_state',
               'output_event',
               'start_in_steady_state',
               'integrate_reduced_model',
               'use_random_seed',
               'output_in_subtask',
               'adjust_initial_conditions',
               'update_model',
               'output_in_subtask',
               'adjust_initial_conditions',
               'create_parameter_sets',
               'calculate_statistics',
               'randomize_start_values',
               ]
        for k, v in dct.items():
            if k in lst:
                if v == True:
                    dct[k] = '1'
                elif v == False:
                    dct[k] = '0'
                elif v == '1':
                    pass
                elif v == '0':
                    pass
                else:
                    raise Exception('{} is not True or False'.format(v))
        return dct

class Bool2Str():
    """
    copasiML expects strings and we pythoners
    want to use python booleans not strings
    This class quickly converts between them
    """
    def __init__(self,dct):
        self.dct = dct
        if isinstance(self.dct,dict)!=True:
            raise errors.InputError('Input must be dict')

        self.acceptable_kwargs = ['append','confirm_overwrite','update_model',
                                  'output_in_subtask','adjust_initial_conditions',
                                  'randomize_start_values','log10','scheduled','output_event']

    def convert(self,boolean):
        if boolean == True:
            return "true"
        elif boolean == False:
            return "false"
        else:
            raise errors.InputError('Input should be boolean not {}'.format(isinstance(boolean)))

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


class CheckIntegrityMixin(Mixin):
    @staticmethod
    def check_integrity(allowed, given):
        """
        Method to raise an error when a wrong
        kwarg is passed to a subclass
        :param allowed:
            `list`. List of allowed kwargs

        :param given: List of kwargs given by user or default

        :return:
            None
        """
        for key in given:
            if key not in allowed:
                raise errors.InputError('{} not in {}'.format(key, allowed))

class CopasiMLParser(object):

    """
    Parse a copasi file into xml.etree.

    Usage:

        >>> model_path = r'/full/path/to/model.cps'
        >>> xml = CopasiMLParser(model_path).xml


    """
    def __init__(self, copasi_file):
        """

        :param copasi_file:
            `str` full path to a copasi file
        """
        self.copasi_file = copasi_file
        if os.path.isfile(self.copasi_file)!=True:
            raise errors.FileDoesNotExistError('{} is not a copasi file'.format(self.copasi_file))
        self.copasiMLTree=self._parse_copasiML()
        self.copasiML=self.copasiMLTree.getroot()
        self.xml = self.copasiMLTree.getroot()

        os.chdir(os.path.dirname(self.copasi_file))

    def _parse_copasiML(self):
        """
        Parse xml doc with lxml
        :return:
        """
        tree= etree.parse(self.copasi_file)
        return tree

    def write_copasi_file(self,copasi_filename, xml):
        """
        write to file with lxml write function
        """
        #first convert the copasiML to a root element tree
        root=etree.ElementTree(xml)
        root.write(copasi_filename)

@mixin(UpdatePropertiesMixin)
@mixin(Bool2Numeric)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
class Run(object):
    """
    Execute a copasi model using CopasiSE. To
    be operational the environment variable CopasiSE
    must be set to point towards the location of
    your CopasiSE executable. This is usually
    done automatically.

    Usage:

    First get a model object
        >>> model_path = r'/full/path/to/model.cps'
        >>> model = model.Model(model_path)

    To run a time_course task
        >>> Run(model, task='time_course', mode=True)

    To run the parameter estimation task:
        >>> Run(model, task='parameter_estimation', mode=True)

    To run the parameter estimation task with :py:mod:`multiprocessing`
        >>> Run(model, task='parameter_estimation', mode='multiprocess')

    To run the scan task but have python write a .sh script for submission to sun grid engine:
        >>> Run(model, task='scan', mode='sge')

    Properties

    ==========          ===================
    Property            Description
    ==========          ===================
    task                Task to run
    mode                How to run the task
    sge_job_filename    Optional name of sh file
                        generated for running sge
    ==========          ===================

    =============
    task options
    =============
    steady_state
    time_course
    scan
    flux_mode
    optimization
    parameter_estimation
    metabolic_control_analysis
    lyapunov_exponents
    time_scale_separation_analysis
    sensitivities
    moieties
    cross_section
    linear_noise_approximation
    =============

    ==============          ==============
    Modes                   Description
    =============           ==============
    False                   Do not run
    True                    Run one at a time
    multiprocess            Run several at once
    sge                     Run on sun grid engine
    =============           ==============
    """
    def __init__(self, model, **kwargs):
        """
        :param model:
            :py:class:`model.Model`

        """
        self.model = self.read_model(model)
        self.kwargs = kwargs

        self.default_properties = {'task': 'time_course',
                                   'mode': True,
                                   'sge_job_filename': None}

        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self._do_checks()

        if self.sge_job_filename == None:
            self.sge_job_filename = os.path.join(os.getcwd(), 'sge_job_file.sh')

        self.model = self.set_task()
        self.model.save()

        if self.mode == True:
            try:
                self.run()
            except errors.CopasiError:
                self.run_linux()

        elif self.mode == 'sge':
            self.submit_copasi_job_SGE()

        elif self.mode == 'multiprocess':
            self.multi_run()


    def _do_checks(self):
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
            raise errors.InputError('{} not in list of tasks. List of tasks are: {}'.format(self.task, tasks))

        modes = [True, False, 'multiprocess', 'parallel', 'sge']
        if self.mode not in modes:
            raise errors.InputError('{} not in {}'.format(self.mode, modes))

    def __str__(self):
        return 'Run({})'.format(self.to_string())

    def multi_run(self):
        ##TODO build Queue.Queue system for multi running. 
        def run(x):
            if os.path.isfile(x) != True:
                raise errors.FileDoesNotExistError('{} is not a file'.format(self.copasi_file))
            subprocess.Popen(['CopasiSE', self.model.copasi_file])
        Process(run(self.model.copasi_file))



    def set_task(self):
        """

        :return:
        """
        # print self.model
        # task = self.task.replace('_', '').replace
        task = self.task.replace(' ', '_').lower()

        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            i.attrib['scheduled'] = "false"  # set all to false
            task_name = i.attrib['name'].lower().replace('-', '_').replace(' ', '_')
            if task == task_name:
                i.attrib['scheduled'] = "true"
        return self.model

    def run(self):
        '''
        Process the copasi file using CopasiSE
        '''
        args = ['CopasiSE', "{}".format(self.model.copasi_file)]
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        d = {}
        d['output'] = output
        d['error'] = err
        if err != '':
            try:
                self.run_linux()
            except:
                raise errors.CopasiError('Failed with Copasi error: \n\n' + d['error'])
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
        os.system('CopasiSE "{}"'.format(self.model.copasi_file))

    def submit_copasi_job_SGE(self, copasi_location='apps/COPASI/4.19.140-Linux-64bit'):
        """
        Submit copasi file as job to SGE based job scheduler.
        :param copasi_location:
            Location to copasi on the sge cluster. Gets passed to `module add` to load copasi

        :return:
            None
        """
        with open(self.sge_job_filename, 'w') as f:
            f.write('#!/bin/bash\n#$ -V -cwd\nmodule add {}\nCopasiSE "{}"'.format(
                copasi_location, self.model.copasi_file
            )
        )

        ## -N option for job namexx
        os.system('qsub "{}" -N "{}" '.format(self.sge_job_filename, self.sge_job_filename))
        ## remove .sh file after used.
        # os.remove(self.sge_job_filename)

@mixin(model.GetModelComponentFromStringMixin)
@mixin(UpdatePropertiesMixin)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
@mixin(Bool2Numeric)
class RunParallel(object):
    def __init__(self, models, **kwargs):
        raise NotImplementedError('still work to do on this class')
        self.models = models
        self.kwargs = kwargs

        self.default_properties = {
            'processes': 1,
            'shell': True,
        }
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), kwargs.keys())
        self._do_checks()

        LOG.info('running with {} processes'.format(self.processes))
        self.q = Queue.Queue(maxsize=self.processes)
        self.results = self.run_parallel()

    def _do_checks(self):
        """

        :return:
        """
        if self.processes > cpu_count():
            raise errors.InputError('number of processes should be less than the number of CPUs')

        if not isinstance(self.models, list):
            raise errors.InputError('input should be a list of models to run')

        for i in self.models:
            if not isinstance(i, model.Model):
                raise errors.InputError('Input should be a list of models to run')


    def run1(self, model):
        '''
        Process the copasi file using CopasiSE
        '''

        args = ['CopasiSE', "{}".format(model.copasi_file)]
        proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        # self.q.put(proc, block=True)
        LOG.info('running from run1 "{}"'.format(model.copasi_file))
        # self.q.join() ##blocks until all tasks are done
        import time
        import psutil


        while proc.poll() != 0:

            time.sleep(1)



    def run_parallel2(self):
        """
        This one works for just a single coapsi file
        at a time
        :return:
        """
        res = {}
        import multiprocessing
        # q = Queue.Queue()
        q = multiprocessing.Queue(3)

        for mod in self.models:
            t = threading.Thread(target=self.run1, args=(mod,),
                                 name=mod.copasi_file)
            LOG.info('current process --> {}'.format(multiprocessing.current_process().name))
            # t.daemon = True
            t.start()
            t.join()
            # res[model] = self.q.get()#.model
        # return res

    def run_parallel2(self):
        """
        :return:
        """
        res = {}
        import multiprocessing
        # q = Queue.Queue()
        q = multiprocessing.Queue(3)
        threads = []
        for mod in self.models:
            t = threading.Thread(target=self.run1, args=(mod,),
                                 name=mod.copasi_file)
            t.daemon = True
            threads.append(t)
        for i in range(len(threads)):
            threads[i].start()
                # i.start()
            #.join()
            # res[model] = self.q.get()#.model
            # return res

    def submit(self, model):
        process = subprocess.Popen(['CopasiSE',model])


    def run1(self, q, model):
        self.submit(model)

    def do_stuff(self, q, model):
        while True:
            q.put(subprocess.Popen(['CopasiSE', '{}'.format(model.copasi_file)]))
            proc = q.get()
            if proc.wait() == 0:
                q.task_done()

    def run_parallel(self):
        q = Queue.Queue()
        num_threads = 1
        num_models = len(self.models)
        batch_size = 1

        while num_models > 0:
            for i in range(num_threads):
                try:
                    num_models = num_models - 1
                    if num_models == 0:
                        break


                    worker = threading.Thread(target=self.do_stuff,
                                          args=(q, self.models[num_models]))
                    worker.daemon = True
                    worker.start()
                except IndexError:
                    break
            q.join()


        # for i in range(num_threads):
        #     for j in range(batch_size):
        #         try:
        #             model = self.models[i*j+j]
        #                 self.models[j].copasi_file))
        #             worker = threading.Thread(target=self.do_stuff,
        #                                       args=(q,self.models[j]))
        #             worker.daemon = True
        #             worker.start()
        #         except IndexError:
        #             break
        #     q.join()

    def get_result(self):
        """

        :return:
        """
        output_dct = {}
        for proc in self.results:
            process = self.results[proc]
            output, error = process.communicate()

            if error != '':
                raise errors.CopasiError('Failed with a Copasi Error:\n\n{}'.format(error))
            output_dct[proc] = output
        return output_dct




@mixin(UpdatePropertiesMixin)
class iPythonParallel(_base._Base):
    NotImplementedError('still work to do on this class')
    def __init__(self, models, **kwargs):
        self.models = models
        self.kwargs = kwargs

        self.default_properties = {
            'processes': 1,
            'shell': True,
        }
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), kwargs.keys())
        raise NotImplementedError


    def _do_checks(self):
        """

        :return:
        """
        if self.processes > cpu_count():
            raise errors.InputError('number of processes should be less than the number of CPUs')

        if not isinstance(self.models, list):
            raise errors.InputError('input should be a list of models to run')

        for i in self.models:
            if not isinstance(i, model.Model):
                raise errors.InputError('Input should be a list of models to run')


    def x(self):
        """

        :return:
        """
        import thread
        thread.start_new_thread(os.system, ('ipcluster start -n 4',))
        import ipyparallel as ipp
        c = ipp.Client()
        print c.ids


    def run1(self, model):
        '''
        Process the copasi file using CopasiSE
        '''



    def run_parallel(self):
        """
        :return:
        """


    def get_result(self):
        """

        :return:
        """




# class ParseStrVariableMixin(Mixin):
#     """
#     Mixin class for taking a string
#     and returning the corresponding
#     model quantity
#     """
#     ## allow a user to input a string not pycotools.model class
#     @staticmethod
#     def conversion(model, variable):
#
#         if isinstance(variable, str):
#             if variable in [i.name for i in model.metabolites]:
#                 variable = model.get('metabolite', variable,
#                                                by='name')
#
#             elif variable in [i.name for i in model.global_quantities]:
#                 variable = model.get('global_quantity', variable, by='name')
#
#             elif self.variable in [i.name for i in self.model.local_parameters]:
#                 variable = model.get('constant', variable, by='name')
#         else:
#             raise errors.SomethingWentHorriblyWrongError('{} is not in your model'.format(variable))
#         return variable


@mixin(model.GetModelComponentFromStringMixin)
# @mixin(GetModelVariableFromStringMixin)
@mixin(UpdatePropertiesMixin)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
@mixin(Bool2Numeric)
class Reports(object):
    """
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

        variable:
            Model component to scan

    """
    def __init__(self, model, **kwargs):
        # super(Reports, self).__init__(model, **kwargs)
        self.model = self.read_model(model)
        self.kwargs = kwargs
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

        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self.__do_checks()

        self.model = self.run()

    def __do_checks(self):
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
            raise errors.InputError('{} not concentration or particle_number'.format(self.quantity_type))

        self.report_types=[None,'profile_likelihood', 'profilelikelihood2',
                           'time_course','parameter_estimation', 'multi_parameter_estimation']
        assert self.report_type in self.report_types,'valid report types include {}'.format(self.report_types)

        quantity_types = ['particle_numbers', 'concentration']
        assert self.quantity_type in quantity_types


        if self.report_name == None:
            if self.report_type == 'profile_likelihood':
                default_report_name='profilelikelihood.txt'

            elif self.report_type=='profile_likelihood2':
                default_report_name='profile_likelihood2.txt'

            elif self.report_type == 'time_course':
                default_report_name='time_course.txt'

            elif self.report_type =='parameter_estimation':
                default_report_name = 'parameter_estimation.txt'

            elif self.report_type == 'multi_parameter_estimation':
                default_report_name = 'multi_parameter_estimation.txt'

            self.report_name = default_report_name

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
                self.model = self.remove_report('time_course')

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


    def scan(self):
        '''
        creates a report to collect scan time course results.

        By default all species and all global quantities are used with
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the metabolites keyword or global quantities to the
        global quantities keyword
        '''
        #get existing report keys

        ##TODO implement self.variable as column in scan
        keys=[]
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name']=='Time-Course':
                self.model = self.remove_report('time_course')

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
            if i.attrib['name']=='profile_likelihood':
                self.model = self.remove_report('profile_likelihood')

        new_key='Report_31'
        while new_key in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes = {'precision': '6',
                             'separator': '\t',
                             'name': 'profile_likelihood',
                             'key': new_key,
                             'taskType': 'Scan'}

        ListOfReports=self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)

        comment=etree.SubElement(report, 'Comment')
        table=etree.SubElement(report, 'Table')
        table.attrib['printTitle']=str(1)

        ##TODO cater for particle numbers
        if self.variable.name in [i.name for i in self.metabolites]:
            cn = '{},{},{}'.format(self.model.reference, self.variable.compartment.reference, self.variable.initial_reference)

        elif self.variable.name in [i.name for i in self.global_quantities]:
            cn = '{},{}'.format(self.model.reference, self.variable.initial_reference)

        elif self.variable.name in [i.name for i in self.local_parameters]:
            cn = '{},{},{}'.format(self.model.reference, self.variable.get_reaction().reference, self.variable.value_reference)

        etree.SubElement(table,'Object',attrib={'cn': cn})
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"})
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
                self.model = self.remove_report('parameter_estimation')

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
                self.model = self.remove_report('multi_parameter_estimation')

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
            self.model = self.parameter_estimation()


        elif self.report_type  == 'multi_parameter_estimation':
            self.model =self.multi_parameter_estimation()

        elif self.report_type == 'profile_likelihood':
            self.model = self.profile_likelihood()

        elif self.report_type == 'time_course':
            self.model = self.timecourse()

        elif self.report_type == None:
            self.model = self.model

        return self.model

    def remove_report(self,report_name):
        """

        remove report called report_name
        :param report_name:
        :return: pycotools.model.Model
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


@mixin(GetModelVariableFromStringMixin)
@mixin(UpdatePropertiesMixin)
@mixin(Bool2Numeric)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
class TimeCourse(object):
    """

    Change the plotting functions of time course.
    Create new class. Like viz in ecell4 for visualizing
    the data. This will give more flexibility than what we presently have.
    The idea is that user will be able to enter x or y variable,
    or multiple such variables for the y axis to plot whatever they like.
    """

    def __init__(self, model, **kwargs):
        self.model = self.read_model(model)
        default_report_name = os.path.join(os.path.dirname(self.model.copasi_file), 'TimeCourseData.txt')

        default_properties = {'intervals': 100,
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
        default_properties.update(kwargs)
        default_properties = self.convert_bool_to_numeric(default_properties)
        self.check_integrity(default_properties.keys(), kwargs.keys())
        self.update_properties(default_properties)
        self._do_checks()

        self.set_timecourse()
        self.set_report()

        self.run_task()


        ## self.correct_output_headers()

        if self.save:
            self.model.save()

    def _do_checks(self):
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
            raise errors.InputError('{} is not a valid method. These are valid methods {}'.format(self.method, method_list))

        if os.path.isabs(self.report_name)!=True:
            self.report_name = os.path.join(os.path.dirname(self.model.copasi_file), self.report_name)

        if not isinstance(self.metabolites, list):
            self.metabolites = [self.metabolites]

        if not isinstance(self.global_quantities, list):
            self.global_quantities = [self.global_quantities]

        for metab in range(len(self.metabolites)):
            if isinstance(self.metabolites[metab], str):
                self.metabolites[metab] = self.get_variable_from_string(
                    self.model, self.metabolites[metab]
                )

        glo_list = []
        for glo in range(len(self.global_quantities)):
            if isinstance(self.global_quantities[glo], str):
                glo_list.append(self.get_variable_from_string(
                    self.model, self.global_quantities[glo]
                    )
                )
            else:
                glo_list.append(self.global_quantities[glo])

        self.global_quantities = glo_list


    def __str__(self):
        return "TimeCourse(method={}, end={}, intervals={}, step_size={})".format(
            self.method, self.end, self.intervals, self.step_size
        )

    def run_task(self):
        R = Run(self.model, task='time_course', mode=self.run)
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

        task = etree.Element('Task', attrib={'key': 'Task_100',
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
                                                 'type': 'Deterministic(LSODA)'})

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
        raise errors.NotImplementedError('The hybrid-RK-45 method is not yet implemented')

    def set_report(self):
        """
        ser a time course report containing time
        and all species or global quantities defined by the user.

        :return: pycotools.model.Model
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
        all_reports = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            all_reports.append(i.attrib['name'])
            if i.attrib['name'] == 'Time-Course':
                key = i.attrib['key']
        if 'Time-Course' not in all_reports:
            raise errors.SomethingWentHorriblyWrongError('No report called "Time-Course". '
                                                             'Have you set one up yet?')
        return key


@mixin(GetModelVariableFromStringMixin)
@mixin(UpdatePropertiesMixin)
@mixin(Bool2Numeric)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
class Scan(object):
    """
    Interface to COPASI scan task
    """
    def __init__(self, model, **kwargs):
        # super(Scan, self).__init__(model, **kwargs)
        self.model = self.read_model(model)
        self.kwargs = kwargs

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
                                   'report_type': 'profile_likelihood',
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
                                   'run': False}
        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self._do_checks()

        ## conflicts with other classes in base
        ## class so just convert the scan log10 argument
        ## to numeric string here
        if self.log10 == False:
            self.log10 = str(0)
        else:
            self.log10 = str(1)


        self.model = self.define_report()
        self.model = self.create_scan()
        self.model = self.set_scan_options()

        if self.save:
            self.model.save()

        self.execute()

    def __str__(self):
        types = {v: k for (k, v) in self.scan_type_numbers.items()}
        subtasks = {v: k for (k, v) in self.subtask_numbers.items()}
        return "Scan(scan_type='{}', subtask='{}', variable='{}', report_type='{}', " \
               "report_name='{}', number_of_steps='{}', minimum={}, maximum={})".format(
            types[self.scan_type], subtasks[self.subtask], self.variable.name, self.report_type,
            self.report_name, self.number_of_steps, self.minimum, self.maximum
        )

    def _do_checks(self):
        """
        Varify integrity of user input
        :return:
        """
        if isinstance(self.variable, str):
            self.variable = self.get_variable_from_string(self.model, self.variable)

        if self.variable != []:
            try:
                if self.variable.name not in self.model.all_variable_names:
                    raise errors.InputError(
                        '"{}" not in model. These are in your model: {}'.format(
                            self.variable.name,
                            self.model.all_variable_names
                        )
                    )
            ##catch for local variables which requires match by global name
            except errors.InputError:
                if self.variable.global_name not in self.model.all_variable_names:
                    raise errors.InputError(
                        '"{}" not in model. These are in your model: {}'.format(
                            self.variable.name,
                            self.model.all_variable_names
                        )
                    )


        if self.clear_scans == True:
            self.model = self.remove_scans()

        if self.scan_type == 'scan':
            if self.output_in_subtask !=True:
                LOG.warning('output_in_subtask is False. '
                            ' This means that the subtask will not output data '
                            'as it is producing that data. For Scan tasks, we need this to be '
                            'True as we would like all the output. For parameter estimations'
                            'or profile likelihood, set this to False as we only want the'
                            'final parameter set')
                # self.output_in_subtask = 'true'  ##string format needed for copasi

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
        self.scan_type_numbers = dict(zip(scan_types, [str(i) for i in scan_type_numbers]))
        for i, j in self.scan_type_numbers.items():
            if i == self.scan_type:
                self.scan_type = j

        for i in zip(scan_types, scan_type_numbers):
            if i[0] == self.scan_type:
                self.scan_type = str(i[1])

        dist_types_numbers = [0, 1, 2, 3]
        self.dist_type_numbers = dict(zip(dist_types, [str(i) for i in dist_types_numbers]))
        for i, j in self.dist_type_numbers.items():
            if i == self.distribution_type:
                self.distribution_type = j

        # for i in zip(dist_types, dist_types_numbers):
        #     if i[0] == self.distribution_type:
        #         self.distribution_type = str(i[1])


        ## allow a user to input a string not pycotools.model class
        if isinstance(self.variable, str):
            if self.variable in [i.name for i in self.model.metabolites]:
                self.variable = self.model.get('metabolite', self.variable,
                                               by='name')

            elif self.variable in [i.name for i in self.model.global_quantities]:
                self.variable = self.model.get('global_quantity', self.variable, by='name')

            elif self.variable in [i.name for i in self.model.local_parameters]:
                self.variable = self.model.get('local_parameter', self.variable, by='global_name')



    def define_report(self):
        """
        Use Report class to create report
        :return:
        """
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
            raise errors.ReportDoesNotExistError('Report doesn\'t exist. Check to see if you have either defined the report manually or used the pycopi.Reports class')
        return key

    def create_scan(self):
        """
        metabolite cn:
            CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=InitialConcentration"/>

        :return:
        """
        ## get model entity if variable is a string
        if isinstance(self.variable, str):
            metab = self.model.get('metabolite', self.variable, by='name')
            glob  = self.model.get('global_quantity', self.variable, by='name')
            loca  = self.model.get('local_parameter', self.variable, by='global_name')

            ##small bit of extra code to check that
            ## we only have one self.variable
            metab_for_checking = []
            glob_for_checking = []
            loca_for_checking = []
            if not isinstance(metab, list):
                metab_for_checking = [metab]

            if not isinstance(glob, list):
                glob_for_checking = [glob]

            if not isinstance(loca, list):
                loca_for_checking = [loca]

            all = metab_for_checking + glob_for_checking + loca_for_checking
            if len(all) > 1:
                raise errors.SomethingWentHorriblyWrongError('Getting variable from model but matched more than one entity')

            if metab != []:
                self.variable = metab

            if glob != []:
                self.variable = glob

            if loca != []:
                self.variable = loca

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
            reaction = self.model.get('reaction', self.variable.reaction_name, by='name')
            cn = '{},{},{}'.format(self.model.reference,
                                   reaction.reference,
                                   self.variable.value_reference)

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

        ##TODO fix output in subtask temp fix
        if self.output_in_subtask == True:
            self.output_in_subtask = 'true'
        elif self.output_in_subtask == False:
            self.output_in_subtask = 'false'

        subtask_attrib = {'type': 'unsignedInteger', 'name': 'Subtask', 'value': self.subtask}
        output_in_subtask_attrib = {'type': 'bool', 'name': 'Output in subtask',
                                    'value': self.output_in_subtask}
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
            for j in i:
                j.getparent().remove(j)
        self.model.save()
        return self.model

    def execute(self):
        R = Run(self.model, task='scan', mode=self.run)

@mixin(model.GetModelComponentFromStringMixin)
@mixin(UpdatePropertiesMixin)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
@mixin(Bool2Numeric)
class ExperimentMapper(object):
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
        self.model = self.read_model(model)
        self.kwargs = kwargs
        # super(ExperimentMapper, self).__init__(model, **kwargs)
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
        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self._do_checks()


        #run the experiment mapper
        self.model = self.map_experiments()

        if self.save:
            self.model.save()


    def _do_checks(self):
        """

        """
        data_types = ['experiment', 'validation']
        if self.type not in data_types:
            raise errors.InputError('{} not in {}'.format(self.type, data_types))

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
            raise errors.NotImplementedError('Validation data sets are currently not supported')

        for j in self.model.xml.xpath(query):
            j.insert(0, experiment_element)
        return self.model


    def map_experiments(self):
        """
        map all experiment sets
        :return:
        """
        self.remove_all_experiments()
        for i in range(len(self.experiment_files)):
            Experiment = self.create_experiment(i)
            self.model = self.add_experiment_set(Experiment)
            # self.save() ## Note sure whether this save is needed. Keep commented until you're sure
        return self.model

@mixin(GetModelVariableFromStringMixin)
@mixin(model.GetModelComponentFromStringMixin)
@mixin(UpdatePropertiesMixin)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
@mixin(Bool2Numeric)
class ParameterEstimation(object):
    '''
    Set up and run a parameter estimation in copasi. Since each parameter estimation
    problem is different, this process cannot be done in a single line of code.
    Instead the user should initialize an instance of the ParameterEstimation
    class with all the relevant keyword arguments. Subsequently use the
    write_item_template() method and modify the resulting xlsx in your copasi file
    directory. save the file then close and run the setup() method to define your
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
        self.model = self.read_model(model)
        self.kwargs = kwargs
        # super(ParameterEstimation, self).__init__(model, **kwargs)
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
                                   'save': False}

        self.default_properties.update(self.kwargs)
        self.default_properties = self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self._remove_multiparameter_estimation_arg()
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())

        self._do_checks()

        self._convert_numeric_arguments_to_string()

        if self.save:
            self.model.save()

    def __str__(self):
        return "ParameterEstimation(method='{}', config_filename='{}', report_name='{}')".format(
            self.method, self.config_filename, self.report_name)

    def get_default_properties(self):
        return self.default_properties

    def _remove_multiparameter_estimation_arg(self):
        """
        MultiParameterEstimation inherits from ParameterEstimation
        and passes new arguments to the ParameterEstimation class
        which get fed into self.check_integrity causing Exception.
        This method removes those arguments
        :return:
        """
        lst = ['copy_number',
               'pe_number',
               'results_directory']
        for i in lst:
            if i in self.kwargs.keys():
                del self.kwargs[i]

    def _do_checks(self):
        """
        Validate integrity of user input
        :return:
        """
        ## Allow acceptance of strings as arguments to metabolites, local_parameters
        ## and global_quantities
        for attr in ['metabolites', 'local_parameters', 'global_quantities']:
            getattribute = getattr(self, attr)
            new_attr = []
            for i in range(len(getattribute)):
                if isinstance(getattribute[i], str):
                    new_attr.append(self.get_variable_from_string(self.model, getattribute[i]))
                    setattr(self, attr, new_attr)

        if os.path.isabs(self.report_name)!=True:
            self.report_name = os.path.join(os.path.dirname(self.model.copasi_file),
                                            self.report_name)

        ## ensure experiment files exist
        for fle in self.experiment_files:
            if os.path.isfile(fle)!=True:
                raise errors.InputError('{} does not exist'.format(fle))

        ## ensure method exists
        self.method_list = ['current_solution_statistics', 'differential_evolution',
                            'evolutionary_strategy_sr', 'evolutionary_program',
                            'hooke_jeeves', 'levenberg_marquardt', 'nelder_mead',
                            'particle_swarm', 'praxis', 'random_search', 'scatter_search',
                            'simulated_annealing', 'steepest_descent', 'truncated_newton',
                            'genetic_algorithm', 'genetic_algorithm_sr']
        if self.method not in self.method_list:
            raise errors.InputError(
                '{} not a valid method. These are valid methods: {}'.format(self.method, self.method_list))

        ## Do not randomize start values if using current solution statistics
        if self.method == 'current_solution_statistics':
            if self.randomize_start_values == True:
                raise errors.InputError(
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
                raise errors.InputError(
                    '"{}" not a local_parameter. These are your local parameters: {}'.format(
                        i, self.model.local_parameters) )

        ## ensure arguments to metabolites exist
        for i in [j.name for j in self.metabolites]:
            if i not in [j.name for j in self.model.metabolites]:
                raise errors.InputError(
                    '"{}" not a metabolite. These are your local parameters: {}'.format(
                        i,self.model.metabolites) )

        ## ensure arguments to global_quantities exist
        for i in [j.name for j in self.global_quantities]:
            if i not in [j.name for j in self.model.global_quantities]:
                raise errors.InputError(
                    '"{}" not a global_quantity. These are your local parameters: {}'.format(
                        i,self.model.global_quantities) )

        if self.use_config_start_values not in [True, False]:
            raise errors.InputError(
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
        self.model = self.define_report()
        self.model = self.remove_all_fit_items()
        self.model = self.set_PE_method()
        self.model = self.set_PE_options()
        self.model = self.insert_all_fit_items()
        assert self.model != None
        assert isinstance(self.model, model.Model)
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
        :return: pycotools.model.Model
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
        :return: pycotools.model.Model
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
        :return: pycotools.model.Model
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
        return self.config_filename

    def read_config_file(self):
        """

        :return:
        """
        if os.path.isfile(self.config_filename) != True:
            raise errors.InputError('ConfigFile does not exist. run \'write_config_file\' method and modify it how you like then run the setup()  method again.')
        df = pandas.read_csv(self.config_filename)
        parameter_names = list(df[df.columns[0]])

        model_parameters = self.model.all_variable_names
        for parameter in parameter_names:
            if parameter not in model_parameters:
                raise errors.InputError('{} not in {}\n\n Ensure you are using the correct PE config file!'.format(parameter, model_parameters))
        return df

    @property
    def item_template(self):
        """
        Collect information about the model in order to
        create a config file template.
        :return: pandas.DataFrame
        """

        keep_metabs = []
        keep_globs = []
        keep_locs = []
        for model_metab in self.model.metabolites:
            for PE_metab in self.metabolites:
                if PE_metab.name == model_metab.name:
                    keep_metabs.append(PE_metab)

        for model_glob in self.model.global_quantities:
            for PE_glob in self.global_quantities:
                if PE_glob.name == model_glob.name:
                    keep_globs.append(PE_glob)


        for model_loc in self.model.local_parameters:
            for PE_loc in self.local_parameters:
                if PE_loc.global_name == model_loc.global_name:
                    keep_locs.append(PE_loc)


        keep_metabs = [i.to_df() for i in keep_metabs]
        keep_globs = [i.to_df() for i in keep_globs]
        keep_locs = [i.to_df() for i in keep_locs]

        metabs = pandas.DataFrame()
        if keep_metabs != []:
            metab = pandas.concat(keep_metabs, axis=1).transpose()
            metab.drop('compartment', inplace=True, axis=1)
            metab.drop('key', inplace=True, axis=1)
            metab.drop('simulation_type', inplace=True, axis=1)
            metab = metab.rename(columns={'value': 'start_value'})

            if self.quantity_type == 'concentration':
                metab.drop('particle_number', axis=1, inplace=True)
                metab = metab.rename(columns={'concentration': 'start_value'})

            elif self.quantity_type == 'particle_number':
                metab.drop('concentration', axis=1, inplace=True)
                metab = metab.rename(columns={'particle_number': 'start_value'})
                metab = metab[['name', 'start_value']]
            metabs = metabs.append(metab)

        if not metabs.empty:
            metabs = metabs.sort_values(by='name')


        los = pandas.DataFrame()
        if keep_locs != []:
            lo = pandas.concat(keep_locs, axis=1).transpose()
            lo = lo.rename(columns={'value': 'start_value'})
            lo = lo[['global_name', 'start_value']]
            lo = lo.rename(columns={'global_name': 'name'})
            los = los.append(lo)

        if not los.empty:
            los = los.sort_values(by='name')


        gls = pandas.DataFrame()
        if keep_globs != []:
            gl = pandas.concat(keep_globs, axis=1).transpose()
            gl = gl.rename(columns={'initial_value': 'start_value'})
            gl = gl[['name', 'start_value']]
            gls = gls.append(gl)

        if not gls.empty:
            gls = gls.sort_values(by='name')

        df = pandas.concat([metabs, gls, los], axis=0)

        df['lower_bound'] = [self.lower_bound]*df.shape[0]
        df['upper_bound'] = [self.upper_bound]*df.shape[0]

        df = df.set_index('name')

        return df


    def add_fit_item(self,item):
        """
        Add fit item to model
        :param item: a row from the config template as pandas series
        :return: pycotools.model.Model
        """
        ## figure out what type of variable item is and assign to component
        if item['name'] in [i.name for i in self.metabolites]:
            component = [i for i in self.metabolites if i.name == item['name']][0]

        elif item['name'] in [i.global_name for i in self.local_parameters]:
            component = [i for i in self.local_parameters if i.global_name == item['name']][0]

        elif item['name'] in [i.name for i in self.global_quantities]:
            component = [i for i in self.global_quantities if i.name == item['name']][0]
        else:
            raise errors.SomethingWentHorriblyWrongError('"{}" is not a metabolite,'
                                                         ' local_parameter or '
                                                         'global_quantity. These are your'
                                                         ' model variables: {}'.format(item['name']),
                                                         str(self.model.all_variable_names))

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
                subA4={'type': 'cn',  'name': 'ObjectCN',  'value': '{},{},{}'.format(
                    self.model.reference,
                    component.compartment.reference,
                    component.initial_particle_reference
                )}

        elif isinstance(component, model.LocalParameter):
            subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{},{}'.format(
                self.model.reference,
                self.model.get('reaction', component.reaction_name, by='name').reference,
                component.value_reference) }

        elif isinstance(component, model.GlobalQuantity):
            subA4={'type': 'cn',  'name': 'ObjectCN',  'value': '{},{}'.format(self.model.reference,
                                                                               component.initial_reference) }

        elif isinstance(component, model.Compartment):
            subA4 = {'type': 'cn',
                     'name': 'ObjectCN',
                     'value': '{},{}'.format(self.model.reference,
                                             component.initial_value_reference)}

        else:
            raise errors.InputError('{} is not a valid parameter for estimation'.format(list(item)))

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
        :return: pycotools.model.Model
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
        Run(self.model, mode=True, task='parameter_estimation')




    # def plot(self):
    #     self.PL=viz.PlotPEData(self.copasi_file,self.experiment_files,self.kwargs.get('report_name'),
    #                     **self.PlotPEDataKwargs)




class MultiParameterEstimation(ParameterEstimation):
    '''

    '''
    ##TODO Merge ParameterEstimation and Multi into one class.
    def __init__(self, model, experiment_files, copy_number=1, pe_number=3,
                 run_mode='multiprocess', results_directory=None, output_in_subtask=False, **kwargs):
        super(MultiParameterEstimation, self).__init__(model, experiment_files, **kwargs)
        ## add to ParameterEstimation defaults
        self.copy_number = copy_number
        self.pe_number = pe_number
        self.run_mode = run_mode
        self.results_directory = results_directory
        self.output_in_subtask = output_in_subtask

        if self.results_directory is None:
            self.results_directory = os.path.join(os.path.dirname(self.model.copasi_file), 'MultipleParameterEstimationResults')


    def __str__(self):
        return 'MultiParameterEstimation(copy_number="{}", pe_number="{}", method="{}", config_filename="{}")'.format(
            self.copy_number, self.pe_number, self.method, self.config_filename
        )

    ##void
    def __do_checks(self):
        '''

        '''
        if self.output_in_subtask:
            LOG.warning('output_in_subtask has been turned on. This means that you\'ll get function evaluations with the best parameter set that the algorithm finds')
        run_arg_list=['multiprocess','SGE']
        if self.run_mode not in run_arg_list:
            raise errors.InputError('run_mode needs to be one of {}'.format(run_arg_list))

        if isinstance(self.copy_number,int)!=True:
            raise errors.InputError('copy_number argument is of type int')

        if isinstance(self.kwargs['pe_number'],int)!=True:
            raise errors.InputError('pe_number argument is of type int')

    def _create_output_directory(self):
        """
        Create directory for estimation results
        :return:
        """
        if os.path.isdir(self.results_directory)!=True:
            os.mkdir(self.results_directory)

    def define_report(self):
        """
        create parameter estimation report
        for result collection
        :return: pycotools.model.Model
        """
        self._report_arguments['report_type'] = 'multi_parameter_estimation'
        return Reports(self.model, **self._report_arguments).model

    def enumerate_PE_output(self):
            """
            Create a filename for each file to collect PE results
            :return: dict['model_copy_number]=enumerated_report_name
            """

            dct = {}
            dire, fle = os.path.split(self.report_name)
            for i in range(self.copy_number):
                new_file = os.path.join(self.results_directory,
                                      fle[:-4]+'{}.txt'.format(str(i)))
                dct[i] = new_file
            return dct

    ##TODO work out whether parameter_estimation report shuold be multi_parameter_estimation

    def copy_model(self):
        """
        Copy the model n times
        Uses deep copy to ensure separate models
        :return: dict[index] = model copy
        """
        dct = {}
        for i in range(self.copy_number):
            dire, fle = os.path.split(self.model.copasi_file)
            new_cps = os.path.join(dire, fle[:-4]+'_{}.cps'.format(i))
            model = deepcopy(self.model)
            model.copasi_file = new_cps
            model.save()
            dct[i] = model
        return dct

    def _setup1scan(self, q, model, report):
        """
        Setup a single scan.
        :param q: queue from multiprocessing
        :param model: pycotools.model.Model
        :param report: str.
        :return:
        """
        start = time.time()
        models = q.put(Scan(model,
                   scan_type='repeat',
                   number_of_steps=self.pe_number,
                   subtask='parameter_estimation',
                   report_type='multi_parameter_estimation',
                   report_name=report,
                   run=False,
                   append=self.append,
                   confirm_overwrite=self.confirm_overwrite,
                   output_in_subtask=self.output_in_subtask,
                   save=True))



    def _setup_scan(self, models):
        """
        Set up `copy_number` repeat items with `pe_number`
        repeats of parameter estimation. Set run_mode to false
        as we want to use the multiprocess mode of the run_mode class
        to process all files at once in CopasiSE
        :return:
        """
        number_of_cpu = cpu_count()
        q = Queue.Queue(maxsize=number_of_cpu)
        report_files = self.enumerate_PE_output()
        res = {}
        for copy_number, model in models.items():
            t = threading.Thread(target=self._setup1scan,
                                 args=(q, model, report_files[copy_number]))
            t.daemon = True
            t.start()
            time.sleep(0.1)

            res[copy_number] = q.get().model
        ## Since this is being executed in parallel sometimes
        ## we get process clashes. Not sure exactly whats going on
        ## but introducing a small delay seems to fix
        time.sleep(0.1)
        return res


    def run(self):
        """

        :return:
        :param models: dict of models. Output from setup()
        """
        ##load cps from pickle in case run not being use straignt after set_up
        try:
            self.models
        except AttributeError:
            raise errors.IncorrectUsageError('You must use the setup method before the run method')

        if self.run_mode == 'SGE':
            try:
                check_call('qhost')
            except errors.NotImplementedError:
                LOG.warning('Attempting to run in SGE mode but SGE specific commands are unavailable. Switching to \'multiprocess\' mode')
                self.run_mode = 'multiprocess'
        # if os.path.isfile(self.copasi_file_pickle):
        #     with open(self.copasi_file_pickle) as f:
        #         self.sub_copasi_files=pickle.load(f)
        for copy_number, model in self.models.items():
            LOG.info('running model: {}'.format(copy_number))
            Run(model, mode=self.run_mode, task='scan')

    def setup(self):
        """
        Over-ride the setup method from parameter estimation.
        Basically do the same thing but add a few methods.

        :return:
        """
        ## create output directory
        self._create_output_directory()

        ## map experiments
        EM = ExperimentMapper(self.model, self.experiment_files, **self._experiment_mapper_args)

        ## get model from ExperimentMapper
        self.model = EM.model

        ## create a report for PE results collection
        self.model = self.define_report()

        ## get rid of existing parameter estimation definition
        self.model = self.remove_all_fit_items()

        ## create new parameter estimation
        self.model = self.set_PE_method()
        self.model = self.set_PE_options()
        self.model = self.insert_all_fit_items()

        ## ensure we have model
        assert self.model != None
        assert isinstance(self.model, model.Model)

        ##copy the number `copy_number` times
        models = self.copy_model()

        ## ensure we have dict of models
        assert isinstance(models, dict)
        assert len(models) == self.copy_number

        ##create a scan per model (again models is dict of model.Model's
        self.models = self._setup_scan(models)
        assert isinstance(models[0], model.Model)
        return models


    # def format_results(self):
    #     """
    #     Copasi output does not have headers. This function
    #     gives PE data output headers
    #     :return: list. Path to report files
    #     """
    #     try:
    #         cps_keys = self.sub_copasi_files.keys()
    #     except AttributeError:
    #         self.setup()
    #         cps_keys = self.sub_copasi_files.keys()
    #     report_keys = self.report_files.keys()
    #     for i in range(len(self.report_files)):
    #         try:
    #             FormatPEData(self.sub_copasi_files[cps_keys[i]], self.report_files[report_keys[i]],
    #                      report_type='multi_parameter_estimation')
    #         except errors.InputError:
    #             LOG.warning('{} is empty. Cannot parse. Skipping this file'.format(self.report_files[report_keys[i]]))
    #             continue
    #     return self.report_files





    ##void

#
#     ## void

#
#


@mixin(UpdatePropertiesMixin)
@mixin(Bool2Numeric)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
class MultiModelFit(object):
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
            use the setup() method. Then open one of the child copasi files
            in order to check that things are configured how you'd like them before
            using the run_mode() method.


        **kwargs:
            copy_number:
                Default = 1. This is how many times to copy a copasi file before
                running the parameter estimation on each model.
            pe_number:
                Default = 3. How many parameter estimations to perform in one model.
                i.e. a repeat scan task is automatically configured.

            All other kwargs are described in runMultiplePEs or ParameterEstimation
    '''
    def __init__(self, project_dir, **kwargs):
        self.project_dir = project_dir
#        self.config_filename=config_filename
        self.kwargs = kwargs

        ## This needs to be before setting default properties
        ## so we have access to exp_files and cps_files for lengths
        self.cps_files, self.exp_files = self.read_fit_config()

        # self.default_properties = {'run_mode': 'multiprocess',
        #                            'copy_number': 1,
        #                            'pe_number': 3,
        #                            'metabolites': [],
        #                            'global_quantities': [],
        #                            'local_parameters': [],
        #                            'report_name': 'PE_report.csv',
        #                            'results_directory': os.path.join(
        #                                os.path.dirname(self.cps_files[0]), 'MultiModelFit'),
        #                            ##default parameters for ParameterEstimation
        #                            'method': 'genetic_algorithm',
        #                            'plot': False,
        #                            'quantity_type': 'concentration',
        #                            'append': False,
        #                            'confirm_overwrite': False,
        #                            'config_filename': 'config_file.csv',
        #                            'overwrite_config_file': False,
        #                            'prune_headers': True,
        #                            'update_model': False,
        #                            'randomize_start_values': True,
        #                            'create_parameter_sets': False,
        #                            'calculate_statistics': False,
        #                            'use_config_start_values': False,
        #                            #method options
        #                            #'DifferentialEvolution',
        #                            'number_of_generations': 200,
        #                            'population_size': 50,
        #                            'random_number_generator': 1,
        #                            'seed': 0,
        #                            'pf': 0.475,
        #                            'iteration_limit': 50,
        #                            'tolerance': 0.0001,
        #                            'rho': 0.2,
        #                            'scale': 10,
        #                            'swarm_size': 50,
        #                            'std_deviation': 0.000001,
        #                            'number_of_iterations': 100000,
        #                            'start_temperature': 1,
        #                            'cooling_factor': 0.85,
        #                            #experiment definition options
        #                            #need to include options for defining multiple experimental files at once
        #                            'row_orientation': [True]*len(self.exp_files),
        #                            'experiment_type': ['timecourse']*len(self.exp_files),
        #                            'first_row': [str(1)]*len(self.exp_files),
        #                            'normalize_weights_per_experiment': [True]*len(self.exp_files),
        #                            'row_containing_names': [str(1)]*len(self.exp_files),
        #                            'separator': ['\t']*len(self.exp_files),
        #                            'weight_method': ['mean_squared']*len(self.exp_files),
        #                            'save': 'overwrite',
        #                            'scheduled': False,
        #                            'lower_bound': 0.000001,
        #                            'upper_bound': 1000000}
        # # print self.exp_files
        # self.convert_bool_to_numeric(self.default_properties)
        # self.update_properties(self.default_properties)
        # self.default_properties.update(self.kwargs)
        # self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self._do_checks()

        self.sub_cps_dirs=self.create_workspace()
        self.MPE_dct=self.instantiate_run_multi_PEs_class()
        self.results_folder_dct=self.get_output_directories()

    def _do_checks(self):
        pass

    def __iter__(self):
        for MPE in self.MPE_dct.values():
            yield MPE

    def __getitem__(self, item):
        return self.MPE_dct[item]

    def __setitem__(self, key, value):
        self.MPE_dct[key] = value

    def __delitem__(self, key):
        del self.MPE_dct[key]

    def keys(self):
        return self.MPE_dct.keys()

    def values(self):
        return self.MPE_dct.values()

    def items(self):
        return self.MPE_dct.items()

    def instantiate_run_multi_PEs_class(self):
        """
        pass correct arguments to the runMultiplePEs class in order
        to instantiate a runMultiplePEs instance for each model.

        :Returns: dict[model_filename]=runMultiplePEs_instance
        """
        dct={}

        for cps_dir in self.sub_cps_dirs:
            os.chdir(cps_dir)

            # if os.path.isabs(self.config_filename):
            #     self.config_filename = os.path.split(self.config_filename)[1]

            m = model.Model(self.sub_cps_dirs[cps_dir])


            dct[self.sub_cps_dirs[cps_dir]] = MultiParameterEstimation(
                self.sub_cps_dirs[cps_dir], self.exp_files,
                **self.kwargs
            )

        return dct

    def get_output_directories(self):
        """
        :returns:Dict. Location of parameter estimation output files
        """
        output_dct={}
        for MPE in self.MPE_dct:
            output_dct[MPE]=self.MPE_dct[MPE].results_directory
        return output_dct

    #void
    def write_config_file(self):
        """
        A class to write a config file template for each
        model in the analysis. Calls the corresponding
        write_config_file from the runMultiplePEs class
        :returns: list. config file paths
        """
        conf_list=[]
        for MPE in self.MPE_dct:
            f = self.MPE_dct[MPE].write_config_file()
            conf_list.append(f)
        return conf_list

    def setup(self):
        """
        A user interface class which calls the corresponding
        method (setup) from the runMultiplePEs class per model.
        Perform the ParameterEstimation.setup() method on each model.
        """
        for MPE in self.MPE_dct:
            self.MPE_dct[MPE].setup()

    def run(self):
        """
        A user interface class which calls the corresponding
        method (run) from the runMultiplePEs class per model.
        Perform the ParameterEstimation.run() method on each model.
        :return:
        """
        for MPE in self.MPE_dct:
            LOG.info('Running models from {}'.format(self.MPE_dct[MPE].results_directory))
            self.MPE_dct[MPE].run()


    def create_workspace(self):
        """
        Creates a workspace from cps and experiment files in self.project_dir

        i.e.
            --project_dir
            ----model1_dir
            ------model1.cps
            ------exp_data.txt
            ----model2_dir
            ------model2.cps
            ------exp_data.txt

        :returns: Dictionary[cps_filename]= Directory for model fit
        """
        LOG.info('Creating workspace from project_dir')
        ## Create entire working directory for analysis
        self.wd = self.project_dir
        if os.path.isdir(self.wd)!=True:
            os.mkdir(self.wd)
        os.chdir(self.project_dir)
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
                raise Exception('Error in copying copasi file to sub directories')
            cps_dirs[sub_cps_dir]=sub_cps_abs
        LOG.info('Workspace created')
        return cps_dirs

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
        if self.project_dir==None:
            raise errors.InputError('Cannot read multifit confuration as no Project kwarg is provided')
        ##make sure we're in the right directory
        os.chdir(self.project_dir)
        LOG.info('project dir is --> {}'.format(self.project_dir))
        cps_list=[]
        for cps_file in glob.glob('*.cps'):
            cps_list.append(cps_file)

        exp_list=[]
        exp_file_types=('*.csv','*.txt')
        for typ in exp_file_types:

            for exp_file in glob.glob(typ):
                exp_list.append(os.path.abspath(exp_file))
        if cps_list==[]:
            raise errors.InputError('No cps files in your project')
        if exp_list==[]:
            raise errors.InputError('No experiment files in your project')
        return cps_list, exp_list


    def format_data(self):
        """
        Method for giving appropiate headers to parameter estimation data
        """
        for MPE in self.MPE_dct:
            self.MPE_dct[MPE].format_results()


@mixin(model.GetModelComponentFromStringMixin)
@mixin(UpdatePropertiesMixin)
@mixin(Bool2Numeric)
@mixin(model.ReadModelMixin)
@mixin(CheckIntegrityMixin)
class ProfileLikelihood(object):
    def __init__(self, model, **kwargs):
        self.model = self.read_model(model)
        self.kwargs = kwargs

        self.default_properties = {
            'x': self.model.fit_item_order,
            'df': None,
            'index': 'current_parameters',
            'parameter_path': None,
            'quantity_type': 'concentration',
            'upper_bound_multiplier': 1000,
            'lower_bound_multiplier': 1000,
            'intervals': 10,
            'log10': True,
            'append': False,
            'output_in_subtask': False,
            'run_mode': False,
            'processes': 1,
            'results_directory': os.path.join(self.model.root,
                                              'ProfileLikelihoods'),
            'method': 'genetic_algorithm',
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

            'parallel_scan': True,
        }
        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self._do_checks()
        self._convert_numeric_arguments_to_string()

        ##configures parameter estimation method parameters
        self.model = self.undefine_other_reports()
        self.model = self.uncheck_randomize_start_values()
        self.model = self.make_experiment_files_absolute()
        self.model = self.set_PE_method()
        self.index_dct, self.parameters = self.insert_parameters()
        self.model_dct = self.copy_model()
        # self.model_dct = self.setup_report()
        self.model_dct = self.setup_parameter_estimation()

        self.model_dct = self.setup_scan()
        self.to_file()
        # self.model_dct['current_parameters'][r'Ski'].open()

        if self.run_mode is not False:
            self.run()




        # else:
        #     self.run()
        #

    def _do_checks(self):
        """

        :return:
        """
        if isinstance(self.index, int):
            self.index = [self.index]
        if self.df is None:
            if self.index == 'current_parameters':
                LOG.warning('Parameter estimation data has been specified without an index so will be ignored. Specify argument to index kwarg')

        if isinstance(self.x, str):
            self.x = self.get_variable_from_string(self.model, self.x)

        if ((self.df is None) and (self.parameter_path is None)) and (self.index != 'current_parameters'):
            LOG.warning('Got index argument without df argument. Setting index to "current_parameters"')
            self.index = 'current_parameters'


    def _convert_numeric_arguments_to_string(self):
        """
        xml requires all numbers to be strings.
        This method makes this conversion
        :return: void
        """
        self.number_of_generations = str(self.number_of_generations)
        self.population_size = str(self.population_size)
        self.random_number_generator = str(self.random_number_generator)
        self.seed = str(self.seed)
        self.pf = str(self.pf)
        self.iteration_limit = str(self.iteration_limit)
        self.tolerance = str(self.tolerance)
        self.rho = str(self.rho)
        self.scale = str(self.scale)
        self.swarm_size = str(self.swarm_size)
        self.std_deviation = str(self.std_deviation)
        self.number_of_iterations = str(self.number_of_iterations)
        self.start_temperature = str(self.start_temperature)
        self.cooling_factor = str(self.cooling_factor)

    def uncheck_randomize_start_values(self):
        """
        Untick the randomize_start_values box
        :return:
            :py:class:`model.Model`
        """
        query = '//*[@name="Parameter Estimation"]'
        for i in self.model.xml.xpath(query):
            if 'type' in i.keys():
                if i.attrib['type'] == 'parameterFitting':
                    for j in i:
                        if j.tag == '{http://www.copasi.org/static/schema}Problem':
                            for k in j:
                                if k.attrib['name'] == 'Maximize':
                                    k.attrib['value'] = str(0)

                                if k.attrib['name'] == 'Randomize Start Values':
                                    k.attrib['value'] = str(0)

                                if k.attrib['name'] == 'Calculate Statistics':
                                    k.attrib['value'] = str(0)
        self.model.save()
        return self.model



    def _select_method(self):
        """
        copied from Parameter estimation class
        :return:
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

    def set_PE_method(self):
        """
        This method is copied from the parameter estimation
        class.
        :return: model
        """

        #Build xml for method.
        method_name, method_type = self._select_method()
        method_params = {'name': method_name, 'type': method_type}
        method_element = etree.Element('Method', attrib=method_params)

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

        method = tasks[5][-1]
        parent = method.getparent()
        parent.remove(method)
        parent.insert(2, method_element)
        return self.model

    def insert_parameters(self):
        """
        If index keyword is 'current_parameters', do nothing but collect
        parameter values which are defined in parameter estimation task.
        If index keyword specified, get the corresponding best parameter
        set from df or parameter_path arguments and insert into the model.

        :return:
            `tuple`. (`dict[index] = model with parameter set`,
                      `dict[index] = estimated parameter values)
        """
        dct = {}
        parameters = {}
        if self.index == 'current_parameters':
            dct['current_parameters'] = self.model
            parameters = self.model.parameters[self.model.fit_item_order]
        else:
            for i in self.index:
                I = model.InsertParameters(
                    self.model, df=self.df,
                    parameter_path=self.parameter_path, index=i
                )
                new_model = I.model
                dct[i] = new_model

                parameters[i] = I.parameters#new_model.parameters[new_model.fit_item_order]
        return dct, parameters


    def copy_model(self):
        """
        copy for each member of x
        :return:
        """
        dct = {}
        for model in self.index_dct:
            dct[model] = {}
            for param in self.x:
                new_dir = os.path.join(self.results_directory, str(model))
                new_copasi_filename = os.path.join(new_dir, misc.RemoveNonAscii(param).filter+'.cps')
                dct[model][param] = self.index_dct[model].copy(new_copasi_filename)
                dct[model][param].save()
                ##problem with model name needing to be changed everywhere
                # dct[model][param].name = param
        return dct

    def make_experiment_files_absolute(self):
        """
        copy data files that are mapped to model
        variables into the profile likelihood directories
        :return:
        """
        query = '//*[@name="File Name"]'
        for i in self.model.xml.xpath(query):
            fle = os.path.abspath(i.attrib['value'])
            i.attrib['value'] = fle
        return self.model


    def undefine_other_reports(self):
        """
        remove reports defined elsewhere, i.e. the parameter estimation task
        :return:
        """
        query = '//*[@target]'
        for i in self.model.xml.xpath(query):
            if i.attrib['target'] != '':
                i.attrib['target'] = ''
        return self.model

    def setup_parameter_estimation(self):
        """
        for each model, remove the x parameter from
        the parameter estimation task
        :return:
        """
        query = "//*[@name='FitItem']" #query="//*[@name='FitItem']"
        for model in self.model_dct:
            count = 0
            for param in self.model_dct[model]:
                ##ascertain which parameter this is
                for i in self.model_dct[model][param].xml.xpath(query):
                    count += 1
                    for j in i:
                        if j.attrib['name'] == 'ObjectCN':
                            ## for globals
                            global_quantities = re.findall('.*Values\[(.*)\]', j.attrib['value'])
                            local_parameters = re.findall('.*Reactions\[(.*)\].*Parameter=(.*),', j.attrib['value'])
                            metabolites = re.findall('.*Metabolites\[(.*)\],', j.attrib['value'])
                            if local_parameters != []:

                                local_parameters = "({}).{}".format(local_parameters[0][0], local_parameters[0][1])
                                if local_parameters == param:
                                    j.getparent().getparent().remove(j.getparent())

                            elif metabolites != []:
                                if metabolites[0] == param:
                                    j.getparent().getparent().remove(j.getparent())

                            elif global_quantities != []:
                                if global_quantities[0] == param:
                                    j.getparent().getparent().remove(j.getparent())

        if count == 0:
            raise errors.NoFitItemsError('Model does not contain any fit items. Please setup a parameter estimation and try again')

        ##save is needed
        self.to_file()

        return self.model_dct

    # def setup_report(self):
    #     for model in self.model_dct:
    #         for param in self.model_dct[model]:
    #             st = misc.RemoveNonAscii(param).filter
    #             self.model_dct[model][param] = Reports(
    #                 self.model_dct[model][param],
    #                 report_type='multi_parameter_estimation',
    #                 report_name=st + '.txt'
    #             ).model
    #             self.model_dct[model][param].save()
    #     return self.model_dct

    def to_file(self):
        """
        create and write our profile likelihood
        analysis to file
        :return:
        """
        dct = {}
        for model in self.model_dct:
            dct[model] = {}
            for param in self.model_dct[model]:
                ##already given new filename in copy_copasi
                self.model_dct[model][param].save()
        return dct


    def setup1scan(self, q, model, report, parameter, parameter_value):
        """
        Setup a single scan.
        :param q: queue from multiprocessing
        :param model: pycotools.model.Model
        :param report: str.
        :return:
        """
        start = time.time()
        models = q.put(Scan(
            model,
            scan_type='scan',
            variable=parameter,
            number_of_steps=self.intervals,
            subtask='parameter_estimation',
            report_type='profile_likelihood',
            report_name=report,
            run=False,
            append=self.append,
            clear_scans=True,
            output_in_subtask=False,#self.output_in_subtask,
            minimum=parameter_value / self.lower_bound_multiplier,
            maximum=parameter_value * self.lower_bound_multiplier,
            log10=self.log10
            )
        )


    def setup_scan(self):
        """
        Set up `copy_number` repeat items with `pe_number`
        repeats of parameter estimation. Set run_mode to false
        as we want to use the multiprocess mode of the run_mode class
        to process all files at once in CopasiSE
        :return:
        """
        number_of_cpu = cpu_count()
        q = Queue.Queue(maxsize=number_of_cpu)
        # report_files = self.enumerate_PE_output()
        res = {}
        res = {}
        for model in self.model_dct:
            res[model] = {}
            for param in self.model_dct[model]:
                report_name = os.path.join(
                    self.model_dct[model][param].root,
                    os.path.splitext(
                        self.model_dct[model][param].copasi_file
                    )[0]+'.csv'
                )
                parameter_value = float(self.parameters[model][param])
                # if self.parallel_scan:
                t = threading.Thread(
                    target=self.setup1scan,
                    args=(
                        q, self.model_dct[model][param],
                        report_name, param, parameter_value
                    )
                )
                t.daemon = True
                t.start()
                # Since this is being executed in parallel sometimes
                # we get process clashes. Not sure exactly whats going on
                # but introducing a small delay seems to fix
                time.sleep(0.1)
                res[model][param] = q.get().model
                res[model][param].save()
        return res


    def run(self):
        """

        :return:
        """
        for model in self.model_dct:
            for param in self.model_dct[model]:
                LOG.info('running {}'.format(self.model_dct[model][param].copasi_file))
                sge_job_filename = "{}_{}".format(param, model)
                sge_job_filename = re.sub('[().]', '', sge_job_filename)
                Run(self.model_dct[model][param], task='scan', mode=self.run_mode, sge_job_filename=sge_job_filename+'.sh')

if __name__=='__main__':
    pass
#    execfile('/home/b3053674/Documents/Models/2017/08_Aug/pycotoolsTests/RunPEs.py')
        #    execfile('/home/b3053674/Documents/pycotools/pycotools/pycotoolsTutorial/Test/testing_kholodenko_manually.py')
