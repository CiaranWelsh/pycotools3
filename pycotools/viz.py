"""
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
 Time:  20:33

This module facilitates the visualziation of modelling tasks such as time courses and
parameter estimations.





Here are some kwargs used in most classes within the viz module:

.. _kwargs:

kwargs
======



.. _plot-kwargs:

Kwargs for plotting
-------------------

These keyword arguments are passed on to matplotlib

==========  ======================================
kwarg       Description
==========  ======================================
linestyle   `str`.
marker      `str`
linewidth   `int`
markersize  `int`
alpha       `float` (0-1). Translucency of a patch
title       `str` figure title
xlabel      `str` label for x axis
ylabel      `str` label for y axis
show        `bool` show the plot
==========  ======================================


Each class in this module share a common set of kwargs to control saving figure to file. They are:

.. _savefig-kwargs:

savefig kwargs
--------------

==================  ========================================
kwarg               Description
==================  ========================================
savefig             `bool`. Save plot to file. Default=False
results_directory   `str`. Folder to save to if savefig=True
title               `str`. Title of the plot
xlabel              `str`. label for x axis
ylabel              `str`. label for y axis
show                `bool`. Show the plot or not
filename            `str` specific filename for plot
                    when savefig=True. Include extention
dpi                 `int`. dots per inch when saving to file
==================  ========================================



.. _truncate-kwargs:

truncate-kwargs
---------------
=========== =============================
Mode        Description
=========== =============================
percentage  Keep top `percentage` percent.
below_theta Keep parameter sets with a
            RSS value below theta.
ranks       Keep the top `ranks` ranks.
=========== =============================

Theta:

======================= =============================
theta arg when`mode` is Description
======================= =============================
percentage              Range between 0 and 100.
below_theta             `float` or `int`. Denotes RSS
                        cut off
ranks                   `list` of integers
======================= =============================

"""


##TODO Fix plot_kwargs
##TODO fix parameter estimation ensembles
import contextlib
import string
import pandas
from pandas.parser import CParserError
from pandas.errors import EmptyDataError
import matplotlib.pyplot as plt
import scipy 
import os
import matplotlib
import itertools
import tasks,errors, misc, model
import seaborn 
import logging
from subprocess import check_call,Popen
import glob
import re
import numpy
from mixin import Mixin, mixin
from textwrap import wrap
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn import model_selection
import _base
from cached_property import cached_property
import matplotlib.patches as mpatches
from multiprocessing import Process, Queue
from math import exp as exponential_function
import math
LOG=logging.getLogger(__name__)

SEABORN_OPTIONS = {'context': 'poster',
                   'font_scale': 2}

seaborn.set_context(context=SEABORN_OPTIONS['context'], font_scale=SEABORN_OPTIONS['font_scale'])



class PlotKwargs(object):
    def plot_kwargs(self):
        plot_kwargs = {
            'linestyle': '-',
            'marker': 'o',
            'linewidth': 3,
            'markersize': 8,
            'alpha': 0.5
        }
        return plot_kwargs

class SaveFigMixin(Mixin):
    """


    """
    @staticmethod
    def save_figure(directory, filename, dpi=300):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')


@mixin(tasks.UpdatePropertiesMixin)
class TruncateData(object):
    """
    Parameter estimation data in systems biology usually have runs which fall
    into a local minima. This class removes these runs from further
    analysis.

    See :ref:`truncate-kwargs` for keyword arguments

    Examples assuming `df` is a `pandas.DataFrame` retuned from
    the `Parse` class:

    Analyze the top 10 percent of parameter fits. Conduct analysis on linear scale.

        >>> data = TruncateData(data, mode=percent, theta=10, log10=False)

    Analyze top 10 best parameter sets on a log10 scale

        >>> data = TruncateData(data, mode='ranks', theta=range(10), log10=True)

    Analyze parameter sets with a RSS value below 10^3.5 (because log10 is set to True)

        >>> data = TruncateData(data, mode='below_x', theta=3.5, log10=True)
    """

    def __init__(self, data, mode='percent', theta=100, log10=False):
        """
        :param data:
            `pandas.DataFrame`. Data to truncate

        :param mode:
            `str`. Mode to use for truncation

        :param theta:
            `int` or `float`. Percentage, cut-off point or ranks

        :param log10:
            `bool` whether to truncate on log10 scale and return log10 scale data
        """

        self.data = data
        self.mode = mode
        self.theta = theta
        self.log10 = log10
        assert self.mode in ['below_theta', 'percent', 'ranks']

        self.data = self.truncate()

    def below_theta(self):
        """
        remove data which is not below theta
        :return:
            :py:class:'pandas.DataFrame`
        """
        assert self.data.shape[0] != 0, 'There are no data with RSS below {}. Choose a higher number'.format(self.theta)
        return self.data[self.data['RSS'] < self.theta]

    def top_theta_percent(self):
        """
        Remove data not in top theta percent
        :return:
            :py:class:'pandas.DataFrame`
        """
        if self.theta > 100 or self.theta < 1:
            raise errors.InputError('{} should be between 0 and 100')
        theta_quantile = int(numpy.round(self.data.shape[0] * (float(self.theta) / 100.0)))
        return self.data.iloc[:theta_quantile]

    def ranks(self):
        """
        Remove data which is not in the top ranks
        parameter estimation data
        :return:
            :py:class:'pandas.DataFrame`
        """
        return self.data.iloc[self.theta]

    def truncate(self):
        """

        :return:
        """
        if self.mode == 'below_theta':
            return self.below_theta()  # self.data
        elif self.mode == 'percent':
            return self.top_theta_percent()
        elif self.mode == 'ranks':
            return self.ranks()

class ParseMixin(Mixin):
    @staticmethod
    def parse(cls, log10, copasi_file=None):
        """
        Mixin method interface to parse class
        :return:
        """
        if type(cls) == Parse:
            return cls.data
        else:
            return Parse(cls, log10=log10, copasi_file=copasi_file).data


class TruncateDataMixin(Mixin):
    @staticmethod
    def truncate(data, mode, theta):
        """
        mixin method interface to truncate data
        """
        df = TruncateData(data,
                            mode=mode,
                            theta=theta).data
        return df

class CreateResultsDirectoryMixin(Mixin):
    @staticmethod
    def create_directory(results_directory):
        """
        create directory for results and switch to it
        :param results_directory:
        :return:
        """
        if not os.path.isdir(results_directory):
            os.makedirs(results_directory)
        os.chdir(results_directory)
        return results_directory

class ChiSquaredStatistics(object):
    def __init__(self, rss, dof, num_data_points, alpha, plot_chi2=False):
        self.alpha = alpha
        self.dof = dof
        self.rss = rss
        self.num_data_points = num_data_points
        self.CL = self.calc_chi2_CL()

        if plot_chi2:
            self.plot_chi2_CL()

    def chi2_lookup_table(self, alpha):
        """
        Looks at the cdf of a chi2 distribution at incriments of
        0.1 between 0 and 100.

        Returns the x axis value at which the alpha interval has been crossed,
        i.e. gets the cut off point for chi2 dist with dof and alpha .
        """
        nums = numpy.arange(0, 100, 0.1)
        table = zip(nums, scipy.stats.chi2.cdf(nums, self.dof))
        for i in table:
            if i[1] <= alpha:
                chi2_df_alpha = i[0]
        return chi2_df_alpha

    def get_chi2_alpha(self):
        """
        return the chi2 threshold for cut off point alpha and dof degrees of freedom
        """
        dct = {}
        alphas = numpy.arange(0, 1, 0.01)
        for i in alphas:
            dct[round(i, 3)] = self.chi2_lookup_table(i)
        return dct[self.alpha]

    def plot_chi2_CL(self):
        """
        Visualize where the alpha cut off is on the chi2 distribution
        """
        x = numpy.linspace(scipy.stats.chi2.ppf(0.01, self.dof), scipy.stats.chi2.ppf(0.99, self.dof), 100)

        plt.figure()
        plt.plot(x, scipy.stats.chi2.pdf(x, self.dof), 'k-', lw=4, label='chi2 pdf')

        y_alpha = numpy.linspace(plt.ylim()[0], plt.ylim()[1])
        x_alpha = [self.get_chi2_alpha()] * len(y_alpha)

        plt.plot(x_alpha, y_alpha, '--', linewidth=4)
        plt.xlabel('x', fontsize=22)
        plt.ylabel('Probability', fontsize=22)
        plt.title('Chi2 distribution with {} dof'.format(self.dof), fontsize=22)

    def calc_chi2_CL(self):
        """

        :return:
        """
        return self.rss * exponential_function((self.get_chi2_alpha() / self.num_data_points))

