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
import time
import threading
import queue as queue
import psutil
import shutil
import numpy
import pandas
import scipy
import os
from lxml import etree
from io import StringIO
import logging
import os
import subprocess
import re
from . import viz
from . import errors
from . import misc
from . import _base
from . import model
from multiprocessing import Process, cpu_count
import glob
import seaborn as sns
from copy import deepcopy
from subprocess import check_call
from collections import OrderedDict
from .mixin import Mixin, mixin
from functools import reduce
import yaml

## TODO use generators when iterating over a function with another function. i.e. plotting
## TODO: create a base class called Task instead of all of these mixin functions.

LOG = logging.getLogger(__name__)
sns.set_context(context='poster',
                font_scale=3)


class _Task(object):
    """
    base class for tasks
    """
    schema = '{http://www.copasi.org/static/schema}'

    @staticmethod
    def get_variable_from_string(m, v, glob=False):
        """
        Use model entity name to get the
        pycotools3 variable
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

    @staticmethod
    def convert_bool_to_numeric(dct):
        """
        CopasiML uses 1's and 0's for True or False in some
        but not all places. When one of these options
        is required by the user and is specified as bool,
        this class converts them into 1's or 0's.

        Use this method in early on in constructor for
        all subclasses where this applies.
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
        """
        CopasiML uses 1's and 0's for True or False in some
        but not all places. When one of these options
        is required by the user and is specified as bool,
        this class converts them into 1's or 0's.

        This is like convert_bool_to_numeric but
        uses setattr

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


class Bool2Str(object):
    """
    copasiML expects strings and we pythoners
    want to use python booleans not strings
    This class quickly converts between them
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
        for kwarg in list(self.dct.keys()):
            if kwarg in self.acceptable_kwargs:
                if self.dct[kwarg] == True:
                    self.dct.update({kwarg: "true"})
                else:
                    self.dct.update({kwarg: "false"})
        #
        return self.dct


