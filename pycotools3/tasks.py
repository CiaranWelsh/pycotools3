# -*- coding: utf-8 -*-
'''
 This file is part of pycotools3.

 pycotools3 is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools3 is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools3.  If not, see <http://www.gnu.org/licenses/>.


 $Author: Ciaran Welsh
 $Date: 12-09-2016
 Time:  13:33

'''
from . import viz
from . import errors
from . import misc
from . import model
from .munch import Munch
from . import munch
import time
import threading
import queue as queue
import psutil
import shutil
import numpy
import pandas
from lxml import etree
from io import StringIO
import logging
import os
import subprocess
import re
from .utils import load_copasi
from multiprocessing import Process, cpu_count
import glob
import seaborn as sns
from copy import deepcopy
from subprocess import check_call
from collections import OrderedDict, Mapping
from .mixin import mixin
from functools import reduce
import yaml, json
import sys
import itertools

# COPASISE, COPASIUI = load_copasi()

LOG = logging.getLogger(__name__)

sns.set_context(context='poster',
                font_scale=3)


class _Task(object):
    """base class for tasks"""
    schema = '{http://www.copasi.org/static/schema}'

    @staticmethod
    def get_variable_from_string(m, v, glob=False):
        """Use model entity name to get the
        pycotools3 variable

        Args:
          m: py:class:`model`
          v: str` variable in model
          glob:  (Default value = False)

        Returns:
          variable as a model component

        """
        if not isinstance(m, model.Model):
            raise errors.InputError('expected model.Model but got "{}" instance'.format(
                type(m)
            ))
        if not isinstance(v, str):
            raise errors.InputError('variable_name should be a string')
        ## allow a user to input a string not pycotools3.model class
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
                raise errors.InputError('Variable "{}" is not in model "{}". '
                                        'These are your model variables:\n '
                                        '{} \n These are local_parameters '
                                        'with global_quantities assigned '
                                        'to them: \n"{}"'.format(v, m.name, m.all_variable_names,
                                                                 [i.global_name for i in assignments]))
        assert isinstance(v, str) != True
        return v

    def update_properties(self, kwargs):
        """method for updating properties from kwargs

        Args:
          kwargs: dict of options for subclass

        Returns:
          void

        """
        for k in kwargs:
            try:
                getattr(self, k)
                setattr(self, k, kwargs[k])
            except AttributeError:
                setattr(self, k, kwargs[k])

    @staticmethod
    def convert_bool_to_numeric(dct):
        """CopasiML uses 1's and 0's for True or False in some
        but not all places. When one of these options
        is required by the user and is specified as bool,
        this class converts them into 1's or 0's.
        
        Use this method in early on in constructor for
        all subclasses where this applies.

        Args:
          dct: 

        Returns:
          dict` with certain boolean args as 1's and 0's

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
        for k, v in list(dct.items()):
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

    def convert_bool_to_numeric2(self):
        """CopasiML uses 1's and 0's for True or False in some
        but not all places. When one of these options
        is required by the user and is specified as bool,
        this class converts them into 1's or 0's.
        
        This is like convert_bool_to_numeric but
        uses setattr

        Args:

        Returns:

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
               'row_orientation',
               'normalize_weights_per_experiment',
               ]
        for attr in lst:
            try:
                ans = getattr(self, attr)
                if isinstance(ans, bool):
                    if ans:
                        setattr(self, attr, '1')
                    elif not ans:
                        setattr(self, attr, '0')
                    else:
                        if ans not in [True, False, '0', '1']:
                            raise ValueError
                elif isinstance(ans, list):
                    new_list = []
                    for b in ans:
                        if not isinstance(b, bool):
                            raise TypeError
                        if b:
                            new_list.append('1')
                        elif not b:
                            new_list.append('0')
                        else:
                            if b not in [True, False, '0', '1']:
                                raise ValueError
                    setattr(self, attr, new_list)
            except AttributeError:
                continue

    @staticmethod
    def check_integrity(allowed, given):
        """Method to raise an error when a wrong
        kwarg is passed to a subclass

        Args:
          allowed: list`. List of allowed kwargs
          given: List of kwargs given by user or default

        Returns:
          None

        """
        for key in given:
            if key not in allowed:
                raise errors.InputError('{} not in {}'.format(key, allowed))


class Bool2Str(object):
    """copasiML expects strings and we pythoners
    want to use python booleans not strings
    This class quickly converts between them

    Args:

    Returns:

    """

    def __init__(self, dct):
        """

        :param dct: dict[kwarg] = boolean
        """
        self.dct = dct
        if isinstance(self.dct, dict) != True:
            raise errors.InputError('Input must be dict')

        self.acceptable_kwargs = [
            'append', 'confirm_overwrite', 'update_model',
            'output_in_subtask', 'adjust_initial_conditions',
            'randomize_start_values', 'log10',
            'scheduled', 'output_event',
        ]

    def convert(self, boolean):
        """

        Args:
          boolean: 

        Returns:

        """
        if boolean == True:
            return "true"
        elif boolean == False:
            return "false"
        else:
            raise errors.InputError('Input should be boolean not {}'.format(isinstance(boolean)))

    def convert_dct(self):
        """----"""
        for kwarg in list(self.dct.keys()):
            if kwarg in self.acceptable_kwargs:
                if self.dct[kwarg] == True:
                    self.dct.update({kwarg: "true"})
                else:
                    self.dct.update({kwarg: "false"})
        #
        return self.dct


class CopasiMLParser(_Task):
    """Parse a copasi file into xml.etree.
    
    .. highlight::

    Args:

    Returns:

    >>> model_path = r'/full/path/to/model.cps'
        >>> xml = CopasiMLParser(model_path).xml
    """

    def __init__(self, copasi_file):
        """

        :param copasi_file:
            `str` full path to a copasi file
        """
        self.copasi_file = copasi_file
        if os.path.isfile(self.copasi_file) != True:
            raise errors.FileDoesNotExistError('{} is not a copasi file'.format(self.copasi_file))
        self.copasiMLTree = self._parse_copasiML()
        self.copasiML = self.copasiMLTree.getroot()
        self.xml = self.copasiMLTree.getroot()

        os.chdir(os.path.dirname(self.copasi_file))

    def _parse_copasiML(self):
        """Parse xml doc with lxml
        :return:

        Args:

        Returns:

        """
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(self.copasi_file, parser)
        return tree

    @staticmethod
    def write_copasi_file(copasi_filename, xml):
        """write to file with lxml write function

        Args:
          copasi_filename: 
          xml: 

        Returns:

        """
        # first convert the copasiML to a root element tree
        root = etree.ElementTree(xml)
        root.write(copasi_filename)