##TODO use cached property
class Parse(object):
    """
    General class for parsing copasi output into Python.

    First argument is an instance of a pycotools class.

    ==================================          ===========================
    instance                                       Description
    ==================================          ===========================
    tasks.TimeCourse                            Parse time course data from
                                                TC.report_name into pandas.df
    tasks.ParameterEstimation                   Parse parameter estimation
                                                data from PE.report_name into pandas.df
    tasks.Scan                                  Parse scan data from scan.report_name
    tasks.MultiParameterEstimation              Parse folder of parameter estimation
                                                data from MPE.results_directory into
                                                pandas.df
    Parse                                       enable parsing from a parse instance.
                                                Just returns itself
    str                                         Parse data from folder of parameter
                                                estimation data into pandas.df. Requires
                                                the copasi file argument.
    ==================================          ===========================
    """
    def __init__(self, cls_instance, log10=False, copasi_file=None):
        """

        :param cls_instance:
            A instance of pycotools class

        :param log10:
            `bool`. Whether to work on log10 scale

        :param copasi_file:
            `str`. Optional but necessary when cls_instance
            is string. Must be the copasi_file which produced
            the parameter estimation data as Parse extracts
            data headers from the copasi file
        """
        self.cls_instance = cls_instance
        self.log10 = log10
        self.copasi_file = copasi_file
        self.model = None
        if self.copasi_file is not None:
            self.model = model.Model(self.copasi_file)

        accepted_types = [tasks.TimeCourse,
                          tasks.Scan,
                          tasks.ParameterEstimation,
                          tasks.MultiParameterEstimation,
                          str,
                          Parse,
                          tasks.ProfileLikelihood]

        if type(self.cls_instance) not in accepted_types:
            raise errors.InputError('{} not in {}'.format(
                self.cls_instance,
                accepted_types)
            )

        if isinstance(self.cls_instance, tasks.Scan):
            ## '1' is copasi code name for a scan
            if self.cls_instance.scan_type != '1':
                raise errors.InputError(
                    'plotting functions are only available for scans (not repeat or random distributions)'
                )

        LOG.debug('type --> {}'.format(self.cls_instance))
        LOG.debug('type --> {}'.format(isinstance(self.cls_instance, tasks.ProfileLikelihood)))
        self.data = self.parse()


    def parse(self):
        """
        determine class type of self.cls_instance
        and call the appropirate method for
        parsing the data type
        :return:
        """
        LOG.debug('type --> {}'.format(type(self.cls_instance)))
        LOG.debug(' --> {}'.format(self.cls_instance))
        data = None

        if isinstance(self.cls_instance, tasks.TimeCourse):
            data = self.from_timecourse()

        elif type(self.cls_instance) == tasks.ParameterEstimation:
            data = self.from_parameter_estimation

        elif type(self.cls_instance) == tasks.MultiParameterEstimation:
            data = self.from_multi_parameter_estimation(self.cls_instance)

        elif type(self.cls_instance) == Parse:
            return self.cls_instance.data

        elif type(self.cls_instance) == tasks.ProfileLikelihood:
            data = self.from_profile_likelihood()

        elif type(self.cls_instance == str):
            data = self.from_folder()


        if self.log10:
            data = numpy.log10(data)
            return data
        else:
            return data

    def from_timecourse(self):
        """
        read time course data into pandas dataframe. Remove
        copasi generated square brackets around the variables
        :return: pandas.DataFrame
        """

        df = pandas.read_csv(self.cls_instance.report_name, sep='\t')
        headers = [re.findall('(Time)|\[(.*)\]', i)[0] for i in list(df.columns)]
        time = headers[0][0]
        headers = [i[1] for i in headers]
        headers[0] = time
        df.columns = headers
        return df

    def parse_scan(self):
        """
        read scan data into pandas Dataframe.
        :return: pandas.DataFrame
        """
        df = pandas.read_csv(
            self.cls_instance.report_name,
            sep='\t',
            skip_blank_lines=False,
        )
        # names = []
        # d = {names[i]: x.dropna() for i, x in df.groupby(df[0].isnull().cumsum())}
        return NotImplementedError('scan plotting features are not yet implemented')

    @cached_property
    def from_parameter_estimation(self):
        """
        Parse parameter estimation data. Store the data in
        a cache.
        :return:
        """
        try:
            df = pandas.read_csv(self.cls_instance.report_name, sep='\t', header=None)
            if '(' in list(df.iloc[0]):
                raise errors.NonFormattedPEFileError
            return df

        except errors.NonFormattedPEFileError:
            df = pandas.read_csv(
                self.cls_instance.report_name,
                sep='\t', header=None,
            )
            data = df.drop(df.columns[0], axis=1)
            width = data.shape[1]
            # remove the extra bracket
            data[width] = data[width].str[1:]
            names = self.cls_instance.model.fit_item_order+['RSS']
            data.columns = names
            os.remove(self.cls_instance.report_name)
            data.to_csv(self.cls_instance.report_name,
                        sep='\t',
                        index=False)
            return data

    @staticmethod
    def from_multi_parameter_estimation(cls_instance, folder=None):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :param cls_instance: instance of MultiParameterEstiamtion
        :param folder: afternative folder to parse from. Useful for tests
        :return:
        """
        ##set default
        if folder == None:
            folder = cls_instance.results_directory
        d = {}
        for report_name in glob.glob(folder+r'/*'):
            report_name = os.path.abspath(report_name)
            if os.path.isfile(report_name) != True:
                raise errors.FileDoesNotExistError('"{}" does not exist'.format(report_name))

            try:
                data = pandas.read_csv(report_name,
                                       sep='\t', header=None, skiprows=[0])
            except:
                LOG.warning('No Columns to parse from file. {} is empty. Skipping this file'.format(
                    report_name))
                continue
            try:
                bracket_columns = data[data.columns[[0, -2]]]

            except IndexError:
                raise errors.SomethingWentHorriblyWrongError(
                    'Rare problem with data file : "{}". Check it manually'
                    ' and remove if it is corrupt'.format(report_name)
                )

            if bracket_columns.iloc[0].iloc[0] != '(':
                data = pandas.read_csv(report_name, sep='\t')
                d[report_name] = data
            else:
                data = data.drop(data.columns[[0, -2]], axis=1)
                data.columns = range(data.shape[1])
                ### parameter of interest has been removed.
                names = cls_instance.model.fit_item_order+['RSS']
                if cls_instance.model.fit_item_order == []:
                    raise errors.SomethingWentHorriblyWrongError('Parameter Estimation task is empty')
                if len(names) != data.shape[1]:
                    raise errors.SomethingWentHorriblyWrongError('length of parameter estimation data does not equal number of parameters estimated')

                if os.path.isfile(report_name):
                    os.remove(report_name)
                data.columns = names
                data.to_csv(report_name, sep='\t', index=False)
                d[report_name] = data
        df = pandas.concat(d)
        columns = df.columns
        ## reindex, drop and sort by RSS
        df = df.reset_index().drop(['level_0', 'level_1'], axis=1).sort_values(by='RSS')

        return df.reset_index(drop=True)

    def from_folder(self):
        """
        
        :param folder: 
        :return: 
        """
        if self.copasi_file is None:
            raise errors.InputError('To read data from a folder of'
                                    'parameter estimation data files '
                                    'specify argument to copasi_file. This'
                                    'should be the configured model '
                                    'that was used to generate the parameter'
                                    ' estimation data. This is necessary to annotate'
                                    ' data with model component names')
        m = model.Model(self.copasi_file)
        ## check that cps has a parameter estimation configured
        if m.fit_item_order == []:
            raise errors.InputError('No fit items exist. Its possible that you have'
                                    ' not given the copasi file that was used to generate this'
                                    ' parameter estimation data')

        d = {}
        for report_name in glob.glob(os.path.join(self.cls_instance, '*.txt')):
            report_name = os.path.abspath(report_name)
            if os.path.isfile(report_name) != True:
                raise errors.FileDoesNotExistError('"{}" does not exist'.format(report_name))

            try:
                data = pandas.read_csv(report_name,
                                       sep='\t', header=None, skiprows=[0])
            except EmptyDataError:
                LOG.warning(
                    'No Columns to parse from file. {} is empty. '
                    'Continuing without parsing from this file'.format(
                        report_name
                    )
                )
                continue
            except CParserError:
                raise CParserError('Parameter estimation data file is empty')

            bracket_columns = data[data.columns[[0, -2]]]
            if bracket_columns.iloc[0].iloc[0] != '(':
                data = pandas.read_csv(report_name, sep='\t')
                d[report_name] = data
            else:
                data = data.drop(data.columns[[0, -2]], axis=1)
                data.columns = range(data.shape[1])
                ### parameter of interest has been removed.
                names = m.fit_item_order + ['RSS']
                if len(names) != data.shape[1]:
                    raise errors.SomethingWentHorriblyWrongError(
                        'length of parameter estimation data does not equal number of parameters estimated')

                if os.path.isfile(report_name):
                    os.remove(report_name)
                data.columns = names
                data.to_csv(report_name, sep='\t', index=False)
                d[report_name] = data
        df = pandas.concat(d)
        columns = df.columns
        ## reindex, drop and sort by RSS
        df = df.reset_index().drop(['level_0', 'level_1'], axis=1).sort_values(by='RSS')

        return df.reset_index(drop=True)

    def from_profile_likelihood(self):
        """
        Parse data from :py:class:`tasks.ProfileLikelihood`
        :return:
            :py:class:`pandas.DataFrame`
        """
        def get_results():
            """
            Get results files as dict
            :return:
                2 element `tuple`.
                First element:
                    dict[model_number][parameter] = path/to/results.csv

                Second element:
                    dict[model_number][parameter] = fit item order for that model
            """
            results_dirs = {}
            fit_item_order_dirs = {}
            param_of_interest_dict = {}
            for model in self.cls_instance.model_dct:
                results_dirs[model] = {}
                fit_item_order_dirs[model] = {}
                param_of_interest_dict[model] = {}
                for param in self.cls_instance.model_dct[model]:
                    copasi_file = self.cls_instance.model_dct[model][param].copasi_file
                    # print os.path.split(copasi_file)
                    results_file = os.path.splitext(copasi_file)[0]+'.csv'
                    if not os.path.isfile(results_file):
                        raise errors.InputError('file does not exist: "{}"'.format(results_file))
                    results_dirs[model][param] = results_file
                    fit_item_order_dirs[model][param] = self.cls_instance.model_dct[model][param].fit_item_order
                    fit_item_order_dirs[model][param] = self.cls_instance.model_dct[model][param].fit_item_order
            return results_dirs, fit_item_order_dirs

        def experiment_files_in_use(mod):
            """
            Search the model specified by mod for experiment
            files defined in the parameter estimation task

            :param mod:
                :py:class:`model.Model`. The
                still configured model that was used
                to generate parameter estimation data

            :return:
                `list` of experiment files
            """
            query = '//*[@name="File Name"]'
            l = []
            for i in mod.xml.xpath(query):
                f = os.path.abspath(i.attrib['value'])
                if os.path.isfile(f) != True:
                    raise errors.InputError(
                        'Experimental files in use cannot be automatically '
                        ' determined. Please give a list of experiment file '
                        'paths to the experiment_files keyword'.format())
                l.append(os.path.abspath(i.attrib['value']))
            return l

        def dof(mod):
            """
            Return degrees of freedom. This is the
            number of estimated parameters minus 1

            :param mod:
                :py:class:`model.Model`. The
                still configured model that was used
                to generate parameter estimation data

            :return:
            """
            return len(mod.fit_item_order) - 1

        def num_data_points(experiment_files):
            """
            number of data points in your data files. Relies on
            being able to locate the experiment files from the
            copasi file

            :return:
                `int`.

            """
            experimental_data = [pandas.read_csv(i, sep='\t') for i in experiment_files]
            l = []
            for i in experimental_data:
                l.append(i.shape[0] * (i.shape[1] - 1))
            s = sum(l)
            if s == 0:
                raise errors.InputError('Number of data points cannot be 0. '
                                        'Experimental data is inferred from the '
                                        'parameter estimation task definition. '
                                        'It might be that copasi_file refers to a '
                                        'fresh copy of the model. Try redefining the '
                                        'same parameter estimation problem that you '
                                        'used in the profile likelihood, using the '
                                        'setup method but not running the '
                                        'parameter estimation before trying again.')
            return s

        def confidence_level(cls, alpha=0.95):
            """
            Get confidence level using ChiSquaredStatistics

            :return:
                dict[index][confidence_level]
            """
            CL_dct = {}
            for index in cls.parameters:
                rss_value = cls.parameters[index]['RSS']
                experiment_files = experiment_files_in_use(cls.model)
                CL_dct[index] = float(ChiSquaredStatistics(
                    rss_value, dof(cls.model), num_data_points(experiment_files),
                    alpha
                ).CL)
            return CL_dct

        def parse_data(results_dict, fit_item_order_dict):
            """
            Parse data from profile likelihood analysis
            into :py:class`pandas.DataFrame`

            :param results_dict:
                dict[model][param] = path/to/csv.
                First element of output from get_results

            :param fit_item_order_dict:
                dict[model][param] = model.fit_item_order.
                second element from output of get_results

            :return:
                :py:class:`pandas.DataFrame`. Results in
                formatted pandas Dataframe
            """
            res = {}
            df_list = []
            for index in results_dict:
                res[index] = {}
                for param in results_dict[index]:
                    LOG.debug('res --> {}'.format(results_dict[index][param]))
                    df = pandas.read_csv(results_dict[index][param],
                                              sep='\t', skiprows=1, header=None)
                    LOG.debug('df --> \n\n{}'.format(df))
                    bracket_indices = [1, -2]
                    df = df.drop(df.columns[bracket_indices], axis=1)
                    fit_items = [param] + fit_item_order_dict[index][param] + ['RSS']
                    # print fit_items
                    df.columns = fit_items
                    df['Parameter Of Interest'] = param
                    CL = confidence_level(self.cls_instance, alpha=0.95)
                    if self.log10:
                        df['Best Parameter Value'] = math.log10(float(self.cls_instance.parameters[index][param]))
                        CL[index] = math.log10(CL[index])
                    else:
                        df['Best Parameter Value'] = float(self.cls_instance.parameters[index][param])
                    df['Confidence Level'] = CL[index]
                    df['Best Fit Index'] = index
                    df = df.set_index(['Best Fit Index', 'Parameter Of Interest', 'Confidence Level', 'Best Parameter Value'], drop=True)
                    df_list.append(df)
            df = pandas.concat(df_list)
            return df

        results, fit_item_order = get_results()

        return parse_data(results, fit_item_order)


@mixin(tasks.UpdatePropertiesMixin)
@mixin(SaveFigMixin)
@mixin(ParseMixin)
@mixin(CreateResultsDirectoryMixin)
class PlotTimeCourse(PlotKwargs):
    """
    Plot time course data

    Time course kwargs:

    ================    ======================================
    kwarg               Description
    ================    ======================================
    x                   `str`. Parameter to go on x axis.
                        defaults to 'Time'. If not 'Time'
                        then  plot is a phase space plot
    y                   `str` or `list` of `str`. Parameters
                        for the y axis.
    log10               `bool` plot on log10 scale
    separate            bool` separate time courses onto
                        different axes. Default: True
    **kwargs            See :ref:`kwargs` for more options
    ================    ======================================
    """
    def __init__(self, cls, **kwargs):
        """

        :param cls:
            Instance of tasks.TimeCourse class

        :param kwargs:
        """
        super(PlotTimeCourse, self).__init__()
        self.cls = cls
        self.kwargs = kwargs

        self.default_properties = {
            'x': 'time',
            'y': None,
            'log10': False,
            'separate': True,
            'savefig': False,
            'results_directory': None,
            'title': 'TimeCourse',
            'xlabel': None,
            'ylabel': None,
            'show': False,
            'filename': None,
            'dpi': 300,
        }
        self.default_properties.update(self.plot_kwargs())
        for i in kwargs.keys():
            assert i in self.default_properties.keys(),'{} is not a keyword ' \
                                                       'argument for PlotTimeCourse'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs())
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, self.log10)
        self.plot()

    def __str__(self):
        """

        :return:
        """
        return "PlotTimeCourse(x='{}', y={}, log10={}, separate={}, savefig={}, results_directory='{}'".format(
            self.x, self.y, self.log10,
            self.separate, self.savefig,
            self.results_directory
        )

    def _do_checks(self):
        """

        :return:
        """
        if not isinstance(self.cls, tasks.TimeCourse):
            raise errors.InputError(
                'PlotTimeCourse class expects an instance of'
                ' tasks.TimeCourse as first argument. '
                'Got {} instead'.format(type(self.cls)))

        if not isinstance(self.x, str):
            raise errors.InputError('x should be a string. Got {}'.format(type(self.x)))

        if self.y is not None:
            if not isinstance(self.y, (str, list)):
                raise errors.InputError('y should be a string or list of strings. Got {}'.format(type(self.y)))

        bool_list = [self.separate,
                     self.savefig]
        for i in bool_list:
            if not isinstance(i, bool):
                raise errors.InputError('{} argument should be boolean. Got {}'.format(i, type(i)))

        if self.results_directory is None:
            self.results_directory = os.path.join(
                self.cls.model.root, 'TimeCourseGraphs'
            )

        if self.x.lower() == 'time':
            self.xlabel = "Time ({})".format(self.cls.model.time_unit)

        if self.xlabel is None:
            self.xlabel = self.x

        if self.ylabel is None:
            self.ylabel = 'Concentration ({})'.format(self.cls.model.quantity_unit)

        if self.savefig and (self.separate is False) and (self.filename is None):
            self.filename = 'TimeCourse.png'
            LOG.warning('filename is None. Setting default filename to {}'.format(self.filename))

    def plot(self):
        """

        :return:
        """
        if self.y == None:
            self.y = self.data.keys()
            self.y = [i for i in self.y if i.lower() != 'time']

        if self.y == 'metabolites':
            self.y = [i.name for i in self.cls.model.metabolites]

        elif self.y == 'global_quantities':
            self.y = [i.name for i in self.cls.model.global_quantities]

        elif self.y == 'local_parameter':
            self.y = [i.global_name for i in self.cls.model.local_parameters]

        if isinstance(self.y, str):
            self.y = [self.y]


        for i in self.y:
            if i not in self.data.keys():
                raise errors.InputError('{} not in {}'.format(i, self.data.keys()))

        if self.x == 'time':
            self.x = 'Time'
        if self.x not in self.data.keys():
            raise errors.InputError('{} not in {}'.format(self.x, self.data.keys()))

        figures = []
        if not self.separate:
            fig = plt.figure()
            figures.append(fig)

        # self.create_results_directory(self.results_directory)

        for y_var in self.y:
            if self.separate:
                fig = plt.figure()
                figures.append(fig)
            y = self.data[y_var]
            x = self.data[self.x]
            plt.plot(x, y, label=y_var)
            plt.legend()
            plt.title(self.title)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            if self.savefig:
                dirs = self.create_directory(self.results_directory)

                if self.separate:
                    fle = os.path.join(dirs, '{}.png'.format(y_var))
                    fig.savefig(fle, dpi=self.dpi, bbox_inches='tight')
                else:
                    fle = os.path.join(dirs, self.filename)
                    fig.savefig(fle, dpi=self.dpi, bbox_inches='tight')

        if self.show:
            plt.show()
        return figures


@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class PlotTimeCourseEnsemble(object):
    """
    Plot a time course ensemble from a model and
    parameter ensemble. If `cls` argument is a
    MultiParameterEstimation instance then the results
    and copasi file are automatically extracted. If cls
    is a string, then it must point to a folder of parameter
    estimation data and a copasi file must be specified.

    One by one the parameter sets are inserted into the copasi
    model and a time course is simulated. The data is aggregated
    using a :py:class:`seaborn.tsplot` using a statistic of
    the users choice (default is :py:meth:`numpy.mean`). Confidence
    intervals are estimated using a bootstrapping method which is
    built-in to :py:class:`seaborn.tsplot`


    kwargs

    ================    ==========================================================
    kwarg               Description
    ================    ==========================================================
    y                   `str` or list of `str`. Variable(s) to
                        put on the y axis
    x                   `str`. Variable to put on x axis.
    truncate_mode       `str`. see :py:class:`TruncateData` class
    theta               `str`. see :py:class:`TruncateData` class
    xtick_rotation      `int`. Rotate the x axis by `xtick_rotation`
                        degrees
    step_size           `int`. Step size for time course integration
    check_as_you_plot   `bool` if ``True``, open each model in turn
                        so that you can manually verify inserted parameter
                        or play around with the model
    estimator           `func` estimator to bootstrap.
                        Passed to :py:class:`seaborn.tsplot`
    n_boot              `int`. number of boot strap samples to perform
    ci                  `int` or `list` of `int`. confidence intervals
                        between 0 and 100. If `list` multiple contours are
                        plotted
    color               `str` colour
    show                `bool`. Show the figure. Default: False
    silent              `bool`. default=True. Print parameters being
                        inserted to screen
    data_filename       `str` file name for writing ensemble time course
                        data to file
    exp_color           `str` colour of the experimental data
    experiment_files    `str` or `list` of `str`. For use only
                        when parsing from folder. Paths to experimental
                        data that was used to generate the parameter estimation
                        data
    run_mode            `str` or `bool`. Passed to :py:class:`tasks.Run`
                        Optionally perform time course simulations in parallel
                        by giving ``run_mode=multiprocess``
    copasi_file         `str` path to copasi file that was used to generate
                        parameter ensemble. Must be still configured for
                        parameter estimation in order to extract parameter headers
    **kwargs            see :ref:`kwargs` for savefig options
    ================    ==========================================================
    """

    def __init__(self, cls, **kwargs):
        """

        :param cls:
            Instance of MultiParameterEstimation or str
            containing path to parameter estimation data. If
            string the same condition as in :py:class:`Parse` applies
            with the `copasi_file` arg.

        :param kwargs:
        """
        self.cls = cls
        options = {'y': None,
                   'x': 'time',
                   'truncate_mode': 'percent',
                   'theta': 100,
                   'xtick_rotation': 'horizontal',
                   'savefig': False,
                   'results_directory': None,
                   'dpi': 300,
                   'step_size': 1,
                   'check_as_you_plot': False,
                   'estimator': numpy.mean,
                   'n_boot': 5000,
                   'ci': 95,
                   'color': 'blue',
                   'show': False,
                   'silent': True,
                   'data_filename': None,  # For outputting ensemble data to file
                   'exp_color': 'red',
                   'experiment_files': None,  # For use only when parsing from folder
                   'title': None,
                   'ylabel': None,
                   'xlabel': None,
                   'run_mode': True,
                   'copasi_file': None,
                   }

        for i in kwargs.keys():
            assert i in options.keys(), '{} is not a keyword argument for ParameterEnsemble'.format(i)
        options.update(kwargs)
        self.kwargs = options
        self.update_properties(self.kwargs)
        self._do_checks()

        self.data = self.parse(self.cls, log10=False, copasi_file=self.copasi_file)
        self.data = self.truncate(self.data,
                                  mode=self.truncate_mode,
                                  theta=self.theta)
        if self.data.empty:
            raise errors.InputError('No data. Check arguments to truncate_data and theta '
                                    'or your parameter estimation configuration '
                                    'and data files')

        self.experimental_data = self.parse_experimental_files
        self.exp_times = self.get_experiment_times
        # print self.simulate_ensemble
        self.ensemble_data = self.simulate_ensemble
        self.ensemble_data.index = self.ensemble_data.index.rename(['Index','Time'])

        if self.data_filename != None:
            self.ensemble_data.to_csv(self.data_filename)
            LOG.info('Data written to {}'.format(self.data_filename))
        self.plot()

    def create_directory(self):
        """
        create a directory for the results
        :return:
        """
        if self.results_directory is None:
            if type(self.cls) == Parse:
                self.results_directory = os.path.join(os.path.dirname(self.cls.copasi_file),
                                                      'EnsembleTimeCourse')
            else:
                self.results_directory = os.path.join(self.cls.model.root,
                                                      'EnsembleTimeCourse')

        if not os.path.isdir(self.results_directory):
            os.makedirs(self.results_directory)
        return self.results_directory

    def _do_checks(self):
        """

        :return:
        """
        if type(self.cls) == Parse:
            if self.experiment_files is None:
                raise errors.InputError('If parsing estimation data from '
                                        'folder, please specify argument'
                                        ' to experiment_files')

        elif type(self.cls) == tasks.MultiParameterEstimation:
            self.experiment_files = self.cls.experiment_files

        if self.experiment_files is not None:
            if isinstance(self.experiment_files, str):
                self.experiment_files = [self.experiment_files]

                #LOG.debug('type after --> {}'.format(type(self.cls)))
                # if self.results_directory == None:
                #     self.results_directory = self.create_directory()
                # self.results_directory = os.path.join(self.cls.model.root, 'EnsembleTimeCourses' )

    @property
    def parse_experimental_files(self):
        """

        :return:
        """
        df_dct = {}

        if type(self.cls) == Parse:
            exp_files = self.experiment_files
        else:
            exp_files = self.cls.experiment_files

        for i in range(len(exp_files)):
            df = pandas.read_csv(exp_files[i],
                                 sep='\t')
            df_dct[exp_files[i]] = df
        return df_dct

    @property
    def get_experiment_times(self):
        d = {}
        for i in self.experimental_data:
            d[i] = {}
            for j in self.experimental_data[i].keys():

                if j.lower() == 'time':
                    d[i] = self.experimental_data[i][j]

        times = {}
        for i in d:
            times[i] = {}
            times[i]['start'] = d[i].iloc[0]
            times[i]['end'] = d[i].iloc[-1]
            times[i]['step_size'] = d[i].iloc[1] - d[i].iloc[0]
            '''
            subtract 1 from intervals to account for header
            '''
            times[i]['intervals'] = int(d[i].shape[0]) - 1
        return times

    @cached_property
    def simulate_ensemble(self):
        """

        """

        ## collect end times for each experiment
        ##in order to find the biggest
        end_times = []
        for i in self.exp_times:
            ## start creating a results dict while were at it
            end_times.append(self.exp_times[i]['end'])
        intervals = max(end_times) / self.step_size
        d = {}
        for i in range(self.data.shape[0]):
            I = model.InsertParameters(self.cls.model, df=self.data, index=i, inplace=True)

            if not self.silent:
                LOG.info('inserting parameter set {}'.format(i))
                LOG.info(I.parameters.transpose().sort_index())
            TC = tasks.TimeCourse(I.model,
                                  end=max(end_times),
                                  step_size=self.step_size,
                                  intervals=intervals,
                                  plot=False,
                                  run=self.run_mode)
            if self.check_as_you_plot:
                self.cls.model.open()
            d[i] = self.parse(TC, log10=False)
        return pandas.concat(d)


    @property
    def observables(self):
        """
        return list of observables
        :return:
        """
        obs = []
        for i in self.experimental_data:
            obs += list(self.experimental_data[i].keys())
        return list(set([i for i in obs if str(i).lower() != 'time']))


    def plot(self):
        """

        """
        if self.y == None:
            self.y = list(self.ensemble_data.keys())

        if isinstance(self.y, list) != True:
            self.y = [self.y]

        for param in self.y:
            if param not in self.ensemble_data.keys():
                raise errors.InputError('{} not in your data set. {}'.format(param, sorted(self.ensemble_data.keys())))

        data = self.ensemble_data.reset_index(level=1, drop=True)
        data.index.name = 'ParameterFitIndex'
        data = data.reset_index()
        data.sort_values(by=['Time', 'ParameterFitIndex']).head(5)
        # seaborn.despine()
        for parameter in self.y:
            if parameter not in ['ParameterFitIndex', 'Time']:
                LOG.info('Plotting "{}"'.format(parameter))
                plt.figure()
                # seaborn.set_palette([self.color])
                ax1 = seaborn.tsplot(
                    data=data, time='Time', value=parameter,
                    unit='ParameterFitIndex',
                    err_style='ci_band',
                    estimator=self.estimator,
                    n_boot=self.n_boot,
                    ci=self.ci,
                    color=self.color,
                )

                if parameter in self.observables:
                    for df in self.experimental_data.values():
                        if parameter in df.keys():
                            # plt.figure()
                            ax2 = plt.plot(list(df['Time']), list(df[parameter]), '--', color=self.exp_color,
                                           label='Exp', alpha=0.4, marker='o')


                    sim_patch = mpatches.Patch(color=self.color, label='Sim', alpha=0.4)
                    exp_patch = mpatches.Patch(color=self.exp_color, label='Exp', alpha=0.4)
                    plt.legend(handles=[sim_patch, exp_patch], loc=(1, 0.5))


                if self.title is None:
                    plt.title('{} (n={})'.format(parameter, self.data.shape[0]))

                else:
                    plt.title(self.title)

                if self.ylabel is None:
                    plt.ylabel('{}'.format(self.cls.model.quantity_unit))

                else:
                    plt.ylabel(self.ylabel)

                if self.xlabel is None:
                    plt.xlabel('Time ({})'.format(self.cls.model.time_unit))

                else:
                    plt.xlabel(self.xlabel)

                if self.savefig:
                    self.results_directory = self.create_directory()
                    fname = os.path.join(self.results_directory, '{}.png'.format(misc.RemoveNonAscii(parameter).filter))
                    plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
        if self.show:
            plt.show()

@mixin(tasks.UpdatePropertiesMixin)
@mixin(SaveFigMixin)
@mixin(ParseMixin)
@mixin(CreateResultsDirectoryMixin)
class PlotScan(object):
    """
    TODO: Create visualization facilities for parameter scans.
    """
    def __init__(self, cls, **kwargs):
        self.cls = cls
        self.kwargs = kwargs

        self.default_properties = {
            'x': 'time',
            'y': [i.name for i in self.cls.model.metabolites],
            'log10': False,
            'separate': False,
            'savefig': False,
            'results_directory': None,
            'title': 'TimeCourse',
            'xlabel': None,
            'ylabel': None,
            'show': False,
            'filename': None,
            'dpi': 300,
        }

        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        raise NotImplementedError

        self.data = self.parse(self.cls, self.log10)

    def __str__(self):
        """

        :return:
        """
        return "PlotScan(x='{}', y={}, log10={}, separate={}, savefig={}, results_directory='{}'".format(
            self.x, self.y, self.log10,
            self.separate, self.savefig,
            self.results_directory
        )

@mixin(tasks.UpdatePropertiesMixin)
@mixin(SaveFigMixin)
@mixin(ParseMixin)
@mixin(CreateResultsDirectoryMixin)
class PlotParameterEstimation(PlotKwargs):
    """
    Visualize parameter estimation runs against a single
    parameter estimation. Similar to PlotTimeCourseEnsemble
    but for a single parameter estimation run.



    =========================================       =========================================
    kwarg                                           Description
    =========================================       =========================================
    y                                               `str` or list of `str`. Parameter for plotting
                                                    on y axis. Defaults to all estimated parameters.
    **savefig_kwargs                                see savefig_kwargs for savefig options
    =========================================       =========================================

    """
    def __init__(self, cls, **kwargs):
        """
        :param cls:
            Instance of :py:class:`tasks.ParameterEstimation`

        :param kwargs:

        """
        self.cls = cls
        self.kwargs = kwargs
        self.plot_kwargs = self.plot_kwargs()


        default_y = [i.name for i in self.cls.model.metabolites] + [i.name for i in self.cls.model.global_quantities]
        self.default_properties = {
            'y': None,
            'savefig': False,
            'results_directory': None,
            'title': 'TimeCourse',
            'xlabel': None,
            'ylabel': None,
            'show': False,
            'filename': None,
            'dpi': 300,
            'log10': False,
        }
        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(),'{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, self.log10)
        self.cls.model = self.update_parameters()
        self.plot()


    def __str__(self):
        """

        :return:
        """
        return "PlotParameterEstimation(x='{}', y={}, savefig={}, results_directory='{}'".format(
            self.x, self.y, self.savefig,
            self.results_directory
        )

    def _do_checks(self):


        if not isinstance(self.cls, tasks.ParameterEstimation):
            raise errors.InputError('first argument should be ParameterEstimation calss. Got {}'.format(type(self.cls)))

        if self.results_directory == None:
            self.results_directory = os.path.join(self.cls.model.root,
                                                  'ParameterEstimationPlots')


    def update_parameters(self):
        """
        Use the InsertParameters class to insert estimated
        parameters into the model
        :return: Model
        """
        I = model.InsertParameters(self.cls.model, df=self.data)
        return I.model

    def create_directories(self):
        """
        create a directory in project root called result_directory
        create subfolders with name of experiments
        :return: dict
        """
        directories = {}
        for fle in self.cls.experiment_files:
            _, fle = os.path.split(fle)
            directories[fle] = os.path.join(self.results_directory, fle[:-4])
            if not os.path.isdir(directories[fle]):
                os.makedirs(directories[fle])
        return directories

    def read_experimental_data(self):
        """
        read the experimental data in order to figure
        out how long a time course we need to simulate
        with the new parameters
        :return:
        """
        dct = {}
        for i in self.cls.experiment_files:
            dct[i] = pandas.read_csv(i, sep='\t')
        return dct

    def get_time(self):
        """
        get dict of experiments and max time
        :return:
        """
        dct = {}
        data_dct = self.read_experimental_data()
        for i in data_dct:
            dct[i] = data_dct[i]['Time'].max()
        return dct

    def simulate_time_course(self):
        """
        simulate a timecourse for each experiment
        which may have different simulation lengths
        :return:
        """
        time_dct = self.get_time()
        d = {}
        step_size = 1
        for i in time_dct:
            TC = tasks.TimeCourse(self.cls.model, end=time_dct[i],
                             step_size=step_size, intervals=time_dct[i]/step_size)
            d[i] = self.parse(TC, log10=False)
        return d

    def plot(self):
        """
        plot experimental data versus best parameter sets
        :return:
        """
        if self.y == None:
            self.y = self.read_experimental_data().values()[0].keys()

            ## remove time from default plotting vars
            self.y = [i for i in self.y if i != 'Time']

            ## remove any independent variable from default plotting vars
            self.y = [i for i in self.y if i[-6:] != '_indep']
        exp_data = self.read_experimental_data()
        sim_data = self.simulate_time_course()

        for exp in exp_data:
            for sim in sim_data:
                if exp == sim:
                    for key in self.y:
                        plt.figure()
                        plt.plot(
                            exp_data[exp]['Time'], exp_data[exp][key],
                            label='Exp', linestyle=self.linestyle,
                            marker=self.marker, linewidth=self.linewidth,
                            markersize=self.markersize,
                            alpha=0.5,
                            color='#0E00FA',
                        )
                        plt.plot(
                            sim_data[sim]['Time'], sim_data[sim][key],
                            label='Sim', linestyle=self.linestyle,
                            marker=self.marker, linewidth=self.linewidth,
                            markersize=self.markersize,
                            alpha=0.5,
                            color='#FC0077'
                        )
                        plt.legend(loc=(1, 0.5))
                        plt.title(key)
                        plt.xlabel('Time({})'.format(self.cls.model.time_unit))
                        plt.ylabel('Abundance\n({})'.format(self.cls.model.quantity_unit))
                        if self.savefig:
                            dirs = self.create_directories()
                            exp_key = os.path.split(exp)[1]
                            fle = os.path.join(dirs[exp_key], '{}.png'.format(key))
                            plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
                            LOG.info('figure saved to "{}"'.format(fle))
        if self.show:
            plt.show()


@mixin(tasks.UpdatePropertiesMixin)
@mixin(SaveFigMixin)
@mixin(ParseMixin)
@mixin(CreateResultsDirectoryMixin)
@mixin(TruncateDataMixin)
class Boxplots(PlotKwargs):
    """
    Plot a boxplot for multi parameter estimation data.

    ============    =================================================
    kwarg           Description
    ============    =================================================
    num_per_plot    Number of parameter per plot. Remainder
                    fills up another plot.
    **kwargs        see :ref:`kwargs`  options
    ============    =================================================
    """
    def __init__(self, cls, **kwargs):
        """

        :param cls:
            instance of tasks.MultiParameterEstimation or string .
            Same as :py:class:`PlotTimeCourseEnsemble`


        :param kwargs:
        """
        self.cls = cls
        self.kwargs = kwargs
        self.plot_kwargs = self.plot_kwargs()


        self.default_properties = {'log10': False,
                                   'truncate_mode': 'percent',
                                   'theta': 100,
                                   'num_per_plot': 6,
                                   'xtick_rotation': 'vertical',
                                   'ylabel': 'Estimated Parameter\n Value(Log10)',
                                   'title': 'Parameter Distributions',
                                   'savefig': False,
                                   'results_directory': None,
                                   'dpi': 300,
                                   'show': False}
        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(),'{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
        self.divide_data()
        self.plot()

    def _do_checks(self):
        pass

    def create_directory(self):
        """

        :return:
        """
        if self.results_directory is None:
            if type(self.cls) == Parse:
                self.results_directory = os.path.join(os.path.dirname(
                    self.cls.copasi_file), 'Boxplots')
            else:
                self.results_directory = os.path.join(self.cls.model.root, 'Boxplots')
            if os.path.isdir(self.results_directory) != True:
                os.makedirs(self.results_directory)
        return self.results_directory

    def plot(self):
        """
        Plot multiple parameter estimation data as boxplot
        :return:
        """

        labels = self.divide_data()
        for label_set in range(len(labels)):
            plt.figure()#
            data = self.data[labels[label_set]]
            seaborn.boxplot(data=data )
            plt.xticks(rotation=self.xtick_rotation)
            plt.title(self.title+'(n={})'.format(data.shape[0]))
            plt.ylabel(self.ylabel)
            if self.savefig:
                self.results_directory = self.create_directory()
                fle = os.path.join(self.results_directory,
                                   'Boxplot{}.png'.format(label_set))
                plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
        if self.show:
            plt.show()

    def divide_data(self):
        """
        split data into multi plot
        :return:
        """
        n_vars = len(self.data.keys())
        n_per_plot = self.num_per_plot
#        assert n_per_plot<n_vars,'number of variables per plot must be smaller than the number of variables'
        int_division = n_vars//n_per_plot
        remainder = n_vars-(n_per_plot*int_division)

        l = []
        for i in range(int_division):
            l.append(list(self.data.keys()[i*n_per_plot:(i+1)*n_per_plot]))
        if remainder is not 0:
            l.append(list(self.data.keys()[-remainder:]))
        return l


@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class RssVsIterations(PlotKwargs):
    """

    Plot the ordered residual sum of squares (RSS) objective
    function value against the RSS's rank of best fit.
    See :ref:`kwargs` for list of keyword arguments.
    """

    def __init__(self, cls, **kwargs):
        """

        :param cls:
            Instance of :py:class:`tasks.MultiParameterEstimation`
            Same as :py:class:`PlotTimeCourseEnsemble`

        :param kwargs:
            see :ref:`kwargs`
        """
        self.cls = cls
        self.kwargs = kwargs
        self.plot_kwargs = self.plot_kwargs()


        self.default_properties = {'log10': False,
                                   'truncate_mode': 'percent',
                                   'theta': 100,
                                   'xtick_rotation': 'vertical',
                                   'ylabel': 'Estimated Parameter\n Value(Log10)',
                                   'title': 'Rss Vs Iterations',
                                   'savefig': False,
                                   'results_directory': None,
                                   'dpi': 300,
                                   'show': False}

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10)
        self.plot()

    def _do_checks(self):
        """

        :return:
        """
        pass


    def create_directory(self):
        """
        create a directory for the results
        :return:
        """
        if self.results_directory is None:
            if type(self.cls) == Parse:
                self.results_directory = os.path.join(os.path.dirname(self.cls.copasi_file), 'RssVsIterations')
            else:
                self.results_directory = os.path.join(self.cls.model.root,
                                                  'RssVsIterations')

        if not os.path.isdir(self.results_directory):
            os.makedirs(self.results_directory)
        return self.results_directory

    def plot(self):
        """
        Plot Rss Vs rank of best fit
        :return:
            None
        """
            
        plt.figure()
        plt.plot(range(self.data['RSS'].shape[0]),
                 self.data['RSS'].sort_values(ascending=True),
                 marker='o')
        plt.xticks(rotation=self.xtick_rotation)
        plt.title(self.title+'(n={})'.format(self.data.shape[0]))
        plt.ylabel(self.ylabel)
        plt.xlabel('Rank of Best Fit')
        if self.savefig:
            self.results_directory = self.create_directory()
            fle = os.path.join(self.results_directory, 'RssVsIterations.png')
            plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')

        if self.show:
            plt.show()


@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class Pca(PlotKwargs):
    """
    Use the :py:class:`PCA` function to conduct
    a principle component analysis on the parameter
    estimation data.

    ===================   ====================
    kwargs                Description
    ===================   ====================
    by                    `str` either Determine which axes of parameter estimation
                          data to undergoe data reduction. When ``by='iterations'``
                          the data is reduced to one data point per parameter estimation
                          run. When ``by='parameters'``, data is reduced to one data point
                          per parameter.
    legend_position       `tuple`. When ``by='parameters`` specify the (horizontal, verticle,
                          line spacing) parameter for the legend location and formatting
    cmap                  `str` a valid matplotlib colour map
    annotate              `bool` annotate. Automatically on when ``by='parameters'``
    annotation_fontsize   `int` or `float`. fontsize for annotation
    **kwargs              See :ref:`kwargs for more options
    ===================   ====================
    """

    def __init__(self, cls, **kwargs):
        self.cls = cls
        self.kwargs = kwargs
        self.plot_kwargs = self.plot_kwargs()

        self.default_properties={'sep': '\t',
                                 'truncate_mode': 'percent',
                                 'theta': 100,
                                 'log10': False,
                                 'ylabel': None,
                                 'xlabel': None,
                                 'title': None,
                                 'savefig': False,
                                 'results_directory': None,
                                 'dpi': 300,
                                 'n_components': 2,
                                 'by': 'parameters', ##iterations or parameters
                                 'legend_position': None, ##Horizontal, verticle, line spacing
                                 'legend_fontsize': 25,
                                 'cmap': 'viridis',
                                 'annotate': False,
                                 'annotation_fontsize': 25,
                                 'show': False,
                                 }


        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Pca'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
        self.pca()


    def create_directory(self):
        """
        create a directory for the results
        :return:
        """
        if self.results_directory is None:
            if type(self.cls) == Parse:
                self.results_directory = os.path.join(os.path.dirname(self.cls.copasi_file),
                                                      'PCA')
            else:
                self.results_directory = os.path.join(self.cls.model.root,
                                                  'PCA')

        if not os.path.isdir(self.results_directory):
            os.makedirs(self.results_directory)
        return self.results_directory

    def _do_checks(self):
        """
        varify integrity of user input
        :return:
        """


        if self.by not in ['parameters','iterations']:
            raise errors.InputError('{} not in {}'.format(
                self.by, ['parameters','iterations']))

        # if self.results_directory is None:
        #     self.results_directory = self.create_directory()

        if self.ylabel==None:
            if self.log10==False:
                self.ylabel = 'PC2'
            elif self.log10==True:
                self.ylabel = 'PC2(Log10)'
            else:
                raise errors.SomethingWentHorriblyWrongError('{} not in {}'.format(
                    self.ylabel, [True, False]))
        
        if self.xlabel==None:
            if self.log10==False:
                self.xlabel = 'PC1'
            elif self.log10==True:
                self.xlabel = 'PC1(Log10)'
            else:
                raise errors.SomethingWentHorriblyWrongError(
                    '{} not in {}'.format(self.ylabel, [True, False]))
 
        
        LOG.info('plotting PCA {}'.format(self.by))
        
        if self.by == 'parameters':
            self.annotate=True
            if self.legend_position==None:
                LOG.critical(
                    'When data reduction is by \'parameters\' you should specify an argument to legend_position. i.e. legend_position=(10,10,1.5) for horizontal, vertical and linespacing')


        if self.legend_position is None:
            self.legend_position = (1, 1, 0.5) ##horizontal, verticle, linespacing

    def pca(self):
        pca = PCA(n_components=self.n_components)
        rss = self.data.RSS
        self.data = self.data.drop('RSS',axis=1)
        fig, ax = plt.subplots()
        if self.by == 'parameters':
            projected = pca.fit(self.data.transpose()).transform(self.data.transpose())
            projected = pandas.DataFrame(projected, index=self.data.columns)
            labels = self.data.columns
            title = 'PCA by Parameters (n={})'.format(len(labels))
            sc = ax.scatter(projected[0], projected[1])


        else:
            projected = pca.fit(self.data).transform(self.data)
            projected = pandas.DataFrame(projected, index=self.data.index)
            labels = list(self.data.index)
            title = 'PCA by Iterations (n={})'.format(len(labels))
            projected = pandas.concat([rss, projected], axis=1)
            sc = ax.scatter(projected[0], projected[1], c=projected['RSS'], cmap=self.cmap)
            cb = plt.colorbar(sc)
            cb.ax.set_title('RSS')
            
            
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.title(title)
        #TODO connect copasi with the python community
        #TODO mjor selling point for pycoools.
        #TODO interafce with pysces, pyDStools and sloppycell
        for i, txt in enumerate(labels):
            if self.annotate:
                ax.annotate(str(i), (projected[0][i], projected[1][i]),
                            fontsize=self.annotation_fontsize)
            if self.by == 'parameters':
                ax.text(self.legend_position[0],
                        self.legend_position[1]-i*self.legend_position[2],
                    '{}: {}'.format(i,txt),fontsize=self.legend_fontsize)
        if self.savefig:
            self.create_directory()
            fle = os.path.join(self.results_directory, 'Pca_by_{}'.format(self.by))
            plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')

@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class Histograms(PlotKwargs):
    """
    Plot a Histograms for multi parameter estimation data.

    See :ref:`kwargs` for more options.
    """

    def __init__(self, cls, **kwargs):
        """

        :param cls:
            Instance of :py:class:`tasks.MultiParameterEstimation`
            Same as :py:class:`PlotTimeCourseEnsemble`

        :param kwargs:
        """
        self.cls = cls
        self.kwargs = kwargs
        self.plot_kwargs = self.plot_kwargs()

        self.default_properties = {'sep': '\t',
                                   'log10': False,
                                   'truncate_mode': 'percent',
                                   'theta': 100,
                                   'xtick_rotation': 'horizontal',
                                   'ylabel': 'Frequency',
                                   'savefig': False,
                                   'results_directory': None,
                                   'dpi': 300,
                                   'title_fontsize': 35,
                                   'show': False}

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Histograms'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
        LOG.info('plotting histograms')
        # self.plot()
        self.coloured_plot()


    def _do_checks(self):
        """

        :return:
        """
        if self.results_directory is None:
            if type(self.cls) == Parse:
                self.results_directory = os.path.join(os.path.dirname(self.cls.copasi_file), 'Histograms')
            else:
                self.results_directory = os.path.join(self.cls.model.root, 'Histograms')


    def plot(self):
        """
        
        """
        for parameter in self.data.keys():
            plt.figure()
            seaborn.distplot(self.data[parameter])
            plt.ylabel(self.ylabel)
            plt.title('{},n={}'.format(parameter, self.data[parameter].shape[0]),
                      fontsize=self.title_fontsize)
            if self.savefig:
                self.create_directory(self.results_directory)
                fname = os.path.join(self.results_directory,
                                     misc.RemoveNonAscii(parameter).filter+'.png')
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')

    def coloured_plot(self):
        """

        :return:
        """
        # for parameter in self.data.keys():
        raise NotImplementedError('this is an attempt to colour bars '
                                  'of histogram by RSS but the code does not '
                                  'work. ')
        parameter = 'Ski'
        num_bins = 10
        width = self.data[parameter].max() - self.data[parameter].min()
        iqr = scipy.stats.iqr(self.data[parameter])
        bins_size = 2 * (iqr/(self.data[parameter].shape[0]**1.0/3.0))
        LOG.debug('bin size == {}'.format(bins_size))

        bins = numpy.arange(self.data[parameter].min(), self.data[parameter].max(),
                            bins_size)#width/num_bins
        ## calculate the density of RSS
        LOG.debug('bins --> {}'.format(bins))

        groups = self.data.groupby([pandas.cut(self.data[parameter], bins), 'RSS'])
        data = groups.size().reset_index([parameter, 'RSS'])
        data2 = data.groupby(parameter)[0].sum()
        # print data2
        data3 = data.groupby(parameter)['RSS'].mean()
        # print data3
        data5 = pandas.concat([data2, data3], axis=1)
        data5['Density'] = data5[0]/(numpy.sum(data5[0].fillna(0).values * numpy.diff(bins)))


        ## colours
        norm = plt.Normalize(numpy.nanmin(data5['RSS'].values),
                             numpy.nanmax(data5['RSS'].values))
        colours = plt.cm.plasma(norm(data5['RSS'].fillna(0).values))

        fig, ax = plt.subplots()

        ax.bar(bins[:-1], data5.fillna(0)['Density'], width=width, color=colours, align='edge')

        # seaborn.kdeplot(data[parameter], ax=ax, color='k', lw=2)

        sm = plt.cm.ScalarMappable(cmap='plasma', norm=norm)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, label='RSS')
        ax.set_ylabel('Density')
        ax.set_xlabel(parameter)
        plt.show()



@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class Scatters(PlotKwargs):
    """
    Plot scatter graphs. When 'x' and 'y' are lists, 2 way
    combinations are automatically plotted and organized into
    folders (when ``savefig=True``). Data is automatically
    coloured by RSS.

    ========    =================================================
    kwarg       Description
    ========    =================================================
    x           `str` or `list` of `str`. Variable(s) to plot on x
                axis. Defaults to ``RSS``
    y           `str` or `list` of `str`. Variable(s) to plot on
                y axis. Defaults to all parameters in data set.
    cmap        `str` a valid matplotlib colour map

    **kwargs    see :ref:`kwargs` for more options
    ========    =================================================
    """

    def __init__(self, cls, **kwargs):
        """

        :param cls:
            Instance of :py:class:`tasks.MultiParameterEstimation`
            Same as :py:class:`PlotTimeCourseEnsemble`

        :param kwargs:
        """
        self.cls = cls
        self.kwargs = kwargs
        self.plot_kwargs = self.plot_kwargs()

        self.default_properties = {
            'x':'RSS',
            'y': None,
            'sep': '\t',
            'log10': False,
            'cmap': 'jet_r',
            'truncate_mode': 'percent',
            'theta': 100,
            'xtick_rotation': 'horizontal',
            'ylabel': 'Frequency',
            'savefig': False,
            'results_directory': None,
            'dpi': 300,
            'title_fontsize': 35,
            'show': False}

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Scatters'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
        self.plot()

    def _do_checks(self):
        """

        :return:
        """
        if isinstance(self.x, str):
            self.x = [self.x]

        if self.results_directory is None:
            self.results_directory = os.path.join(self.cls.model.root, 'Scatters')

    def plot(self):
        """

        :return:
        """
        if self.y is None:
            self.y = self.data.keys()

        for x_var in self.x:
            if x_var not in sorted(list(self.data.keys())):
                raise errors.InputError('"{}" invalid. These are valid: "{}"'.format(
                    x_var, self.data.keys()
                ))
            for y_var in self.y:
                if x_var not in sorted(list(self.data.keys())):
                    raise errors.InputError('"{}" invalid. These are valid: "{}"'.format(
                        y_var, self.data.keys()
                    )
                )
                LOG.info('Plotting "{}" Vs "{}"'.format(x_var, y_var))
                plt.figure()
                plt.scatter(
                    self.data[x_var], self.data[y_var],
                    cmap=self.cmap, c=self.data['RSS'],
                )
                cb = plt.colorbar()
                if self.log10:
                    cb.set_label('log10(RSS)')
                    plt.xlabel("log10({})".format(x_var))
                    plt.ylabel('log10({})'.format(y_var))
                else:
                    cb.set_label('RSS')
                    plt.xlabel(x_var)
                    plt.ylabel(y_var)
                plt.title('Scatter graph of\n {} Vs {}.(n={})'.format(
                    x_var, y_var, self.data.shape[0]
                    )
                )
                if self.savefig:
                    x_dir = os.path.join(self.results_directory, x_var)
                    self.create_directory(x_dir)
                    fle = os.path.join(x_dir, '{}.png'.format(y_var))
                    plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')

        if self.show:
            plt.show()

@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class LinearRegression(PlotKwargs):
    """
    Perform multiple linear regression using
    :py:module:`sklearn.linear_model`.

    ========    =================================================
    kwarg       Description
    ========    =================================================
    lin_model   `func`. default=LassoCV. Any linear model supported
                by :py:module:`sklearn.linear_model`. see `here`

                .. _here: http://scikit-learn.org/stable/modules/linear_model.html

    n_alphas    `int` number of alphas
    max_iter    `int`. Number of iterations.
    **kwargs    see :ref:`kwargs` for more options
    ========    =================================================

    """

    def __init__(self, cls, **kwargs):
        """

        :param cls:
            Instance of :py:class:`tasks.MultiParameterEstimation`
            Same as :py:class:`PlotTimeCourseEnsemble`

        :param kwargs:
        """
        self.cls = cls
        self.kwargs = kwargs
        self.plot_kwargs = self.plot_kwargs()

        self.default_properties = {
            'lin_model': linear_model.LassoCV,
            'log10': False,
            'truncate_mode': 'percent',
            'theta': 100,
            'xtick_rotation': 'horizontal',
            'ylabel': 'Frequency',
            'savefig': False,
            'results_directory': None,
            'dpi': 300,
            'title_fontsize': 35,
            'show': False,
            'n_alphas': 100,
            'max_iter': 20000
        }

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for LinearRegression'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)

        self.scores, self.coef = self.compute_coefficients()
        self.coef = self.coef.fillna(value=0)
        
        self.plot_rss()
        self.plot_scores()
        self.plot_coef()

    def _do_checks(self):
        """

        :return:
        """
        if self.results_directory is None:
            self.results_directory = os.path.join(self.cls.model.root, 'LinearRegression')


    def compute1coef(self, parameter):
        """
        Compute coefficients for a single parameter
        using self['lin_model'] from sklearn
        """
        y = numpy.array(self.data[parameter])
        X = self.data.drop(parameter, axis=1)
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y)

        lin_model = self.lin_model(fit_intercept=True, n_alphas=self.n_alphas,
                    max_iter=self.max_iter)

        lin_model.fit(X_train, y_train)
        df = pandas.DataFrame(lin_model.coef_, index=X.columns, columns=[parameter])#.sort_values(by='Coefficients')
        df['abs_values'] = numpy.absolute(df[parameter])
        df = df.sort_values(by='abs_values', ascending=False)
        df = df.drop('abs_values', axis=1)
        scores = [lin_model.score(X_train, y_train), lin_model.score(X_test, y_test)]
        scores = pandas.DataFrame(scores, index=['TrainScore', 'TestScore'])
        return scores, df

    def compute_coefficients(self):
        parameters = list(self.data.columns)
        df_dct = {}
        score_dct={}
        for y in parameters:
            score_dct[y], df_dct[y] = self.compute1coef(y)

        df1 = pandas.concat(score_dct,axis=1).transpose().sort_values(by='TestScore',
                           ascending=False)
        df2 = pandas.concat(df_dct,axis=1)
        return df1, df2

    def plot_scores(self):
        """

        """
        plt.figure()
        seaborn.heatmap(self.scores)
        plt.title('Model Fitting Test and Train Scores'+'(n={})'.format(self.data.shape[0]),
                  fontsize=self.title_fontsize)
        if self.savefig:
            save_dir = os.path.join(self.results_directory, 'LinearRegression')
            self.create_directory(self.results_directory)
            fname = os.path.join(self.results_directory, 'linregress_scores.png')
            plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')


    def plot_rss(self):
        plt.figure()
        seaborn.heatmap(self.coef.RSS.sort_values(by='RSS', ascending=False))
        plt.title('Lasso Regression \n(Y=RSS) (n={})'.format(self.data.shape[0]), fontsize=self.title_fontsize)
        if self.savefig:
            self.create_directory(self.results_directory)
            fname = os.path.join(self.results_directory, 'linregress_RSS.png')
            plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')


    def plot_coef(self):
        """

        :return:
        """
        self.coef = self.coef.drop('RSS', axis=1)
        self.coef = self.coef.drop('RSS', axis=0)
        plt.figure()
        seaborn.heatmap(self.coef)
        plt.title('Coefficient Heatmap',fontsize=self.title_fontsize)
        plt.xlabel('')
        if self.savefig:
            self.create_directory(self.results_directory)
            fname = os.path.join(self.results_directory, 'linregress_parameters.png')
            plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')


@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class ModelSelection(object):
    """
    Calculate model selection criteria AIC (corrected) and
    BIC for a selection of models that have undergone fitting
    using the :py:class:`tasks.MultiModelFit` class. Plot as
    boxplots and histograms.
    """

    def __init__(self, multi_model_fit, savefig=False,
                 dpi=300, log10=False, filename=None, pickle=None):
        """

        :param multi_model_fit:
            a :py:class:`tasks.MultiModelFit` object

        :param filename:
            `str` file to save model selection data to

        :param pickle:
            `str` pickle path to save data too
        """
        self.multi_model_fit = multi_model_fit
        self.number_models = self.get_num_models()
        self.savefig = savefig
        self.results_directory = self.multi_model_fit.project_dir
        self.dpi = dpi
        self.log10 = log10
        self.filename = filename
        self.pickle = pickle
        self._do_checks()

        ## do model selection stuff
        self.results_folder_dct = self._get_results_directories()
        self.model_dct = self._get_model_dct()
        self.data_dct = self._parse_data()
        self.number_model_parameters = self._get_number_estimated_model_parameters()
        self.number_observations = self._get_n()
        self.model_selection_data = self.calculate_model_selection_criteria()

        self.to_csv(self.filename)
        self.boxplot()

    def __iter__(self):
        for MPE in self.multi_model_fit:
            yield MPE

    def __getitem__(self, item):
        return self.multi_model_fit[item]

    def __setitem__(self, key, value):
        self.multi_model_fit[key] = value

    def __delitem__(self, key):
        del self.multi_model_fit[key]

    def keys(self):
        return self.multi_model_fit.keys()

    def values(self):
        return self.multi_model_fit.values()

    def items(self):
        return self.multi_model_fit.items()

    def _do_checks(self):
        """

        :return:
        """
        if self.filename is None:
            save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
            self.filename = os.path.join(save_dir, 'ModelSelectionCriteria.csv')

        # if self.pickle is None:
        #     self.pickle = os.path.splitext(self.filename)[0]+'.pickle'

    def _get_results_directories(self):
        '''
        Find the results directories embedded within MultimodelFit
        and RunMutliplePEs.
        '''
        return  self.multi_model_fit.results_folder_dct

    def get_num_models(self):
        return len(self.multi_model_fit.cps_files)

    def to_excel(self, filename=None):
        if filename is None:
            filename = self.filename[:-4]+'.xlsx'
        self.model_selection_data.to_excel(filename)

    def to_csv(self, filename=None):
        if filename is None:
            filename = self.filename
        LOG.info('model selection data saved to {}'.format(filename))
        self.model_selection_data.to_csv(filename)

    def to_pickle(self, filename=None):
        if filename is None:
            filename = os.path.splitext(self.filename)[0]+'.pickle'

        LOG.info('model selection pickle saved to {}'.format(filename))
        self.model_selection_data.to_pickle(filename)

    def _get_model_dct(self):
        """
        Get a model dct. The model must be a configured model
        (i.e. not the original and with a number after it)
        :return:
        """
        dct={}
        for MPE in self.multi_model_fit:

            ## get the first cps file configured for eastimation in each MMF obj
            cps_1 = glob.glob(
                os.path.join(
                    os.path.dirname(MPE.results_directory),
                    '*_1.cps')
            )[0]
            dct[MPE.results_directory] = model.Model(cps_1)
        return dct

    def _parse_data(self):
        '''

        '''
        if self.pickle is not None:
            #     self.pickle = os.path.splitext(self.filename)[0]+'.pickle'
            return pandas.read_pickle(self.pickle)
        else:
            dct={}
            for MPE in self.multi_model_fit:

                ## get the first cps file configured for eastimation in each MMF obj
                cps_1 = glob.glob(
                    os.path.join(
                        os.path.dirname(MPE.results_directory),
                        '*_1.cps')
                )[0]
                dct[cps_1] = Parse(MPE.results_directory,
                                   copasi_file=cps_1,
                                   log10=self.log10)
            return dct

    def _get_number_estimated_model_parameters(self):
        k_dct={}
        for mod in self.model_dct.values():
            k_dct[mod.copasi_file] = len(mod.fit_item_order)
        return k_dct

    def _get_n(self):
        '''
        get number of observed data points for AIC calculation
        '''
        n={}
        for exp in self.multi_model_fit.exp_files:
            data=pandas.read_csv(exp,sep='\t')
            l=[]
            for key in data.keys() :
                if key.lower()!='time':
                    if key[-6:]!='_indep':
                        l.append(int(data[key].shape[0]))
            n[exp]=sum(l)
        n=sum(n.values())
        return n

    def calculate1AIC(self,RSS,K,n):
        """
        Calculate the corrected AIC:

            AICc = -2*ln(RSS/n) + 2*K + (2*K*(K+1))/(n-K-1)

            or if likelihood function used instead of RSS

            AICc = -2*ln(likelihood) + 2*K + (2*K*(K+1))/(n-K-1)

        Where:
            RSS:
                Residual sum of squares for model fit
            n:
                Number of observations collectively in all data files

            K:
                Number of model parameters
        """
        return n*numpy.log((RSS/n)) + 2*K + (2*K*(K+1))/(n-K-1)


    def calculate1BIC(self,RSS,K,n):
        '''
        Calculate the bayesian information criteria
            BIC = -2*ln(likelihood) + k*ln(n)

                Does this then go to:

            BIC = -2*ln(RSS/n) + k*ln(n)
        '''
        return  (n*numpy.log(RSS/n) ) + K*numpy.log(n)

    def calculate_model_selection_criteria(self):
        '''

        '''
        df_dct = {}
        for model_num in range(len(self.model_dct)):
            keys = self.model_dct.keys()
            cps_key = self.model_dct[keys[model_num]].copasi_file

            k = self.number_model_parameters[cps_key]
            n = self.number_observations #constant throughout analysis
            rss = self.data_dct[cps_key].data.RSS
            aic_dct = {}
            bic_dct = {}
            for i in range(len(rss)):
                aic = self.calculate1AIC(rss.iloc[i], k, n)
                bic = self.calculate1BIC(rss.iloc[i], k, n)
                aic_dct[i] = aic
                bic_dct[i] = bic
            aic = pandas.DataFrame.from_dict(aic_dct,orient='index')
            rss = pandas.DataFrame(rss)
            bic = pandas.DataFrame.from_dict(bic_dct,orient='index')
            df = pandas.concat([rss, aic,bic],axis=1)
            df.columns = ['RSS', 'AICc', 'BIC']
            df.index.name = 'RSS Rank'
            df_dct[os.path.split(cps_key)[1][:-6]] = df
        df = pandas.concat(df_dct, axis=1)
        return df

    def boxplot(self):
        """

        :return:
        """
        seaborn.set_context(context='poster')
        data = self.model_selection_data

        data = data.unstack()
        data = data.reset_index()
        data = data.rename(columns={'level_0': 'Model',
                                    'level_1': 'Metric',
                                    0: 'Score'})
        for metric in data['Metric'].unique():
            plt.figure()
            seaborn.boxplot(data=data[data['Metric'] == metric],
                            x='Model', y='Score')
            plt.xticks(rotation='vertical')
            plt.title('{} Scores'.format(metric))
            plt.xlabel(' ')
            if self.savefig:
                save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
                if os.path.isdir(save_dir)!=True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, 'boxplot_{}.png'.format(metric))
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                LOG.info('boxplot saved to : "{}"'.format(fname))


    def histogram(self):
        """

        :return:
        """
        seaborn.set_context(context='poster')
        data = self.model_selection_data

        data = data.unstack()
        data = data.reset_index()
        data = data.rename(columns={'level_0': 'Model',
                                    'level_1': 'Metric',
                                    0: 'Score'})
        for label, df in data.groupby(by=['Metric']):
            plt.figure()
            for label2, df2 in df.groupby(by='Model'):
                plot_data = df2['Score'].dropna()
                seaborn.kdeplot(plot_data, shade=True, label=label2,
                                legend=True)
                plt.title("{} Score (n={})".format(label, plot_data.shape[0]))
                plt.ylabel("Frequency")
                plt.xlabel("Score".format(label, plot_data.shape[0]))
                plt.legend(loc=(0, -0.5))


            if self.savefig:
                save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
                if os.path.isdir(save_dir) != True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, 'Histogram_{}_{}.png'.format(label2, label))
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                LOG.info('histograms saved to : "{}"'.format(fname))

    def chi2_lookup_table(self, alpha):
        '''
        Looks at the cdf of a chi2 distribution at incriments of
        0.1 between 0 and 100.

        Returns the x axis value at which the alpha interval has been crossed,
        i.e. gets the cut off point for chi2 dist with DOF and alpha .
        '''
        nums = numpy.arange(0,100,0.1)
        table=zip(nums, scipy.stats.chi2.cdf(nums,self.kwargs.get('DOF')) )
        for i in table:
            if i[1]<=alpha:
                chi2_df_alpha=i[0]
        return chi2_df_alpha

    def get_chi2_alpha(self):
        '''
        return the chi2 threshold for cut off point alpha and DOF degrees of freedom
        '''
        dct={}
        alphas=numpy.arange(0,1,0.01)
        for i in alphas:
            dct[round(i,3)]=self.chi2_lookup_table(i)
        return dct[0.05]

    def compare_sim_vs_exp(self):
        '''

        '''
        LOG.info('Visually comparing simulated Versus Experiemntal data.')

        for cps, res in self.multi_model_fit.results_folder_dct.items():
            tasks.InsertParameters(cps,parameter_path=res, index=0)
            PE=tasks.ParameterEstimation(cps,self.multi_model_fit.exp_files,
                                       randomize_start_values=False,
                                       method='CurrentSolutionStatistics',
                                       plot=True,savefig=True,
                                       )
            PE.set_up()
            PE.run()
            PE.format_results()


    def get_best_parameters(self,filename=None):
        '''

        '''
        df=pandas.DataFrame()
        for cps, res in self.multi_model_fit.results_folder_dct.items():
            df[os.path.split(cps)[1]]= ParsePEData(res).data.iloc[0]

        if filename==None:
            return df
        else:
            df.to_excel(filename)
            return df



    def compare_model_parameters(self,parameter_list,filename=None):
        '''
        Compare all the parameters accross multiple models
        in a bar chart averaging and STD for a parameter accross
        all models.

        May have a problem with different models have different
        parameters as they are not directly comparible
        '''
        best_parameters=self.get_best_parameters()
        data= best_parameters.loc[parameter_list].transpose()
        f=seaborn.barplot(data=numpy.log10(data))
        f.set_xticklabels(parameter_list,rotation=90)
        plt.legend(loc=(1,1))
        plt.title('Barplot Comparing Parameter Estimation Results for specific\nParameters accross all models')
        plt.ylabel('log10(parameter_value),Err=SEM')
        if filename!=None:
            plt.savefig(filename,dpi=200,bbox_inches='tight')
#

@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class PlotProfileLikelihood(object):
    """

    """
    def __init__(self, cls, data=None, **kwargs):
        """
        Plot profile likelihoods
        :param data:
        :param kwargs:
        """
        self.cls = cls


        self.default_properties = {'x': None,
                                   'y': None,
                                   'log10': True,
                                   'estimator': numpy.mean,
                                   'n_boot': 10000,
                                   'ci_band_level': 95,  ## CI for estimator bootstrap
                                   'err_style': 'ci_band',
                                   'savefig': False,
                                   'results_directory': self.cls.model.root,
                                   'dpi': 300,
                                   'plot_cl': True,
                                   'title': None,
                                   'xlabel': None,
                                   'ylabel': None,
                                   'color_palette': 'bright',
                                   'legend_location': None,
                                   'show': False,

                                   }

        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Scatters'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)

        ## parse data
        self.data = Parse(cls, log10=self.log10).data

        ## do some checks
        self._do_checks()

        ## do plotting
        self.plot()

    def _do_checks(self):
        if isinstance(self.data, pandas.core.frame.DataFrame) != True:
            raise errors.InputError('{} should be a dataframe. Parse data with ParsePEData first.'.format(self.data))

        self.parameter_list = sorted(list(self.data.columns))

        if self.x == None:
            raise errors.InputError('x cannot be None')

        if self.y == None:
            self.y = self.parameter_list

        if self.y == None:
            raise errors.InputError('y cannot be None')

        if self.x not in self.parameter_list:
            raise errors.InputError('{} not in {}'.format(self.x, self.parameter_list))

        if isinstance(self.y, str):
            if self.y not in self.parameter_list:
                raise errors.InputError('{} not in {}'.format(self.y, self.parameter_list))

        if isinstance(self.y, list):
            for y_param in self.y:
                if y_param not in self.parameter_list:
                    raise errors.InputError('{} not in {}'.format(y_param, self.parameter_list))

        if self.savefig:
            if self.results_directory == None:
                raise errors.InputError('Please specify argument to results_directory')

        n = list(set(self.data.index.get_level_values(0)))
        if self.title == None:
            self.title = 'Profile Likelihood for\n{} (Rank={})'.format(self.x, n)

        self.data.rename(columns={'ParameterOfInterestValue': self.x})

    #
    # def __getitem__(self, key):
    #     if key not in self.kwargs:
    #         raise errors.InputError('{} not in {}'.format(key, self.kwargs.keys()))
    #     return self.kwargs[key]
    #
    # def __setitem__(self, key, value):
    #     self.kwargs[key] = value
    #
    def plot(self):
        """

        """
        if self.y == self.x:
            LOG.warning(errors.InputError(
                'x parameter {} cannot equal y parameter {}. Plot function returned None'.format(
                    self.x, self.y)
            )
            )
            return None

        ## get x data
        # data = self.data.reset_index()
        # x_data = self.data[self.x]
        # print x_data
        self.data.to_csv('/home/b3053674/Documents/Models/2017/10_Oct/Smad7ZiModels2/PL/data.csv')
        # x_data = pandas.DataFrame(self.data[self.x])

        # for label, df in self.data.groupby(level=[1]):
        #     pass
            # if label == self.x:
            #         data = df[self.y]
            # if isinstance(data, pandas.core.frame.Series):
            #     data = pandas.DataFrame(data)
            # if isinstance(data, pandas.core.frame.DataFrame):
            #     data = pandas.DataFrame(data.stack(), columns=['Value'])
            # print data
            # try:
            #     data.index = data.index.rename(['ParameterSetRank',
            #                                     'ConfidenceLevel',
            #                                     'ParameterOfInterest',
            #                                     'ParameterOfInterestValue',
            #                                     'YParameter'])
            # except UnboundLocalError:
            #     return 1
            #
            # data = data.reset_index()
            # if self.log10:
            #     data['ConfidenceLevel'] = numpy.log10(data['ConfidenceLevel'])
            #     data['Value'] = numpy.log10(data['Value'])
            #     data['ParameterOfInterestValue'] = numpy.log10(data['ParameterOfInterestValue'])
            #
            # plt.figure()
            # if self.plot_cl:
            #     cl_data = data[['ParameterSetRank', 'ConfidenceLevel',
            #                     'ParameterOfInterestValue']]
            #     cl_data = cl_data.drop_duplicates()
            #     seaborn.tsplot(data=cl_data,
            #                    time='ParameterOfInterestValue',
            #                    value='ConfidenceLevel',
            #                    unit='ParameterSetRank',
            #                    color='green', linestyle='--',
            #                    estimator=self.estimator,
            #                    err_style=self.err_style,
            #                    n_boot=self.n_boot,
            #                    ci=self.ci_band_level)
            #
            # seaborn.color_palette('husl', 8)
            # seaborn.tsplot(data=data,
            #                time='ParameterOfInterestValue',
            #                value='Value',
            #                condition='YParameter',
            #                unit='ParameterSetRank',
            #                estimator=self.estimator,
            #                err_style=self.err_style,
            #                n_boot=self.n_boot,
            #                ci=self.ci_band_level,
            #                color=seaborn.color_palette(self.color_palette, len(self.y))
            #                )
            # plt.title(self.title)
            # if self.ylabel != None:
            #     plt.ylabel(self.ylabel)
            # if self.xlabel != None:
            #     plt.xlabel(self.x_label)
            #
            # if self.legend_location != None:
            #     plt.legend(loc=self.legend_location)
            #
            # if self.savefig:
            #     #            save_dir = os.path.join(self['results_directory'], 'ProfileLikelihood')
            #     if os.path.isdir(self.results_directory) != True:
            #         os.makedirs(self.results_directory)
            #     os.chdir(self.results_directory)
            #     fle = os.path.join(self.results_directory, '{}Vs{}.jpeg'.format(self.x, self.y))
            #     plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
            #     LOG.info('figure saved to --> {}'.format())
            #
            # if self.show:
            #     plt.show()

@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class ParsePLData(object):
    """
    get data from file into an appropriate format
    1) ensure data is properly formatted with headers
    2) read data into a df.
        index 1 = parameter set
        index 2 = parameter of interest
        index 3 = best parameter value
        index 4 = parameter scan value
            data = matrix
    """

    def __init__(self, copasi_file, pl_directory, **kwargs):
        self.copasi_file = copasi_file
        self.pl_directory = pl_directory
        self.copasiML = tasks.CopasiMLParser(self.copasi_file).copasiML

        options = {'parameter_path': None,
                   'index': -1,
                   'rss': None,
                   'dof': None,
                   'num_data_points': None,
                   'experiment_files': None,
                   'alpha': 0.95,
                   'log10': True,
                   }

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Scatters'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()


        if self.parameter_path == None:
            if self.rss == None:
                raise errors.InputError('If parameter_path equals None then rss must not equal None')
        if self.parameter_path != None:
            if self.index == -1:
                raise errors.InputError(
                    'An argument is given to parameter_path but index is -1 (for PL around current parameter set). Change the index parameter')

        if self.index != -1:
            if selfparameter_path == None:
                raise errors.InputError(
                    'If index is not -1 (i.e. current parameter set in model) then an argument to parameter_path needs to be specified')

        if self.experiment_files == None:
            self.experiment_files = self.get_experiment_files_in_use()

        self.index_dirs = self.get_index_dirs()

        self.pl_data_files = self.get_pl_data_files()
        self.pl_data_files = self.format_pl_data_files()
        self.data = self.parse_data()
        self.data = self.infer_parameter_of_interest()
        if self.dof == None:
            self.dof = self.get_dof()

        if self.num_data_points == None:
            self.num_data_points = self.get_num_data_points()

        if self.rss == None:
            self.rss = self.get_rss()

        self.data = self.get_confidence_level()
        self.data = self.data.drop('ParameterFile', axis=1)

    def get_index_dirs(self):
        """
        Under the ProfileLikelihood folder are a list of folders named after
        the integer rank of best fit (.e. -1,0,1,2 ...)
        returns list of these directories
        :return:
        """
        l = []
        for i in glob.glob(os.path.join(self.pl_directory, '*')):
            if os.path.isdir(i):
                dire, fle = os.path.split(i)
                try:
                    int(fle)
                    l.append(i)
                except ValueError:
                    LOG.warning(
                        '{} is not a number and therefore does not contain a profile likleihood analysis. It will be ignored')
                    continue
                if os.path.isdir(i) != True:
                    raise errors.FolderDoesNotExistError(i)
        return l

    def get_pl_data_files(self):
        """
        return all text files in
        """
        res = {}
        for index_dir in self.index_dirs:
            i = os.path.split(index_dir)[1]
            try:
                int(i)
            except ValueError:
                raise errors.InputError(
                    'Cannot convert {} to int. Check there are no extra files in your profile likelihood directory'.format(
                        i))
            res[int(i)] = {}
            for f in glob.glob(os.path.join(index_dir, '*.txt')):
                dire, fle = os.path.split(f)
                res[int(i)][fle] = f
        if res == {}:
            raise errors.InputError(
                'Can\'t find PL data files. Have you given the correct path to profile likelihood directory?')

        return res

    def format_pl_data_files(self):
        """

        """
        res = {}
        for i in self.pl_data_files:
            res[i] = {}
            for j in self.pl_data_files[i]:
                cps = self.pl_data_files[i][j][:-4] + '.cps'
                try:
                    res[i][j] = FormatPLData(cps, self.pl_data_files[i][j]).format
                except errors.FileDoesNotExistError:
                    pass
        return res

    def parse_data(self):
        """

        """
        res = {}
        df_dct = {}
        for index in self.pl_data_files:
            res[index] = {}
            for data_file in self.pl_data_files[index]:
                df_temp = pandas.read_csv(self.pl_data_files[index][data_file],
                                          sep='\t', index_col=0)
                res[index][data_file] = pandas.read_csv(self.pl_data_files[index][data_file],
                                                        sep='\t',
                                                        index_col=0)
            df_dct[index] = pandas.concat(res[index])
        df = pandas.concat(df_dct)
        df.index = df.index.rename(['ParameterSetRank', 'ParameterFile', 'ParameterOfInterestValue'])
        return df

    def infer_parameter_of_interest(self):
        """
        """
        parameters = sorted(list(self.data.columns))
        filenames = sorted(list(set(self.data.index.get_level_values(1))))
        #        print parameters, filenames
        zipped = dict(zip(filenames, parameters))
        self.data = self.data.reset_index(level=1)
        l = []
        for i in self.data['ParameterFile']:
            l.append(zipped[i])
        self.data['ParameterOfInterest'] = l
        return self.data

    def get_experiment_files_in_use(self):
        '''
        Need to exclude data files fromlist of parameters to plot
        '''
        query = '//*[@name="File Name"]'
        l = []
        for i in self.copasiML.xpath(query):
            f = os.path.abspath(i.attrib['value'])
            if os.path.isfile(f) != True:
                raise errors.InputError(
                    'Experimental files in use cannot be automatically '
                    ' determined. Please give a list of experiment file '
                    'paths to the experiment_files keyword'.format())
            l.append(os.path.abspath(i.attrib['value']))
        return l

    def get_dof(self):
        '''
        The number of parameters being estimated minus 1
        '''
        GMQ = tasks.GetModelQuantities(self.copasi_file)
        return len(GMQ.get_fit_items().keys()) - 1

    #        return self.get_num_estimated_paraemters()-1

    def get_num_data_points(self):
        '''
        returns number of data points in your data files
        '''
        experimental_data = [pandas.read_csv(i, sep='\t') for i in self.experiment_files]
        l = []
        for i in experimental_data:
            l.append(i.shape[0] * (i.shape[1] - 1))
        s = sum(l)
        if s == 0:
            raise errors.InputError('Number of data points cannot be 0. '
                                    'Experimental data is inferred from the '
                                    'parameter estimation task definition. '
                                    'It might be that copasi_file refers to a '
                                    'fresh copy of the model. Try redefining the '
                                    'same parameter estimation problem that you '
                                    'used in the profile likelihood, using the '
                                    'setup method but not running the '
                                    'parameter estimation before trying again.')
        return s

    def get_rss(self):
        rss = {}

        if self.index == -1:
            assert self.rss != None
            rss[-1] = self.rss
            return rss
        else:
            PED = viz.ParsePEData(self.parameter_path)
            if isinstance(self.index, int):
                rss[self.index] = PED.data.iloc[self.index.RSS]
            elif isinstance(self.index, list):
                for i in self.index:
                    rss[i] = PED.data.iloc[i]['RSS']
            return rss

    def get_confidence_level(self):
        """

        """
        CL_dct = {}
        for index in self.rss:
            rss = self.rss[index]
            CL_dct[index] = ChiSquaredStatistics(
                rss, self.dof, self.num_data_points,
                self.alpha
            ).CL

        ranks = list(self.data.index.get_level_values(0))
        #        print CL_dct
        CL_list = [CL_dct[i] for i in ranks]
        self.data['ConfidenceLevel'] = CL_list
        self.data = self.data.reset_index()
        self.data = self.data.set_index(
            ['ParameterSetRank', 'ConfidenceLevel', 'ParameterOfInterest', 'ParameterOfInterestValue'])
        return self.data


#


if __name__=='__main__':
    pass
#    execfile('/home/b3053674/Documents/pycotools/pycotools/pycotoolsTutorial/Test/testing_kholodenko_manually.py')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




