class CopasiMLParser(_Task):
    """
    Parse a copasi file into xml.etree.

    .. highlight::

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
        """
        Parse xml doc with lxml
        :return:
        """
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(self.copasi_file, parser)
        return tree

    @staticmethod
    def write_copasi_file(copasi_filename, xml):
        """
        write to file with lxml write function
        """
        # first convert the copasiML to a root element tree
        root = etree.ElementTree(xml)
        root.write(copasi_filename)


@mixin(model.ReadModelMixin)
class Run(_Task):
    """
    Execute a copasi model using CopasiSE. To
    be operational the environment variable CopasiSE
    must be set to point towards the location of
    your CopasiSE executable. This is usually
    done automatically.

    .. highlight::

        ## First get a model object
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
    parallel                Run several at once
    sge                     Run on sun grid engine
    slurm                   Run on Slurm
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
                                   'sge_job_filename': None,
                                   'copasi_location': 'apps/COPASI/4.21.166-Linux-64bit',  # for sge mode
                                   }

        self.default_properties.update(self.kwargs)
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(list(self.default_properties.keys()), list(self.kwargs.keys()))
        self._do_checks()

        if self.sge_job_filename == None:
            self.sge_job_filename = os.path.join(os.getcwd(), 'sge_job_file.sh')

        if self.mode is 'slurm':
            self.copasi_location = r'COPASI/4.22.170'

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
            raise ValueError('"multiprocess" has been deprecated. Please'
                             'use mode="parallel" instead')

        elif self.mode == 'slurm':
            self.submit_copasi_job_slurm()

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

        modes = [True, False, 'multiprocess', 'parallel', 'sge', 'slurm']
        if self.mode not in modes:
            raise errors.InputError('{} not in {}'.format(self.mode, modes))

    def __str__(self):
        return 'Run({})'.format(self.to_string())

    def multi_run(self):
        pids = []

        ##TODO build Queue.Queue system for multi running.
        def run(x):
            if os.path.isfile(x) != True:
                raise errors.FileDoesNotExistError('{} is not a file'.format(self.copasi_file))
            p = subprocess.Popen(['CopasiSE', self.model.copasi_file])
            return p.pid

        Process(run(self.model.copasi_file))

    def set_task(self):
        """

        :return:
        """
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

    def submit_copasi_job_SGE(self):
        """
        Submit copasi file as job to SGE based job scheduler.
        :param copasi_location:
            Location to copasi on the sge cluster. Gets passed to `module add` to load copasi

        :return:
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
        """
        Submit copasi file as job to SGE based job scheduler.
        :param copasi_location:
            Location to copasi on the sge cluster. Gets passed to `module add` to load copasi

        :return:
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
    """


    """

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

        ##TODO put Try except block here once you remember which error
        ##is being raised
        self.run_parallel()

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
        """

        :return:
        """
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
        """
        Run models in parallel. Only have self.max_active
        models running at once
        :return:
            None
        """
        pids = []
        num_models_to_process = len(self.models)

        while num_models_to_process > 0:

            # for copy_number, model in self.models.items():
            model = self.models[num_models_to_process - 1]
            if len(pids) < self.max_active:
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
    """
    Creates reports in copasi output specification section. Which report is
    controlled by the report_type key word. The following are valid types of
    report:

    .. _report_kwargs:
    ------------------

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
    """

    def __init__(self, model, **kwargs):
        """

        :param model:
            :py:class:`model.Model`.

        :param kwargs: see :ref:`report_kwargs`
        """
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
        '''
        creates a report to collect time course results.

        By default all species and all global quantities are used with
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the metabolites keyword or global quantities to the
        global quantities keyword
        '''
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

        '''
        generate more SubElements dynamically
        '''
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
        '''
        creates a report to collect scan time course results.

        By default all species and all global quantities are used with
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the metabolites keyword or global quantities to the
        global quantities keyword
        '''
        # get existing report keys

        ##TODO implement self.variable as column in scan
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
        '''
        Create report of a parameter and best value for a parameter estimation
        for profile likelihoods
        '''
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

        ##TODO cater for particle numbers
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
        '''
        Define a parameter estimation report and include the progression
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords.
        '''
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
        '''
        Define a parameter estimation report and include the progression
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords.
        '''
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
        '''
        Execute code that builds the report defined by the kwargs
        '''
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
        """

        remove report called report_name
        :param report_name:
        :return: pycotools3.model.Model
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
        """
        Having multile reports defined at once can be really annoying
        and give you unexpected results. Use this function to remove all reports
        before defining a new one to ensure you only have one active report any once.
        :return:
        """
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            for j in list(i):
                if 'target' in list(j.attrib.keys()):
                    j.attrib['target'] = ''
        return self.model


@mixin(model.ReadModelMixin)
class TimeCourse(_Task):
    """
    ##todo implement arguments that get passed on to report
    as **report_kwargs

    .. _timecourse_kwargs:

    =================
    TimeCourse Kwargs
    =================
    
    These kwargs are directly passed on to copasi in the right situations. 
    See copasi documentation for mode details.
    
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
    <report_kwargs>                 Arguments for :ref:`_report_kwargs` are also
                                    accepted here
    ===========================     ==============================================
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

    def run_task(self):
        R = Run(self.model, task='time_course', mode=self.run)
        return R.model

    def create_task(self):
        """
        Begin creating the segment of xml needed
        for a time course. Define task and problem
        definition. This section of xml is common to all
        methods
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
        """
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
        """
        :return:
        """
        raise errors.NotImplementedError('The hybrid-RK-45 method is not yet implemented')

    def set_report(self):
        """
        ser a time course report containing time
        and all species or global quantities defined by the user.

        :return: pycotools3.model.Model
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
        """
        cross reference the timecourse task with the newly created
        time course reort to get the key
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
    """
    Interface to COPASI scan task

    .. _scan_kwargs:

    Scan Kwargs
    ===========

    ===========================     ==============================================
    Scan Kwargs               Description
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
    <report_kwargs>                 Arguments for :ref:`_report_kwargs` are also
                                    accepted here
    ===========================     ==============================================
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
            raise errors.ReportDoesNotExistError(
                'Report doesn\'t exist. Check to see if you have either defined the report manually or used the pycopi.Reports class')
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
@mixin(model.ReadModelMixin)
class ParameterEstimation(_Task):
    """
    Set up and run a parameter estimation in copasi.

    To setup:

        # Make text or csv files containing experimental data. This is the
        same as you would using the COPASI GUI except column headers **MUST**
        be identical to the model component. For this reason, all model
        components must have unique names. See Caveats in documentation.
        # instantiate the ParameterEstimation class with all the
          options that you want.
        # run the write_config_file() method
        # If options for which model components you want to include are
        in point 1 then skip this point. If you are manually defining which
        parameters you want to estimate, open the config file and
        modify as you see fit.
        # Use the setup() method
        # use the run method

    .. _parameter_estimation_kwargs:

    ParameterEstimation kwargs
    ==========================

    ===========================     ==================================================
    ParameterEstimation Kwargs               Description
    ===========================     ==================================================
    update_model                    Default: False
    randomize_start_values          Default: True
    create_parameter_sets           Default: False
    calculate_statistics            Default: False
    use_config_start_values         Default: False. Use starting values from config file
                                    Set randomize_start_values to False
    method                          Default: 'genetic_algorithm'
    number_of_generations           Default: 200
    population_size                 Default: 50
    random_number_generator         Default: 1
    seed                            Default: 0
    pf                              Default: 0.475
    iteration_limit                 Default: 50
    tolerance                       Default: 0.00001
    rho                             Default: 0.2
    scale                           Default: 10
    swarm_size                      Default: 50
    std_deviation                   Default: 0.000001
    number_of_iterations            Default: 100000
    start_temperature               Default: 1
    cooling_factor                  Default: 0.85
    scheduled                       Default: False
    lower_bound                     Default: 0.000001
    upper_bound                     Default: 1000000
    start_value                     Default: 0.1
    save                            Default: False
    run_mode                        Default: True. Passed on to :ref:`run`
    max_active                      Default: None. Max number of models to run at once.
    metabolites                     Default: All metabolites. Metabolites to
                                    include in the config file
    global_quantities               Default: All global_quantities. Global quantities
                                    to include in the config file
    local_parameters                Default: All local_parameters. local parameters
                                    to include in the config file
    <report_kwargs>                 Arguments for :ref:`_report_kwargs` are also
                                    accepted here and passed on
    <experiment_mapper_kwargs>      Arguments for :ref:`_experiment_mapper_kwargs` are
                                    accepted here and passed on
    ===========================     ==================================================



     ===========================     ==================================================
     ParameterEstimation Kwargs               Description
     ===========================     ==================================================
     copy_number                     default: 1. Number of model copies to configure
     pe_number                       default: 1. Number of parameter estimations per
                                     model
     run_mode                        default: True
     results_directory               default: MultiParameterEstimationResults in
                                     same directory as :py:attr:`coapsi_file`
     max_active                      default: None. Number of models to run
                                     simultaneously. If None then run all.
     ===========================     ==================================================

    """

    def __init__(self, model, experiment_files, **kwargs):
        """

        :param model:
            :py:class:`model.Model`

        :param experiment_files:
            `list` Each element a string to an appropriately
            configured data file.

        :param kwargs:
            :ref:`parameter_estimation_kwargs`

        """
        self.model = self.read_model(model)
        self.kwargs = kwargs
        # super(ParameterEstimation, self).__init__(model, **kwargs)
        self.experiment_files = experiment_files
        if isinstance(self.experiment_files, list) != True:
            self.experiment_files = [self.experiment_files]

        # default_report_name = os.path.join(os.path.dirname(self.model.copasi_file), 'PEData.txt')
        config_file = os.path.join(os.path.dirname(self.model.copasi_file), 'config_file.yaml')


        self.default_properties = {
            'metabolites': self.model.metabolites,
            'global_quantities': self.model.global_quantities,
            'local_parameters': self.model.local_parameters,
            'copy_number': 1,
            'pe_number': 1,
            'results_directory': os.path.join(self.model.root, 'ParameterEstimationResults'),
            'quantity_type': 'concentration',
            'report_name': 'PEData.txt',
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
            'experiment_keys': ["Experiment_{}".format(i) for i in range(len(self.experiment_files))],
            'first_row': [str(1)] * len(self.experiment_files),
            'normalize_weights_per_experiment': [True] * len(self.experiment_files),
            'row_containing_names': [1] * len(self.experiment_files),
            'separator': ['\t'] * len(self.experiment_files),
            'weight_method': ['mean_squared'] * len(self.experiment_files),
            'validation': [False] * len(self.experiment_files),
            'validation_weight': 1,
            'validation_threshold': 5,
            'affected_experiments': {},
            'affected_validation_experiments': {},
            'scheduled': False,
            'lower_bound': 0.000001,
            'upper_bound': 1000000,
            'lower_bound_dct': {},
            'upper_bound_dct': {},
            'start_value': 0.1,
            'save': False,
            'run_mode': True,
            'max_active': None,
            'mappings': None,
        }

        self.default_properties.update(self.kwargs)
        self.update_properties(self.default_properties)
        self.check_integrity(list(self.default_properties.keys()), list(self.kwargs.keys()))

        self._do_checks()

        # self.default_properties = self.convert_bool_to_numeric(self.default_properties)
        # self._convert_numeric_arguments_to_string()

        if self.save:
            self.model.save()

    def __str__(self):
        return "ParameterEstimation(method='{}', config_filename='{}', report_name='{}')".format(
            self.method, self.config_filename, self.report_name)

    def _do_checks(self):
        """

        """
        for i in self.validation:
            if not isinstance(i, bool):
                raise errors.InputError('"validation" should be of type bool. Got "{}"'.format(
                    type(i)))

        for i in range(len(self.experiment_files)):
            if os.path.isabs(self.experiment_files[i]) != True:
                self.experiment_files[i] = os.path.abspath(self.experiment_files[i])

        assert isinstance(self.separator, list)
        for i in self.separator:
            assert isinstance(i, str), 'separator should be given asa python list'

        ## Allow acceptance of strings as arguments to metabolites, local_parameters
        ## and global_quantities
        for attr in ['metabolites', 'local_parameters', 'global_quantities']:
            getattribute = getattr(self, attr)
            new_attr = []
            for i in range(len(getattribute)):
                if isinstance(getattribute[i], str):
                    new_attr.append(self.get_variable_from_string(self.model, getattribute[i]))
                    setattr(self, attr, new_attr)

        ## ensure experiment files exist
        for fle in self.experiment_files:
            if os.path.isfile(fle) != True:
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
                        i, self.model.local_parameters))

        ## ensure arguments to metabolites exist
        for i in [j.name for j in self.metabolites]:
            if i not in [j.name for j in self.model.metabolites]:
                raise errors.InputError(
                    '"{}" not a metabolite. These are your local parameters: {}'.format(
                        i, self.model.metabolites))

        ## ensure arguments to global_quantities exist
        for i in [j.name for j in self.global_quantities]:
            if i not in [j.name for j in self.model.global_quantities]:
                raise errors.InputError(
                    '"{}" not a global_quantity. These are your local parameters: {}'.format(
                        i, self.model.global_quantities))

        if self.use_config_start_values not in [True, False]:
            raise errors.InputError(
                ''' Argument to the use_config_start_values must be \'True\' or \'False\' not {}'''.format(
                    self.use_config_start_values))
            if self.randomize_start_values in ['true', 1, '1', True]:
                LOG.warning('using config start values but randomize start '
                            'values is set to True. ')

        ## if start_value is series make it a df
        if type(self.start_value) is pandas.Series:
            self.start_value = pandas.DataFrame(self.start_value)

        ## if start_value is is pandas dataframe set randomize start values to false
        ## and use_config_start_values to True
        if type(self.start_value) is pandas.DataFrame:
            LOG.info('using user specified starting parameters so setting '
                     'randomize_start_values to False')

            self.randomize_start_values = '0'
            self.use_config_start_values = True

        run_arg_list = [False, True, 'parallel', 'sge']

        if self.run_mode not in run_arg_list:
            raise errors.InputError('run_mode needs to be one of {}'.format(run_arg_list))

        if isinstance(self.copy_number, int) != True:
            raise errors.InputError('copy_number argument is of type int')

        if isinstance(self.pe_number, int) != True:
            raise errors.InputError('pe_number argument is of type int')

    @property
    def _experiments(self):
        existing_experiment_list = []
        query = '//*[@name="Experiment Set"]'

        for i in self.model.xml.xpath(query):
            for j in list(i):
                existing_experiment_list.append(j)
        return existing_experiment_list

    @property
    def _validations(self):
        existing_validation_list = []
        query = '//*[@name="Validation Set"]'

        for i in self.model.xml.xpath(query):
            for j in list(i):
                existing_validation_list.append(j)
        return existing_validation_list

    def _create_metabolite_reference(self, parent, metabolite, role):
        if not isinstance(metabolite, model.Metabolite):
            raise ValueError('Input should be "model.Metabolite" class. Got "{}"'.format(type(metabolite)))

        if role == 'independent':
            cn = '{},{},{}'.format(self.model.reference,
                               metabolite.compartment.reference,
                               metabolite.initial_reference)
        elif role == 'dependent':
            cn = '{},{},{}'.format(self.model.reference,
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

    def _create_local_parameter_reference(self, parent, local_parameter, role):
        """
        Not used because local parameters are not usually mapped to experimental
        variables. However, this method will be kept until the next release
        to ensure no bugs arise because of a lack of local parameter reference

        :param parent:
        :param local_parameter:
        :param role:
        :return:
        """
        if not isinstance(local_parameter, model.LocalParameter):
            raise ValueError('Input should be "model.LocalParameter" class. Got "{}"'.format(type(metabolite)))

        if role == 'independent':
            cn = '{},{},{}'.format(self.model.reference,
                                   local_parameter.compartment.reference,
                                   local_parameter.initial_reference)
        elif role == 'dependent':
            cn = '{},{},{}'.format(self.model.reference,
                                   local_parameter.compartment.reference,
                                   local_parameter.transient_reference)
        else:
            raise ValueError

        local_attrs = {
            'type': 'cn',
            'name': 'Object CN',
            'value': cn
        }
        parent = etree.SubElement(parent, 'Parameter', attrib=local_attrs )
        return parent

    def _create_global_quantity_reference(self, parent, global_quantity, role):
        if not isinstance(global_quantity, model.GlobalQuantity):
            raise ValueError('Input should be "model.GlobalQuantity" class. Got "{}"'.format(type(global_quantity)))

        if role == 'independent':
            cn = '{},{}'.format(self.model.reference,
                                global_quantity.initial_reference)

        elif role == 'dependent':
            cn = '{},{}'.format(self.model.reference,
                                global_quantity.initial_reference)
        else:
            raise ValueError

        global_attrs = {
            'type': 'cn',
            'name': 'Object CN',
            'value': cn
        }
        etree.SubElement(parent, 'Parameter', attrib=global_attrs )
        return parent

    def _assign_role(self, parent, role):
        """
        Used in create experiment to correctly map the role of each variable in
        experiemtnal data columns
        :return:
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
            raise ValueError('"{}" is not a valid role'.format(role) )

        return parent

    def _create_experiment(self, index):
        """
        Adds a single experiment set to the parameter estimation task
        exp_file is an experiment filename with exactly matching headers (independent variablies need '_indep' appended to the end)
        since this method is intended to be used in a loop in another function to
        deal with all experiment sets, the second argument 'i' is the index for the current experiment

        i is the exeriment_file index
        """
        assert isinstance(index, int)
        data = pandas.read_csv(
            self.experiment_files[index],
            sep=self.separator[index])
        obs = list(data.columns)
        num_rows = str(data.shape[0])
        num_columns = str(data.shape[1])

        # if exp_file is in the same directory as copasi_file only use relative path
        if os.path.dirname(self.model.copasi_file) == os.path.dirname(self.experiment_files[index]):
            exp = os.path.split(self.experiment_files[index])[1]
        else:
            exp = self.experiment_files[index]

        experiment_file = {'type': 'file',
                           'name': 'File Name',
                           'value': exp}
        key = {'type': 'key',
               'name': 'Key',
               'value': self.experiment_keys[index]
               }

        # necessary XML attributes
        experiment_group = etree.Element('ParameterGroup',
                                         attrib={
                                             'name': os.path.split(self.experiment_files[index])[1][:-4]
                                         })

        row_orientation = {'type': 'bool',
                           'name': 'Data is Row Oriented',
                           'value': self.row_orientation[index]}

        experiment_type = {'type': 'unsignedInteger',
                           'name': 'Experiment Type',
                           'value': self.experiment_type[index]}

        first_row = {'type': 'unsignedInteger',
                     'name': 'First Row',
                     'value': str(self.first_row[index])}

        last_row = {'type': 'unsignedInteger',
                    'name': 'Last Row',
                    'value': str(int(num_rows) + 1)}  # add 1 to account for 0 indexed python

        normalize_weights_per_experiment = {'type': 'bool',
                                            'name': 'Normalize Weights per Experiment',
                                            'value': self.normalize_weights_per_experiment[index]}

        number_of_columns = {'type': 'unsignedInteger',
                             'name': 'Number of Columns',
                             'value': num_columns}

        object_map = {'name': 'Object Map'}

        row_containing_names = {'type': 'unsignedInteger',
                                'name': 'Row containing Names',
                                'value': str(self.row_containing_names[index])}

        separator = {'type': 'string',
                     'name': 'Separator',
                     'value': self.separator[index]}

        weight_method = {'type': 'unsignedInteger',
                         'name': 'Weight Method',
                         'value': self.weight_method[index]}
        etree.SubElement(experiment_group, 'Parameter', attrib=key)
        etree.SubElement(experiment_group, 'Parameter', attrib=experiment_file)
        etree.SubElement(experiment_group, 'Parameter', attrib=row_orientation)
        etree.SubElement(experiment_group, 'Parameter', attrib=first_row)
        etree.SubElement(experiment_group, 'Parameter', attrib=last_row)
        etree.SubElement(experiment_group, 'Parameter', attrib=experiment_type)
        etree.SubElement(experiment_group, 'Parameter', attrib=normalize_weights_per_experiment)
        etree.SubElement(experiment_group, 'Parameter', attrib=separator)
        etree.SubElement(experiment_group, 'Parameter', attrib=weight_method)
        etree.SubElement(experiment_group, 'Parameter', attrib=row_containing_names)
        etree.SubElement(experiment_group, 'Parameter', attrib=number_of_columns)
        map = etree.SubElement(experiment_group, 'ParameterGroup', attrib=object_map)

        experiment_name = os.path.split(self.experiment_files[index])[1][:-4]

        for i in self.mappings:
            if i == experiment_name:
                data_column_number = 0
                for data_column_name in self.mappings[i]:
                    if data_column_name not in obs:
                        raise errors.InputError('Incorrect Mapping. In your config file you have '
                                                'specified a column ({}) that is not present '
                                                'in your experiment ("{}"). These are variables '
                                                'in your data file: "{}"'.format(
                            data_column_name, experiment_name, obs
                        ))
                    column_mapping = self.mappings[i][data_column_name]['model_object']

                    # if column_mapping[-6:] == '_indep':
                    #     column_mapping = column_mapping[:-6]


                    ## use data column number for column name
                    map_group = etree.SubElement(map, 'ParameterGroup', attrib={'name': str(data_column_number)})
                    data_column_number += 1

                    # if self.experiment_type[index] == str(1): ##str(1) is code for timecourse
                    #     if current_col == 0:
                    #         etree.SubElement(map_group, 'Parameter', attrib=time_role)


                    if column_mapping.lower() == 'time':
                        self._assign_role(map_group, self.mappings[i][data_column_name]['role'])
                        # map_group = etree.SubElement(map_group, 'Parameter', attrib=time_role)

                    elif column_mapping in [j.name for j in self.model.metabolites]:
                        metab = [j for j in self.model.metabolites if j.name == column_mapping]
                        assert len(metab) == 1

                        ## create appropriate reference for metabolite
                        self._create_metabolite_reference(
                            map_group,
                            metab[0],
                            self.mappings[i][data_column_name]['role'])
                        self._assign_role(map_group, self.mappings[i][data_column_name]['role'])

                    elif column_mapping in [j.name for j in self.model.global_quantities]:
                        global_quantity = [j for j in self.model.global_quantities if j.name == column_mapping]
                        assert len(global_quantity) == 1
                        map_group = self._create_global_quantity_reference(
                            map_group,
                            global_quantity[0],
                            self.mappings[i][data_column_name]['role']
                        )

                        self._assign_role(map_group, self.mappings[i][data_column_name]['role'])


                    else:
                        LOG.warning('data_column_name "{}" is not in your model '
                                    'metabolites, local_parameters or global_quantities and '
                                    'therefore is being ignored in your estimation. Please '
                                    'review. '.format(column_mapping))
        return experiment_group

                    # elif self.experiment_types[index] == str(0): ##code for steady state
                    #     pass


                    # else:
                    #     raise ValueError('Experiment type is not a 1 or 0')

                    # print(experiment_name, column, self.mappings[i][current_col])

        # for i in range(int(num_columns)):
        #     map_group = etree.SubElement(map, 'ParameterGroup', attrib={'name': (str(i))})
        #     if self.experiment_type[index] == str(1):  # when Experiment type is set to time course it should be 1
        #         ## first column is time
        #         if i == 0:
        #             etree.SubElement(map_group, 'Parameter', attrib=time_role)
        #         else:
        #             ## map independent variables
        #             if obs[i][-6:] == '_indep':
        #                 if obs[i][:-6] in [j.name for j in self.model.metabolites]:
        #                     metab = [j for j in self.model.metabolites if j.name == obs[i][:-6]][0]
        #                     cn = '{},{},{}'.format(self.model.reference,
        #                                            metab.compartment.reference,
        #                                            metab.initial_reference)
        #                     independent_ICs = {'type': 'cn',
        #                                        'name': 'Object CN',
        #                                        'value': cn}
        #                     etree.SubElement(map_group, 'Parameter', attrib=independent_ICs)
        #
        #                 elif obs[i][:-6] in [j.name for j in self.model.global_quantities]:
        #                     glob = [j for j in self.model.global_quantities if j.name == obs[i][:-6]][0]
        #                     cn = '{},{}'.format(self.model.reference,
        #                                         glob.initial_reference)
        #
        #                     independent_globs = {'type': 'cn',
        #                                          'name': 'Object CN',
        #                                          'value': cn}
        #
        #                     etree.SubElement(map_group,
        #                                      'Parameter',
        #                                      attrib=independent_globs)
        #                 else:
        #                     continue
        #                     ##etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
        #                     LOG.warning('{} not found. Set to ignore'.format(obs[i]))
        #                 etree.SubElement(map_group, 'Parameter', attrib=independent_variable_role)
        #
        #             ## now do dependent variables
        #             elif obs[i][:-6] != '_indep':
        #                 ## metabolites
        #                 if obs[i] in [j.name for j in self.model.metabolites]:
        #                     metab = [j for j in self.model.metabolites if j.name == obs[i]][0]
        #                     cn = '{},{},{}'.format(self.model.reference,
        #                                            metab.compartment.reference,
        #                                            metab.transient_reference)
        #
        #                     dependent_ICs = {'type': 'cn',
        #                                      'name': 'Object CN',
        #                                      'value': cn}
        #
        #                     etree.SubElement(map_group, 'Parameter', attrib=dependent_ICs)
        #
        #                 ## global quantities
        #                 elif obs[i] in [j.name for j in self.model.global_quantities]:
        #                     glob = [j for j in self.model.global_quantities if j.name == obs[i]][0]
        #                     cn = '{},{}'.format(self.model.reference,
        #                                         glob.initial_reference)
        #                     dependent_globs = {'type': 'cn',
        #                                        'name': 'Object CN',
        #                                        'value': cn}
        #                     etree.SubElement(map_group,
        #                                      'Parameter',
        #                                      attrib=dependent_globs)
        #                 ## remember that local parameters are not mapped to experimental
        #                 ## data
        #                 else:
        #                     continue
        #                     ##etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
        #                     LOG.warning('{} not found. Set to ignore'.format(obs[i]))
        #                 ## map for time course dependent variable
        #                 etree.SubElement(map_group, 'Parameter', attrib=dependent_variable_role)
        #
        #     ## and now for steady state data
        #     else:
        #
        #         ## do independent variables first
        #         if obs[i][-6:] == '_indep':
        #
        #             ## for metabolites
        #             if obs[i][:-6] in [j.name for j in self.model.metabolites]:
        #                 metab = [j for j in self.model.metabolites if j.name == obs[i][:-6]][0]
        #                 cn = '{},{},{}'.format(self.model.reference,
        #                                        metab.compartment.reference,
        #                                        metab.initial_reference)
        #
        #                 independent_ICs = {'type': 'cn',
        #                                    'name': 'Object CN',
        #                                    'value': cn}
        #                 x = etree.SubElement(map_group, 'Parameter', attrib=independent_ICs)
        #
        #             ## now for global quantities
        #             elif obs[i][:-6] in [j.name for j in self.model.global_quantities]:
        #                 glob = [j for j in self.model.global_quantities if j.name == obs[i]][0]
        #                 cn = '{},{}'.format(self.model.reference,
        #                                     glob.initial_reference)
        #
        #                 independent_globs = {'type': 'cn',
        #                                      'name': 'Object CN',
        #                                      'value': cn}
        #
        #                 etree.SubElement(map_group,
        #                                  'Parameter',
        #                                  attrib=independent_globs)
        #             ## local parameters are never mapped
        #             else:
        #                 continue
        #                 # etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
        #                 LOG.warning('{} not found. Set to ignore'.format(obs[i]))
        #             etree.SubElement(map_group, 'Parameter', attrib=independent_variable_role)
        #
        #
        #         elif obs[i][-6:] != '_indep':
        #             ## for metabolites
        #             if obs[i] in [j.name for j in self.model.metabolites]:
        #                 metab = [j for j in self.model.metabolites if j.name == obs[i]][0]
        #                 cn = '{},{},{}'.format(self.model.reference,
        #                                        metab.compartment.reference,
        #                                        metab.transient_reference)
        #                 independent_ICs = {'type': 'cn',
        #                                    'name': 'Object CN',
        #                                    'value': cn}
        #                 etree.SubElement(map_group, 'Parameter', attrib=independent_ICs)
        #
        #             ## now for global quantities
        #             elif obs[i] in [j.name for j in self.model.global_quantities]:
        #                 glob = [j for j in self.model.global_quantities if j.name == obs[i]][0]
        #                 cn = '{},{}'.format(self.model.reference,
        #                                     glob.transient_reference)
        #
        #                 independent_globs = {'type': 'cn',
        #                                      'name': 'Object CN',
        #                                      'value': cn}
        #
        #                 etree.SubElement(map_group,
        #                                  'Parameter',
        #                                  attrib=independent_globs)
        #             ## local parameters are never mapped
        #             else:
        #                 continue
        #                 ##etree.SubElement(map_group, 'Parameter', attrib=ignored_role)
        #                 LOG.warning('{} not found. Set to ignore'.format(obs[i]))
        #             etree.SubElement(map_group, 'Parameter', attrib=dependent_variable_role)
        # return experiment_group

    def _remove_experiment(self, experiment_name):
        """
        name attribute of experiment. usually Experiment_1 or something
        """
        query = '//*[@name="Experiment Set"]'
        for i in self.model.xml.xpath(query):
            for j in list(i):
                if j.attrib['name'] == experiment_name:
                    j.getparent().remove(j)
        return self.model

    def _remove_all_experiments(self):
        for i in self._experiments:
            experiment_name = i.attrib['name']
            self._remove_experiment(experiment_name)
        return self.model

    def _remove_validation_experiment(self, validation_experiment_name):
        """
        name attribute of experiment. usually Experiment_1 or something
        """
        query = '//*[@name="Validation Set"]'
        for i in self.model.xml.xpath(query):
            for j in list(i):
                if j.attrib['name'] == validation_experiment_name:
                    j.getparent().remove(j)
        return self.model

    def _remove_all_validation_experiments(self):
        for i in self._validations:
            validation_experiment_name = i.attrib['name']
            self._remove_experiment(validation_experiment_name)
        return self.model

    def _map_experiments(self):
        """
        map all experiment sets
        :return:
        """

        self._remove_all_experiments()
        self._remove_all_validation_experiments()
        for index in range(len(self.experiment_files)):

            ## read data to get headers.
            ## read in such a way that duplicate columns are not mangled
            data = pandas.read_csv(self.experiment_files[index], sep=self.separator[index], skip_blank_lines=False,
                                   header=None)
            data = data.rename(columns=data.iloc[0], copy=False).iloc[1:].reset_index(drop=True)

            ## if none of the variables in the experiment file exist then skip
            variable_exists_list = []
            for i in data.columns:
                if i not in self.model.all_variable_names:
                    variable_exists_list.append(False)
                else:
                    variable_exists_list.append(True)

            ## if variable exists list ends up being False, we know
            ## that none of the data in the datafile have
            ## variables correlating to model components. In this case,
            ## pycotools3 skips mapping this file and sends a warning

            if (list(set(variable_exists_list))[0] == False) and (len(list(set(variable_exists_list))) == 1):
                LOG.warning('None of the column headers in your experimental '
                            'data file ("{}") match any model variable in model "{}". If '
                            'this is intentional, you can ignore this warning. This '
                            'most commonly occurs when using MultiModelFit. In this case '
                            'the data file is intended for an alternative model which is '
                            'why the variable is not in the model. If this is not the case, '
                            'please check your experimental data variable names to ensure they exactly match '
                            'corresponding model variable names. For convenience here is a list of '
                            'variables in your model: \n "{}"'.format(self.experiment_files[index],
                                                                      self.model.name,
                                                                      self.model.all_variable_names))
                continue
            experiment_element = self._create_experiment(index)

            if self.validation[index]:
                query = '//*[@name="Validation Set"]'
            else:
                query = '//*[@name="Experiment Set"]'

            for j in self.model.xml.xpath(query):
                j.insert(0, experiment_element)
                if self.validation[index]:
                    for k in list(j):
                        if k.attrib['name'] == 'Weight':
                            k.attrib['value'] = str(self.validation_weight)
                        if k.attrib['name'] == 'Threshold':
                            k.attrib['value'] = str(self.validation_threshold)

        return self.model

    def _select_method(self):
        """
        #determine which method to use
        :return: tuple. (str, str), (method_name, method_type)
        """
        if self.method == 'current_solution_statistics'.lower():
            method_name = 'Current Solution Statistics'
            method_type = 'CurrentSolutionStatistics'

        if self.method == 'differential_evolution'.lower():
            method_name = 'Differential Evolution'
            method_type = 'DifferentialEvolution'

        if self.method == 'evolutionary_strategy_sr'.lower():
            method_name = 'Evolution Strategy (SRES)'
            method_type = 'EvolutionaryStrategySR'

        if self.method == 'evolutionary_program'.lower():
            method_name = 'Evolutionary Programming'
            method_type = 'EvolutionaryProgram'

        if self.method == 'hooke_jeeves'.lower():
            method_name = 'Hooke &amp; Jeeves'
            method_type = 'HookeJeeves'

        if self.method == 'levenberg_marquardt'.lower():
            method_name = 'Levenberg - Marquardt'
            method_type = 'LevenbergMarquardt'

        if self.method == 'nelder_mead'.lower():
            method_name = 'Nelder - Mead'
            method_type = 'NelderMead'

        if self.method == 'particle_swarm'.lower():
            method_name = 'Particle Swarm'
            method_type = 'ParticleSwarm'

        if self.method == 'praxis'.lower():
            method_name = 'Praxis'
            method_type = 'Praxis'

        if self.method == 'random_search'.lower():
            method_name = 'Random Search'
            method_type = 'RandomSearch'

        if self.method == 'simulated_annealing'.lower():
            method_name = 'Simulated Annealing'
            method_type = 'SimulatedAnnealing'

        if self.method == 'steepest_descent'.lower():
            method_name = 'Steepest Descent'
            method_type = 'SteepestDescent'

        if self.method == 'truncated_newton'.lower():
            method_name = 'Truncated Newton'
            method_type = 'TruncatedNewton'

        if self.method == 'scatter_search'.lower():
            method_name = 'Scatter Search'
            method_type = 'ScatterSearch'

        if self.method == 'genetic_algorithm'.lower():
            method_name = 'Genetic Algorithm'
            method_type = 'GeneticAlgorithm'

        if self.method == 'genetic_algorithm_sr'.lower():
            method_name = 'Genetic Algorithm SR'
            method_type = 'GeneticAlgorithmSR'

        return method_name, method_type

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
        self.lower_bound = str(self.lower_bound)
        if isinstance(self.start_value, (float, int)):
            self.start_value = str(self.start_value)
        self.upper_bound = str(self.upper_bound)

    @property
    def _report_arguments(self):
        """
        collect report specific arguments in a dict
        :return: dict
        """
        # report specific arguments
        report_dict = {}
        report_dict['metabolites'] = self.metabolites
        report_dict['global_quantities'] = self.global_quantities
        report_dict['local_parameters'] = self.local_parameters
        report_dict['quantity_type'] = self.quantity_type
        report_dict['report_name'] = self.report_name
        report_dict['append'] = self.append
        report_dict['confirm_overwrite'] = self.confirm_overwrite
        report_dict['report_type'] = 'multi_parameter_estimation'
        return report_dict

    def _define_report(self):
        """
        create parameter estimation report
        for result collection
        :return: pycotools3.model.Model
        """
        return Reports(self.model, **self._report_arguments).model

    def _get_report_key(self):
        """
        After creating the report to collect
        results, this method gets the corresponding key
        There is probably a more efficient way to do this
        but this works...
        :return:
        """
        for i in self.model.xml.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'].lower() == 'multi_parameter_estimation':
                key = i.attrib['key']
        assert key != None
        return key

    @property
    def _fit_items(self):
        """
        Get existing fit items
        :return: dict
        """
        d = {}
        query = '//*[@name="FitItem"]'
        for i in self.model.xml.xpath(query):
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
                        d[match2] = j.attrib
        return d

    def _remove_fit_item(self, item):
        """
        Remove item from parameter estimation
        :param item:
        :return: pycotools3.model.Model
        """
        all_items = list(self._fit_items.keys())
        query = '//*[@name="FitItem"]'
        assert item in all_items, '{} is not a fit item. These are the fit items: {}'.format(item, all_items)
        item = self._fit_items[item]
        for i in self.model.xml.xpath(query):
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
        return self.model

    def _remove_all_fit_items(self):
        """
        Iterate over all fit items and remove them
        from the parameter estimation task
        :return: pycotools3.model.Model
        """
        for i in self._fit_items:
            self.model = self._remove_fit_item(i)
        return self.model

    def write_config_file(self):
        """
        write a parameter estimation config file to
        self.config_filename.
        :return: str. Path to config file
        """
        exp_kwargs = {}
        exp_kwargs['row_orientation'] = self.row_orientation
        exp_kwargs['experiment_type'] = self.experiment_type
        exp_kwargs['experiment_keys'] = self.experiment_keys
        exp_kwargs['first_row'] = self.first_row
        exp_kwargs['normalize_weights_per_experiment'] = self.normalize_weights_per_experiment
        exp_kwargs['row_containing_names'] = self.row_containing_names
        exp_kwargs['separator'] = self.separator
        exp_kwargs['weight_method'] = self.weight_method
        exp_kwargs['validation'] = self.validation
        exp_kwargs['validation_weight'] = self.validation_weight
        exp_kwargs['validation_threshold'] = self.validation_threshold
        exp_kwargs['mappings'] = self.mappings

        settings_dct = OrderedDict()
        settings_dct['randomize_start_values'] = self.randomize_start_values
        settings_dct['run_mode'] = self.run_mode
        settings_dct['method'] = self.method
        settings_dct['copy_number'] = self.copy_number
        settings_dct['pe_number'] = self.pe_number
        settings_dct['results_directory'] = self.results_directory
        settings_dct['quantity_type'] = self.quantity_type
        settings_dct['report_name'] = self.report_name
        settings_dct['update_model'] = self.update_model
        settings_dct['create_parameter_sets'] = self.create_parameter_sets
        settings_dct['calculate_statistics'] = self.calculate_statistics

        experiment_set_mapping_dct = OrderedDict()

        for i in range(len(self.experiment_files)):
            df = pandas.read_csv(self.experiment_files[i], sep=exp_kwargs['separator'][i])
            name = os.path.split(self.experiment_files[i])[1][:-4]
            experiment_set_mapping_dct[name] = OrderedDict()
            experiment_set_mapping_dct[name]['filename'] = self.experiment_files[i]
            experiment_set_mapping_dct[name]['key'] = 'Experiment_{}'.format(i)
            experiment_set_mapping_dct[name]['experiment_type'] = exp_kwargs['experiment_type'][i]
            experiment_set_mapping_dct[name]['first_row'] = int(exp_kwargs['first_row'][i])
            experiment_set_mapping_dct[name]['last_row'] = int(df.shape[0])
            experiment_set_mapping_dct[name]['normalize_weights_per_experiment'] = exp_kwargs['normalize_weights_per_experiment'][i]
            experiment_set_mapping_dct[name]['weight_method'] = exp_kwargs['weight_method'][i]
            experiment_set_mapping_dct[name]['row_containing_names'] = exp_kwargs['row_containing_names'][i]
            experiment_set_mapping_dct[name]['separator'] = exp_kwargs['separator'][i]
            experiment_set_mapping_dct[name]['validation'] = exp_kwargs['validation'][i]

            experiment_set_mapping_dct[name]['mappings'] = OrderedDict()
            for item in range(df.shape[1]):
                model_obj = df.columns[item]

                role = 'ignored'
                if df.columns[item][-6:] == '_indep':
                    role = 'independent'
                    model_obj = df.columns[item][:-6]
                elif df.columns[item] in self.model.all_variable_names:
                    role = 'dependent'
                elif df.columns[item].lower() == 'time':
                    role = 'time'
                elif role == 'ignored':
                    pass
                else:
                    raise ValueError('role cannot be "{}". Must be one of "ignored", "dependent", '
                                     '"independent" or "time"'.format(df.columns[item]))

                experiment_set_mapping_dct[name]['mappings'][df.columns[item]] = OrderedDict()
                experiment_set_mapping_dct[name]['mappings'][df.columns[item]]['model_object'] = model_obj
                experiment_set_mapping_dct[name]['mappings'][df.columns[item]]['role'] = role

        ## convert start_value to numeric to keep yaml file consistent
        item_template = self._item_template.transpose()
        item_template.loc['start_value'] = pandas.to_numeric(item_template.loc['start_value'])
        item_template = item_template.to_dict()

        dct = OrderedDict(
            ParameterEstimationSettings=settings_dct,
            ExperimentSetMapping=experiment_set_mapping_dct,
            OptimizationItemList=item_template,
            OptimizationConstraintList=OrderedDict()
        )
        yaml.add_representer(OrderedDict,
                             lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

        ## modify dumper class so that we do not write aliases for variables
        ## yaml have seen before.
        noalias_dumper = yaml.dumper.Dumper
        noalias_dumper.ignore_aliases = lambda self, data: True

        if (os.path.isfile(self.config_filename) == False) or (self.overwrite_config_file == True):
            with open(self.config_filename, 'w') as f:
                yaml.dump(dct, stream=f, default_flow_style=False)
        return self.config_filename

    def _read_config_file(self):
        """

        :return:
        """
        if os.path.isfile(self.config_filename) != True:
            raise errors.InputError(
                'ConfigFile does not exist. run \'write_config_file\' method and modify it how you like then run the setup()  method again.')
        if os.path.splitext(self.config_filename)[1] == '.csv':
            opt = pandas.read_csv(self.config_filename)
            setattr(self, 'optimization_item_list', opt)

            parameter_names = list(opt[opt.columns[0]])
            model_parameters = self.model.all_variable_names
            for parameter in parameter_names:
                if parameter not in model_parameters:
                    raise errors.InputError(
                        '{} not in {}\n\n Ensure you are using the correct PE config file!'.format(parameter,
                                                                                                   model_parameters))

        elif os.path.splitext(self.config_filename)[1] == '.yaml':
            with open(self.config_filename, 'r') as f:
                dct = yaml.load(f)
                mappings = OrderedDict()
                for k in dct:
                    if k == 'ParameterEstimationSettings':
                        for setting, value in dct[k].items():
                            setattr(self, setting, value)

                    elif k == 'ExperimentSetMapping':
                        experiment_mapping_args = dct[k]
                        experiment_files = []
                        experiment_type = []
                        experiment_keys = []
                        first_row = []
                        last_row = []
                        normalize_weights_per_experiment = []
                        weight_method = []
                        row_containing_names = []
                        separator = []
                        validation = []


                        for experiment_name in experiment_mapping_args:
                            # print(experiment_name, experiment_mapping_args[experiment_name])
                            experiment_files.append(experiment_mapping_args[experiment_name]['filename'])
                            experiment_type.append(experiment_mapping_args[experiment_name]['experiment_type'])
                            experiment_keys.append(experiment_mapping_args[experiment_name]['key'])
                            first_row.append(experiment_mapping_args[experiment_name]['first_row'])
                            last_row.append(experiment_mapping_args[experiment_name]['last_row'])
                            normalize_weights_per_experiment.append(
                                experiment_mapping_args[experiment_name]['normalize_weights_per_experiment'])
                            weight_method.append(experiment_mapping_args[experiment_name]['weight_method'])
                            row_containing_names.append(
                                experiment_mapping_args[experiment_name]['row_containing_names'])
                            separator.append(experiment_mapping_args[experiment_name]['separator'])
                            validation.append(experiment_mapping_args[experiment_name]['validation'])
                            mappings[experiment_name] = experiment_mapping_args[experiment_name]['mappings']

                        ## convert weight method to numerical values that are
                        ## interpreted by COAPSI - with some input checking
                        weight_method_strings = ['mean_squared', 'stardard_deviation',
                                                'value_scaling', 'mean']  # line 2144
                        for i in weight_method:
                            if i not in weight_method_strings:
                                raise errors.InputError(
                                    '"{}" is not a valid weight method. Please choose '
                                    'on of "{}"'.format(i, weight_method_strings)
                                )

                        weight_method_numbers = [str(i) for i in [1, 2, 3, 4]]
                        weight_method_dict = dict(list(zip(weight_method_strings, weight_method_numbers)))
                        weight_method = [weight_method_dict[i] for i in weight_method]

                        ## convert experiment type to numerical values that are
                        ## interpreted by COAPSI - with some input checking
                        experiment_type_strings = ['steadystate', 'timecourse']

                        for i in experiment_type:
                            if i not in experiment_type_strings:
                                raise errors.InputError(
                                    '"{}" is not a valid experiment type. Please choose '
                                    'on of "{}"'.format(i, experiment_type_strings)
                                )

                        experiment_type_numbers = [str(i) for i in [0, 1]]
                        experiment_type_dict = dict(list(zip(experiment_type_strings, experiment_type_numbers)))
                        experiment_type = [experiment_type_dict[i] for i in experiment_type]


                        setattr(self, 'experiment_type', experiment_type)
                        setattr(self, 'experiment_keys', experiment_keys)
                        setattr(self, 'first_row', first_row)
                        setattr(self, 'last_row', last_row)
                        setattr(self, 'normalize_weights_per_experiment', normalize_weights_per_experiment)
                        setattr(self, 'weight_method', weight_method)
                        setattr(self, 'row_containing_names', row_containing_names)
                        setattr(self, 'separator', separator)
                        setattr(self, 'validation', validation)
                        setattr(self, 'mappings', mappings)


                    elif k == 'OptimizationItemList':
                        opt = pandas.DataFrame(dct[k]).transpose()
                        setattr(self, 'optimization_item_list', opt)

                    elif k == 'OptimizationConstraintList':
                        constr = pandas.DataFrame(dct[k]).transpose()
                        setattr(self, 'optimization_constraint_list', constr)

                        print('Warning: OptimizationConstraintList is not yet implemented. Entried are being'
                              ' ignored. ')

        else:
            raise ValueError('Config filename is not of a supported file type. Please ensure the config file '
                             'was generated with write config file')

    def _get_experiment_keys(self):
        """
        Experiment keys are always 'Experiment_i' where 'i' indexes
        the experiment in the order they are given in the experiment
        list. This method extracts the _experiments that are not for validation
        :return:
        """
        dct = OrderedDict()
        for i in range(len(self.experiment_files)):
            if not self.validation[i]:
                key = "Experiment_{}".format(i)
                name = os.path.split(self.experiment_files[i])[1][:-4]
                dct[name] = key
        return dct

    def _get_validation_keys(self):
        """
        Experiment keys are always 'Experiment_i' where 'i' indexes
        the experiment in the order they are given in the experiment
        list. This method extracts the _experiments that are for validation

        :return:
        """
        dct = OrderedDict()
        for i in range(len(self.experiment_files)):
            if self.validation[i]:
                key = "Experiment_{}".format(i)
                name = os.path.split(self.experiment_files[i])[1][:-4]
                dct[name] = key
        return dct

    @property
    def _item_template(self):
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
                metab.drop('particle_numbers', axis=1, inplace=True)
                metab = metab.rename(columns={'concentration': 'start_value'})

            elif self.quantity_type == 'particle_numbers':
                metab.drop('concentration', axis=1, inplace=True)
                metab = metab.rename(columns={'particle_numbers': 'start_value'})
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
        df = df.set_index('name')
        if isinstance(self.lower_bound, (float, int)):
            df['lower_bound'] = [self.lower_bound] * df.shape[0]
        else:
            raise ValueError

        for i in [self.lower_bound_dct, self.upper_bound_dct]:
            if not isinstance(i, dict):
                raise errors.InputError('{} argument must be a '
                                    'dict mapping parameter estimation boundaries '
                                    'to integers. Got "{}"'.format(i, type(self.lower_bound_dct)))

        for k, v in self.lower_bound_dct.items():
            if k not in df.index:
                raise IndexError('The key "{0}" is not available. These are available: "{1}. Check for typo\'s '
                                 'and check that you have included "{0}" in your '
                                 'estimation by adding it as argument to "metabolites" '
                                 '"local_parameters" or "global_quantities" argument'.format(k, df.index))
            df.loc[k, 'lower_bound'] = v


        if isinstance(self.upper_bound, (float, int)):
            df['upper_bound'] = [self.upper_bound] * df.shape[0]
        else:
            raise ValueError

        for k, v in self.upper_bound_dct.items():
            if k not in df.index:
                raise IndexError('The key "{0}" is not available. These are available: "{1}. Check for typo\'s '
                                 'and check that you have included "{0}" in your '
                                 'estimation by adding it as argument to "metabolites" '
                                 '"local_parameters" or "global_quantities" argument'.format(k, df.index))
            df.loc[k, 'upper_bound'] = v

        if isinstance(self.affected_experiments, str):
            df['affected_experiments'] = ['all'] * df.shape[0]
        elif isinstance(self.affected_experiments, dict):
            df['affected_experiments'] = ['all'] * df.shape[0]
            for k, v in self.affected_experiments.items():
                if k not in df.index:
                    raise IndexError('The key "{0}" is not available. These are available: "{1}. Check for typo\'s '
                                     'and check that you have included "{0}" in your '
                                     'estimation by adding it as argument to "metabolites" '
                                     '"local_parameters" or "global_quantities" argument'.format(k, df.index))
                df.at[k, 'affected_experiments'] = v
        else:
            raise errors.InputError('affected_experiments argument must be "all" '
                                    'or dict mapping estimated parameters '
                                    'to a list of experiment names')

        if isinstance(self.affected_validation_experiments, str):
            df['affected_validation_experiments'] = ['all'] * df.shape[0]
        elif isinstance(self.affected_validation_experiments, dict):
            df['affected_validation_experiments'] = ['all'] * df.shape[0]
            for k, v in self.affected_validation_experiments.items():
                if k not in df.index:
                    raise IndexError('The key "{0}" is not available. These are available: "{1}. Check for typo\'s '
                                     'and check that you have included "{0}" in your '
                                     'estimation by adding it as argument to "metabolites" '
                                     '"local_parameters" or "global_quantities" argument'.format(k, df.index))
                df.at[k, 'affected_validation_experiments'] = v
        else:
            raise errors.InputError('"affected_validation_experiments" argument must be "all" '
                                    'or dict mapping estimated parameters '
                                    'to a list of experiment names')


        if isinstance(self.start_value, pandas.core.frame.DataFrame):
            if len(self.start_value.columns) != 1:
                raise errors.InputError('start values should have only one column. Got \n\n{}'.format(self.start_value))
            self.start_value.columns = ['start_value']
            for i in list(self.start_value.index):
                if i != 'RSS':
                    if i not in self.model.all_variable_names:
                        raise errors.InputError('"{}" not in model. '
                                                'These are in your model "{}"'.format(i, self.model.all_variable_names))

                    df.loc[i]['start_value'] = float(self.start_value.loc[i])

        return df

    def _add_fit_item(self, item, constraint=False):
        """
        Add fit item to model
        :param item: a row from the config template as pandas series
        :return: pycotools3.model.Model
        """
        ## figure out what type of variable item is and assign to component
        if item.name in [i.name for i in self.metabolites]:
            component = [i for i in self.metabolites if i.name == item.name][0]

        elif item.name in [i.global_name for i in self.local_parameters]:
            component = [i for i in self.local_parameters if i.global_name == item.name][0]

        elif item.name in [i.name for i in self.global_quantities]:
            component = [i for i in self.global_quantities if i.name == item.name][0]
        else:
            raise errors.SomethingWentHorriblyWrongError(
                '"{}" is not a metabolite,'
                ' local_parameter or '
                'global_quantity. These are your'
                ' model variables: {}'.format(
                    item.name,
                    str(self.model.all_variable_names))
            )

        # initialize new element
        fit_item_element = etree.Element('ParameterGroup', attrib={'name': 'FitItem'})


        affected_experiments = {'name': 'Affected Experiments'}
        ## read affected _experiments from config file.yaml
        affected_experiments_attr = OrderedDict()
        ## when affected _experiments is 'all', the affected experiment element is empty
        if item['affected_experiments'] != 'all':
            ## convert a string to a list of 1 so we can cater for the case
            ## where we have a list of strings with the same code
            if isinstance(item['affected_experiments'], str):
                item['affected_experiments'] = [item['affected_experiments']]

            ## iterate over list. Raise ValueError is can't find experiment name
            ## otherwise add the corresponding experiment key to the affected _experiments attr dict
            for affected_experiment in item['affected_experiments']:  ## iterate over the list
                if affected_experiment in self._get_validation_keys():
                    raise ValueError('"{}" has been given as a validation experiment and therefore '
                                     'I cannot add this experiment to the list of _experiments that '
                                     'affect the {} parameter'.format(
                        affected_experiment, component.name
                    ))

                if affected_experiment not in self._get_experiment_keys():
                    raise ValueError('"{}" is not one of your _experiments. These are '
                                     'your valid experimments: "{}"'.format(
                        affected_experiment, self._get_experiment_keys().keys()
                    ))

                affected_experiments_attr[affected_experiment] = {}
                affected_experiments_attr[affected_experiment]['name'] = 'Experiment Key'
                affected_experiments_attr[affected_experiment]['type'] = 'key'
                affected_experiments_attr[affected_experiment]['value'] = self._get_experiment_keys()[
                    affected_experiment]

        ## add affected _experiments to element
        affected_experiments_element = etree.SubElement(fit_item_element, 'ParameterGroup', attrib=affected_experiments)

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

            ## iterate over list. Raise ValueError is can't find experiment name
            ## otherwise add the corresponding experiment key to the affected _experiments attr dict
            for affected_validation_experiment in item['affected_validation_experiments']:  ## iterate over the list
                if affected_validation_experiment in self._get_experiment_keys():
                    raise ValueError('"{}" has been given as an experiment and therefore '
                                     'I cannot add this experiment to the list of validation _experiments that '
                                     'affect the {} parameter'.format(
                        affected_validation_experiment, component.name
                    ))

                if affected_validation_experiment not in self._get_validation_keys():
                    raise ValueError('"{}" is not one of your _experiments. These are '
                                     'your valid experimments: "{}"'.format(
                        affected_validation_experiment, self._get_validation_keys().keys()
                    ))

                affected_validation_experiments_attr[affected_validation_experiment] = {}
                affected_validation_experiments_attr[affected_validation_experiment]['name'] = 'Experiment Key'
                affected_validation_experiments_attr[affected_validation_experiment]['type'] = 'key'
                affected_validation_experiments_attr[affected_validation_experiment]['value'] = self._get_validation_keys()[
                    affected_validation_experiment]

        affected_cross_validation_experiments = {'name': 'Affected Cross Validation Experiments'}

        affected_cross_validation_experiments_element = etree.SubElement(fit_item_element, 'ParameterGroup', attrib=affected_cross_validation_experiments)

        ## now add the attributes to the affected _experiments element
        for affected_validation_experiment_attr in affected_validation_experiments_attr:
            etree.SubElement(
                affected_cross_validation_experiments_element, 'Parameter',
                attrib=affected_validation_experiments_attr[affected_validation_experiment_attr]
            )

        ## get lower bound from config file and add to element
        lower_bound_element = {'type': 'cn', 'name': 'LowerBound', 'value': str(item['lower_bound'])}
        etree.SubElement(fit_item_element, 'Parameter', attrib=lower_bound_element)

        if self.use_config_start_values == True:
            start_value_element = {'type': 'float', 'name': 'StartValue', 'value': str(item['start_value'])}

        ## get upper bound from config file and add to element
        upper_bound_element = {'type': 'cn', 'name': 'UpperBound', 'value': str(item['upper_bound'])}
        etree.SubElement(fit_item_element, 'Parameter', attrib=upper_bound_element)

        if self.use_config_start_values == True:
            etree.SubElement(fit_item_element, 'Parameter', attrib=start_value_element)

        ## Now begin creating the object map.
        # for IC parameters
        if isinstance(component, model.Metabolite):
            if self.quantity_type == 'concentration':
                subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{},{}'.format(self.model.reference,
                                                                                      component.compartment.reference,
                                                                                      component.initial_reference)}
            else:
                subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{},{}'.format(
                    self.model.reference,
                    component.compartment.reference,
                    component.initial_particle_reference
                )}

        elif isinstance(component, model.LocalParameter):
            subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{},{}'.format(
                self.model.reference,
                self.model.get('reaction', component.reaction_name, by='name').reference,
                component.value_reference)}

        elif isinstance(component, model.GlobalQuantity):
            subA4 = {'type': 'cn', 'name': 'ObjectCN', 'value': '{},{}'.format(self.model.reference,
                                                                               component.initial_reference)}

        elif isinstance(component, model.Compartment):
            subA4 = {'type': 'cn',
                     'name': 'ObjectCN',
                     'value': '{},{}'.format(self.model.reference,
                                             component.initial_value_reference)}

        else:
            raise errors.InputError('{} is not a valid parameter for estimation'.format(list(item)))

        ## add element
        etree.SubElement(fit_item_element, 'Parameter', attrib=subA4)

        ##insert fit item

        list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        parameter_est = self.model.xml.find(list_of_tasks)[5]
        problem = parameter_est[1]
        assert problem.tag == '{http://www.copasi.org/static/schema}Problem'

        if constraint:
            item_list = problem[4]
            assert list(item_list.attrib.values())[0] == 'OptimizationConstraintList'
        else:
            item_list = problem[3]
            assert list(item_list.attrib.values())[0] == 'OptimizationItemList'
        item_list.append(fit_item_element)
        return self.model

    def _insert_all_fit_items(self):
        """
        insert all fit items defined in config file
        into the model
        :return:
        """

        ## for optimization items
        for row in range(self.optimization_item_list.shape[0]):
            assert row != 'nan'
            ## feed each item from the config file into _add_fit_item
            self.model = self._add_fit_item(self.optimization_item_list.iloc[row])

        ## for constraints
        for row in range(self.optimization_constraint_list.shape[0]):
            assert row != 'nan'
            self.model = self._add_fit_item(self.optimization_constraint_list.iloc[row], constraint=True)
        return self.model

    def _set_PE_method(self):
        '''
        Choose PE algorithm and set algorithm specific parameters
        '''
        # Build xml for method.
        method_name, method_type = self._select_method()
        method_params = {'name': method_name, 'type': method_type}
        method_element = etree.Element('Method', attrib=method_params)

        # list of attribute dictionaries
        # Evolutionary strategy parametery
        number_of_generations = {'type': 'unsignedInteger', 'name': 'Number of Generations',
                                 'value': self.number_of_generations}
        population_size = {'type': 'unsignedInteger', 'name': 'Population Size', 'value': self.population_size}
        random_number_generator = {'type': 'unsignedInteger', 'name': 'Random Number Generator',
                                   'value': self.random_number_generator}
        seed = {'type': 'unsignedInteger', 'name': 'Seed', 'value': self.seed}
        pf = {'type': 'float', 'name': 'Pf', 'value': self.pf}
        # local method parameters
        iteration_limit = {'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.iteration_limit}
        tolerance = {'type': 'float', 'name': 'Tolerance', 'value': self.tolerance}
        rho = {'type': 'float', 'name': 'Rho', 'value': self.rho}
        scale = {'type': 'unsignedFloat', 'name': 'Scale', 'value': self.scale}
        # Particle Swarm parmeters
        swarm_size = {'type': 'unsignedInteger', 'name': 'Swarm Size', 'value': self.swarm_size}
        std_deviation = {'type': 'unsignedFloat', 'name': 'Std. Deviation', 'value': self.std_deviation}
        # Random Search parameters
        number_of_iterations = {'type': 'unsignedInteger', 'name': 'Number of Iterations',
                                'value': self.number_of_iterations}
        # Simulated Annealing parameters
        start_temperature = {'type': 'unsignedFloat', 'name': 'Start Temperature', 'value': self.start_temperature}
        cooling_factor = {'type': 'unsignedFloat', 'name': 'Cooling Factor', 'value': self.cooling_factor}

        # build the appropiate xML, with method at root (for now)
        if self.method == 'current_solution_statistics':
            pass  # no additional parameter elements required

        if self.method == 'differential_evolution'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'evolutionary_strategy_sr'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
            etree.SubElement(method_element, 'Parameter', attrib=pf)

        if self.method == 'evolutionary_program'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'hooke_jeeves'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=rho)

        if self.method == 'levenberg_marquardt'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
        #
        if self.method == 'nelder_mead'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=scale)

        if self.method == 'particle_swarm'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=swarm_size)
            etree.SubElement(method_element, 'Parameter', attrib=std_deviation)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'praxis'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)

        if self.method == 'random_search'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_iterations)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'simulated_annealing'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=start_temperature)
            etree.SubElement(method_element, 'Parameter', attrib=cooling_factor)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
        #
        if self.method == 'steepest_descent'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
        #
        if self.method == 'truncated_newton'.lower():
            # required no additonal paraemters
            pass
        #
        if self.method == 'scatter_search'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_iterations)

        if self.method == 'genetic_algorithm'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'genetic_algorithm_sr'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
            etree.SubElement(method_element, 'Parameter', attrib=pf)

        tasks = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')

        method = tasks[5][-1]
        parent = method.getparent()
        parent.remove(method)
        parent.insert(2, method_element)
        return self.model

    def _set_PE_options(self):
        """
        Set parameter estimation sepcific arguments
        :return: pycotools3.model.Model
        """

        scheluled_attrib = {'scheduled': self.scheduled,
                            'updateModel': self.update_model}

        report_attrib = {'append': self.append,
                         'reference': self._get_report_key(),
                         'target': self.report_name,
                         'confirmOverwrite': self.confirm_overwrite}

        randomize_start_values = {'type': 'bool',
                                  'name': 'Randomize Start Values',
                                  'value': self.randomize_start_values}

        calculate_stats = {'type': 'bool', 'name': 'Calculate Statistics', 'value': self.calculate_statistics}
        create_parameter_sets = {'type': 'bool', 'name': 'Create Parameter Sets', 'value': self.create_parameter_sets}

        query = '//*[@name="Parameter Estimation"]' and '//*[@type="parameterFitting"]'
        for i in self.model.xml.xpath(query):
            i.attrib.update(scheluled_attrib)
            for j in list(i):
                if self.report_name != None:
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
        return self.model

    def _create_output_directory(self):
        """
        Create directory for estimation results
        :return:
        """
        if os.path.isdir(self.results_directory) != True:
            os.mkdir(self.results_directory)

    def _enumerate_PE_output(self):
        """
        Create a filename for each file to collect PE results
        :return: dict['model_copy_number]=enumerated_report_name
        """

        dct = {}
        for i in range(self.copy_number):
            new_file = os.path.join(
                self.results_directory, '{}_{}.txt'.format(self.report_name, i)
            )

            dct[i] = new_file
        return dct

    def _copy_model(self):
        """
        Copy the model n times
        Uses deep copy to ensure separate models
        :return: dict[index] = model copy
        """
        dct = {}
        dct[0] = deepcopy(self.model)
        for i in range(1, self.copy_number):
            dire, fle = os.path.split(self.model.copasi_file)
            new_cps = os.path.join(dire, fle[:-4] + '_{}.cps'.format(i))
            model = deepcopy(self.model)
            model.copasi_file = new_cps
            model.save()
            dct[i] = model
        return dct

    def _setup1scan(self, q, model, report):
        """
        Setup a single scan.
        :param q: queue from multiprocessing
        :param model: pycotools3.model.Model
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
                            output_in_subtask=False,
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
        q = queue.Queue(maxsize=number_of_cpu)
        report_files = self._enumerate_PE_output()
        res = {}
        for copy_number, model in list(models.items()):
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

        if self.run_mode == 'sge':
            try:
                check_call('qhost')
            except errors.NotImplementedError:
                LOG.warning(
                    'Attempting to run in SGE mode but SGE specific commands are unavailable. Switching to \'parallel\' mode')
                self.run_mode = 'parallel'
        if self.run_mode == 'parallel':
            RunParallel(list(self.models.values()), mode=self.run_mode, max_active=self.max_active,
                        task='scan')
        elif self.run_mode:
            for copy_number, model in list(self.models.items()):
                LOG.info('running model: {}'.format(copy_number))
                Run(model, mode=self.run_mode, task='scan')
        elif not self.run_mode:
            pass

        else:
            raise ValueError('"{}" is not a valid argument'.format(self.run_mode))

    def setup(self):
        """
        :return:
        """
        ## read config file
        self._read_config_file()

        ## make appropriate changes to arguments to make them compatible
        ## with the copasi xml
        self.convert_bool_to_numeric2()
        # self.default_properties = self.convert_bool_to_numeric(self.default_properties)
        self._convert_numeric_arguments_to_string()
        # Try moving the above two lines to the constructor
        ## create output directory
        self._create_output_directory()

        ## create a report for PE results collection
        self.model = self._define_report()

        ## map _experiments
        # EM = ExperimentMapper(self.model, self.experiment_files, **self._experiment_mapping_args)

        ## get model from ExperimentMapper
        self.model = self._map_experiments()

        ## get rid of existing parameter estimation definition
        self.model = self._remove_all_fit_items()

        # self.convert_bool_to_numeric()

        ## create new parameter estimation
        self.model = self._set_PE_method()
        self.model = self._set_PE_options()
        self.model = self._insert_all_fit_items()

        ## ensure we have model
        assert self.model != None
        assert isinstance(self.model, model.Model)

        ##copy the number `copy_number` times
        models = self._copy_model()

        ## ensure we have dict of models
        assert isinstance(models, dict)
        assert len(models) == self.copy_number

        ##create a scan per model (again models is dict of model.Model's
        self.models = self._setup_scan(models)
        assert isinstance(models[0], model.Model)
        return models


class ChaserParameterEstimations(_Task):
    """
    Perform secondary hook and jeeves parameter estimations
    starting from the best values of a primary global estimator.

    #todo: This class performs slowly in serial. Parallelize the configuration
    of the parameter estimation class in each model.
    """

    def __init__(self, cls=None, model=None, parameter_path=None, truncate_mode='percent',
                 experiment_files=None, theta=100, iteration_limit=100,
                 tolerance=1e-6, results_directory=None,
                 run_mode=False, max_active=2, **kwargs):
        """

        :param cls:
            A :class:`MultiParameterEstimation` object. If present
            then model, experiment_files and parameter path args are not
            required.
        :param model:
            Used when :class:`MultiParameterEstimation` is None. A
            :class:`model.Model` object that was used to
            run the primary global estimations. If using model arg,
            parameter_path and experiment_files must also be specified.
        :param parameter_path:
            Used when :class:`MultiParameterEstimation` is None. This
            argument is passed on :class:`viz.Parse` to read parameter estimation
            data from the folder containing parameter estimation data. Used with
            model and experiment_files arguments.
        :param experiment_files:
            Used when :class:`MultiParameterEstimation` is None. This argument is
            passed along to :class:`ParameterEstimation` and should be path or list
            of paths to experimental data to be used in the parameter estimation.
        :param truncate_mode:
            Either 'percent', 'below_x' or 'ranks'. Default: 'percent'. Determines
            how to truncate the parameter estimation data. Used in conjunction with
            the theta argument.
        :param theta:
            When truncate_mode is 'percent', a number between 0 and 100, the percentage of
            best parameter sets to chase.
            When truncate_mode is 'below_x': a number representing a RSS value cut off. All
            parameter sets with a RSS lower than theta are chased.
            When truncate_mode is 'ranks', a list of numbers containing the ranks of best fitting
            parameter sets to include. For example range(10) would chase the top 10.
        :param iteration_limit:
            The Hook and Jeeves iteration limit parameter
        :param tolerance:
            The Hook and Jeeves tolerance parameter
        :param results_directory:
            The name of the directory for the results. If not exists, create it. Defaults to
            ChaserEstimations in the same directory as the model (or cls.model)
        :param run_mode:
            Passed on to :class:`Run`.
        :param max_active:
            Passed on to :class:`Run`.
        :param kwargs:
            Any other keyword argument to be passed on
            to :class:`ParameterEstimation`
        """

        ## Define class variables
        self.model = model
        self.experiment_files = experiment_files
        self.truncate_mode = truncate_mode
        self.theta = theta
        self.cls = cls
        self.parameter_path = parameter_path
        self.iteration_limit = iteration_limit
        self.tolerance = tolerance
        self.results_directory = results_directory
        self.run_mode = run_mode
        self.max_active = max_active
        self.kwargs = kwargs

        ## verify integrity of user input
        self.do_checks()

        ## converge the two routes of user input
        self._assign_model_and_pe_data_arguments_from_cls()

        if self.results_directory is None:
            self.results_directory = os.path.join(
                os.path.dirname(self.model.copasi_file),
                'ChaserEstimations'
            )

        if not os.path.isdir(self.results_directory):
            os.makedirs(self.results_directory)

        ## Parse the parameter estimation data
        self.data = self.parse_pe_data()
        # ##truncate the data to only parameter sets to improve
        self.data = viz.TruncateData(self.data,
                                     mode=self.truncate_mode,
                                     theta=self.theta).data
        self.pe_dct = self.configure()

        self.setup()

        self.run()

    def do_checks(self):
        """

        :return:
        """

        if self.model is None and self.cls is None and self.parameter_path is None:
            raise errors.InputError('Please give argument to either "cls" which '
                                    'should be an instance of MultiParameterEstimation '
                                    'or arguments to both "model" and "parameter_path" which are'
                                    'the model and data you want to use in the chaser estimations')

        if (self.model is not None) and (self.parameter_path is None):
            raise errors.InputError('If you have given argument to '
                                    '"model" argument you need to also'
                                    ' give an argument to "parameter_path" and "experiment_files"')

        if self.parameter_path is not None and self.model is None:
            raise errors.InputError('If you have given argument to '
                                    '"parameter_path" argument you need to also'
                                    ' give an argument to "model" and "experiment_files"')

        if self.model is not None and self.experiment_files is None:
            raise errors.InputError('If using the "model" argument '
                                    'please give argument to "experiment_files"')

        if self.cls is not None:
            if type(self.cls) != MultiParameterEstimation:
                raise errors.InputError('"cls" argument should '
                                        'be an instance of MultiParameterEstimation. '
                                        'got "{}" instead'.format(type(self.cls)))

    def _assign_model_and_pe_data_arguments_from_cls(self):
        """
        if argument to cls is not none, assign the model and pe_data
        from cls (which is of type MultiParameterEstimation)
        :return:
        """
        if self.cls is not None:
            self.model = self.cls.model
            self.parameter_path = self.cls.results_directory
            self.experiment_files = self.cls.experiment_files

    def parse_pe_data(self):
        """

        :return:
        """
        ## if pe_data is string it shuold be path to folder of pe_data
        if type(self.parameter_path) == str:

            ## A save is required to update the model on file
            ## with the parameter estimation configuration in self.model
            self.model.save()
            data = viz.Parse(self.parameter_path, copasi_file=self.model.copasi_file).data
        ## can also already be a dataframe
        elif type(self.parameter_path) == pandas.core.frame.DataFrame:
            data = viz.Parse(self.parameter_path).data

        return data

    # def configure(self):
    #     """
    #     Iterate over parameter sets.
    #     :return:
    #     """
    #     q = multiprocessing.Queue()
    #     # cps_dct = {}
    #     original_cps_filename = self.model.copasi_file
    #     ## Iterate over parameter sets
    #     jobs = []
    #     for i in range(self.data.shape[0]):
    #
    #         ## Create new cps name
    #         new_cps = original_cps_filename[:-4]+'_'+str(i)+'.cps'
    #
    #         filename = os.path.join(self.results_directory, "PE_data_{}.txt".format(i))
    #         # cps_dct[new_cps] = filename
    #         ## save model to new name and do d
    #
    #         mod = deepcopy(self.model.save(new_cps))
    #         p = multiprocessing.Process(target=self.configure1, args=(mod, filename, self.data, i))
    #         p.start()
    #         p.join()
    #
    #     # for proc in jobs:
    #     #     proc.join()
    #
    #
    #     # return cps_dct
    #
    # def configure1(self, mod, filename, data, index):
    #     """
    #     function to parallelize
    #     :return:
    #     """
    #     # LOG.debug('data --> {}'.format(self.data))
    #
    #     mod.insert_parameters(df=data, index=index, inplace=True)
    #     PE = ParameterEstimation(mod, self.experiment_files,
    #                              report_name=filename,
    #                              method='hooke_jeeves',
    #                              tolerance=self.tolerance,
    #                              randomize_start_values=False,
    #                              iteration_limit=self.iteration_limit,
    #                              run_mode=False,
    #                              **self.kwargs)
    #     PE.setup()
    #     self.pe_dct[mod.copasi_file] = PE
    #
    #     return PE

    def configure(self):
        """
        Iterate over parameter sets.
        :return:
        """
        pe_dct = OrderedDict()
        original_cps_filename = self.model.copasi_file
        ## Iterate over parameter sets
        for i in range(self.data.shape[0]):
            ## Create new cps name
            new_cps = original_cps_filename[:-4] + '_' + str(i) + '.cps'

            filename = os.path.join(self.results_directory, "PE_data_{}.txt".format(i))

            ## save model to new name and do d
            mod = deepcopy(self.model.save(new_cps))

            mod.insert_parameters(df=self.data, index=i, inplace=True)
            PE = MultiParameterEstimation(
                mod, self.experiment_files,
                report_name=filename,
                method='hooke_jeeves',
                tolerance=self.tolerance,
                randomize_start_values=False,
                ieration_limit=self.iteration_limit,
                run_mode=False,
                copy_number=1,
                pe_number=1,
                **self.kwargs
            )
            PE.setup()
            pe_dct[new_cps] = PE

        return pe_dct

    def setup(self):
        """

        :return:
        """
        for pe in self.pe_dct:
            self.pe_dct[pe].setup()
            self.pe_dct[pe].model.save()

    def run(self):
        """

        :return:
        """
        mod_dct = OrderedDict()
        for cps, pe in list(self.pe_dct.items()):
            mod_dct[cps] = self.pe_dct[cps].model

        if self.run_mode is False:
            return mod_dct

        elif self.run_mode is 'parallel':
            LOG.info('running "{}" in parallel'.format(cps))
            RunParallel(list(mod_dct.values()), max_active=self.max_active,
                        task='parameter_estimation')

        else:
            for cps, mod in list(mod_dct.items()):
                LOG.info('running "{}"'.format(cps))
                Run(mod, task='parameter_estimation', mode=self.run_mode)