@mixin(model.ReadModelMixin)
class Run(_Task):
    """Execute a copasi model using CopasiSE. To
    be operational the environment variable CopasiSE
    must be set to point towards the location of
    your CopasiSE executable. This is usually
    done automatically.
    
    .. highlight::
    
        ## First get a model object
    
    To run a time_course task
    
    To run the parameter estimation task:
    
    To run the parameter estimation task with :py:mod:`multiprocessing`
    
    To run the scan task but have python write a .sh script for submission to sun grid engine:
    
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
    parallel                Run several at once
    sge                     Run on sun grid engine
    slurm                   Run on Slurm
    =============           ==============

    Args:

    Returns:

    >>> model_path = r'/full/path/to/model.cps'
        >>> model = model.Model(model_path)
    
        >>> Run(model, task='time_course', mode=True)
    
        >>> Run(model, task='parameter_estimation', mode=True)
    
        >>> Run(model, task='parameter_estimation', mode='multiprocess')
    
        >>> Run(model, task='scan', mode='sge')
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
                                   'sge_job_filename': None,
                                   # 'copasi_location': COPASI_DIR
                                   # 'copasi_location': 'apps/COPASI/4.21.166-Linux-64bit',  # for sge mode
                                   }

        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(list(self.default_properties.keys()), list(self.kwargs.keys()))
        self._do_checks()

        if self.sge_job_filename is None:
            self.sge_job_filename = os.path.join(os.getcwd(), 'sge_job_file.sh')

        # if self.mode is 'slurm':
        #     self.copasi_location = r'COPASI/4.22.170'

        self.model = self.set_task()
        self.model.save()

        if self.mode is True:
            try:
                self.run()
            except errors.CopasiError:
                self.run_linux()

        elif self.mode == 'sge':
            self.submit_copasi_job_SGE()

        elif self.mode == 'slurm':
            self.submit_copasi_job_slurm()

    def _do_checks(self):
        """Varify integrity of user input
        :return:

        Args:

        Returns:

        """
        tasks = ['steady_state', 'time_course',
                 'scan', 'flux_mode', 'optimization',
                 'parameter_estimation', 'metabolic_control_analysis',
                 'lyapunov_exponents', 'time_scale_separation_analysis',
                 'sensitivities', 'moieties', 'cross_section',
                 'linear_noise_approximation']
        if self.task not in tasks:
            raise errors.InputError('{} not in list of tasks. List of tasks are: {}'.format(self.task, tasks))

        modes = [True, False, 'multiprocess', 'parallel', 'sge', 'slurm']
        if self.mode not in modes:
            raise errors.InputError('{} not in {}'.format(self.mode, modes))

    def __str__(self):
        return 'Run({})'.format(self.to_string())

    def multi_run(self):
        """ """
        pids = []

        def run(x):
            """

            Args:
              x: 

            Returns:

            """
            if os.path.isfile(x) != True:
                raise errors.FileDoesNotExistError('{} is not a file'.format(self.copasi_file))
            p = subprocess.Popen(
                [
                    f'CopasiSE', self.model.copasi_file
                ], shell=True
            )
            return p.pid

        Process(run(self.model.copasi_file))

    def set_task(self):
        """:return:"""
        task = self.task.replace(' ', '_').lower()

        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            i.attrib['scheduled'] = "false"  # set all to false
            task_name = i.attrib['name'].lower().replace('-', '_').replace(' ', '_')
            if task == task_name:
                i.attrib['scheduled'] = "true"
        return self.model

    def run(self):
        """Run copasi model with CopasiSE distributed with pycotools
        :return:

        Args:

        Returns:

        """
        p = subprocess.Popen(f'CopasiSE "{self.model.copasi_file}"', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
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
        """Linux systems do not respond to the run function
        in the same way as windows. This ffunction
        uses basic os.system instead, which linux systems
        do respond to. This solution is less than elegant.
        Look into it further.
        :return:

        Args:

        Returns:

        """
        ##TODO find better solution for running copasi files on linux
        os.system(f'CopasiSE {self.model.copasi_file}')

    def submit_copasi_job_SGE(self):
        """Submit copasi file as job to SGE based job scheduler.

        Args:
          copasi_location: Location to copasi on the sge cluster. Gets passed to `module add` to load copasi

        Returns:
          None

        """
        self.sge_job_filename = self.sge_job_filename.replace('/', '_')
        with open(self.sge_job_filename, 'w') as f:
            f.write('#!/bin/bash\n#$ -V -cwd\nmodule add {}\nCopasiSE "{}"'.format(
                self.copasi_location, self.model.copasi_file
            )
            )

        ## -N option for job namexx
        os.system('qsub "{}" -N "{}" '.format(self.sge_job_filename, self.sge_job_filename))
        os.remove(self.sge_job_filename)

    def submit_copasi_job_slurm(self):
        """Submit copasi file as job to SGE based job scheduler.

        Args:
          copasi_location: Location to copasi on the sge cluster. Gets passed to `module add` to load copasi

        Returns:
          None

        """
        self.sge_job_filename = self.sge_job_filename.replace('/', '_')
        with open(self.sge_job_filename, 'w') as f:
            f.write('#!/bin/bash\n#$ \nmodule add {}\nCopasiSE "{}"'.format(
                self.copasi_location, self.model.copasi_file
            )
            )

        ## -N option for job namexx
        os.system('sbatch "{}"  --job-name "{}"'.format(self.sge_job_filename, self.sge_job_filename))
        ## remove .sh file after used.
        os.remove(self.sge_job_filename)


@mixin(model.GetModelComponentFromStringMixin)
@mixin(model.ReadModelMixin)
class RunParallel(_Task):
    """ """

    def __init__(self, models, **kwargs):
        self.models = models
        self.kwargs = kwargs
        self.default_properties = {
            'max_active': None,
            'task': 'parameter_estimation',
        }
        self.default_properties.update(self.kwargs)
        self.default_properties = self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(list(self.default_properties.keys()), list(self.kwargs.keys()))
        self._do_checks()
        # self.set_task()

        self.models = self.set_task()
        [i.save() for i in self.models]
        self.run_parallel()

    def _do_checks(self):
        """Varify integrity of user input
        :return:

        Args:

        Returns:

        """
        tasks = ['steady_state', 'time_course',
                 'scan', 'flux_mode', 'optimization',
                 'parameter_estimation', 'metabolic_control_analysis',
                 'lyapunov_exponents', 'time_scale_separation_analysis',
                 'sensitivities', 'moieties', 'cross_section',
                 'linear_noise_approximation']
        if self.task not in tasks:
            raise errors.InputError('{} not in list of tasks. List of tasks are: {}'.format(self.task, tasks))

        # modes = [False, 'multiprocess']
        # if self.mode not in modes:
        #     raise errors.InputError('{} not in {}'.format(self.mode, modes))
        if not isinstance(self.models, list):
            raise errors.InputError('input should be a list of models to run')

        for i in self.models:
            if not isinstance(i, model.Model):
                raise errors.InputError('Input should be a list of models to run')

        if self.max_active is None:
            self.max_active = len(self.models)

    # def __str__(self):
    #     return 'RunParallel({})'.format()

    def set_task(self):
        """:return:"""
        task = self.task.replace(' ', '_').lower()
        model_list = []
        for model in self.models:
            for i in model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
                i.attrib['scheduled'] = "false"  # set all to false
                task_name = i.attrib['name'].lower().replace('-', '_').replace(' ', '_')
                if task == task_name:
                    i.attrib['scheduled'] = "true"
            model_list.append(model)
        assert len(self.models) == len(model_list)
        return model_list

    def run_parallel(self):
        """Run models in parallel. Only have self.max_active
        models running at once
        :return:
            None

        Args:

        Returns:

        """
        pids = []
        num_models_to_process = len(self.models)

        while num_models_to_process > 0:

            # for copy_number, model in self.models.items():
            model = self.models[num_models_to_process - 1]
            if len(pids) < int(self.max_active):
                num_models_to_process -= 1
                subp = subprocess.Popen(['CopasiSE', model.copasi_file])
                pids.append(subp.pid)

            try:
                for pid in range(len(pids)):
                    try:
                        p = psutil.Process(pids[pid])
                    except psutil.NoSuchProcess:
                        LOG.info('No such process: {}. Skipping'.format(pid))
                        continue
                    if psutil.pid_exists(pids[pid]) is False:
                        del pids[pid]

                    if p.status() is 'zombie':
                        LOG.info('is zombie')

                        del pids[pid]

            except IndexError:
                LOG.warning('index error skipped')
                continue


@mixin(model.GetModelComponentFromStringMixin)
@mixin(model.ReadModelMixin)
class Reports(_Task):
    """Creates reports in copasi output specification section. Which report is
    controlled by the report_type key word. The following are valid types of
    report:
    
    .. report_kwargs_:

    
    ===========================     ==============================================
    Report Types                    Description
    ===========================     ==============================================
    time_course                     Report definition for collection of
                                    time course data.
    parameter_estimation            Collect parameter estimates from parameter
                                    estimations run from the parameter estimation
                                    task
    multi_parameter_estimation      Collect parameter estimation data from
                                    parameter estimations run from the scan
                                    task with copasi's repeat feature
    profile_likelihood              Collect both the parameter being scanned
                                    value and the parameter estimates
    ===========================     ==============================================
    
    Here are the keyword arguments accepted by the Reports class.
    
    ===========================     ==============================================
    Report options                  Description
    ===========================     ==============================================
    metabolites                     `str` or list of `str`. Metabolites to included
                                    in report
    global_quantities               `str` or list of `str`. global quantities
                                    to included in report
    local_parameters               `str` or list of `str`. local parameters to included
                                    in report
    quantity_type                   `str`. either 'concentration' or 'particle_numbers'
    report_name                     `str` valid path to where you want the report saved
    append                          `bool`. Passed onto to copasi report options
    confirm_overwrite               `bool`. Passed onto to copasi report options
    update_model                    `bool`. Passed onto to copasi report options
    
    variable                        `str` which variable scanned in profile likelihood
    directory                       `str` directory to save report in
    ===========================     ==============================================

    Args:

    Returns:

    """

    def __init__(self, model, **kwargs):
        """
        A class for configuring reports
        Args:
            model(:py:class:`model.Model`):
                Model to add report configuration to

            **kwargs:
                Arguments for report
        """
        # super(Reports, self).__init__(model, **kwargs)
        self.model = self.read_model(model)
        self.kwargs = kwargs
        self.default_properties = {'metabolites': self.model.metabolites,
                                   'global_quantities': self.model.global_quantities,
                                   'local_parameters': self.model.local_parameters,
                                   'compartments': self.model.compartments,
                                   'quantity_type': 'concentration',
                                   'report_name': None,
                                   'append': False,
                                   'confirm_overwrite': False,
                                   'separator': '\t',
                                   'update_model': False,
                                   'report_type': 'parameter_estimation',
                                   'variable': self.model.metabolites[0],  # only for profile_likelihood
                                   'directory': None,
                                   }

        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(list(self.default_properties.keys()), list(self.kwargs.keys()))
        self.__do_checks()

        self.model = self.run()

    def __do_checks(self):
        """
        Varify integrity of user input
        :return:
        """

        if isinstance(self.metabolites, str):
            self.metabolites = [self.metabolites]

        if isinstance(self.global_quantities, str):
            self.global_quantities = [self.global_quantities]

        if isinstance(self.local_parameters, str):
            self.local_parameters = [self.local_parameters]

        if self.quantity_type not in ['concentration', 'particle_numbers']:
            raise errors.InputError('{} not concentration or particle_numbers'.format(self.quantity_type))

        self.report_types = [None, 'profile_likelihood', 'profilelikelihood2',
                             'time_course', 'parameter_estimation', 'multi_parameter_estimation',
                             'sensitivity']
        assert self.report_type in self.report_types, 'valid report types include {}'.format(self.report_types)

        quantity_types = ['particle_numbers', 'concentration']
        assert self.quantity_type in quantity_types

        if self.report_name == None:
            if self.report_type == 'profile_likelihood':
                default_report_name = 'profilelikelihood.txt'

            elif self.report_type == 'profile_likelihood2':
                default_report_name = 'profile_likelihood2.txt'

            elif self.report_type == 'time_course':
                default_report_name = 'time_course.txt'

            elif self.report_type == 'parameter_estimation':
                default_report_name = 'parameter_estimation.txt'

            elif self.report_type == 'multi_parameter_estimation':
                default_report_name = 'multi_parameter_estimation.txt'

            elif self.report_type == 'sensitivity':
                default_report_name = 'sensitivities.txt'

            else:
                raise NotImplementedError

            self.report_name = default_report_name

    def __str__(self):
        return 'Report({})'.format(self.to_string())

    def timecourse(self):
        """creates a report to collect time course results.
        
        By default all species and all global quantities are used with
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the metabolites keyword or global quantities to the
        global quantities keyword

        Args:

        Returns:

        """
        # get existing report keys
        keys = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name'] == 'Time-Course':
                self.model = self.remove_report('time_course')

        new_key = 'Report_30'
        while new_key in keys:
            new_key = 'Report_{}'.format(numpy.random.randint(30, 100))

        ListOfReports = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports,
                                  'Report',
                                  attrib={'precision': '6',
                                          'separator': '\t',
                                          'name': 'Time-Course',
                                          'key': new_key,
                                          'taskType': 'Time-Course'})
        comment = etree.SubElement(report, 'Comment')
        comment = comment  # get rid of annoying squiggly line above
        table = etree.SubElement(report, 'Table')
        table.attrib['printTitle'] = str(1)
        # Objects for the report to report
        time = etree.SubElement(table, 'Object')
        # first element always time.
        time.attrib['cn'] = 'CN=Root,Model={},Reference=Time'.format(self.model.name)

        # for metabolites
        if self.metabolites != None:
            for i in self.metabolites:
                if self.quantity_type == 'concentration':
                    '''
                    A coapsi 'reference' for metabolite in report
                    looks like this:
                        "CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration"
                    '''
                    cn = '{},{},{}'.format(self.model.reference,
                                           i.compartment.reference,
                                           i.transient_reference)
                elif self.quantity_type == 'particle_numbers':
                    cn = '{},{},{}'.format(self.model.reference,
                                           i.compartment.reference,
                                           i.reference)

                # add to xml
                Object = etree.SubElement(table, 'Object')
                Object.attrib['cn'] = cn

        # for global quantities
        if self.global_quantities != None:
            for i in self.global_quantities:
                """
                A Copasi 'reference' for global_quantities in report
                looks like this:
                    cn="CN=Root,Model=New Model,Vector=Values[B2C],Reference=Value"
                """
                cn = '{},{}'.format(self.model.reference, i.transient_reference)
                Object = etree.SubElement(table, 'Object')
                Object.attrib['cn'] = cn
        return self.model

    def scan(self):
        """creates a report to collect scan time course results.
        
        By default all species and all global quantities are used with
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the metabolites keyword or global quantities to the
        global quantities keyword

        Args:

        Returns:

        """
        # get existing report keys

        keys = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name'] == 'Time-Course':
                self.model = self.remove_report('time_course')

        new_key = 'Report_30'
        while new_key in keys:
            new_key = 'Report_{}'.format(numpy.random.randint(30, 100))

        ListOfReports = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports,
                                  'Report',
                                  attrib={'precision': '6',
                                          'separator': '\t',
                                          'name': 'Time-Course',
                                          'key': new_key,
                                          'taskType': 'Time-Course'})
        comment = etree.SubElement(report, 'Comment')
        comment = comment  # get rid of annoying squiggly line above
        table = etree.SubElement(report, 'Table')
        table.attrib['printTitle'] = str(1)
        # Objects for the report to report
        time = etree.SubElement(table, 'Object')
        # first element always time.
        time.attrib['cn'] = 'CN=Root,Model={},Reference=Time'.format(self.model.name)

        if self.metabolites != None:
            for i in self.metabolites:
                if self.quantity_type == 'concentration':
                    '''
                    A coapsi 'reference' for metabolite in report
                    looks like this:
                        "CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration"
                    '''
                    cn = '{},{},{}'.format(self.model.reference,
                                           i.compartment.reference,
                                           i.transient_reference)
                elif self.quantity_type == 'particle_numbers':
                    cn = '{},{},{}'.format(self.model.reference,
                                           i.compartment.reference,
                                           i.reference)

                # add to xml
                Object = etree.SubElement(table, 'Object')
                Object.attrib['cn'] = cn

        # for global quantities
        if self.global_quantities != None:
            for i in self.global_quantities:
                """
                A Copasi 'reference' for global_quantities in report
                looks like this:
                    cn="CN=Root,Model=New Model,Vector=Values[B2C],Reference=Value"
                """
                cn = '{},{}'.format(self.model.reference, i.transient_reference)
                Object = etree.SubElement(table, 'Object')
                Object.attrib['cn'] = cn
        return self.model

    def profile_likelihood(self):
        """Create report of a parameter and best value for a parameter estimation
        for profile likelihoods

        Args:

        Returns:

        """
        # get existing report keys
        keys = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name'] == 'profile_likelihood':
                self.model = self.remove_report('profile_likelihood')

        new_key = 'Report_31'
        while new_key in keys:
            new_key = 'Report_{}'.format(numpy.random.randint(30, 100))
        report_attributes = {'precision': '6',
                             'separator': '\t',
                             'name': 'profile_likelihood',
                             'key': new_key,
                             'taskType': 'Scan'}

        ListOfReports = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports, 'Report')
        report.attrib.update(report_attributes)

        comment = etree.SubElement(report, 'Comment')
        table = etree.SubElement(report, 'Table')
        table.attrib['printTitle'] = str(1)

        if self.variable.name in [i.name for i in self.metabolites]:
            cn = '{},{},{}'.format(self.model.reference, self.variable.compartment.reference,
                                   self.variable.initial_reference)

        elif self.variable.name in [i.name for i in self.global_quantities]:
            cn = '{},{}'.format(self.model.reference, self.variable.initial_reference)

        elif self.variable.name in [i.name for i in self.local_parameters]:
            cn = '{},{},{}'.format(self.model.reference, self.variable.get_reaction().reference,
                                   self.variable.value_reference)

        etree.SubElement(table, 'Object', attrib={'cn': cn})
        etree.SubElement(table, 'Object', attrib={
            'cn': "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"})
        etree.SubElement(table, 'Object', attrib={
            'cn': "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.model

    def parameter_estimation(self):
        """Define a parameter estimation report and include the progression
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords.

        Args:

        Returns:

        """
        # get existing report keys
        keys = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name'] == 'parameter_estimation':
                self.model = self.remove_report('parameter_estimation')

        new_key = 'Report_32'
        while new_key in keys:
            new_key = 'Report_{}'.format(numpy.random.randint(30, 100))
        report_attributes = {'precision': '6',
                             'separator': '\t',
                             'name': 'parameter_estimation',
                             'key': new_key,
                             'taskType': 'parameterFitting'}

        ListOfReports = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports, 'Report')
        report.attrib.update(report_attributes)
        comment = etree.SubElement(report, 'Comment')
        footer = etree.SubElement(report, 'Footer')
        Object = etree.SubElement(footer, 'Object')
        Object.attrib[
            'cn'] = "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"
        Object = etree.SubElement(footer, 'Object')
        Object.attrib[
            'cn'] = "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"
        return self.model

    def multi_parameter_estimation(self):
        """Define a parameter estimation report and include the progression
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords.

        Args:

        Returns:

        """
        # get existing report keys
        keys = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name'] == 'multi_parameter_estimation':
                self.model = self.remove_report('multi_parameter_estimation')

        new_key = 'Report_32'
        while new_key in keys:
            new_key = 'Report_{}'.format(numpy.random.randint(30, 100))
        report_attributes = {'precision': '6',
                             'separator': '\t',
                             'name': 'multi_parameter_estimation',
                             'key': new_key,
                             'taskType': 'parameterFitting'}

        ListOfReports = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports, 'Report')
        report.attrib.update(report_attributes)
        comment = etree.SubElement(report, 'Comment')
        table = etree.SubElement(report, 'Table')
        table.attrib['printTitle'] = str(1)
        etree.SubElement(table, 'Object', attrib={
            'cn': "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"})
        etree.SubElement(table, 'Object', attrib={
            'cn': "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.model

    def sensitivity(self):
        """ """
        # get existing report keys
        keys = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name'] == 'sensitivity':
                self.model = self.remove_report('sensitivity')

        new_key = 'Report_31'
        while new_key in keys:
            new_key = 'Report_{}'.format(numpy.random.randint(30, 100))
        report_attributes = {'precision': '6',
                             'separator': '\t',
                             'name': 'sensitivity',
                             'key': new_key,
                             'taskType': 'Sensitivities'}

        ListOfReports = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports, 'Report')
        report.attrib.update(report_attributes)

        comment = etree.SubElement(report, 'Comment')
        table = etree.SubElement(report, 'Table')
        table.attrib['printTitle'] = str(1)

        etree.SubElement(table, 'Object', attrib={
            'cn': "CN=Root,Vector=TaskList[Sensitivities],Object=Result"
        })
        return self.model

    def run(self):
        """Execute code that builds the report defined by the kwargs"""
        if self.report_type == 'parameter_estimation':
            self.model = self.parameter_estimation()

        elif self.report_type == 'multi_parameter_estimation':
            self.model = self.multi_parameter_estimation()

        elif self.report_type == 'profile_likelihood':
            self.model = self.profile_likelihood()

        elif self.report_type == 'time_course':
            self.model = self.timecourse()

        elif self.report_type == 'sensitivity':
            self.model = self.sensitivity()

        elif self.report_type == None:
            self.model = self.model

        else:
            raise NotImplementedError

        return self.model

    def remove_report(self, report_name):
        """remove report called report_name

        Args:
          report_name: return: pycotools3.model.Model

        Returns:
          pycotools3.model.Model

        """
        assert report_name in self.report_types, '{} not a valid report type. These are valid report types: {}'.format(
            report_name, self.report_types)
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if report_name == 'time_course':
                report_name = 'time-course'
            if i.attrib['name'].lower() == report_name.lower():
                i.getparent().remove(i)
        return self.model

    def clear_all_reports(self):
        """Having multile reports defined at once can be really annoying
        and give you unexpected results. Use this function to remove all reports
        before defining a new one to ensure you only have one active report any once.
        :return:

        Args:

        Returns:

        """
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            for j in list(i):
                if 'target' in list(j.attrib.keys()):
                    j.attrib['target'] = ''
        return self.model


@mixin(model.ReadModelMixin)
class TimeCourse(_Task):
    """
    Simulate a time course

    A class for running a time course from python using a copasi model. All but one
    of copasi's solvers are supported and available via the `method` kwarg.

    .. _timecourse_kwargs:

    
    ===========================     ==============================================
    TimeCourse Kwargs               Description
    ===========================     ==============================================
    intervals                       Default: 100
    step_size                       Default: 0.01
    end                             Default: 1
    start                           Default: 0
    update_model                    Default: False
    method                          Default: deterministic
    output_event                    Default: False
    scheduled                       Default: True
    automatic_step_size             Default: False
    start_in_steady_state           Default: False
    integrate_reduced_model         Default: False
    relative_tolerance              Default: 1e-6
    absolute_tolerance              Default: 1e-12
    max_internal_steps              Default: 10000
    max_internal_step_size          Default: 0
    subtype                         Default: 2
    use_random_seed                 Default: True
    random_seed                     Default: 1
    epsilon                         Default: 0.001
    lower_limit                     Default: 800
    upper_limit                     Default: 1000
    partitioning_interval           Default: 1
    runge_kutta_step_size           Default: 0.001
    run                             Default: True
    correct_headers                 Default: True
    save                            Default: False
    <report_kwargs>                 Arguments for :ref:` report_kwargs <report_kwargs>` are also
                                    accepted here
    ===========================     ==============================================

    Args:

    Returns:

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
                              'correct_headers': True,
                              'save': False,
                              }
        default_properties.update(kwargs)
        default_properties = self.convert_bool_to_numeric(default_properties)
        self.check_integrity(list(default_properties.keys()), list(kwargs.keys()))
        self.update_properties(default_properties)
        self._do_checks()

        self.set_timecourse()
        self.set_report()

        self.simulate()

        ## self.correct_output_headers()

        if self.save:
            self.model.save()

    def _do_checks(self):
        """method for checking user input
        :return: void

        Args:

        Returns:

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
            raise errors.InputError(
                '{} is not a valid method. These are valid methods {}'.format(self.method, method_list))

        if os.path.isabs(self.report_name) != True:
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

    def simulate(self):
        """ """
        R = Run(self.model, task='time_course', mode=self.run)
        return R.model

    def create_task(self):
        """Begin creating the segment of xml needed
        for a time course. Define task and problem
        definition. This section of xml is common to all
        methods
        :return: lxml.etree._Element

        Args:

        Returns:

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
        """Set method specific sections of xml. This
        is a method element after the problem element
        that looks like this:
        
        :return: lxml.etree._Element

        Args:

        Returns:

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
        """:return:lxml.etree._Element"""
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
        """:return:"""
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
        """:return:"""
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
        """:return:"""
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
        """:return:"""
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
        """:return:"""
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
               'value': str(self.upper_limit)}
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
        """:return:"""
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
               'value': str(self.upper_limit)}
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
        """:return:"""
        raise errors.NotImplementedError('The hybrid-RK-45 method is not yet implemented')

    def set_report(self):
        """ser a time course report containing time
        and all species or global quantities defined by the user.
        
        :return: pycotools3.model.Model

        Args:

        Returns:

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
                if 'append' and 'target' in list(j.attrib.keys()):
                    present = True
                    j.attrib.update(arg_dct)
            if present == False:
                report = etree.Element('Report', attrib=arg_dct)
                i.insert(0, report)
        return self.model

    def get_report_key(self):
        """cross reference the timecourse task with the newly created
        time course reort to get the key

        Args:

        Returns:

        """
        all_reports = []
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            all_reports.append(i.attrib['name'])
            if i.attrib['name'] == 'Time-Course':
                key = i.attrib['key']
        if 'Time-Course' not in all_reports:
            raise errors.SomethingWentHorriblyWrongError('No report called "Time-Course". '
                                                         'Have you set one up yet?')
        return key


@mixin(model.ReadModelMixin)
class Scan(_Task):
    """Interface to COPASI scan task
    
    .. _scan_kwargs:
    
    Scan kwargs
    -----------
    
    ===========================     ==============================================
    Scan Kwargs                     Description
    ===========================     ==============================================
    update_model                    Default: False
    subtask                         Default: parameter_estimation
    report_type                     Default: profile_likelihood. Name of report from
                                    :py:class:`Reports` class
    output_in_subtask               Default: False
    adjust_initial_conditions       Default: False
    number_of_steps                 Default: 10
    maximum                         Default: 100
    minimum                         Default: 0.01
    log10                           Default: False
    distribution_type               Default: normal
    scan_type                       Default: scan
    scheduled                       Default: True
    save                            Default: False
    clear_scans                     Default: True.  If true, will remove all scans
                                    present then add new scan
    run                             Default: False
    <report_kwargs>                 Arguments for :ref:`report_kwargs` are also
                                    accepted here
    ===========================     ==============================================

    Args:

    Returns:

    """

    def __init__(self, model, **kwargs):
        """

        :param model:
            :py:class:`Model`

        :param kwargs:

        """
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
        self.check_integrity(list(self.default_properties.keys()), list(self.kwargs.keys()))
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
        types = {v: k for (k, v) in list(self.scan_type_numbers.items())}
        subtasks = {v: k for (k, v) in list(self.subtask_numbers.items())}
        return "Scan(scan_type='{}', subtask='{}', variable='{}', report_type='{}', " \
               "report_name='{}', number_of_steps='{}', minimum={}, maximum={})".format(
            types[self.scan_type], subtasks[self.subtask], self.variable.name, self.report_type,
            self.report_name, self.number_of_steps, self.minimum, self.maximum
        )

    def _do_checks(self):
        """Varify integrity of user input
        :return:

        Args:

        Returns:

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

        # if self.scan_type == 'scan':
        #     if self.output_in_subtask !=True:
        #         LOG.warning('output_in_subtask is False. '
        #                     ' This means that the subtask will not output data '
        #                     'as it is producing that data. For Scan tasks, we need this to be '
        #                     'True as we would like all the output. For parameter estimations'
        #                     'or profile likelihood, set this to False as we only want the'
        #                     'final parameter set')
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
        self.subtask_numbers = dict(list(zip(subtasks, [str(i) for i in self.subtask_numbers])))
        for i, j in list(self.subtask_numbers.items()):
            if i == self.subtask:
                self.subtask = j

        scan_type_numbers = [1, 0, 2]
        self.scan_type_numbers = dict(list(zip(scan_types, [str(i) for i in scan_type_numbers])))
        for i, j in list(self.scan_type_numbers.items()):
            if i == self.scan_type:
                self.scan_type = j

        for i in zip(scan_types, scan_type_numbers):
            if i[0] == self.scan_type:
                self.scan_type = str(i[1])

        dist_types_numbers = [0, 1, 2, 3]
        self.dist_type_numbers = dict(list(zip(dist_types, [str(i) for i in dist_types_numbers])))
        for i, j in list(self.dist_type_numbers.items()):
            if i == self.distribution_type:
                self.distribution_type = j

        # for i in zip(dist_types, dist_types_numbers):
        #     if i[0] == self.distribution_type:
        #         self.distribution_type = str(i[1])

        ## allow a user to input a string not pycotools3.model class
        if isinstance(self.variable, str):
            if self.variable in [i.name for i in self.model.metabolites]:
                self.variable = self.model.get('metabolite', self.variable,
                                               by='name')

            elif self.variable in [i.name for i in self.model.global_quantities]:
                self.variable = self.model.get('global_quantity', self.variable, by='name')

            elif self.variable in [i.name for i in self.model.local_parameters]:
                self.variable = self.model.get('local_parameter', self.variable, by='global_name')

    def define_report(self):
        """Use Report class to create report
        :return:

        Args:

        Returns:

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
        """ """
        # ammend the time course option
        if self.report_type.lower() == 'time_course':
            self.report_type = 'time-course'
        key = None
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'].lower() == self.report_type.lower():
                key = i.attrib['key']
        if key == None:
            raise errors.ReportDoesNotExistError(
                'Report doesn\'t exist. Check to see if you have either defined the report manually or used the pycopi.Reports class')
        return key

    def create_scan(self):
        """metabolite cn:
            CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=InitialConcentration"/>
        
        :return:

        Args:

        Returns:

        """
        ## get model entity if variable is a string
        if isinstance(self.variable, str):
            metab = self.model.get('metabolite', self.variable, by='name')
            glob = self.model.get('global_quantity', self.variable, by='name')
            loca = self.model.get('local_parameter', self.variable, by='global_name')

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
                raise errors.SomethingWentHorriblyWrongError(
                    'Getting variable from model but matched more than one entity')

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

            elif self.quantity_type == 'particle_numbers':
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
                                  'value': str(self.number_of_steps)}

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
        for i in self.model.xml.xpath(query):
            i.append(scanItem_element)
        return self.model

    def set_scan_options(self):
        """ """
        report_attrib = {'append': self.append,
                         'target': self.report_name,
                         'reference': self.get_report_key(),
                         'confirmOverwrite': self.confirm_overwrite}

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
        """Remove all scans that have been defined.
        
        :return:

        Args:

        Returns:

        """
        query = '//*[@name="ScanItems"]'
        for i in self.model.xml.xpath(query):
            for j in i:
                j.getparent().remove(j)
        self.model.save()
        return self.model

    def execute(self):
        """ """
        R = Run(self.model, task='scan', mode=self.run)


@mixin(model.GetModelComponentFromStringMixin)
@mixin(model.ReadModelMixin)
class ParameterEstimation(_Task):
    """
    Interface to COPASI's parameter estimation task

    Examples:
        Assuming a :py:class:`ParameterEstimation.Config` object has been
        configured and is called `config`
        >>> pe = ParameterEstimation(config)

    """

    valid_methods = ['current_solution_statistics',
                     'differential_evolution',
                     'evolutionary_strategy_sr',
                     'evolutionary_program',
                     'hooke_jeeves',
                     'levenberg_marquardt',
                     'nelder_mead',
                     'particle_swarm',
                     'praxis',
                     'random_search',
                     'simulated_annealing',
                     'steepest_descent',
                     'truncated_newton',
                     'scatter_search',
                     'genetic_algorithm',
                     'genetic_algorithm_sr']

    @staticmethod
    class _Defaults:
        """
        Class holding the defaults arguments for ParameterEstimation
        """

        def __init__(self):
            """
            Calls all the methods in the class which are essentially
            organised sets of default parameters
            """
            self.experiments = self._experiments()
            self.validations = self._validations()
            self.datasets = self._datasets()
            self.fit_items = self._fit_items()
            self.constraint_items = self._constraint_items()
            self.settings = self._settings()

        def _datasets(self):
            """ store default datasets argument"""
            return {
                'validations': {}
            }

        @staticmethod
        def _mappings(filename: str, sep: str):
            """

            Args:
              filename (str): the filename of the data file to be mapped
              sep (str): separator argument

            Returns: dict
                Object map dict for configuration
                of parameter estimation class
            """
            if not isinstance(filename, str):
                raise ValueError

            if not isinstance(sep, str):
                raise ValueError
            df = pandas.read_csv(filename, sep=sep)
            roles = {}
            for i in df.columns:
                if i.lower() == 'time':
                    roles[i] = 'time'
                elif i[:-6] == '_indep':
                    roles[i] = 'independent'
                else:
                    roles[i] = 'dependent'

            return {
                i: {
                    'model_object': i,
                    'role': roles[i]
                } for i in list(df.columns)
            }

        def _experiments(self):
            """ Stores default experiment kwargs for parameter estimation class"""
            return {
                'filename': '',
                'normalize_weights_per_experiment': True,
                'separator': '\t',
                'affected_models': 'all',
                'mappings': {},

            }

        def _validations(self):
            """ Stores default validation kwargs for parameter estimation class """
            return {
                'filename': '',
                'affected_models': 'all',
                'normalize_weights_per_experiment': True,
                'separator': '\t',
                'mappings': {},
            }

        def _fit_items(self):
            """ Stores default fit_item kwargs for parameter estimation class """

            return {
                'lower_bound': 1e-6,
                'upper_bound': 1e6,
                'start_value': 'model_value',
                'affected_experiments': 'all',
                'affected_validation_experiments': 'all',
                'affected_models': 'all'
            }

        def _constraint_items(self):
            """ Stores default constraint item kwargs for parameter estimation class """
            return {
                'lower_bound': 1e-6,
                'upper_bound': 1e6,
                'start_value': 'model_value',
                'affected_experiments': 'all',
                'affected_validation_experiments': 'all',
                'affected_models': 'all',
            }

        def _settings(self):
            """ Stores default setting kwargs for parameter estimation class"""
            return {
                'copy_number': 1,
                'pe_number': 1,
                'results_directory': 'ParameterEstimationData',
                'config_filename': 'config.yml',
                'overwrite_config_file': False,
                'update_model': False,
                'randomize_start_values': False,
                'create_parameter_sets': False,
                'calculate_statistics': False,
                'use_config_start_values': False,
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
                'lower_bound': 0.000001,
                'upper_bound': 1000000,
                'start_value': 0.1,
                'save': False,
                'run_mode': False,
                'working_directory': '',
                'quantity_type': 'concentration',
                'report_name': 'PEData.txt',
                'problem': 'Problem1',
                'fit': 1,
                'weight_method': 'mean_squared',
                'validation_weight': 1,
                'validation_threshold': 5,
                'max_active': 3,
                'prefix': None,
                'context': 's',
                'pl_upper_bound': 1000,
                'pl_lower_bound': 1000,
                'cross_validation_depth': 1
            }

    @staticmethod
    class Config(_Task, Munch):
        """
        A class for holding a parameter estimation configuration

        Stores all the settings needed for configuration of a parameter estimation
        using COPASI.

        Examples:
            >>> ## create a model
            >>> antimony_string = '''
            ...             model TestModel1()
            ...                 R1: A => B; k1*A;
            ...                 R2: B => A; k2*B
            ...                 A = 1
            ...                 B = 0
            ...                 k1 = 4;
            ...                 k2 = 9;
            ...             end
            ...             '''
            >>> copasi_filename = os.path.join(os.path.dirname(__file__), 'example_model.cps')
            >>> with model.BuildAntimony(copasi_filename) as loader:
            ...     mod = loader.load(antimony_string)
            >>> ## Simulate some data from the model and write to file
            >>> fname = os.path.join(os.path.dirname(__file__), 'timeseries.txt')
            >>> data = self.model.simulate(0, 10, 11)
            >>> data.to_csv(fname)
            >>> ## create nested dict containing all the relevant arguments for your configuration
            >>> config_dict = dict(
            ...        models=dict(
            ...             ## model name is the users choice here
            ...            example1=dict(
            ...                copasi_file=copasi_filename
            ...            )
            ...        ),
            ...        datasets=dict(
            ...            experiments=dict(
            ...                 ## experiment names are the users choice
            ...                report1=dict(
            ...                    filename=self.TC1.report_name,
            ...                ),
            ...            ),
            ...            ## our validations entry is empty here
            ...            ## but if you have validation data this should
            ...            ## be the same as the experiments section
            ...            validations=dict(),
            ...        ),
            ...        items=dict(
            ...            fit_items=dict(
            ...                A=dict(
            ...                    affected_experiments='report1'
            ...                ),
            ...                B=dict(
            ...                    affected_validation_experiments=['report2']
            ...                ),
            ...            k1={},
            ...            k2={},
            ...            ),
            ...            constraint_items=dict(
            ...                k1=dict(
            ...                    lower_bound=1e-2,
            ...                    upper_bound=10
            ...                )
            ...            )
            ...        ),
            ...        settings=dict(
            ...            method='genetic_algorithm_sr',
            ...            population_size=2,
            ...            number_of_generations=2,
            ...            working_directory=os.path.dirname(__file__),
            ...            copy_number=4,
            ...            pe_number=2,
            ...            weight_method='value_scaling',
            ...            validation_weight=2.5,
            ...            validation_threshold=9,
            ...            randomize_start_values=True,
            ...            calculate_statistics=False,
            ...            create_parameter_sets=False
            ...        )
            ...    )
            >>> config = ParameterEstimation.Config(**config_dict)
        """

        def __init__(self, models, datasets, items, settings={}, defaults=None):
            """
            Initialisation method for Config class
            Args:
                models (dict):
                    Dict containing model names and paths to copasi files
                datasets(dict):
                    Dict containing experiments and validation experiments
                items(dict):
                    Dict containing fit items and constraint items
                settings(dict):
                    Dict containing all other settings for parameter estimation
                defaults(ParameterEstimation._Defaults):
                    Custom set of Defaults to use for unspecified arguments
            """
            self.models = models
            self.datasets = datasets
            self.items = items
            self.settings = settings
            self.defaults = defaults

            if self.defaults is None:
                self.defaults = ParameterEstimation._Defaults()

            if not isinstance(self.defaults, ParameterEstimation._Defaults):
                raise TypeError('incorrect defaults argument')

            self.kwargs = Munch.fromDict({
                'models': self.models,
                'datasets': self.datasets,
                'items': self.items,
                'settings': self.settings
            })

            for kw in self.kwargs:
                setattr(self, kw, self.kwargs[kw])

            self._load_models()
            self.configure()
            self._validate_integrity_of_user_input()

        def __iter__(self):
            for attr in self.kwargs.keys():
                yield attr

        def __str__(self):
            return self.to_yaml()

        def __repr__(self):
            return self.__str__()

        def to_json(self):
            """
            Output arguments as json

            Returns: str
                All arguments in json format

            """
            kwargs = deepcopy(self.kwargs)
            for k, v in kwargs.models.items():
                for k2, v2 in kwargs.models[k].items():
                    if k2 == 'model':
                        kwargs.models[k][k2] = str(kwargs.models[k][k2])

            return json.dumps(kwargs, indent=4)

        def from_json(self, string):
            """
            Create config object from json format
            Args:
              string (Str):
                a valid json string

            Returns:
                ParameterEstimation.Config
            """
            raise NotImplementedError('Do this when needed')

        def to_yaml(self, filename=None):
            """

            Output arguments as yaml

            Args:
                filename (str, None):
                    If not None (default), path to write yaml configuration to

            Returns:
                Config object as string in yaml format

            """
            kwargs = deepcopy(self.kwargs)
            for k, v in kwargs.models.items():
                for k2, v2 in kwargs.models[k].items():
                    if k2 == 'model':
                        kwargs.models[k][k2] = str(kwargs.models[k][k2])

            yml = munch.toYAML(kwargs)

            if filename is not None:
                with open(filename, 'w') as f:
                    f.write(yml)
            return yml

        def from_yaml(self, yml):
            """
            Read config object from yaml file
            Args:
              yml (str):
                full path to text file containing configuration arguments in yaml format

            Returns:
                ParameterEstimation.Config

            """
            if os.path.isfile(yml):
                with open(yml, 'r') as f:
                    yml_string = f.read()
            else:
                yml_string = yml
            raise NotImplementedError('Do this when needed')

        @staticmethod
        def _add_defaults_to_dict(dct, defaults):
            """

            Args:
              dct:
              defaults:

            Returns:

            """
            for k in defaults:
                if k not in dct:
                    dct[k] = defaults[k]
            return dct

        def _validate_integrity_of_user_input(self):
            """
            Ensure user input is accurate
            Returns:
                None

            """
            for i in self.settings:
                if i not in self.defaults.settings.keys():
                    raise errors.InputError(
                        '"{}" is an invalid argument for "settings". These are valid '
                        'arguments: "{}"'.format(i, list(self.defaults.settings.keys()))
                    )

            if not isinstance(self.models, dict):
                raise errors.InputError(
                    'The "models" argument should be a dict containing'
                    ' model names as keys and "model.Model" object or "copasi file"'
                )

            if not isinstance(self.datasets, dict):
                raise TypeError(
                    'The "datasets" argument should be a nested dict containing'
                    ' "experiments" and/or "validations" dicts'
                )

            if not isinstance(self.items, dict):
                raise TypeError(
                    'The "items" argument should be a nested dict containing'
                    ' "fit_items" and/or "constraint_items" dicts'
                )

            if not isinstance(self.settings, dict):
                raise TypeError(
                    'The "settings" argument should be a dict containing'
                    ' arguments to valid settings.'
                )

            if self.settings.working_directory in ['', False, None] or not os.path.isdir(
                    self.settings.working_directory):
                raise errors.InputError(
                    'A valid argument must be given to config.settings.working_directory. Got "{}"'.format(
                        self.settings.working_directory
                    ))

            exp_names = list(self.datasets.experiments.keys())
            exp_filenames = [self.datasets.experiments[i].filename for i in self.datasets.experiments]
            if len(set(exp_names)) != len(set(exp_filenames)):
                raise errors.InputError(
                    f'Your experiment filenames are not unique. It is likely that you '
                    f'have the same experiment file under multiple experiment names'
                )
            val_exp_names = list(self.datasets.validations.keys())
            val_exp_filenames = [self.datasets.validations[i].filename for i in self.datasets.validations]
            if len(set(val_exp_names)) != len(set(val_exp_filenames)):
                raise errors.InputError(
                    f'Your experiment filenames are not unique. It is likely that you '
                    f'have the same experiment file under multiple experiment names'
                )

        def _load_models(self):
            """
            Load models from disk

            User usually specifies a copasi_file as argument. This method loads
            the copasi file into a :py:class:`model.Model` object and stores a
            reference to the model under the `model` entry of the `models` tag.

            Returns:
                This method operates inplace and returns None

            """
            for mod in self.models:
                if 'model' not in self.models[mod].keys():
                    if 'copasi_file' not in self.models[mod].keys():
                        raise errors.InputError('Config object is ill informed. Please specify '
                                                'either a string argument to the copasi_file keyword '
                                                'or a pycotools3.model.Model object to the model keyword')
                if 'copasi_file' in self.models[mod].keys():
                    self.models[mod]['model'] = model.Model(self.models[mod].copasi_file)

        def configure(self):
            """
            Configure the class for production of parameter estimation config

            Like a main method for this class. Uses the other methods in the class
            to configure a :py:class:`ParameterEstimation.Config object`

            Returns:
                Operates inplace and returns None
            """
            ## adds any settings that are missing from defaults.
            for k in self.defaults.settings:
                if k not in self.settings:
                    self.settings[k] = self.defaults.settings[k]

            for k in self.defaults.datasets:
                if k not in self.datasets:
                    self.datasets[k] = self.defaults.datasets[k]

            self._set_default_experiments()

            self._set_default_validation_experiments()

            self._set_default_fit_items()

            self._set_default_constraint_items()

        def _set_default_experiments(self):
            """
            Configure missing entries for datasets.experiments with defaults

            Returns:
                None, the method operates on class attributes inplace
            """
            for experiment_name in self.experiment_names:
                for default_kwarg in self.defaults.experiments:
                    if default_kwarg not in self.datasets.experiments[experiment_name]:
                        self.datasets.experiments[experiment_name][default_kwarg] = self.defaults.experiments[
                            default_kwarg]

                if self.datasets.experiments[experiment_name].affected_models == 'all':
                    self.datasets.experiments[experiment_name].affected_models = list(self.models.keys())[0] if len(
                        self.models.keys()) == 1 else list(self.models.keys())

                if isinstance(self.datasets.experiments[experiment_name]['affected_models'], str):
                    self.datasets.experiments[experiment_name]['affected_models'] = [
                        self.datasets.experiments[experiment_name]['affected_models']]

                if self.datasets.experiments[experiment_name].mappings == {}:
                    self.datasets.experiments[experiment_name].mappings = Munch.fromDict(self.defaults._mappings(
                        self.datasets.experiments[experiment_name].filename,
                        self.datasets.experiments[experiment_name].separator)
                    )

                for mapping in self.datasets.experiments[experiment_name].mappings:
                    mapp = self.datasets.experiments[experiment_name].mappings.get(mapping)
                    if mapp.role != 'time':
                        model_keys = list(self.models.keys())
                        mod = self.models[model_keys[0]].model
                        model_obj = []
                        try:
                            model_obj = self.get_variable_from_string(
                                mod,
                                mapp.model_object[:-6] if mapp.model_object[-6:] == '_indep' else mapp.model_object
                            )
                        except errors.InputError:
                            LOG.warning(f'skipping variable "{mapp.model_object}" as it was not found in '
                                        f'model "{mod}"')

                        if mapp == {}:
                            mapp = {
                                'model_object': mapping,
                                'role': 'dependent',
                                'object_type': type(model_obj).__name__
                            }
                        else:
                            mapp.update({'object_type': type(model_obj).__name__})

        def _set_default_validation_experiments(self):
            """
            Configure missing entries for datasets.validations with defaults

            Returns:
                None, the method operates on class attributes inplace

            """
            if self.datasets.validations is None:
                return {}

            validations = self.datasets.validations

            for validation_experiment in self.validation_names:
                validation_dataset = validations.get(validation_experiment)
                validation_defaults = self.defaults.validations

                for default_kwarg in validation_defaults:
                    if default_kwarg not in validation_dataset:
                        validation_dataset[default_kwarg] = validation_defaults[default_kwarg]

                if validation_dataset.affected_models == 'all':
                    validation_dataset.affected_models = list(self.models.keys())[0] if len(
                        self.models.keys()) == 1 else list(self.models.keys())

                if validation_dataset.mappings == {}:
                    validation_dataset.mappings = Munch.fromDict(self.defaults._mappings(
                        validation_dataset.filename, validation_dataset.separator)
                    )

                for mapping in validation_dataset.mappings:
                    mapp = validation_dataset.mappings.get(mapping)
                    if mapp.role != 'time':
                        model_keys = list(self.models.keys())
                        mod = self.models[model_keys[0]].model
                        model_obj = self.get_variable_from_string(
                            mod,
                            mapp.model_object[:-6] if mapp.model_object[-6:] == '_indep' else mapp.model_object

                        )
                        if mapp == {}:
                            mapp = {
                                'model_object': mapping,
                                'role': 'dependent',
                                'object_type': type(model_obj).__name__
                            }
                        else:
                            mapp.update({'object_type': type(model_obj).__name__})
                    self.datasets.validations[validation_experiment].mappings[mapping] = mapp

        def _set_default_fit_items(self):
            """
            Configure missing entries for items.fit_items with defaults

            Returns:
                None. Method operates inplace on class attributes

            """
            if isinstance(self.items.fit_items, str):
                self.set_default_fit_items_str()
            else:
                self.set_default_fit_items_dct()

        def set_default_fit_items_str(self):
            """

            Configure missing entries for items.fit_items when they are
            strings pointing towards model variables

            Returns:
                None. Method operates inplace on class attributes

            """
            if not isinstance(self.items.fit_items, str):
                raise TypeError

            estimated_variables = {}
            for model_name in self.models:
                mod = self.models[model_name].model
                estimated_variables[model_name] = mod.get_variable_names(
                    self.items.fit_items, include_assignments=False, prefix=self.settings.prefix
                )
            dct = {}
            for model_name in estimated_variables:
                dct[model_name] = {}
                for parameter in estimated_variables[model_name]:
                    dct[model_name][parameter] = {}

            estimated_variables = dct

            for model_name in self.models:
                dct = {}

                for fit_item in estimated_variables[model_name]:
                    item = estimated_variables[model_name][fit_item]
                    if item == {}:
                        item = self.defaults.fit_items

                    else:
                        for i in self.defaults.fit_items:
                            if i not in item:
                                item[i] = self.defaults.fit_items[i]

                    if item['affected_experiments'] == 'all':
                        if isinstance(self.experiment_names, str):
                            item['affected_experiments'] = [self.experiment_names]
                        else:
                            item['affected_experiments'] = self.experiment_names

                    if item['affected_validation_experiments'] == 'all':
                        if isinstance(self.validation_names, str):
                            item['affected_validation_experiments'] = [self.validation_names]
                        else:
                            item['affected_validation_experiments'] = self.validation_names

                    if item['affected_models'] == 'all':
                        item['affected_models'] = [
                            i for i in self.models if fit_item in self.models[model_name].model
                        ]
                    dct[fit_item] = item

            self.items.fit_items = Munch.fromDict(dct)

        def set_default_fit_items_dct(self):
            """

            Configure missing entries for items.fit_items when they are
            in nested dict format

            Returns:
                None. Method operates inplace on class attributes

            """
            ## remove fit items if prefix condition is not satisified
            for fit_item in self.items.fit_items:
                item = self.items.fit_items.get(fit_item)
                self.defaults.fit_items['upper_bound'] = self.settings.upper_bound
                self.defaults.fit_items['lower_bound'] = self.settings.lower_bound

                if item == {}:
                    item = self.defaults.fit_items
                else:
                    for i in self.defaults.fit_items:
                        if i not in item:
                            item[i] = self.defaults.fit_items[i]
                ## set lower bound, upper bound and model value

                ## if start_value is model_value, we cannot resolve here as
                ## we need the model to get the value. This is resolved in the main class
                if item['start_value'] != 'model_value':
                    item['start_value'] = self.settings.start_value

                if item['affected_experiments'] == 'all':
                    if isinstance(self.experiment_names, str):
                        item['affected_experiments'] = [self.experiment_names]
                    else:
                        item['affected_experiments'] = self.experiment_names

                if isinstance(item['affected_experiments'], str):
                    item['affected_experiments'] = [item['affected_experiments']]

                if item['affected_validation_experiments'] == 'all':
                    if isinstance(self.validation_names, str):
                        item['affected_validation_experiments'] = [self.validation_names]
                    else:
                        item['affected_validation_experiments'] = self.validation_names

                if item['affected_models'] == 'all':
                    item['affected_models'] = list(self.models.keys())

                self.items.fit_items[fit_item] = Munch.fromDict(item)  #

            ## caters for the situation where we define a config file but
            ## need to update it due to a change in prefix argument
            tmp_dct = {}
            if self.settings.prefix is not None:
                if not isinstance(self.settings.prefix, str):
                    raise TypeError(f'config.settings.prefix argument should be of type "str"')
                tmp = {fit_item: self.items.fit_items[fit_item] for fit_item in self.items.fit_items if
                       fit_item.startswith(self.settings.prefix)}
                self.items.fit_items = Munch.fromDict(tmp)

        def _set_default_constraint_items(self):
            """ 
            
            Configure missing entries for items.constraint_items when they are
            strings pointing towards model variables

            Returns:
                None. Method operates inplace on class attributes

            """
            if 'constraint_items' in self.items:
                if self.items.constraint_items == {}:
                    item = {}

                for constraint_item in self.items.constraint_items:
                    item = self.items.constraint_items.get(constraint_item)

                    if item == {}:
                        item = self.defaults.constraint_items

                    else:
                        for i in self.defaults.constraint_items:
                            if i not in item:
                                item[i] = self.defaults.constraint_items[i]

                    if item.affected_experiments == 'all':
                        if isinstance(self.experiment_names, str):
                            item.affected_experiments = [self.experiment_names]
                        else:
                            item.affected_experiments = self.experiment_names

                    if item.affected_validation_experiments == 'all':
                        if isinstance(self.validation_names, str):
                            item.affected_validation_experiments = [self.validation_names]
                        else:
                            item.affected_validation_experiments = self.validation_names

                    if item.affected_models == 'all':
                        item.affected_models = list(self.models.keys())

                self.items.constraint_items[constraint_item] = Munch.fromDict(item)
            # else:
            #     self.items['constraint_items'] = {}

        @property
        def experiments(self):
            """
            The experiments property
            Returns:
                datasets.experiments as dict
            """
            return self.datasets.experiments

        @property
        def validations(self):
            """
            The validations property
            Returns:
                datasets.validations as dict
            """
            return self.datasets.validations

        @property
        def experiment_filenames(self):
            """
            Returns:
                A list of experiment filesnames
            """
            filenames = []
            for i in self.experiments:
                filenames.append(self.experiments[i].filename)
            return filenames

        @property
        def validation_filenames(self):
            """

            Returns:
                a list of validation filenames

            """
            filenames = []
            for i in self.validations:
                filenames.append(self.validations[i].filename)
            return filenames

        @property
        def experiment_names(self):
            """

            Returns:
                A list of experiment names

            """
            experiment_names = []
            for i in self.experiments:
                experiment_names.append(i)

            return experiment_names

        @property
        def validation_names(self):
            """
            
            Returns:
                A list of validation names

            """
            validation_names = []
            for i in self.validations:
                validation_names.append(i)

            return validation_names

        @property
        def models_affected_experiments(self):
            """
            Get which experiment datasets affect which models

            Returns:
                dict. Keys are model names, value are list of affected models
            """
            dct = {}
            for model_name in self.models:
                dct[model_name] = []
                for experiment_name in self.experiments:
                    if model_name in self.experiments[experiment_name].affected_models:
                        dct[model_name].append(experiment_name)

            return dct

        @property
        def models_affected_validation_experiments(self):
            """
            Get which experiment datasets affect which models

            Returns:
                dict. Keys are model names, value are list of affected models
            """
            dct = {}
            for model_name in self.models:
                dct[model_name] = []
                for experiment_name in self.validations:
                    if model_name in self.validations[experiment_name].affected_models:
                        dct[model_name].append(experiment_name)
            return dct

        @property
        def model_objects(self):
            """

            Returns:
                A list of model objects for mapping

            """
            model_obj = []
            for i in self.experiment_names:
                for j in self.experiments[i].mappings:
                    if self.experiments[i].mappings[j] is not None:
                        model_obj.append(self.experiments[i].mappings[j].model_object)

            for i in self.validation_names:
                for j in self.validations[i].mappings:
                    if self.validations[i].mappings[j] is not None:
                        model_obj.append(self.validations[i].mappings[j].model_object)

            return list(set(model_obj))

        @property
        def fit_items(self):
            """

            Returns:
                The fit items as nested dict
            """
            return self.items.fit_items

        @property
        def constraint_items(self):
            """

            Returns:
                The constraint items as nested dict

            """
            return self.items.constraint_items

    def __init__(self, config):
        """
        Configure a the parameter estimation task in copasi

        Pycotools supports all the features of parameter estimation configuration
        as copasi, plus a few additional ones (such as the affected models setting).

        Args:
            config (ParameterEstimation.Config):
                An appropriately configured :py:class:`ParameterEstimation.Config` class

        Examples:
            See :py:class:`ParameterEstimation.Config` or :py:class:`ParameterEstimation.Context`
            for detailed information on how to produce a :py:class:`ParameterEstimation.Config` object.
            Note that the :py:class:`ParameterEstimation.Context` class is higher level and should be the preferred way of
            constructing a :py:class:`ParameterEstimation.Config` object while the :py:class:`ParameterEstimation.Config` class
            gives you the same level of control as copasi but is bulkier to write.

            Assuming the :py:class:`ParameterEstimation.Config` class has already been created
            >>> pe = ParameterEstimation(config)
        """
        self.config = config
        self.do_checks()

        self.model_copies = self._setup()

        if self.config.settings.run_mode is not False:
            self.run(self.model_copies)

    def do_checks(self):
        """ validate integrity of user input"""
        if not isinstance(self.config, self.Config):
            raise errors.InputError(
                f'config argument is of type {type(self.config)} '
                f'but was expecting an instance of '
                f'ParameterEstimation.Config'
            )

    def __str__(self):
        return f"ParameterEstimation(\n\t{self.config}\n)"

    @property
    def problem_dir(self):
        """
        Property holding the directory where the parameter estimation problem is stored
        Returns:
            str. A directory.
        """
        dire = os.path.join(self.config.settings.working_directory, f'{self.config.settings.problem}')
        if not os.path.isdir(dire):
            os.makedirs(dire)
        return dire

    @property
    def fit_dir(self):
        """
        Property holding the directory where the parameter estimation fitting occurs. This can
        be enumerated under a single problem directory to group similar parameter estimations
        Returns:
            str. A directory.
        """
        dire = os.path.join(self.problem_dir, f'Fit{self.config.settings.fit}')
        if not os.path.isdir(dire):
            os.makedirs(dire)
        return dire

    @property
    def models_dir(self):
        """
        A directory containing models

        Each model will be configured in a different directory when multiple models are being configured simultaneously
        Returns:
            dct. Location of models directories

        """
        dct = {}
        for model_name in self.models:
            dct[model_name] = os.path.join(self.fit_dir, model_name)
            if not os.path.isdir(dct[model_name]):
                os.makedirs(dct[model_name])
        return dct

    @property
    def results_directory(self):
        """
        A directory containing results, parameter estimation report files
        from copasi

        Each model configured will have their own results directory
        Returns:
            dict[model] = results_directory
        """
        dct = {}
        for model_name in self.models:
            dct[model_name] = os.path.join(
                self.models_dir[model_name],
                self.config.settings.results_directory
            )
            if not os.path.isdir(dct[model_name]):
                os.makedirs(dct[model_name])
        return dct

    def get_model_objects_from_strings(self):
        """
        Get model objects from the strings
        provided by the user in the Config class
        :return: list of `model.Model` objects

        Returns:
            list of model objects

        """
        number_of_model_objects_in_parameter_estimation = len(self.config.model_objects)
        model_objs = []
        for mod in self.config.models:
            for obj in self.config.model_objects:
                current_model = self.config.models[mod].model
                try:
                    model_objs.append(
                        self.get_variable_from_string(current_model, obj)
                    )
                    number_of_model_objects_in_parameter_estimation -= 1
                    if number_of_model_objects_in_parameter_estimation == 0:
                        break
                ## allow a mechanism for iterating over models that
                ## do not all have the same variables
                except errors.InputError:
                    continue
        return model_objs

    @property
    def metabolites(self):
        """

        Returns:
            list of strings of metabolites in the model

        """
        return [i.name for i in self.get_model_objects_from_strings() if isinstance(i, model.Metabolite)]

    @property
    def local_parameters(self):
        """

        Returns:
            list of strings of local parameters in the model

        """
        return [i.name for i in self.get_model_objects_from_strings() if isinstance(i, model.LocalParameter)]

    @property
    def global_quantities(self):
        """

        Returns:
            list of strings of global quantities present in the models

        """
        return [i.name for i in self.get_model_objects_from_strings() if isinstance(i, model.GlobalQuantity)]

    @property
    def _report_arguments(self):
        """collect report specific arguments in a dict
        :return: dict

        Returns:
            dict[arg] = value

        """
        # report specific arguments
        report_dict = {}
        report_dict['metabolites'] = self.metabolites
        report_dict['global_quantities'] = self.global_quantities
        report_dict['local_parameters'] = self.local_parameters
        report_dict['quantity_type'] = self.config.settings.quantity_type
        report_dict['report_name'] = self.config.settings.report_name
        report_dict['append'] = False
        report_dict['confirm_overwrite'] = False
        report_dict['report_type'] = 'multi_parameter_estimation'
        return report_dict

    def _define_report(self):
        """create parameter estimation report
        for result collection
        :return: pycotools3.model.Model

        Returns:
            the models attribute

        """
        for model_name in self.models:
            mod = self.models[model_name].model
            for glo in self._report_arguments['global_quantities']:
                if glo not in [i.name for i in mod.global_quantities]:
                    del self._report_arguments['global_quantities'][glo]

            for loc in self._report_arguments['global_quantities']:
                if loc not in [i.name for i in mod.global_quantities]:
                    del self._report_arguments['global_quantities'][loc]

            for met in self._report_arguments['metabolites']:
                if met not in [i.name for i in mod.metabolites]:
                    del self._report_arguments['metabolites'][met]

            self.models[model_name].model = Reports(mod, **self._report_arguments).model

        return self.models

    def _get_report_key(self):
        """After creating the report to collect
        results, this method gets the corresponding key
        There is probably a more efficient way to do this
        but this works...
        :return:

        Args:

        Returns:

        """
        keys = {}
        for model_name in self.models:
            mod = self.models[model_name].model
            for i in mod.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
                if i.attrib['name'].lower() == 'multi_parameter_estimation':
                    key = i.attrib['key']
            assert key is not None
            keys[model_name] = key

        return keys

    @property
    def models(self):
        """
        Get models

        Returns:
            the models entry of the :py:class:`ParameterEstimation.Config` object

        """
        return self.config.models

    @models.setter
    def models(self, models):
        """
        Set models attribute
        Args:
          models:
            dict
        Returns:
            None
        """
        self.config.models = models

    @property
    def _experiments(self):
        """

        Returns:
            A dict containing a list of experiments pertinent for each
            model being configured

        """
        existing_experiment_list_dct = {}
        query = '//*[@name="Experiment Set"]'
        for mod in self.models:
            existing_experiment_list = []
            m = self.models[mod].model
            for i in m.xml.xpath(query):
                for j in list(i):
                    existing_experiment_list.append(j)
            existing_experiment_list_dct[mod] = existing_experiment_list
        return existing_experiment_list_dct

    @property
    def _validations(self):
        """

        Returns:
            A dict containing a list of validation experiments pertinent for each
            model being configured
        """
        existing_validation_list_dct = {}
        query = '//*[@name="Experiment Set"]'
        for mod in self.models:
            existing_validation_list = []
            m = self.models[mod].model
            for i in m.xml.xpath(query):
                for j in list(i):
                    existing_validation_list.append(j)
            existing_validation_list_dct[mod] = existing_validation_list
        return existing_validation_list_dct

    @staticmethod
    def _create_metabolite_reference(mod, parent, metabolite, role):
        """
        Build a xml entry from :py:class:`model.Metabolite`

        Args:
          mod (model.Model): 
            The model being configured 
          parent: 
            The parent xml element 
          metabolite: 
            a :py:class:`model.Metabolite` object
          role: 
            role of metabolite ('dependent' or 'independent')

        Returns:
            etree.Element containing COAPSI reference to metabolite
        """
        if not isinstance(metabolite, model.Metabolite):
            raise ValueError('Input should be "model.Metabolite" class. Got "{}"'.format(type(metabolite)))

        if role == 'independent':
            cn = '{},{},{}'.format(mod.reference,
                                   metabolite.compartment.reference,
                                   metabolite.initial_reference)
        elif role == 'dependent':
            cn = '{},{},{}'.format(mod.reference,
                                   metabolite.compartment.reference,
                                   metabolite.transient_reference)
        else:
            raise ValueError

        ics_attrs = {
            'type': 'cn',
            'name': 'Object CN',
            'value': cn
        }
        return etree.SubElement(parent, 'Parameter', attrib=ics_attrs)

    @staticmethod
    def _create_local_parameter_reference(mod, parent, local_parameter, role):
        """Not used because local parameters are not usually mapped to experimental
        variables. However, this method will be kept until the next release
        to ensure no bugs arise because of a lack of local parameter reference

        Returns:

        """
        if not isinstance(local_parameter, model.LocalParameter):
            raise ValueError('Input should be "model.LocalParameter" class. Got "{}"'.format(type(local_parameter)))

        if role == 'independent':
            cn = '{},{},{}'.format(mod.reference,
                                   local_parameter.compartment.reference,
                                   local_parameter.initial_reference)
        elif role == 'dependent':
            cn = '{},{},{}'.format(mod.reference,
                                   local_parameter.compartment.reference,
                                   local_parameter.transient_reference)
        else:
            raise ValueError

        local_attrs = {
            'type': 'cn',
            'name': 'Object CN',
            'value': cn
        }
        parent = etree.SubElement(parent, 'Parameter', attrib=local_attrs)
        return parent

    @staticmethod
    def _create_global_quantity_reference(mod, parent, global_quantity, role):

        """
        Build a xml entry from :py:class:`model.GlobalQuantitt`

        Args:
          mod (model.Model):
            The model being configured
          parent:
            The parent xml element
          global_quantity:
            a :py:class:`model.GlobalQuantity` object
          role:
            role of metabolite ('dependent' or 'independent')

        Returns:
            etree.Element containing COAPSI reference to metabolite
        """
        if not isinstance(global_quantity, model.GlobalQuantity):
            raise ValueError('Input should be "model.GlobalQuantity" class. Got "{}"'.format(type(global_quantity)))

        if role == 'independent':
            cn = '{},{}'.format(mod.reference,
                                global_quantity.initial_reference)

        elif role == 'dependent':
            cn = '{},{}'.format(mod.reference,
                                global_quantity.initial_reference)
        else:
            raise ValueError

        global_attrs = {
            'type': 'cn',
            'name': 'Object CN',
            'value': cn
        }
        etree.SubElement(parent, 'Parameter', attrib=global_attrs)
        return parent

    def _assign_role(self, parent, role):
        """Used in create experiment to correctly map the role of each variable in
        experiemtnal data columns
        :return:

        Args:
          parent:
            The parent xml object
          role:
            'ignored' (default), 'dependent', 'independent', 'time' or

        Returns:
            etree.lxml object

        """
        # define object role attributes
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

        ## assign the correct role
        if role == 'dependent':
            parent = etree.SubElement(parent, 'Parameter', attrib=dependent_variable_role)
        elif role == 'independent':
            parent = etree.SubElement(parent, 'Parameter', attrib=independent_variable_role)
        elif role == 'time':
            parent = etree.SubElement(parent, 'Parameter', attrib=time_role)
        elif role == 'ignored':
            parent = etree.SubElement(parent, 'Parameter', attrib=ignored_role)
        else:
            raise ValueError('"{}" is not a valid role'.format(role))

        return parent

    def _map1experiment(self, model_name, mod, experiment_names, experiments,
                        keys_function, validation, query, weight_method_lookup_dct
                        ):
        for experiment_name in experiment_names:
            ## if experiment_name exists, remove and reconfigure
            experiment = experiments[experiment_name]
            if not isinstance(experiment.affected_models, list):
                experiment.affected_models = [experiment.affected_models]

            ## This implements the affected_models aspect of configuration for experiments
            if model_name not in experiment.affected_models:
                message = f'Trying to map experiment "{experiment_name}" (validation={validation}) ' \
                    f'to model "{model_name}" but it is not in ' \
                    f'model "{model_name}" but it is not in  ' \
                    f'the affected models list for this model: ' \
                    f'"{experiment.affected_models}". This configuration has been skipped.'
                ## in cross validation we expect to see some of these
                ## these messages whereas with other types of analysis
                ## they probably mean something ominus.
                if self.config.settings.context == 'cv':
                    LOG.debug(message)
                else:
                    LOG.warning(message)
                continue
            ## also need to remove from affected_models attrib
            ##todo if all remove affected experiments

            data = pandas.read_csv(
                experiment.filename,
                sep=experiment.separator
            )
            experiment_type = 'steadystate'

            if 'time' in [i.lower() for i in data.columns]:
                experiment_type = 'timecourse'

            experiment_type = str(1) if experiment_type == 'timecourse' else str(0)

            num_rows = str(data.shape[0])
            num_columns = str(data.shape[1])

            experiment_file = {'type': 'file',
                               'name': 'File Name',
                               'value': experiment.filename}
            key = {'type': 'key',
                   'name': 'Key',
                   'value': keys_function()[model_name][experiment_name]
                   }

            # necessary XML attributes
            experiment_group = etree.Element('ParameterGroup',
                                             attrib={
                                                 'name': experiment_name
                                             })

            row_orientation = {'type': 'bool',
                               'name': 'Data is Row Oriented',
                               'value': True}

            experiment_type_dct = {'type': 'unsignedInteger',
                                   'name': 'Experiment Type',
                                   'value': experiment_type}

            first_row = {'type': 'unsignedInteger',
                         'name': 'First Row',
                         'value': str(1)}

            last_row = {'type': 'unsignedInteger',
                        'name': 'Last Row',
                        'value': str(int(num_rows) + 1)}  # add 1 to account for 0 indexed python

            normalize_weights_per_experiment = {'type': 'bool',
                                                'name': 'Normalize Weights per Experiment',
                                                'value': experiment.normalize_weights_per_experiment}

            number_of_columns = {'type': 'unsignedInteger',
                                 'name': 'Number of Columns',
                                 'value': num_columns}

            object_map = {'name': 'Object Map'}

            row_containing_names = {'type': 'unsignedInteger',
                                    'name': 'Row containing Names',
                                    'value': str(1)}

            separator = {'type': 'string',
                         'name': 'Separator',
                         'value': experiment.separator}

            weight_method = {'type': 'unsignedInteger',
                             'name': 'Weight Method',
                             'value': weight_method_lookup_dct[
                                 self.config.settings.weight_method
                             ]}

            for i in [
                key,
                experiment_file,
                row_orientation,
                first_row,
                last_row,
                experiment_type_dct,
                normalize_weights_per_experiment,
                separator,
                weight_method,
                row_containing_names,
                number_of_columns,
            ]:
                for j, k in i.items():
                    if isinstance(k, bool):
                        i[j] = str(int(k))
                    elif isinstance(k, int):
                        i[j] = str(k)
                etree.SubElement(experiment_group, 'Parameter', attrib=i)
            map = etree.SubElement(experiment_group, 'ParameterGroup', attrib=object_map)

            data_column_number = 0
            for data_name in experiment.mappings:

                map_group = etree.SubElement(map, 'ParameterGroup', attrib={'name': str(data_column_number)})
                data_column_number += 1

                if experiment.mappings[data_name].model_object.lower() == 'time':
                    self._assign_role(map_group, experiment.mappings[data_name].role)

                elif experiment.mappings[data_name].object_type == 'Metabolite':
                    metab = [i for i in mod.metabolites if
                             i.name == experiment.mappings[data_name].model_object or i.name == experiment.mappings[
                                                                                                    data_name].model_object[
                                                                                                :-6]]
                    assert len(metab) == 1
                    self._create_metabolite_reference(
                        mod,
                        map_group,
                        metab[0],
                        experiment.mappings[data_name].role
                    )
                    self._assign_role(map_group, experiment.mappings[data_name].role)

                elif experiment.mappings[data_name].object_type == 'GlobalQuantity':
                    glo = [i for i in mod.global_quantities if
                           i.name == experiment.mappings[data_name].model_object or i.name == experiment.mappings[
                                                                                                  data_name].model_object[
                                                                                              :-6]]
                    assert len(metab) == 1
                    self._create_global_quantity_reference(
                        mod,
                        map_group,
                        glo[0],
                        experiment.mappings[data_name].role
                    )

                    self._assign_role(map_group, experiment.mappings[data_name].role)

                for j in mod.xml.xpath(query):
                    j.insert(0, experiment_group)
                    if validation:
                        for k in list(j):
                            if k.attrib['name'] == 'Weight':
                                k.attrib['value'] = str(self.config.settings.validation_weight)
                            if k.attrib['name'] == 'Threshold':
                                k.attrib['value'] = str(self.config.settings.validation_threshold)

    def _map_experiments(self, validation=False):
        """Adds experiment sets to the parameter estimation task
        exp_file is an experiment filename with exactly matching headers (independent variablies need '_indep' appended to the end)
        since this method is intended to be used in a loop in another function to
        deal with all experiment sets, the second argument 'i' is the index for the current experiment
        
        i is the exeriment_file index

        Args:
          validation (bool):
            Set to True for configuring a validation experiment, False (default) otherwise

        Returns:
            :py:attr:`ParameterEstimation.models`

        """
        ## build a reference dct for weight method numbers
        weight_method_string = ['mean_squared', 'stardard_deviation', 'value_scaling',
                                'mean']
        weight_method_numbers = [str(i) for i in [1, 2, 3, 4]]
        weight_method_lookup_dct = dict(list(zip(weight_method_string, weight_method_numbers)))

        for model_name in self.models:
            mod = self.models[model_name].model

            if validation:
                query = '//*[@name="Validation Set"]'
                experiment_names = self.config.validation_names
                experiments = self.config.datasets.validations

                keys_function = self._get_validation_keys
                # self._remove_all_validation_experiments()
            else:
                query = '//*[@name="Experiment Set"]'
                experiment_names = self.config.experiment_names
                experiments = self.config.datasets.experiments
                keys_function = self._get_experiment_keys
                # self._remove_all_experiments()

            ## I have had to put the inner loop in a separate method because
            ## in python it is impossible to 'continue' an inner loop and
            ## not also skip the outer loop
            ## (see https://stackoverflow.com/questions/1859072/python-continuing-to-next-iteration-in-outer-loop/1859099)
            self._map1experiment(
                model_name, mod, experiment_names, experiments,
                keys_function, validation, query, weight_method_lookup_dct
            )
        return self.models

    def _remove_all_experiments(self):
        """
        Removes all experiments from parameter estimation task
        Returns:
            None
        """
        query = '//*[@name="Experiment Set"]'
        query2 = '//*[@name="FitItem"]'
        for model_name in self.models:
            for i in self.models[model_name].model.xml.xpath(query):
                for j in i:
                    j.getparent().remove(j)

            for i in self.models[model_name].model.xml.xpath(query2):
                for j in i:
                    if j.attrib['name'] == 'Affected Experiments':
                        for k in j:
                            k.getparent().remove(k)

    def _remove_all_validation_experiments(self):
        """
        Removates all validation experiments from parameter estimation task
        Returns:
                None
        """
        query = '//*[@name="Validation Set"]'
        query2 = '//*[@name="FitItem"]'
        for model_name in self.models:
            for i in self.models[model_name].model.xml.xpath(query):
                for j in i:
                    if j.attrib['name'] not in ['Weight', 'Threshold']:
                        j.getparent().remove(j)

            for i in self.models[model_name].model.xml.xpath(query2):
                for j in i:
                    if j.attrib['name'] == 'Affected Cross Validation Experiments':
                        for k in j:
                            k.getparent().remove(k)

    def _select_method(self):
        """
        Converts user input into the form required by the COPASI xml.

        Returns:
            tuple. (method_name, method_type)

        """
        if self.config.settings.method == 'current_solution_statistics'.lower():
            method_name = 'Current Solution Statistics'
            method_type = 'CurrentSolutionStatistics'

        elif self.config.settings.method == 'differential_evolution'.lower():
            method_name = 'Differential Evolution'
            method_type = 'DifferentialEvolution'

        elif self.config.settings.method == 'evolutionary_strategy_sr'.lower():
            method_name = 'Evolution Strategy (SRES)'
            method_type = 'EvolutionaryStrategySR'

        elif self.config.settings.method == 'evolutionary_program'.lower():
            method_name = 'Evolutionary Programming'
            method_type = 'EvolutionaryProgram'

        elif self.config.settings.method == 'hooke_jeeves'.lower():
            method_name = 'Hooke &amp; Jeeves'
            method_type = 'HookeJeeves'

        elif self.config.settings.method == 'levenberg_marquardt'.lower():
            method_name = 'Levenberg - Marquardt'
            method_type = 'LevenbergMarquardt'

        elif self.config.settings.method == 'nelder_mead'.lower():
            method_name = 'Nelder - Mead'
            method_type = 'NelderMead'

        elif self.config.settings.method == 'particle_swarm'.lower():
            method_name = 'Particle Swarm'
            method_type = 'ParticleSwarm'

        elif self.config.settings.method == 'praxis'.lower():
            method_name = 'Praxis'
            method_type = 'Praxis'

        elif self.config.settings.method == 'random_search'.lower():
            method_name = 'Random Search'
            method_type = 'RandomSearch'

        elif self.config.settings.method == 'simulated_annealing'.lower():
            method_name = 'Simulated Annealing'
            method_type = 'SimulatedAnnealing'

        elif self.config.settings.method == 'steepest_descent'.lower():
            method_name = 'Steepest Descent'
            method_type = 'SteepestDescent'

        elif self.config.settings.method == 'truncated_newton'.lower():
            method_name = 'Truncated Newton'
            method_type = 'TruncatedNewton'

        elif self.config.settings.method == 'scatter_search'.lower():
            method_name = 'Scatter Search'
            method_type = 'ScatterSearch'

        elif self.config.settings.method == 'genetic_algorithm'.lower():
            method_name = 'Genetic Algorithm'
            method_type = 'GeneticAlgorithm'

        elif self.config.settings.method == 'genetic_algorithm_sr'.lower():
            method_name = 'Genetic Algorithm SR'
            method_type = 'GeneticAlgorithmSR'

        else:
            raise errors.InputError(
                f'"{self.config.settings.method}" is an invalid '
                f'method argument. Please choose from "{sorted(self.valid_methods)}"'
            )

        return method_name, method_type

    def _convert_numeric_arguments_to_string(self):
        """
        xml requires all numbers to be strings. This method makes this conversion

        Returns:
            None

        """
        self.config.settings.number_of_generations = str(self.config.settings.number_of_generations)
        self.config.settings.population_size = str(self.config.settings.population_size)
        self.config.settings.random_number_generator = str(self.config.settings.random_number_generator)
        self.config.settings.seed = str(self.config.settings.seed)
        self.config.settings.pf = str(self.config.settings.pf)
        self.config.settings.iteration_limit = str(self.config.settings.iteration_limit)
        self.config.settings.tolerance = str(self.config.settings.tolerance)
        self.config.settings.rho = str(self.config.settings.rho)
        self.config.settings.scale = str(self.config.settings.scale)
        self.config.settings.swarm_size = str(self.config.settings.swarm_size)
        self.config.settings.std_deviation = str(self.config.settings.std_deviation)
        self.config.settings.number_of_iterations = str(self.config.settings.number_of_iterations)
        self.config.settings.start_temperature = str(self.config.settings.start_temperature)
        self.config.settings.cooling_factor = str(self.config.settings.cooling_factor)
        self.config.settings.lower_bound = str(self.config.settings.lower_bound)
        if isinstance(self.start_value, (float, int)):
            self.config.settings.start_value = str(self.config.settings.start_value)
        self.config.settings.upper_bound = str(self.config.settings.upper_bound)

    @property
    def _fit_items(self):
        """
        Get existing fit items
        Returns:
            dict containing models with fit_items

        """
        models_dct = {}
        for model_name in self.models:
            mod = self.models[model_name].model
            models_dct[model_name] = {}
            # d = {}
            query = '//*[@name="FitItem"]'
            for i in mod.xml.xpath(query):
                for j in list(i):
                    if j.attrib['name'] == 'ObjectCN':
                        match = re.findall('Reference=(.*)', j.attrib['value'])[0]

                        if match == 'Value':
                            match2 = re.findall('Reactions\[(.*)\].*Parameter=(.*),', j.attrib['value'])
                            if match2 != []:
                                match2 = '({}).{}'.format(match2[0][0], match2[0][1])

                        elif match == 'InitialValue':
                            match2 = re.findall('Values\[(.*)\]', j.attrib['value'])
                            if match2 != []:
                                match2 = match2[0]
                        elif match == 'InitialConcentration':

                            match2 = re.findall('Metabolites\[(.*)\]', j.attrib['value'])
                            if match2 != []:
                                match2 = match2[0]
                        if match2 != []:
                            models_dct[model_name][match2] = j.attrib

        return models_dct

    def _remove_all_fit_items(self):
        """
        Remove item from parameter estimation

        Returns:
            :py:attr:`ParameterEstimation.models`

        """

        for model_name in self.models:
            mod = self.models[model_name].model
            for item in self._fit_items[model_name]:

                all_items = list(self._fit_items[model_name].keys())

                query = '//*[@name="FitItem"]'
                assert item in all_items, '{} is not a fit item. These are the fit items: {}'.format(item, all_items)
                item = self._fit_items[model_name][item]
                for i in mod.xml.xpath(query):
                    for j in list(i):
                        if j.attrib['name'] == 'ObjectCN':
                            # locate references
                            # remove local parameters from PE task
                            match = re.findall('Reference=(.*)', j.attrib['value'])[0]
                            if match == 'Value':
                                pattern = 'Reactions\[(.*)\].*Parameter=(.*),Reference=(.*)'
                                match2_copasiML = re.findall(pattern, j.attrib['value'])
                                if match2_copasiML != []:
                                    match2_item = re.findall(pattern, item['value'])
                                    if match2_item != []:
                                        if match2_item == match2_copasiML:
                                            i.getparent().remove(i)

                            # rempve global parameters from PE task
                            elif match == 'InitialValue':
                                pattern = 'Values\[(.*)\].*Reference=(.*)'
                                match2_copasiML = re.findall(pattern, j.attrib['value'])
                                if match2_copasiML != []:
                                    match2_item = re.findall(pattern, item['value'])
                                    if match2_item == match2_copasiML:
                                        i.getparent().remove(i)

                            # remove IC parameters from PE task
                            elif match == 'InitialConcentration' or match == 'InitialParticleNumber':
                                pattern = 'Metabolites\[(.*)\],Reference=(.*)'
                                match2_copasiML = re.findall(pattern, j.attrib['value'])
                                if match2_copasiML != []:
                                    if match2_copasiML[0][1] == 'InitialConcentration' or match2_copasiML[0][
                                        1] == 'InitialParticleNumber':
                                        match2_item = re.findall(pattern, item['value'])
                                        if match2_item != []:
                                            if match2_item == match2_copasiML:
                                                i.getparent().remove(i)
                            else:
                                raise TypeError(
                                    'Parameter {} is not a local parameter, initial concentration parameter or a global parameter.initial_value'.format(
                                        match2_item))
            self.models[model_name].model = mod
        return self.models

    def _get_experiment_keys(self):
        """Experiment keys are always 'Experiment_i' where 'i' indexes
        the experiment in the order they are given in the experiment
        list. This method extracts the _experiments that are not for validation
        :return:

        Args:

        Returns:

        """
        dct = OrderedDict()

        for model_name in self.models:
            # model_name = self.models[model_name].model
            dct[model_name] = OrderedDict()

            for experiment_name in self.config.experiment_names:
                # experiment = self.config.datasets.experiments[experiment_name]
                key = "Experiment_{}".format(experiment_name)
                dct[model_name][experiment_name] = key
        return dct

    def _get_validation_keys(self):
        """
        Get keys for validation experiments

        Returns:
            dict[model] = list(validation_keys)

        """
        dct = OrderedDict()

        for model_name in self.models:
            # model_name = self.models[model_name].model
            dct[model_name] = OrderedDict()

            for validation_name in self.config.validation_names:
                # experiment = self.config.datasets.experiments[experiment_name]
                key = "Experiment_{}".format(validation_name)
                dct[model_name][validation_name] = key
        return dct

    def _add_fit_items(self, constraint=False):
        """
        Add a fit item to the model
        Args:
            constraint (bool): Set to True to configure fit item for constraints

        Returns:
            :py:attr:`ParameterEstimation.models`

        """
        for model_name in self.models:
            mod = self.models[model_name].model
            if constraint:
                ## Constraint items are not obligatory so skip if there
                ## are none.
                if 'constraint_items' not in self.config.items.keys():
                    return self.models
                else:
                    items = self.config.items.constraint_items
            else:
                items = self.config.items.fit_items

            for item_name in items:
                item = items[item_name]
                if not isinstance(item.affected_models, list):
                    item.affected_models = [item.affected_models]

                if model_name not in item.affected_models:
                    LOG.warning(f'model "{model_name}" is not in the affected models list '
                                f'({item.affected_models}) for item "{item_name}"'
                                f' and is therefore being skipped')
                    continue

                ## figure out what type of variable item is and assign to component
                item_type = None
                ## while we are distinguishing between component type we retrieve its
                ## model value so if the user specifies that the start value should be the
                ## model value, we can use the model_value that is collected here

                if item_name in mod.get_variable_names('m'):
                    component = [i for i in mod.metabolites if i.name == item_name][0]
                    item_type = 'metabolite'
                    if self.config.settings.quantity_type == 'concentration':
                        model_value = mod.get(item_type, item_name, by='name').concentration
                    elif self.config.settings.quantity_type == 'particle_numbers':
                        model_value = mod.get(item_type, item_name, by='name').particle_numbers
                    else:
                        raise errors.InputError(f'settings.quantity_type option must be'
                                                f' either "concentration" or "particle_numbers" '
                                                f'Got {self.config.settings.quantity_type}')

                elif item_name in mod.get_variable_names('l'):
                    component = [i for i in mod.local_parameters if i.global_name == item_name][0]
                    item_type = 'local_parameter'
                    model_value = mod.get(item_type, item_name, by='global_name').value

                elif item_name in mod.get_variable_names('g'):
                    component = [i for i in mod.global_quantities if i.name == item_name][0]
                    item_type = 'global_quantity'
                    model_value = mod.get(item_type, item_name, by='name').initial_value

                elif item_name in mod.get_variable_names('c'):
                    component = [i for i in mod.compartments if i.name == item_name][0]
                    item_type = 'compartment'
                    model_value = mod.get(item_type, item_name, by='name').initial_value

                else:
                    raise errors.SomethingWentHorriblyWrongError(
                        '"{}" is not a metabolite,'
                        ' local_parameter or '
                        'global_quantity. These are your'
                        ' model variables: {}'.format(
                            item_name,
                            str(mod.get_variable_names('a', include_assignments=False)))
                    )

                assert item_type is not None
                if item['start_value'] == 'model_value':
                    item['start_value'] = model_value

                # initialize new element
                fit_item_element = etree.Element('ParameterGroup', attrib={'name': 'FitItem'})

                '''
                We have a problem here in that when we ignore an experiment for a model 
                via the affected models arg, we also need to remove that experiment 
                from any fit items which may depend on it. 
                
                solutions
                ----------
                1. If affected experiments is 'all' change it so that the Affected Experiments element 
                   is blank, as it is when copasi configures the parameter estimation. 
                2. Modify the below section of code such that if an experiment doesn't exist for a 
                   model, we remove it from the affected experiments section. 
                3. Remove experiment from experiment_keys
                
                '''
                affected_experiments = {'name': 'Affected Experiments'}
                ## read affected _experiments from config file.yaml
                affected_experiments_attr = OrderedDict()

                ## the 'all' keyword argument for affected_experiments, affected_validations_Experiments
                ## and affected models needs resolving to lists of appropriate values

                ## when affected _experiments is 'all', the affected experiment element is empty
                if item['affected_experiments'] != 'all':
                    ## convert a string to a list of 1 so we can cater for the case
                    ## where we have a list of strings with the same code
                    if isinstance(item['affected_experiments'], str):
                        item['affected_experiments'] = [item['affected_experiments']]

                    ## when the list of affected experiments equals the set of experiment names
                    ## provided by the user we can just skip as the default behaviour is
                    ## for all experiments to affect a parameter when this field is empty
                    ignore_affected_experiments = False
                    if sorted(item['affected_experiments']) == sorted(self.config.experiment_names):
                        ignore_affected_experiments = True

                    if not ignore_affected_experiments:
                        ## iterate over list. Raise ValueError is can't find experiment name
                        ## otherwise add the corresponding experiment key to the affected _experiments attr dict
                        for affected_experiment in item['affected_experiments']:  ## iterate over the list
                            ## ensures that the parameter being configured `item_name`
                            ## has only experiments under its affected experiments attribute
                            ## that are actually in the model.
                            if affected_experiment not in self.config.models_affected_experiments[model_name]:
                                LOG.warning(
                                    f'ignoring {item_name} as {affected_experiment} not in '
                                    f'{self.config.models_affected_experiments[model_name]}'
                                )
                                continue

                            if affected_experiment in self._get_validation_keys()[model_name]:
                                raise ValueError('"{}" has been given as a validation experiment and therefore '
                                                 'I cannot add this experiment to the list of _experiments that '
                                                 'affect the {} parameter'.format(
                                    affected_experiment, component.name
                                ))

                            if affected_experiment not in self._get_experiment_keys()[model_name]:
                                raise ValueError('"{}" (type({}))is not one of your _experiments. These are '
                                                 'your valid experimments: "{}"'.format(
                                    affected_experiment, type(affected_experiment),
                                    self._get_experiment_keys()[model_name].keys()
                                ))

                            affected_experiments_attr[affected_experiment] = {}
                            affected_experiments_attr[affected_experiment]['name'] = 'Experiment Key'
                            affected_experiments_attr[affected_experiment]['type'] = 'key'
                            affected_experiments_attr[affected_experiment]['value'] = \
                                self._get_experiment_keys()[model_name][affected_experiment]

                ## add affected _experiments to element
                affected_experiments_element = etree.SubElement(fit_item_element, 'ParameterGroup',
                                                                attrib=affected_experiments)

                ## now add the attributes to the affected _experiments element
                for affected_experiment in affected_experiments_attr:
                    etree.SubElement(
                        affected_experiments_element, 'Parameter', attrib=affected_experiments_attr[affected_experiment]
                    )

                ## read affected validation _experiments from config file.yaml
                affected_validation_experiments_attr = OrderedDict()
                ## when affected _experiments is 'all', the affected experiment element is empty
                if item['affected_validation_experiments'] != 'all':
                    ## convert a string to a list of 1 so we can cater for the case
                    ## where we have a list of strings with the same code
                    if isinstance(item['affected_validation_experiments'], str):
                        item['affected_validation_experiments'] = [item['affected_validation_experiments']]

                    ignore_affected_validation_experiments = False
                    if sorted(item['affected_validation_experiments']) == sorted(self.config.validation_names):
                        ignore_affected_validation_experiments = True

                    if not ignore_affected_validation_experiments:
                        for affected_validation_experiment in item[
                            'affected_validation_experiments']:  ## iterate over the list

                            ## Analogous to affected_experiments above
                            if affected_validation_experiment not in self.config.models_affected_validation_experiments[
                                model_name]:
                                LOG.warning(f'ignoring {item_name} as {affected_experiment} not in '
                                      f'{self.config.models_affected_experiments[model_name]}')
                                continue

                            if affected_validation_experiment in self._get_experiment_keys()[model_name]:
                                raise ValueError('"{}" has been given as an experiment and therefore '
                                                 'I cannot add this experiment to the list of validation _experiments that '
                                                 'affect the {} parameter'.format(
                                    affected_validation_experiment, component.name
                                ))

                            if affected_validation_experiment not in self._get_validation_keys()[model_name]:
                                raise ValueError('"{}" is not one of your _experiments. These are '
                                                 'your valid experimments: "{}"'.format(
                                    affected_validation_experiment, self._get_validation_keys()[model_name].keys()
                                ))

                            affected_validation_experiments_attr[affected_validation_experiment] = {}
                            affected_validation_experiments_attr[affected_validation_experiment][
                                'name'] = 'Experiment Key'
                            affected_validation_experiments_attr[affected_validation_experiment]['type'] = 'key'
                            affected_validation_experiments_attr[affected_validation_experiment]['value'] = \
                                self._get_validation_keys()[model_name][affected_validation_experiment]

                affected_cross_validation_experiments = {'name': 'Affected Cross Validation Experiments'}

                affected_cross_validation_experiments_element = etree.SubElement(fit_item_element, 'ParameterGroup',
                                                                                 attrib=affected_cross_validation_experiments)

                ## now add the attributes to the affected _experiments element
                for affected_validation_experiment_attr in affected_validation_experiments_attr:
                    etree.SubElement(
                        affected_cross_validation_experiments_element, 'Parameter',
                        attrib=affected_validation_experiments_attr[affected_validation_experiment_attr]
                    )

                ## get lower bound from config file and add to element
                lower_bound_element = {'type': 'cn', 'name': 'LowerBound', 'value': str(item['lower_bound'])}
                etree.SubElement(fit_item_element, 'Parameter', attrib=lower_bound_element)
                start_value_element = {'type': 'float', 'name': 'StartValue', 'value': str(item['start_value'])}

                ## get upper bound from config file and add to element
                upper_bound_element = {'type': 'cn', 'name': 'UpperBound', 'value': str(item['upper_bound'])}
                etree.SubElement(fit_item_element, 'Parameter', attrib=upper_bound_element)

                etree.SubElement(fit_item_element, 'Parameter', attrib=start_value_element)

                ## Now begin creating the object map.
                # for IC parameters
                if isinstance(component, model.Metabolite):
                    if self.config.settings.quantity_type == 'concentration':
                        subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{},{}'.format(mod.reference,
                                                                                              component.compartment.reference,
                                                                                              component.initial_reference)}
                    else:
                        subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{},{}'.format(
                            mod.reference,
                            component.compartment.reference,
                            component.initial_particle_reference
                        )}

                elif isinstance(component, model.LocalParameter):
                    subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{},{}'.format(
                        mod.reference,
                        mod.get('reaction', component.reaction_name, by='name').reference,
                        component.value_reference)}

                elif isinstance(component, model.GlobalQuantity):
                    subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{}'.format(mod.reference,
                                                                                       component.initial_reference)}

                elif isinstance(component, model.Compartment):
                    subA4 = {'type': 'cn',
                             'name': 'ObjectCN',
                             'value': '{},{}'.format(mod.reference,
                                                     component.initial_volume_reference())}

                else:
                    raise errors.InputError('{} is not a valid parameter for estimation'.format(list(item)))

                ## add element
                etree.SubElement(fit_item_element, 'Parameter', attrib=subA4)

                ##insert fit item

                list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
                parameter_est = mod.xml.find(list_of_tasks)[5]
                problem = parameter_est[1]
                assert problem.tag == '{http://www.copasi.org/static/schema}Problem'

                if constraint:
                    item_list = problem[4]
                    assert list(item_list.attrib.values())[0] == 'OptimizationConstraintList'
                else:
                    item_list = problem[3]
                    assert list(item_list.attrib.values())[0] == 'OptimizationItemList'
                item_list.append(fit_item_element)

        return self.models

    def _set_method(self):
        """
        Choose algorithm and set algorithm specific parameters

        Returns:
            :py:attr:`ParameterEstimation.models`

        """

        # Build xml for method.
        method_name, method_type = self._select_method()
        method_params = {'name': method_name, 'type': method_type}
        method_element = etree.Element('Method', attrib=method_params)

        # list of attribute dictionaries
        # Evolutionary strategy parametery
        number_of_generations = {'type': 'unsignedInteger', 'name': 'Number of Generations',
                                 'value': str(self.config.settings.number_of_generations)}
        population_size = {'type': 'unsignedInteger', 'name': 'Population Size',
                           'value': str(self.config.settings.population_size)}
        random_number_generator = {'type': 'unsignedInteger', 'name': 'Random Number Generator',
                                   'value': str(self.config.settings.random_number_generator)}
        seed = {'type': 'unsignedInteger', 'name': 'Seed', 'value': str(self.config.settings.seed)}
        pf = {'type': 'float', 'name': 'Pf', 'value': str(self.config.settings.pf)}
        # local method parameters
        iteration_limit = {'type': 'unsignedInteger', 'name': 'Iteration Limit',
                           'value': str(self.config.settings.iteration_limit)}
        tolerance = {'type': 'float', 'name': 'Tolerance', 'value': str(self.config.settings.tolerance)}
        rho = {'type': 'float', 'name': 'Rho', 'value': str(self.config.settings.rho)}
        scale = {'type': 'unsignedFloat', 'name': 'Scale', 'value': str(self.config.settings.scale)}
        # Particle Swarm parmeters
        swarm_size = {'type': 'unsignedInteger', 'name': 'Swarm Size', 'value': str(self.config.settings.swarm_size)}
        std_deviation = {'type': 'unsignedFloat', 'name': 'Std. Deviation',
                         'value': str(self.config.settings.std_deviation)}
        # Random Search parameters
        number_of_iterations = {'type': 'unsignedInteger', 'name': 'Number of Iterations',
                                'value': str(self.config.settings.number_of_iterations)}
        # Simulated Annealing parameters
        start_temperature = {'type': 'unsignedFloat', 'name': 'Start Temperature',
                             'value': str(self.config.settings.start_temperature)}
        cooling_factor = {'type': 'unsignedFloat', 'name': 'Cooling Factor',
                          'value': str(self.config.settings.cooling_factor)}

        # build the appropiate xML, with method at root (for now)
        if self.config.settings.method == 'current_solution_statistics':
            pass  # no additional parameter elements required

        if self.config.settings.method == 'differential_evolution'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.config.settings.method == 'evolutionary_strategy_sr'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
            etree.SubElement(method_element, 'Parameter', attrib=pf)

        if self.config.settings.method == 'evolutionary_program'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.config.settings.method == 'hooke_jeeves'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=rho)

        if self.config.settings.method == 'levenberg_marquardt'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
        #
        if self.config.settings.method == 'nelder_mead'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=scale)

        if self.config.settings.method == 'particle_swarm'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=swarm_size)
            etree.SubElement(method_element, 'Parameter', attrib=std_deviation)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.config.settings.method == 'praxis'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)

        if self.config.settings.method == 'random_search'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_iterations)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.config.settings.method == 'simulated_annealing'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=start_temperature)
            etree.SubElement(method_element, 'Parameter', attrib=cooling_factor)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
        #
        if self.config.settings.method == 'steepest_descent'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
        #
        if self.config.settings.method == 'truncated_newton'.lower():
            # required no additonal paraemters
            pass
        #
        if self.config.settings.method == 'scatter_search'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_iterations)

        if self.config.settings.method == 'genetic_algorithm'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.config.settings.method == 'genetic_algorithm_sr'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
            etree.SubElement(method_element, 'Parameter', attrib=pf)
        models = {}

        for model_name in self.models:
            ## You must deep copy the method element or
            ## when dealing with multiple models only the last
            ## model will contain the method element.
            method_element = deepcopy(method_element)
            mod = self.models[model_name].model
            tasks = mod.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')
            method = tasks[5][-1]
            parent = method.getparent()
            parent.remove(method)
            parent.insert(2, method_element)
        return self.models

    def _set_options(self):
        """
        Set parameter estimation sepcific arguments

        Returns:
            :py:attr:ParameterEstimation.models
        """
        for model_name in self.models:
            mod = self.models[model_name].model

            scheluled_attrib = {'scheduled': False,
                                'updateModel': str(int(self.config.settings.update_model))}

            report_attrib = {'append': False,
                             'reference': self._get_report_key()[model_name],
                             'target': self.config.settings.report_name,
                             'confirmOverwrite': False}

            randomize_start_values = {'type': 'bool',
                                      'name': 'Randomize Start Values',
                                      'value': str(int(self.config.settings.randomize_start_values))}

            calculate_stats = {'type': 'bool', 'name': 'Calculate Statistics',
                               'value': str(int(self.config.settings.calculate_statistics))}
            create_parameter_sets = {'type': 'bool', 'name': 'Create Parameter Sets',
                                     'value': str(int(self.config.settings.create_parameter_sets))}

            for i in [
                scheluled_attrib,
                report_attrib,
                randomize_start_values,
                calculate_stats,
                create_parameter_sets]:

                for k, v in i.items():
                    i[k] = str(v)

            query = '//*[@name="Parameter Estimation"]' and '//*[@type="parameterFitting"]'
            for i in mod.xml.xpath(query):
                i.attrib.update(scheluled_attrib)
                for j in list(i):
                    if self.config.settings.report_name != None:
                        if 'append' in list(j.attrib.keys()):
                            j.attrib.update(report_attrib)
                    if list(j) != []:
                        for k in list(j):
                            if k.attrib['name'] == 'Randomize Start Values':
                                k.attrib.update(randomize_start_values)
                            elif k.attrib['name'] == 'Calculate Statistics':
                                k.attrib.update(calculate_stats)
                            elif k.attrib['name'] == 'Create Parameter Sets':
                                k.attrib.update(create_parameter_sets)
            self.models[model_name].model = mod
        return self.models

    def _enumerate_output(self):
        """
        Enumerates parameter estimation output files for each model

        Returns:
            dict[model_name][copy_number] = filename

        """

        dct = {}
        report_name = self.config.settings.report_name
        for model_name in self.models:
            dct[model_name] = {}
            for i in range(int(self.config.settings.copy_number)):
                new_file = os.path.join(
                    self.results_directory[model_name],
                    f'{report_name}{i}.txt' \
                        if report_name[-4:] != \
                           '.txt' else f'{report_name[:-4]}{i}.txt'
                )
                dct[model_name][i] = new_file
        return dct

    def _copy_model(self):
        """
        Copy the model n times Uses deep copy to ensure separate models
        Returns:
            dict[index] = model copy
        """
        dct = {}
        for model_name in self.models:
            mod = self.models[model_name].model
            ## a save is required here to 'commit' changed to xml before copying
            mod.save()
            ## copy model into fit problem dir
            fle = os.path.split(mod.copasi_file)[1]
            fname = os.path.join(self.models_dir[model_name], fle)
            shutil.copy(mod.copasi_file, fname)
            dct[model_name] = {}
            dct[model_name][0] = model.Model(fname)
            for i in range(1, int(self.config.settings.copy_number)):
                # dire, fle = os.path.split(fname)
                new_cps = os.path.join(self.models_dir[model_name], fle[:-4] + f'_{i}.cps')
                shutil.copy(fname, new_cps)
                dct[model_name][i] = model.Model(new_cps)
        return dct

    def _setup1scan(self, q, mod, report):
        """Setup a single scan.

        Args:
          q: queue from multiprocessing
          mod: pycotools3.model.Model
          report: str.

        Returns:
            None

        """
        if self.config.settings.context == 'pl':
            scan_variable = os.path.split(mod.copasi_file)[1][:-4]
            ##todo implement ability to modify boundaries
            ## scan_obj = [i for i in self.get_model_objects_from_strings() if i.name == scan_variable]
            scan_obj = mod.get_model_object(scan_variable)
            if isinstance(scan_obj, model.Metabolite):
                if self.config.settings.quantity_type == 'concentration':
                    scan_obj_init_value = scan_obj.concentration
                else:
                    scan_obj_init_value = scan_obj.particle_numbers
            elif isinstance(scan_obj, model.GlobalQuantity):
                scan_obj_init_value = scan_obj.initial_value
            elif isinstance(scan_obj, model.Compartment):
                scan_obj_init_value = scan_obj.initial_value
            elif isinstance(scan_obj, model.LocalParameter):
                scan_obj_init_value = scan_obj.value
            q.put(Scan(
                mod,
                scan_type='scan',
                minimum=float(scan_obj_init_value) / float(self.config.settings.pl_lower_bound),
                maximum=float(scan_obj_init_value) * float(self.config.settings.pl_upper_bound),
                variable=scan_variable,
                subtask='parameter_estimation',
                report_type='multi_parameter_estimation',
                report_name=report,
                run=False,
                append=False,
                confirm_overwrite=False,
                output_in_subtask=False,
                save=True,
                log10=True)
            )
        else:
            q.put(Scan(mod,
                       scan_type='repeat',
                       number_of_steps=self.config.settings.pe_number,
                       subtask='parameter_estimation',
                       report_type='multi_parameter_estimation',
                       report_name=report,
                       run=False,
                       append=False,
                       confirm_overwrite=False,
                       output_in_subtask=False,
                       save=True)
                  )

    def _setup_scan(self, models):
        """Set up `copy_number` repeat items with `pe_number`
        repeats of parameter estimation. Set run_mode to false
        as we want to use the multiprocess mode of the run_mode class
        to process all files at once in CopasiSE
        :return:

        Args:
          models: 

        Returns:
            result dict

        """
        res = {}
        for model_name in models:
            res[model_name] = {}
            # for model_i in self.models[model_name]:
            number_of_cpu = cpu_count()
            q = queue.Queue(maxsize=number_of_cpu)
            report_files = self._enumerate_output()[model_name]
            for copy_number, mod in list(models[model_name].items()):
                t = threading.Thread(target=self._setup1scan,
                                     args=(q, mod, report_files[copy_number]))
                t.daemon = True
                t.start()
                time.sleep(0.1)

                res[model_name][copy_number] = q.get().model
            ## Since this is being executed in parallel sometimes
            ## we get process clashes. Not sure exactly whats going on
            ## but introducing a small delay seems to fix
            time.sleep(0.1)
        return res

    def _setup(self):
        """
        Setup the copasi parameter estimation task

        Uses the other methods in this class to configure the parameter estimation
        according to the :py:class:`ParameterEstimation.Config`
        Returns:
            dict[model_name][sub_model_index] = :py:class:`model.Model` object

        """

        self.models = self._define_report()

        ## we must remove existing experiments prior to reconfiguring
        ## or invite a world of pain
        self._remove_all_experiments()
        self._remove_all_validation_experiments()

        self._map_experiments(validation=True)
        self._map_experiments(validation=False)

        ## get rid of existing parameter estimation definition
        self._remove_all_fit_items()
        self._add_fit_items(constraint=False)
        self._add_fit_items(constraint=True)

        self._set_options()
        self._set_method()

        ##copy
        copied_models = self._copy_model()
        ##configure scan task
        copied_models = self._setup_scan(copied_models)

        return copied_models

    def run(self, models):
        """
        Run a parameter estimation using command line copasi.

        Args:
          models: dict of models. Output from _setup()

        Returns:
          param models: dict of models. Output from _setup()

        """

        if self.config.settings.run_mode == 'sge':
            try:
                check_call('qhost')
            except errors.NotImplementedError:
                LOG.warning(
                    'Attempting to run in SGE mode but SGE specific commands are unavailable. Switching to \'parallel\' mode')
                self.config.settings.run_mode = 'parallel'

        if self.config.settings.run_mode == 'parallel':
            for model_name in models:
                RunParallel(
                    list(models[model_name].values()),
                    mode=self.config.settings.run_mode,
                    max_active=self.config.settings.max_active,
                    task='scan')

        elif self.config.settings.run_mode is True:
            for model_name in models:
                for copy_number, mod in list(models[model_name].items()):
                    LOG.info(f'running model {model_name}: {copy_number}')
                    Run(mod, mode=self.config.settings.run_mode, task='scan')

        elif not self.config.settings.run_mode:
            pass

        else:
            raise ValueError('"{}" is not a valid argument'.format(self.config.settings.run_mode))

    class Context:
        """
        A high level interface to create a :py:class:`ParameterEstimation.Config` object.

        Enables the construction of a :py:class:`ParameterEstimation.Config` object
        assuming one of several common patterns of usage.

        Examples:
            Assuming that we have two copasi models (`mod1` and `mod2`) and
            two experimental data files (`fname1`, `fname2`), correctly formatted according
            to the copasi specification. We can generate a config object that specifies
            the fitting of both experiments to both models and to fit all global and
            local parameters `parameters='gl'` in each.

            .. code-block:: python

                with ParameterEstimation.Context(
                    [mod1, mod2], [fname1, fname2],
                    context='s', parameters='gl') as context:
                    context.set('method', 'genetic_algorithm_sr')
                    context.set('number_of_generations', 25)
                    context.set('population_size', 10)
                    config = context.get_config()

                pe = ParameterEstimation(config)

            Or for profile likelihoods on the first model `mod1`

            .. code-block python

               with ParameterEstimation.Context(
                   mod, experiment_filename,
                   context='pl', parameters='gm'
               ) as context:
                   context.set('method', 'hooke_jeeves')
                   context.set('pl_lower_bound', 1000)
                   context.set('pl_upper_bound', 1000)
                   context.set('number_of_steps', 25)
                   context.set('run_mode', True)
                   config = context.get_config()

                pe = ParameterEstimation(config)


        """

        acceptable_context_args = {
            'm': 'model_selection',
            's': 'single_parameter_estimation',
            'r': 'repeat_parameter_estimation',
            'c': 'chaser_estimations',
        }

        acceptable_parameters_args = {
            'a': 'all',
            'g': 'global_quantities',
            'l': 'local_parameters',
            'c': 'initial_concentrations',
            'gl': 'global_quantities_and_local_parameters',
            'gc': 'global_quantities_and_initial_concentrations',
            'lc': 'local_parameters_and_initial_concentrations',
            '_': 'prefixed_with_underscore'
            ##todo implement a means of including a list of parameters as sings to this class
        }

        experiment_filetypes = ['.txt', '.csv']

        def __init__(self, models, experiments, working_directory=None,
                     context='s', parameters='mg', filename=None,
                     validation_experiments={}, settings={}):
            self.models = models
            self.experiments = experiments
            self.working_directory = working_directory
            self.context = context
            self.parameters = parameters
            self.filename = filename
            self.validation_experiments = validation_experiments
            self.settings = settings

            self.defaults = ParameterEstimation._Defaults()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):

            if exc_type:
                LOG.critical(f'exc_type: {exc_type}')
                LOG.critical(f'exc_value: {exc_value}')
                LOG.critical(f'exc_traceback: {exc_traceback}')

        def set(self, parameter, value):
            """
            Set the value of :code:`parameter` to :code:`value`.

            Looks for the first instance of :code:`parameter` and sets its value to :code:`value`.
            To set all values of a parameter, see :py:meth:`ParameterEstimation.Config.set_all`


            Args:
                parameter: A key somewhere in the nested structure of the config object
                value: A value to replace the current value with

            Returns:
                None

            """

            if parameter in self.defaults.settings:
                self.defaults.settings[parameter] = value

            elif parameter in self.defaults.constraint_items:
                self.defaults.constraint_items[parameter] = value

            elif parameter in self.defaults.fit_items:
                self.defaults.fit_items[parameter] = value

            elif parameter in self.defaults.experiments:
                self.defaults.experiments[parameter] = value

            elif parameter in self.defaults.validations:
                self.defaults.validations[parameter] = value

            else:
                raise errors.InputError(
                    f'"{parameter}" is not a valid argument'
                )

        def get_config(self):
            if self.context == 's':
                return self.get_config_simple()
            elif self.context == 'pl':
                return self.get_config_pl()
            elif self.context == 'cv':
                return self.get_config_cv()
            else:
                raise ValueError

        def get_config_simple(self):
            ## update the config
            self._add_models(self.models)
            self._add_settings(self.settings)
            self._add_experiments(self.experiments)
            self._add_validation_experiments(self.validation_experiments)
            self._add_working_directory(self.working_directory)
            dct = dict(
                models=self.models,
                datasets=dict(
                    experiments=self.experiments,
                    validations=self.validation_experiments
                ),
                items=dict(
                    fit_items=self.parameters
                ),
                settings=self.settings
            )

            config = ParameterEstimation.Config(**dct, defaults=self.defaults)

            if self.filename is not None:
                if os.path.isfile(self.filename) and not config.settings.overwrite_config_file:
                    LOG.critical(f'"{self.filename}" already exists. To force an overwrite, '
                                 f'set `settings.overwrite_config_file` to True')
                elif os.path.isfile(self.filename) and config.settings.overwrite_config_file:
                    config.to_yaml(self.filename)

                elif not os.path.isfile(self.filename):
                    config.to_yaml(self.filename)

                else:
                    raise errors.SomethingWentHorriblyWrongError(
                        'Something weird happened.'
                    )
            return config

        def get_config_pl(self):
            """
            configure for profile likelihoods
            Returns:

            """
            ## change the results_directory settings
            config = self.get_config_simple()
            if len(config.models) != 1:
                NotImplementedError(
                    'Currently pycotools3 only supports the configuration of profile likelihoods'
                    ' for a single model at a time'
                )

            config.settings['problem'] = 'ProfileLikelihoods'
            config.settings['randomize_start_values'] = False
            config.settings['context'] = self.context

            if not os.path.isdir(config.settings['problem']):
                os.makedirs(config.settings['problem'])

            parameters = list(config.items.fit_items.keys())

            files = {}
            for p in parameters:
                new_file = os.path.join(config.settings['problem'], f'{p}.cps')
                shutil.copy(config.models[list(config.models.keys())[0]].copasi_file,
                            new_file)
                files[p] = os.path.abspath(new_file)

            assert len(glob.glob(os.path.join(config.settings['problem'], '*.cps'))) == len(parameters)

            ##change the models which appear in the config
            new_models_attr = {}
            for p in files:
                mod = model.Model(files[p])
                new_models_attr[p] = dict(
                    copasi_file=files[p],
                    model=mod
                )

            ## now modify affected models attribute
            for fit_item in config.items.fit_items:
                model_list = [i for i in parameters if i != fit_item]
                config.items.fit_items[fit_item].affected_models = model_list

            ##todo change affect models for experiments as well
            for experiment in config.experiments:
                config.experiments[experiment].affected_models = parameters

            for experiment in config.validations:
                config.validations[experiment].affected_models = parameters

            new_config = ParameterEstimation.Config(
                models=new_models_attr,
                datasets=config.datasets,
                items=config.items,
                settings=config.settings
            )

            return new_config

        def get_config_cv(self):
            """
            configure for cross validation
            Returns:

            """
            ## change the results_directory settings
            config = self.get_config_simple()
            if len(config.models) != 1:
                NotImplementedError(
                    'Currently pycotools3 only supports the configuration of cross validation parameter estimations'
                    ' for a single model at a time'
                )

            config.settings['problem'] = 'CrossValidation'
            config.settings['context'] = self.context

            if not os.path.isdir(config.settings['problem']):
                os.makedirs(config.settings['problem'])

            config.datasets.validations = deepcopy(config.datasets.experiments)

            experiments = list(config.experiments.keys())

            if config.settings.cross_validation_depth > len(experiments):
                raise errors.InputError(
                    f'Number of experiments cannot '
                    f'exceed that of the '
                    f'cross_validation_depth setting '
                    f'({config.settings.cross_validation_depth} > {len(self.experiments)}'
                )

            ## work out how many models we need
            ## and create the correct combinations
            experiments_combs = {}
            validation_combs = {}
            count = 0
            for current_depth in range(config.settings.cross_validation_depth + 1):
                num_exp = len(experiments) - current_depth
                e = list(itertools.combinations(self.experiments, num_exp))
                count += len(list(e))
                for experiment_set in range(len(e)):
                    experiments_combs[f'{num_exp}_{experiment_set}'] = e[experiment_set]
                    validation_combs[f'{num_exp}_{experiment_set}'] = list(set(experiments).difference(set(e[experiment_set])))

            LOG.info(f'Configuring cross validation. {count} models needed')

            model_keys = list(self.models.keys())
            copasi_file = config.models[model_keys[0]].model.copasi_file
            model_dct = {}
            ## copy model
            for exp_id in experiments_combs:
                for exp_name in experiments_combs[exp_id]:
                    fname = os.path.join(config.settings.problem,
                                         f'{os.path.splitext(copasi_file)[0]}'
                                         f'{exp_id}.cps')
                    shutil.copy(copasi_file, fname)
                    model_dct[exp_id] = os.path.abspath(fname)

            new_models_attr = {}
            for i in model_dct:
                mod = model.Model(model_dct[i])
                new_models_attr[i] = dict(
                    copasi_file=model_dct[i],
                    model=mod
                )


            ## prepare affected models dct
            new_aff_models_exp = {}
            for exp in experiments:
                new_aff_models_exp[exp] = []
                for model_name in experiments_combs:
                    if exp in experiments_combs[model_name]:
                        new_aff_models_exp[exp] += [model_name]

            new_aff_models_val = {}
            for val in experiments:
                new_aff_models_val[val] = []
                for model_name in validation_combs:
                    if val in validation_combs[model_name]:
                        new_aff_models_val[val] += [model_name]


            datasets = deepcopy(config.datasets)
            for exp in experiments:
                datasets.experiments[exp].affected_models = new_aff_models_exp[exp]

            for exp in experiments:
                datasets.validations[exp].affected_models = new_aff_models_val[exp]


            datasets = dict(
                experiments=datasets.experiments,
                validations=datasets.validations
            )

            fit_items = deepcopy(config.items.fit_items)

            for fit_item in fit_items:
                fit_items[fit_item].affected_models = 'all'

            items = dict(
                fit_items=fit_items,
                # constraint_items=config.items.constraint_items
            )

            new_config = ParameterEstimation.Config(
                models=new_models_attr,
                datasets=datasets,
                items=items,
                settings=config.settings
            )
            return new_config

        def _add_models(self, models: (str, list)):
            """
            Add models to class attributes

            Args:
              models (str, list): Path to copasi file or list of paths to copasi files

            Returns:
                None
            """
            ## if models passed as a string
            if not isinstance(models, list):
                models = [models]

            cps_file_list = []
            for i in models:
                if isinstance(i, model.Model):
                    cps_file_list.append(i.copasi_file)
                elif isinstance(i, str):
                    if not os.path.isfile(i):
                        raise errors.InputError(
                            f'"{i}" does not an existing file'
                        )
                    cps_file_list.append(i)

            models = {os.path.split(i)[1][:-4]: {
                'copasi_file': i
            } for i in cps_file_list}

            setattr(self, 'models', models)

        def _add_experiments(self, experiments: (str, list)):
            """
            Add list of experiments to class attributes
            Args:
                experiments (str, list): Path pointing to experimental data file or list of paths pointing to experimental data files

            Returns:
                None
            """

            if not isinstance(experiments, list):
                experiments = [experiments]

            for i in experiments:
                ## todo support for dataframes, dict and other
                ## python objects as arguments

                if not os.path.isfile(i):
                    raise errors.InputError(
                        f'"{i}" does not an existing file'
                    )
                if os.path.splitext(i)[1] not in self.experiment_filetypes:
                    raise errors.InputError(
                        f'File with "{os.path.splitext(i)[1]}" is not supported'
                    )

            experiments = {os.path.split(i)[1][:-4]: {
                'filename': i
            } for i in experiments}

            setattr(self, 'experiments', experiments)

        def _add_validation_experiments(self, experiments: (str, list)):
            """Add experiments to validation_experiments attribute

            Args:
              experiments (str, list): path to validation data or list of paths to validation data

            Returns:
                None
            """
            if experiments is None or experiments == {}:
                return None
            if not isinstance(experiments, list):
                experiments = [experiments]

            if isinstance(experiments, list):
                for i in experiments:
                    if not os.path.isfile(i):
                        raise errors.InputError(
                            f'"{i}" does not an existing file'
                        )
                    if os.path.splitext(i)[1] not in self.experiment_filetypes:
                        raise errors.InputError(
                            f'File with "{os.path.splitext(i)[1]}" is not supported'
                        )

            experiments = {os.path.split(i)[1][:-4]: {
                'filename': i
            } for i in experiments}

            setattr(self, 'validation_experiments', experiments)

        def _add_working_directory(self, working_directory: str):
            """
            Add working_directory to class attributes. Put in same path
            as first copasi model if argument not specified.
            Args:
                working_directory (str): Path to location on the system to store analysis

            Returns:
                None
            """
            if working_directory is None or working_directory == '':
                model_keys = list(self.models.keys())
                working_directory = os.path.dirname(self.models[model_keys[0]]['copasi_file'])

            if not os.path.isdir(working_directory):
                raise errors.InputError(f'"{working_directory}" does not exist')

            self.settings['working_directory'] = working_directory

        def _add_setting(self, setting, value):
            """

            Args:
              setting:
              value:

            Returns:

            """
            if not hasattr(self, 'settings'):
                setattr(self, 'settings', {})
            self.settings[setting] = value

        def _add_settings(self, settings):
            """

            Args:
              settings:

            Returns:

            """
            if not isinstance(settings, dict):
                raise TypeError(f'add_settings expects a dict as argument. Got "{type(settings)}"')
            self.settings.update(settings)