@mixin(model.ReadModelMixin)
class MultiModelFit(_Task):
    """
    Coordinate a systematic multi model fitting parameter estimation and
    compare results using :py:class:`viz.ModelSelection`

    Usage:
        # Setup a new folder containing all models that you would like to fit
          and all data you would like to fit to the model.
          Do not have any other text or csv files in this folder as python will try and setup
          fits for them.

                i.e.:
                    ./project_dir
                        --Exp_data_1.csv
                        --Exp_data_n.csv
                        --model1.cps
                        --model2.cps

        # Instantiate instance of the MultimodelFit class with all relevant
          keywords. Python automatically creates subdirectories  for each model in your
          model selection problem and maps all data files in the main directory
          to each of the models.
        # Use the write_config_file() method to create a spreadsheet containing
          a config file per model. See :py:meth:`ParameterEstimation.write_config_file`.
        # use run() method to run all models simultaneously.

    .. _multi_model_fit_kwargs:

    MultiModelFit Kwargs
    ====================


    """

    def __init__(self, project_dir, **kwargs):
        """

        :param project_dir:
            The directory to your model selection directory

        :param kwargs:
                All kwargs that are accepted in :ref:`parameter_estimation_kwargs` and
                :ref:`mutli_parameter_estimation_kwargs` are accepted here.
        """
        self.project_dir = project_dir
        #        self.config_filename=config_filename
        self.kwargs = kwargs

        ## This needs to be before setting default properties
        ## so we have access to exp_files and cps_files for lengths
        self.cps_files, self.exp_files = self.read_fit_config()

        self._do_checks()

        self.sub_cps_dirs = self.create_workspace()
        self.MPE_dct = self.instantiate_parameter_estimation_classes()
        self.results_folder_dct = self.get_output_directories()

    def _do_checks(self):
        pass

    def __iter__(self):
        for MPE in list(self.MPE_dct.values()):
            yield MPE

    def __getitem__(self, item):
        return self.MPE_dct[item]

    def __setitem__(self, key, value):
        self.MPE_dct[key] = value

    def __delitem__(self, key):
        del self.MPE_dct[key]

    def keys(self):
        return list(self.MPE_dct.keys())

    def values(self):
        return list(self.MPE_dct.values())

    def items(self):
        return list(self.MPE_dct.items())

    def instantiate_parameter_estimation_classes(self):
        """
        pass correct arguments to the runMultiplePEs class in order
        to instantiate a runMultiplePEs instance for each model.

        :Returns: dict[model_filename]=runMultiplePEs_instance
        """
        dct = {}

        for cps_dir in self.sub_cps_dirs:
            os.chdir(cps_dir)

            # if os.path.isabs(self.config_filename):
            #     self.config_filename = os.path.split(self.config_filename)[1]

            m = model.Model(self.sub_cps_dirs[cps_dir])

            dct[self.sub_cps_dirs[cps_dir]] = ParameterEstimation(
                self.sub_cps_dirs[cps_dir], self.exp_files,
                **self.kwargs
            )

        return dct

    def get_output_directories(self):
        """
        :returns:Dict. Location of parameter estimation output files
        """
        output_dct = {}
        for MPE in self.MPE_dct:
            output_dct[MPE] = self.MPE_dct[MPE].results_directory
        return output_dct

    # void
    def write_config_file(self):
        """
        A class to write a config file template for each
        model in the analysis. Calls the corresponding
        write_config_file from the runMultiplePEs class
        :returns: list. config file paths
        """
        conf_list = []
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
        if os.path.isdir(self.wd) != True:
            os.mkdir(self.wd)
        os.chdir(self.project_dir)
        cps_dirs = {}
        for cps in self.cps_files:
            cps_abs = os.path.abspath(cps)
            cps_filename = os.path.split(cps_abs)[1]
            sub_cps_dir = os.path.join(self.wd, cps_filename[:-4])
            if os.path.isdir(sub_cps_dir) != True:
                os.mkdir(sub_cps_dir)
            sub_cps_abs = os.path.join(sub_cps_dir, cps_filename)
            shutil.copy(cps_abs, sub_cps_abs)
            if os.path.isfile(sub_cps_abs) != True:
                raise Exception('Error in copying copasi file to sub directories')
            cps_dirs[sub_cps_dir] = sub_cps_abs
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
        if self.project_dir == None:
            raise errors.InputError('Cannot read multifit confuration as no Project kwarg is provided')
        ##make sure we're in the right directory
        os.chdir(self.project_dir)
        LOG.info('project dir is --> {}'.format(self.project_dir))
        cps_list = []
        for cps_file in glob.glob('*.cps'):
            cps_list.append(cps_file)

        exp_list = []
        exp_file_types = ('*.csv', '*.txt')
        for typ in exp_file_types:

            for exp_file in glob.glob(typ):
                exp_list.append(os.path.abspath(exp_file))

        if cps_list == []:
            raise errors.InputError('No cps files in your project')

        if exp_list == []:
            raise errors.InputError('No experiment files in your project')
        return cps_list, exp_list

    def format_data(self):
        """
        Method for giving appropiate headers to parameter estimation data
        """
        for MPE in self.MPE_dct:
            self.MPE_dct[MPE].format_results()

    # def insert_best_parameters(self):
    #     """
    #     Insert Best parameters for each model into the model
    #     :return:
    #     """
    #     for MPE in self.MPE_dct:
    #         MPE.model.insert_parameters()