@mixin(model.GetModelComponentFromStringMixin)
@mixin(model.ReadModelMixin)
class Sensitivities(_Task):
    """Interface to COPASI sensitivity task"""

    ## subtasks
    subtasks = {
        'evaluation': '0',
        'steady_state': '1',
        'time_series': '2',
        'parameter_estimation': '3',
        'optimization': '4',
        'cross_section': '5',
    }

    evaluation_effect = [
        'not_set'
        'single_object',
        'concentration_fluxes',
        'particle_fluxes',
        'concentration_rates',
        'particle_rates',
        'non_constant_global_quantities'
    ]

    steady_state_effect = evaluation_effect + [
        'all_variables',
        'non_constant_species_concentrations',
        'non_constant_species_numbers',
        'real_part_of_eigenvalues_of_jacobian',
        'imaginary_part_of_eigenvalues_of_jacobian'
    ]
    time_series_effect = [i for i in steady_state_effect if i not in ['real_part_of_eigenvalues_of_reduced_jacobian',
                                                                      'imaginary_part_of_eigenvalues_of_reduced_jacobian']]

    parameter_estimation_effect = ['single_object']
    optimization_effect = deepcopy(parameter_estimation_effect)
    cross_section_effect = deepcopy(parameter_estimation_effect)

    steady_state_cause = [
        'not_set',
        'single_object',
        'local_parameters',
        'all_parameters',
        'initial_concentrations'
    ]

    time_series_cause = steady_state_cause + [
        'all_parameters_and_initial_concentrations'
    ]

    parameter_estimation_cause = deepcopy(time_series_cause)
    optimization_cause = deepcopy(time_series_cause)
    cross_section_cause = deepcopy(time_series_cause)

    evaluation_cause = [
        'not_set',
        'single_object',
        'non_constant_species_concentration',
        'species_concentration',
        'non_constant_species_numbers',
        'non_constant_global_quantities',
        'global_quantities',
        'local_parameters',
        'all_parameters'
    ]

    ## for the 'ObjectListType xml element
    sensitivitity_number_map = {
        'single_object': '1',
        'concentration_fluxes': '21',
        'particle_fluxes': '22',
        'concentration_rates': '17',
        'particle_rates': '18',
        'global_quantity_rates': '30',
        'all_variables': '43',
        'non_constant_species_concentrations': '7',
        'non_constant_species_numbers': '8',
        'non_constant_global_quantities': '26',
        'real_part_of_eigenvalues_of_jacobian': '45',
        'imaginary_part_of_eigenvalues_of_jacobian': '46',
        'not_set': '0',
        'species_concentrations': '5',
        'global_quaantities': '25',
        'local_parameter_values': '40',
        'all_parameters': '41',
        'initial_concentrations': '3',
        'all_parameters_and_initial_concentrations': '42',
    }

    update_model = False

    def __init__(self, model, **kwargs):
        self.model = self.read_model(model)
        default_report_name = os.path.join(os.path.dirname(self.model.copasi_file), 'sensitivities.txt')

        default_properties = {
            'subtask': 'time_series',
            'cause': 'all_parameters',
            'effect': 'all_variables',
            'effect_single_object': None,
            'cause_single_object': None,
            'secondary_cause_single_object': None,
            'secondary_cause': 'not_set',
            'delta_factor': 0.001,
            'delta_minimum': 1e-12,
            'report_name': default_report_name,
            'append': False,
            'confirm_overwrite': False,
            'scheduled': True,
            'run': True,
        }

        default_properties.update(kwargs)
        default_properties = self.convert_bool_to_numeric(default_properties)
        self.check_integrity(list(default_properties.keys()), list(kwargs.keys()))
        self.update_properties(default_properties)
        self._do_checks()

        ## change signle obejct reference for the pycotools3 model variable equiv
        self.get_single_object_references()
        ## add a report to output specifications
        self.model = self.create_new_report()

        ## build up task sequentially. This list of commands shold
        ## be executed in order
        self.task = self.create_sensitivity_task()
        self.task = self.set_report()
        self.task = self.create_problem()
        self.task = self.set_subtask()
        self.task = self.set_effect()
        self.task = self.add_list_of_variables_element()
        self.task = self.set_cause()
        self.task = self.set_secondary_cause()
        self.task = self.set_method()
        self.model = self.replace_sensitivities_task()
        self.model = self.run_task()

        ## extract relevant (non scaled) data from the copasi report
        self.sensitivities = self.process_data()

        ## overwrite the copasi report with only relevant data
        self.sensitivities.to_csv(self.report_name, sep='\t')

    def _do_checks(self):
        """ """
        if self.subtask == 'evaluation':
            if self.cause not in self.evaluation_cause:
                raise errors.InputError('cause "{}" not in "{}"'.format(self.cause, self.evaluation_cause))

            if self.effect not in self.evaluation_effect:
                raise errors.InputError('effect  "{}" not in "{}"'.format(self.effect, self.evaluation_effect))

            if self.secondary_cause not in self.evaluation_cause:
                raise errors.InputError(
                    'secondary cause "{}" not in "{}"'.format(self.secondary_cause, self.evaluation_cause))

        elif self.subtask == 'steady_state':
            if self.cause not in self.steady_state_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.steady_state_cause))

            if self.effect not in self.steady_state_effect:
                raise errors.InputError('effect "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(
                    self.effect, self.subtask, self.steady_state_effect))

            if self.secondary_cause not in self.steady_state_cause:
                raise errors.InputError('Secondary cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.steady_state_cause))

        elif self.subtask == 'time_series':
            if self.cause not in self.time_series_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.time_series_cause))

            if self.effect not in self.time_series_effect:
                raise errors.InputError('effect "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.effect, self.subtask,
                                                                                    self.time_series_cause))

            if self.secondary_cause not in self.time_series_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.time_series_cause))

        elif self.subtask == 'parameter_estimation':
            if self.cause not in self.parameter_estimation_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.parameter_estimation_cause))

            if self.effect not in self.parameter_estimation_effect:
                raise errors.InputError('effect "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.effect, self.subtask,
                                                                                    self.parameter_estimation_cause))

            if self.secondary_cause not in self.parameter_estimation_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.parameter_estimation_cause))

        elif self.subtask == 'optimization':
            if self.cause not in self.optimization_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.optimization_cause))

            if self.effect not in self.optimization_effect:
                raise errors.InputError('effect "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.effect, self.subtask,
                                                                                    self.optimization_cause))

            if self.secondary_cause not in self.optimization_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.optimization_cause))

        elif self.subtask == 'cross_section':
            if self.cause not in self.cross_section_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.cross_section_cause))

            if self.effect not in self.cross_section_effect:
                raise errors.InputError('effect "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.effect, self.subtask,
                                                                                    self.cross_section_cause))

            if self.secondary_cause not in self.cross_section_cause:
                raise errors.InputError('cause "{}" not in available for "{}" '
                                        'subtask. These are available: "{}"'.format(self.cause, self.subtask,
                                                                                    self.cross_section_cause))

        ## verify that single objects are actually in the model
        ## and are strings
        if self.effect_single_object is not None:
            if not isinstance(self.effect_single_object, str):
                raise errors.TypeError("effect_single_object parameter should be of type str. "
                                       "Got '{}' instead".format(type(self.effect_single_object)))

            if self.effect_single_object not in self.model.all_variable_names:
                raise errors.InputError('Variable "{}" is not in model. These '
                                        'are in your model "{}"'.format(self.effect_single_object,
                                                                        self.model.all_variable_names))

        if self.cause_single_object is not None:
            if not isinstance(self.cause_single_object, str):
                raise errors.TypeError("cause_single_object parameter should be of type str. "
                                       "Got '{}' instead".format(type(self.cause_single_object)))

            if self.cause_single_object not in self.model.all_variable_names:
                raise errors.InputError('Variable "{}" is not in model. These '
                                        'are in your model "{}"'.format(self.cause_single_object,
                                                                        self.model.all_variable_names))

        if self.secondary_cause_single_object is not None:
            if not isinstance(self.secondary_cause_single_object, str):
                raise errors.TypeError("secondary_cause_single_object  parameter should be of type str. "
                                       "Got '{}' instead".format(type(self.secondary_cause_single_object)))

            if self.secondary_cause_single_object not in self.model.all_variable_names:
                raise errors.InputError('Variable "{}" is not in model. These '
                                        'are in your model "{}"'.format(self.secondary_cause_single_object,
                                                                        self.model.all_variable_names))

    def get_single_object_references(self):
        """ """
        if self.cause_single_object is not None:
            self.cause_single_object = self.get_variable_from_string(self.model, self.cause_single_object)

        if self.effect_single_object is not None:
            self.cause_single_object = self.get_variable_from_string(self.model, self.effect_single_object)

        if self.secondary_cause_single_object is not None:
            self.cause_single_object = self.get_variable_from_string(self.model, self.secondary_cause_single_object)

    def sensitivity_task_key(self):
        """Get the sensitivity task as it currently is
        in the model as etree.Element
        :return:

        Args:

        Returns:

        """
        # query = './/Task/*[@name="Sensitivities"]'
        tasks = self.model.xml.findall(self.schema + 'ListOfTasks')[0]
        for i in tasks:
            if i.attrib['name'] == 'Sensitivities':
                return i.attrib['key']

    def create_sensitivity_task(self):
        """ """
        return etree.Element('Task', attrib=OrderedDict({
            'key': self.sensitivity_task_key(),
            'name': 'Sensitivities',
            'type': 'sensitivities',
            'scheduled': 'false',
            'updateModel': 'false'
        }))

    def create_new_report(self):
        """ """
        report_options = OrderedDict({
            'report_name': self.report_name,
            'append': self.append,
            'confirm_overwrite': self.confirm_overwrite,
            'update_model': self.update_model,
            'report_type': 'sensitivity'
        })
        report = Reports(self.model, **report_options)
        return report.model

    def get_report_key(self):
        """ """
        ## get the report key
        for i in self.model.xml:
            if i.tag == self.schema + 'ListOfReports':
                for j in i:
                    if j.attrib['name'] == 'sensitivity':
                        return j.attrib['key']

    def set_report(self):
        """ """
        attrib = OrderedDict({
            'reference': self.get_report_key(),
            'target': self.report_name,
            'append': self.append,
            'confirmOverwrite': self.confirm_overwrite
        })
        etree.SubElement(self.task, 'Report', attrib=attrib)
        return self.task

    def create_problem(self):
        """ """
        etree.SubElement(self.task, 'Problem')
        return self.task

    def set_subtask(self):
        """ """
        assert self.task[1].tag == 'Problem'
        attrib = OrderedDict({
            'name': 'SubtaskType',
            'type': 'unsignedInteger',
            'value': self.subtasks[self.subtask]
        })
        etree.SubElement(self.task[1], 'Parameter', attrib=attrib)
        return self.task

    def set_effect(self):
        """ """
        assert self.task[1].tag == 'Problem'
        parameter_group = etree.SubElement(self.task[-1], 'ParameterGroup',
                                           attrib={'name': 'TargetFunctions'})
        single_object_attrib = OrderedDict({
            'name': 'SingleObject',
            'type': 'cn',
            'value': "" if self.effect_single_object is None else self.effect_single_object
        })
        object_list_type_attrib = OrderedDict({
            'name': 'ObjectListType',
            'type': 'unsignedInteger',
            'value': self.sensitivitity_number_map[self.effect]
        })
        etree.SubElement(parameter_group, 'Parameter', attrib=single_object_attrib)
        etree.SubElement(parameter_group, 'Parameter', attrib=object_list_type_attrib)
        return self.task

    def add_list_of_variables_element(self):
        """ """
        assert self.task[1].tag == 'Problem'
        parameter_group = etree.SubElement(self.task[-1], 'ParameterGroup',
                                           attrib={'name': 'ListOfVariables'})
        return self.task

    def set_cause(self):
        """ """
        assert self.task[1].tag == 'Problem'
        assert self.task[1][2].attrib['name'] == 'ListOfVariables'
        parameter_group = etree.SubElement(
            self.task[1][2], 'ParameterGroup', attrib={'name': 'Variables'}
        )

        single_object_attrib = OrderedDict({
            'name': 'SingleObject',
            'type': 'cn',
            'value': "" if self.cause_single_object is None else self.cause_single_object
        })
        object_list_type_attrib = OrderedDict({
            'name': 'ObjectListType',
            'type': 'unsignedInteger',
            'value': self.sensitivitity_number_map[self.cause]
        })
        etree.SubElement(parameter_group, 'Parameter', attrib=single_object_attrib)
        etree.SubElement(parameter_group, 'Parameter', attrib=object_list_type_attrib)
        return self.task

    def set_secondary_cause(self):
        """ """
        pass
        assert self.task[1].tag == 'Problem'
        assert self.task[1][2].attrib['name'] == 'ListOfVariables'
        parameter_group = etree.SubElement(
            self.task[1][2], 'ParameterGroup', attrib={'name': 'Variables'}
        )
        single_object_attrib = OrderedDict({
            'name': 'SingleObject',
            'type': 'cn',
            'value': "" if self.secondary_cause_single_object is None else self.secondary_cause_single_object
        })
        object_list_type_attrib = OrderedDict({
            'name': 'ObjectListType',
            'type': 'unsignedInteger',
            'value': self.sensitivitity_number_map[self.secondary_cause]
        })
        etree.SubElement(parameter_group, 'Parameter', attrib=single_object_attrib)
        etree.SubElement(parameter_group, 'Parameter', attrib=object_list_type_attrib)
        return self.task

    def set_method(self):
        """ """
        method_attrib = OrderedDict({
            'name': 'Sensitivities Method',
            'type': 'SensitivitiesMethod',
        })
        method = etree.SubElement(self.task, 'Method', attrib=method_attrib)
        etree.SubElement(method, 'Parameter', attrib=OrderedDict({
            'name': 'Delta factor',
            'type': 'unsignedFloat',
            'value': str(self.delta_factor)
        }))

        etree.SubElement(method, 'Parameter', attrib=OrderedDict({
            'name': 'Delta minimum',
            'type': 'unsignedFloat',
            'value': str(self.delta_minimum)
        }))
        return self.task

    def replace_sensitivities_task(self):
        """ """
        task_list = self.model.xml.findall(self.schema + 'ListOfTasks')[0]
        for i in task_list:
            if i.attrib['name'] == 'Sensitivities':
                i.getparent().remove(i)
        task_list.insert(9, self.task)
        return self.model

    def run_task(self):
        """ """
        r = Run(self.model, task='sensitivities', mode=self.run)
        return r.model

    def process_data(self):
        """ """
        if not os.path.isfile(self.report_name):
            raise ValueError('Sensitivity report missing. Please ensure you have '
                             'executed the sensitivity task and the report exists. '
                             'The report should be here "{}"'.format(self.report_name))

        with open(self.report_name, 'r') as f:
            data = f.read()

        pattern = 'Sensitivities array(.*)Scaled sensitivities array'
        data = re.findall(pattern, data, re.DOTALL)
        data = [i.strip() for i in data]
        assert data[0][:4] == 'Rows'
        data = data[0].split('\n')
        data = reduce(lambda x, y: x + '\n' + y, data[2:])
        data = StringIO(data)
        df = pandas.read_csv(data, sep='\t', index_col=0)
        new_headers = []
        for i in df.columns:
            match = re.findall('.*\[(.*)\]', i)
            if match == []:
                new_headers.append(i)
            else:
                new_headers.append(match[0])
        df.columns = new_headers
        df.columns.name = self.cause

        new_index = []
        for i in df.index:
            match = re.findall('.*\[(.*)\]', i)
            if match == []:
                new_index.append(i)
            else:
                new_index.append(match[0])

        df[self.effect] = new_index
        return df.set_index(self.effect)


class FIM(Sensitivities):
    """Let S = matrix of partial derivatives of metabolites with respect to
    kinetic parameters. Then the fisher information matrix (FIM) is:
        FIM = S^TS

    Args:

    Returns:

    """
    subtask = 'time_series'
    effect = 'all_variables'
    cause = 'all_parameters'
    secondary_cause = 'not_set'

    def __init__(self, model, **kwargs):
        kwargs['subtask'] = self.subtask
        kwargs['effect'] = self.effect
        kwargs['cause'] = self.cause
        kwargs['secondary_cause'] = self.secondary_cause
        super(FIM, self).__init__(model, **kwargs)

    @property
    def fim(self):
        """ """
        return self.sensitivities.transpose().dot(self.sensitivities)


class Hessian(Sensitivities):
    """ """
    pass


class GlobalSensitivities(Sensitivities):
    """Sensitivity around parameter estimates"""
    pass


##todo implements the steady state task

if __name__ == '__main__':
    pass
#    execfile('/home/b3053674/Documents/Models/2017/08_Aug/pycotoolsTests/RunPEs.py')
#    execfile('/home/b3053674/Documents/pycotools3/pycotools3/pycotoolsTutorial/Test/testing_kholodenko_manually.py')