@mixin(model.GetModelComponentFromStringMixin)
@mixin(model.ReadModelMixin)
class ProfileLikelihood(_Task):
    """


    .. _profile_likelihood_kwargs:

    ProfileLikelihood Kwargs
    ========================

    ===========================     ==================================================
    ProfileLikelihood  Kwargs       Description
    ===========================     ==================================================
    x                               default: All fit items configured in model.
                                    This specifies which parameters to perform
                                    a profile likelihood for. List or strings.
    quantity_type                   default: 'concentration'. Alternative
                                    'particle_numbers`
    upper_bound_multiplier          default: 1000
    lower_bound_multiplier          1000
    intervals                       default: 10
    log10                           default: True
    run                             default: False. Passed on to Run or RunParallel
    max_active                      default: None. number of models to run
                                    simultaneously. None=all. For when run='parallel'
    results_directory               default: ProfileLikelihoods in the
                                    :py:attr:`model.root` directory
    method                          default: 'hooke_jeeves'
    number_of_generations           default: 200
    population_size                 default: 50
    random_number_generator         default: 1
    seed                            default: 0
    pf                              default: 0.475
    iteration_limit                 default: 50
    tolerance                       default: 0.00001
    rho                             default: 0.2
    scale                           default: 10
    swarm_size                      default: 50
    std_deviation                   default: 0.000001
    number_of_iterations            default: 100000
    start_temperature               default: 1
    cooling_factor                  default: 0.85
    <InsertParameters kwargs>       All parameters accepted in
                                    :py:class:`model.InsertParameters` are accepted
                                    here.
    <Report kwargs>                 Arguments to :py:class:`Reports` are accepted here
    ===========================     ==================================================


    """

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
            'run': False,
            'processes': 1,
            'results_directory': os.path.join(self.model.root,
                                              'ProfileLikelihoods'),
            'method': 'hooke_jeeves',
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
            'max_active': 3,
            'parallel_scan': True,
        }
        self.default_properties.update(self.kwargs)
        if self.default_properties.get('run_mode') is not None:
            raise errors.InputError('"run_mode" argument given but for ProfileLikelihood should be "run" instead')
        self.convert_bool_to_numeric(self.default_properties)
        self.update_properties(self.default_properties)
        self.check_integrity(list(self.default_properties.keys()), list(self.kwargs.keys()))
        self._do_checks()
        self._convert_numeric_arguments_to_string()

        ##protect against using run_mode instead of run

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

        if self.run is not False:
            self.run_analysis()

    def _do_checks(self):
        """

        :return:
        """
        if isinstance(self.index, int):
            self.index = [self.index]
        if self.df is None:
            if self.index == 'current_parameters':
                LOG.warning(
                    'Parameter estimation data has been specified without an index so will be ignored. Specify argument to index kwarg')

        if isinstance(self.x, str):
            self.x = self.get_variable_from_string(self.model, self.x)

        if ((self.df is None) and (self.parameter_path is None)) and (self.index != 'current_parameters'):
            LOG.warning('Got index argument without df argument. Setting index to "current_parameters"')
            self.index = 'current_parameters'

        if not os.path.isabs(self.results_directory):
            self.results_directory = os.path.join(self.model.root, self.results_directory)

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
            if 'type' in list(i.keys()):
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
            method_name = 'Current Solution Statistics'
            method_type = 'CurrentSolutionStatistics'

        if self.method == 'differential_evolution'.lower():
            method_name = 'Differential Evolution'
            method_type = 'DifferentialEvolution'

        if self.method == 'evolutionary_strategy_sr'.lower():
            method_name = 'Evolution Strategy (SRES)'
            method_type = 'EvolutionaryStrategySR'

        if self.method == 'evolutionary_program'.lower():
            method_name = 'Evolutionary Programming'
            method_type = 'EvolutionaryProgram'

        if self.method == 'hooke_jeeves'.lower():
            method_name = 'Hooke &amp; Jeeves'
            method_type = 'HookeJeeves'

        if self.method == 'levenberg_marquardt'.lower():
            method_name = 'Levenberg - Marquardt'
            method_type = 'LevenbergMarquardt'

        if self.method == 'nelder_mead'.lower():
            method_name = 'Nelder - Mead'
            method_type = 'NelderMead'

        if self.method == 'particle_swarm'.lower():
            method_name = 'Particle Swarm'
            method_type = 'ParticleSwarm'

        if self.method == 'praxis'.lower():
            method_name = 'Praxis'
            method_type = 'Praxis'

        if self.method == 'random_search'.lower():
            method_name = 'Random Search'
            method_type = 'RandomSearch'

        if self.method == 'simulated_nnealing'.lower():
            method_name = 'Simulated Annealing'
            method_type = 'SimulatedAnnealing'

        if self.method == 'steepest_descent'.lower():
            method_name = 'Steepest Descent'
            method_type = 'SteepestDescent'

        if self.method == 'truncated_newton'.lower():
            method_name = 'Truncated Newton'
            method_type = 'TruncatedNewton'

        if self.method == 'scatter_search'.lower():
            method_name = 'Scatter Search'
            method_type = 'ScatterSearch'

        if self.method == 'genetic_algorithm'.lower():
            method_name = 'Genetic Algorithm'
            method_type = 'GeneticAlgorithm'

        if self.method == 'genetic_algorithm_sr'.lower():
            method_name = 'Genetic Algorithm SR'
            method_type = 'GeneticAlgorithmSR'

        return method_name, method_type

    def set_PE_method(self):
        """
        This method is copied from the parameter estimation
        class.
        :return: model
        """

        # Build xml for method.
        method_name, method_type = self._select_method()
        method_params = {'name': method_name, 'type': method_type}
        method_element = etree.Element('Method', attrib=method_params)

        # list of attribute dictionaries
        # Evolutionary strategy parametery
        number_of_generations = {'type': 'unsignedInteger', 'name': 'Number of Generations',
                                 'value': self.number_of_generations}
        population_size = {'type': 'unsignedInteger', 'name': 'Population Size', 'value': self.population_size}
        random_number_generator = {'type': 'unsignedInteger', 'name': 'Random Number Generator',
                                   'value': self.random_number_generator}
        seed = {'type': 'unsignedInteger', 'name': 'Seed', 'value': self.seed}
        pf = {'type': 'float', 'name': 'Pf', 'value': self.pf}
        # local method parameters
        iteration_limit = {'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.iteration_limit}
        tolerance = {'type': 'float', 'name': 'Tolerance', 'value': self.tolerance}
        rho = {'type': 'float', 'name': 'Rho', 'value': self.rho}
        scale = {'type': 'unsignedFloat', 'name': 'Scale', 'value': self.scale}
        # Particle Swarm parmeters
        swarm_size = {'type': 'unsignedInteger', 'name': 'Swarm Size', 'value': self.swarm_size}
        std_deviation = {'type': 'unsignedFloat', 'name': 'Std. Deviation', 'value': self.std_deviation}
        # Random Search parameters
        number_of_iterations = {'type': 'unsignedInteger', 'name': 'Number of Iterations',
                                'value': self.number_of_iterations}
        # Simulated Annealing parameters
        start_temperature = {'type': 'unsignedFloat', 'name': 'Start Temperature', 'value': self.start_temperature}
        cooling_factor = {'type': 'unsignedFloat', 'name': 'Cooling Factor', 'value': self.cooling_factor}

        # build the appropiate xML, with method at root (for now)
        if self.method == 'current_solution_statistics':
            pass  # no additional parameter elements required

        if self.method == 'differential_evolution'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'evolutionary_strategy_sr'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
            etree.SubElement(method_element, 'Parameter', attrib=pf)

        if self.method == 'evolutionary_program'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'hooke_jeeves'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=rho)

        if self.method == 'levenberg_marquardt'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
        #
        if self.method == 'nelder_mead'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=scale)

        if self.method == 'particle_swarm'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=swarm_size)
            etree.SubElement(method_element, 'Parameter', attrib=std_deviation)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'praxis'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)

        if self.method == 'random_search'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_iterations)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'simulated_annealing'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=start_temperature)
            etree.SubElement(method_element, 'Parameter', attrib=cooling_factor)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
        #
        if self.method == 'steepest_descent'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=iteration_limit)
            etree.SubElement(method_element, 'Parameter', attrib=tolerance)
        #
        if self.method == 'truncated_newton'.lower():
            # required no additonal paraemters
            pass
        #
        if self.method == 'scatter_search'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_iterations)

        if self.method == 'genetic_algorithm'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)

        if self.method == 'genetic_algorithm_sr'.lower():
            etree.SubElement(method_element, 'Parameter', attrib=number_of_generations)
            etree.SubElement(method_element, 'Parameter', attrib=population_size)
            etree.SubElement(method_element, 'Parameter', attrib=random_number_generator)
            etree.SubElement(method_element, 'Parameter', attrib=seed)
            etree.SubElement(method_element, 'Parameter', attrib=pf)

        tasks = self.model.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')

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
            dct[0] = self.model
            parameters = self.model.parameters[self.model.fit_item_order]
            parameters['index'] = [0]
            parameters = parameters.set_index('index', drop=True)

        else:
            for i in self.index:
                I = model.InsertParameters(
                    self.model, df=self.df,
                    parameter_path=self.parameter_path, index=i
                )
                new_model = I.model
                dct[i] = new_model

                parameters[i] = I.parameters  # new_model.parameters[new_model.fit_item_order]
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
                param_name = misc.RemoveNonAscii(param).filter + '.cps'

                new_copasi_filename = os.path.join(new_dir, param_name)
                dct[model][param] = self.index_dct[model].copy(new_copasi_filename)
                dct[model][param].save()
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
        query = "//*[@name='FitItem']"  # query="//*[@name='FitItem']"
        for model in self.model_dct:
            count = 0
            for param in self.model_dct[model]:
                # self.model_dct[model][param].open()
                ##ascertain which parameter this is
                for i in self.model_dct[model][param].xml.xpath(query):
                    count = count + 1
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
            raise errors.NoFitItemsError(
                'Model does not contain any fit items. Please setup a parameter estimation and try again')
        ##save is needed
        self.to_file()

        return self.model_dct

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
        :param model: pycotools3.model.Model
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
            output_in_subtask=False,  # self.output_in_subtask,
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
        q = queue.Queue(maxsize=number_of_cpu)
        res = {}
        for model in self.model_dct:
            res[model] = {}
            for param in self.model_dct[model]:
                report_name = os.path.join(
                    self.model_dct[model][param].root,
                    os.path.splitext(
                        self.model_dct[model][param].copasi_file
                    )[0] + '.csv'
                )
                ## cater for the case where index=='current_parameters'
                if self.index == 'current_parameters':
                    assert model == 0
                    parameter_value = float(self.parameters.loc[0][param])


                ## then all other situations
                else:
                    parameter_value = float(self.parameters[model][param])  # if self.parallel_scan:
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

    def run_analysis(self):
        """

        :return:
        """
        model_list = []
        if self.run is 'parallel':
            for i in self.model_dct:
                for j in self.model_dct[i]:
                    model_list.append(self.model_dct[i][j])
        RunParallel(model_list, max_active=self.max_active, task='scan')

        for m in self.model_dct:
            for param in self.model_dct[m]:
                LOG.info('running {}'.format(self.model_dct[m][param].copasi_file))
                sge_job_filename = "{}_{}".format(param, m)
                sge_job_filename = re.sub('[().]', '', sge_job_filename)
                Run(self.model_dct[m][param], task='scan', mode=self.run, sge_job_filename=sge_job_filename + '.sh')


@mixin(model.GetModelComponentFromStringMixin)
@mixin(model.ReadModelMixin)
class Sensitivities(_Task):
    """
    Interface to COPASI sensitivity task

    """

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
        if self.cause_single_object is not None:
            self.cause_single_object = self.get_variable_from_string(self.model, self.cause_single_object)

        if self.effect_single_object is not None:
            self.cause_single_object = self.get_variable_from_string(self.model, self.effect_single_object)

        if self.secondary_cause_single_object is not None:
            self.cause_single_object = self.get_variable_from_string(self.model, self.secondary_cause_single_object)

    def sensitivity_task_key(self):
        """
        Get the sensitivity task as it currently is
        in the model as etree.Element
        :return:
        """
        # query = './/Task/*[@name="Sensitivities"]'
        tasks = self.model.xml.findall(self.schema + 'ListOfTasks')[0]
        for i in tasks:
            if i.attrib['name'] == 'Sensitivities':
                return i.attrib['key']

    def create_sensitivity_task(self):
        return etree.Element('Task', attrib=OrderedDict({
            'key': self.sensitivity_task_key(),
            'name': 'Sensitivities',
            'type': 'sensitivities',
            'scheduled': 'false',
            'updateModel': 'false'
        }))

    def create_new_report(self):
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
        ## get the report key
        for i in self.model.xml:
            if i.tag == self.schema + 'ListOfReports':
                for j in i:
                    if j.attrib['name'] == 'sensitivity':
                        return j.attrib['key']

    def set_report(self):
        attrib = OrderedDict({
            'reference': self.get_report_key(),
            'target': self.report_name,
            'append': self.append,
            'confirmOverwrite': self.confirm_overwrite
        })
        etree.SubElement(self.task, 'Report', attrib=attrib)
        return self.task

    def create_problem(self):
        etree.SubElement(self.task, 'Problem')
        return self.task

    def set_subtask(self):
        assert self.task[1].tag == 'Problem'
        attrib = OrderedDict({
            'name': 'SubtaskType',
            'type': 'unsignedInteger',
            'value': self.subtasks[self.subtask]
        })
        etree.SubElement(self.task[1], 'Parameter', attrib=attrib)
        return self.task

    def set_effect(self):
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
        assert self.task[1].tag == 'Problem'
        parameter_group = etree.SubElement(self.task[-1], 'ParameterGroup',
                                           attrib={'name': 'ListOfVariables'})
        return self.task

    def set_cause(self):
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
        task_list = self.model.xml.findall(self.schema + 'ListOfTasks')[0]
        for i in task_list:
            if i.attrib['name'] == 'Sensitivities':
                i.getparent().remove(i)
        task_list.insert(9, self.task)
        return self.model

    def run_task(self):
        r = Run(self.model, task='sensitivities', mode=self.run)
        return r.model

    def process_data(self):
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
    """
    Let S = matrix of partial derivatives of metabolites with respect to
    kinetic parameters. Then the fisher information matrix (FIM) is:
        FIM = S^TS



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
        return self.sensitivities.transpose().dot(self.sensitivities)


class Hessian(Sensitivities):
    pass


class GlobalSensitivities(Sensitivities):
    """
    Sensitivity around parameter estimates
    """
    pass


if __name__ == '__main__':
    pass
#    execfile('/home/b3053674/Documents/Models/2017/08_Aug/pycotoolsTests/RunPEs.py')
#    execfile('/home/b3053674/Documents/pycotools3/pycotools3/pycotoolsTutorial/Test/testing_kholodenko_manually.py')
