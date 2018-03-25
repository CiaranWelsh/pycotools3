# -*-coding: utf-8 -*-
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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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
from scipy.interpolate import interp1d
from scipy.stats.mstats import pearsonr
from itertools import combinations, combinations_with_replacement, permutations
LOG=logging.getLogger(__name__)



class SeabornContextMixin(Mixin):
    def context(context='poster', font_scale=3, rc=None):
        seaborn.set_context(
            context=context, font_scale=font_scale, rc=rc
        )



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
        self.data = self.data.sort_values(by='RSS')
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

            if log10:
                return numpy.log10(cls.data)
            else:
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
    def __init__(self, rss, dof, num_data_points, alpha,
                 plot_chi2=False, show=False):
        self.alpha = alpha
        self.dof = dof
        self.rss = rss
        self.num_data_points = num_data_points
        self.CL = self.calc_chi2_CL()
        self.show = show

        if self.alpha > 1 or self.alpha < 0 or len(str(self.alpha)) > 4:
            raise errors.InputError('alpha parameter should be between 0 and 1 and be '
                                    'to 2 decimal places. I.e. 0.95')


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
        if self.show:
            plt.show()

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
    def __init__(self, cls_instance, log10=False, copasi_file=None, alpha=0.95):
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
        self.alpha = alpha
        if self.copasi_file is not None:
            self.model = model.Model(self.copasi_file)

        accepted_types = [tasks.TimeCourse,
                          tasks.Scan,
                          tasks.ParameterEstimation,
                          tasks.MultiParameterEstimation,
                          str,
                          Parse,
                          tasks.ProfileLikelihood,
                          pandas.DataFrame,
                          tasks.ChaserParameterEstimations]

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

        self.data = self.parse()


    def parse(self):
        """
        determine class type of self.cls_instance
        and call the appropirate method for
        parsing the data type
        :return:
        """
        data = None

        if isinstance(self.cls_instance, tasks.TimeCourse):
            data = self.from_timecourse()

        elif type(self.cls_instance) == tasks.ParameterEstimation:
            data = self.from_parameter_estimation

        elif type(self.cls_instance) == tasks.MultiParameterEstimation:
            data = self.from_multi_parameter_estimation(self.cls_instance)

        elif type(self.cls_instance) == Parse:
            data = self.cls_instance.data

        elif type(self.cls_instance) == tasks.ProfileLikelihood:
            data = self.from_profile_likelihood()

        elif type(self.cls_instance) == tasks.ChaserParameterEstimations:
            data = self.from_chaser_estimations(self.cls_instance)

        elif type(self.cls_instance) == pandas.core.frame.DataFrame:
            data = self.cls_instance
            if 'RSS' not in data.keys():
                raise errors.InputError('DataFrame should have an RSS column. Your '
                                        'df only has these: "{}"'.format(data.columns))
            data = data.sort_values(by='RSS')

        ##They are all strings. So only do this last
        elif type(self.cls_instance == str):
            data = self.from_folder()

        if self.log10:
            if not type(self.cls_instance) == tasks.ProfileLikelihood:
                data = numpy.log10(data)
                return data
            else:
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

        for report_name in glob.glob(folder+r'/*.txt'):
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

    # @cached_property
    def from_chaser_estimations(self, cls_instance, folder=None):
        """
        :return:
        """

        if folder == None:
            folder = cls_instance.results_directory

        d = []

        report_names = glob.glob(os.path.join(folder, '*.txt'))
        for report_name in report_names:
            # report_name = os.path.abspath(report_name)
            if os.path.isfile(report_name) is not True:
                raise errors.FileDoesNotExistError('"{}" does not exist'.format(report_name))

            try:
                ## read df without header
                df = pandas.read_csv(report_name, sep='\t', header=None)

                ## if first column is brckets we have raw copasi output which needs
                ## formatting. Raise the error and then pick up from below
                if '(' in list(df.iloc[0]):
                    raise errors.NonFormattedPEFileError

                ## if data already formatted, set the index to top column
                ## before adding to list to concat below
                df = df.transpose().set_index(0).transpose()
                d.append(df)

            #
            #     # raise NotImplementedError('Still developing this function to read data from CPE')
            #
            except errors.NonFormattedPEFileError:
                df = pandas.read_csv(
                    report_name,
                    sep='\t', header=None,
                )

                data = df.drop(df.columns[0], axis=1)
                width = data.shape[1]
            #     # remove the extra bracket
                data[width] = data[width].str[1:]
                names = self.cls_instance.model.fit_item_order + ['RSS']
                data.columns = names
                # os.remove(report_name)
                # data.to_csv(report_name,
                #             sep='\t',
                #             index=False)
            #     # d[report_name] = data
                d.append(data)

            except ValueError as e:
                if str(e) == 'No columns to parse from file':
                    LOG.info('Empty file "{}". Skipping'.format(report_name))

        df = pandas.concat(d)
        df = df.sort_values(by='RSS').reset_index(drop=True)
        return df.apply(pandas.to_numeric)#astype('float')

    def from_folder(self):
        """
        
        :param folder: 
        :return: 
        """
        if self.copasi_file is None:
            raise errors.InputError('To read data from a folder of'
                                    'parameter estimation data files '
                                    'specify argument to copasi_file. This '
                                    'should be the configured model '
                                    'that was used to generate the parameter '
                                    ' estimation data. This is necessary to annotate '
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
            # LOG.warning('You have commented out a try except block because '
            #             'pandas has deprecated the error in use. This warning '
            #             'is here to remind you that you have removed the try '
            #             'except block until you find out which error has replaced '
            #             'the pandas.error.EmptyDataError')

            # data = pandas.read_csv(report_name, sep='\t', header=None, skiprows=[0])
            # LOG.debug('data --> {}'.format(data))
            # data = pandas.read_csv(report_name, sep='\t', header=None)
            try:
                data = pandas.read_csv(report_name, sep='\t', header=None, skiprows=[0])
                read_type = 'multi_parameter_estimation'
                # LOG.debug('data -- > {}'.format(data))

            except ValueError as e:
                if str(e) == 'No columns to parse from file':
                    LOG.warning(
                        'No Columns to parse from file. {} is empty. '
                        'Continuing without parsing from this file'.format(
                            report_name
                        )
                    )
                    continue
                try:
                    data = pandas.read_csv(report_name, sep='\t', header=None)
                    read_type = 'parameter_estimation'
                except ValueError as e:
                    if str(e) == 'No columns to parse from file':
                        LOG.warning(
                            'No Columns to parse from file. {} is empty. '
                            'Continuing without parsing from this file'.format(
                                report_name
                            )
                        )
                        continue
                    else:
                        raise ValueError(e)

            except CParserError:
                raise CParserError('Parameter estimation data file is empty')

            if read_type == 'multi_parameter_estimation':
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

            elif read_type == 'parameter_estimation':
                left_bracket_columns = data[data.columns[0]]
                data = data.drop(data.columns[0], axis=1)
                # LOG.debug('file is --> {}'.format(report_name))
                # LOG.debug('data --> {}'.format(data))
                data[data.columns[-1]] = float(data[data.columns[-1]].str[1:][0])
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

            ## iterate over models in ProfileLikelihood task
            for model in self.cls_instance.model_dct:

                ## create dict's for collection of results
                results_dirs[model] = {}
                fit_item_order_dirs[model] = {}
                param_of_interest_dict[model] = {}

                ## iterate over parameters in models
                for param in self.cls_instance.model_dct[model]:

                    ## get the copasi file from that model
                    copasi_file = self.cls_instance.model_dct[model][param].copasi_file

                    ## infer the results file from copasi file
                    results_file = os.path.splitext(copasi_file)[0]+'.csv'

                    ## ensure it exists
                    if not os.path.isfile(results_file):
                        raise errors.InputError('file does not exist: "{}"'.format(results_file))

                    ## assign to dict
                    results_dirs[model][param] = results_file

                    ## collect fit items
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

        def confidence_level(cls):
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
                    self.alpha
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
                    df = pandas.read_csv(results_dict[index][param],
                                         sep='\t', skiprows=1, header=None)
                    bracket_indices = [1, -2]
                    df = df.drop(df.columns[bracket_indices], axis=1)
                    df.columns = range(len(df.columns))
                    items = ['Parameter Of Interest Value'] + fit_item_order_dict[index][param] + ['RSS']
                    df.columns = items
            #         # print numpy.log10(df['Parameter Of Interest Value'])
                    if self.log10:
                        df_list2 = []
                        for key in df.keys():
                            l = []
                            for i in range(df[key].shape[0]):
                                l.append(numpy.log10(df[key].iloc[i]))
                            df_list2.append(pandas.DataFrame(l, columns=[key]))
                        df = pandas.concat(df_list2, axis=1)
                    # print df.head()
                    # print self.cls_instance.parameters
                    CL = confidence_level(self.cls_instance)
                    if self.log10:
                        df['Best Parameter Value'] = math.log10(float(self.cls_instance.parameters[index][param]))
                        df['Best RSS Value'] = math.log10(float(self.cls_instance.parameters[index]['RSS']))
                        CL[index] = math.log10(CL[index])
                    else:
                        df['Best Parameter Value'] = float(self.cls_instance.parameters[index][param])
                        df['Best RSS Value'] = float(self.cls_instance.parameters[index]['RSS'])

                    df['Confidence Level'] = CL[index]
                    df['Best Fit Index'] = index
                    df['Parameter Of Interest'] = param
                    df = df.set_index(['Parameter Of Interest', 'Best Fit Index', 'Confidence Level',
                                       'Best Parameter Value', 'Best RSS Value',
                                       'Parameter Of Interest Value'], drop=True)
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

        #TODO implement `separate` keyword as `share` insteady

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
            'context': 'talk',
            'font_scale': 1.5,
            'rc': None,
            'copasi_file': None,
            'despine': True,
            'linewidth': 3,
            'color': 'red',
            'linestyle': '-',
            'ext': 'png',
            'legend_loc': 'best',
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

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

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
        else:
            if not os.path.isabs(self.results_directory):
                self.results_directory = os.path.join(self.cls.model.root, self.results_directory)

        if self.x.lower() == 'time':
            self.xlabel = "Time ({})".format(self.cls.model.time_unit)

        if self.xlabel is None:
            self.xlabel = self.x

        if self.ylabel is None:
            self.ylabel = 'Concentration ({})'.format(self.cls.model.quantity_unit)

        if self.savefig and (self.separate is False) and (self.filename is None):
            self.filename = 'TimeCourse.{}'.format(self.ext)
            LOG.warning('filename is None. Setting default filename to {}'.format(self.filename))

    def plot(self):
        """

        :return:
        """
        if self.y == None:
            self.y = [i.name for i in self.cls.model.metabolites]
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
            plt.plot(x, y, label=y_var, linewidth=self.linewidth,
                     linestyle=self.linestyle)

            if self.legend_loc is 'best':
                plt.legend(loc='best')
            else:
                plt.legend(loc=self.legend_loc)

            plt.title(self.title)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)

            if self.despine:
                seaborn.despine(fig=fig, top=True, right=True)


            if self.savefig:
                dirs = self.create_directory(self.results_directory)
                fle = os.path.join(dirs, '{}.{}'.format(y_var, self.ext))

                if self.separate:
                    fig.savefig(fle, dpi=self.dpi, bbox_inches='tight')
                else:
                    fig.savefig(self.filename, dpi=self.dpi, bbox_inches='tight')

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


    #todo
    =====
    Currently initial values are used as starting conditions but in some situations
    like when independent variables are used to set starting parameters for an experiment
    this is not being captured in the ensemble time course.

    Therefore, modify to follow directions in data files from independent data. Also run
    multiple times if you have multiple experiments measuring the same varibale.
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
                   'despine': True,
                   'legend': True,
                   'ext': 'png',
                   'context': 'talk',
                   'font_scale': 1.5,
                   'rc': None,
                   'copasi_file': None,
                   'normalize_y_axis': False,
                   'ymin': None,
                   'ymax': None,
                   }

        for i in kwargs.keys():
            assert i in options.keys(), '{} is not a keyword argument for ParameterEnsemble'.format(i)
        options.update(kwargs)
        self.kwargs = options
        self.update_properties(self.kwargs)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)



        self.data = self.parse(self.cls, log10=False, copasi_file=self.copasi_file)

        if self.copasi_file is not None:
            self.cls.model = model.Model(self.copasi_file)

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
        self.ensemble_data.index = self.ensemble_data.index.rename(['Index', 'Time'])

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


    @property
    def parse_experimental_files(self):
        """

        :return:
        """
        df_dct = {}
        if type(self.cls) == Parse:
            exp_files = self.experiment_files

        elif type(self.cls) is pandas.core.frame.DataFrame:
            exp_files = self.experiment_files

        else:
            exp_files = self.cls.experiment_files

        if exp_files is None:
            raise errors.InputError('if input class is Parse or pandas.DataFrame object '
                                    'experiment_files argument cannot be None')

        ## if exp_files is empty then read_csv would not be called
        for i in range(len(exp_files)):
            df = pandas.read_csv(exp_files[i],
                                 sep='\t', skip_blank_lines=False)
            is_null = df.isnull().all(1)
            from collections import Counter
            count = Counter(is_null)
            if count[True] > 0:
                df_list = numpy.split(df, df[df.isnull().all(1)].index)
                df_list = [j.dropna(how='all') for j in df_list]
                for j in range(len(df_list)):
                    if df_list[j].empty:
                        print 'empty'
                        continue
                    else:
                        df_dct[exp_files[i]+str(j)] = df_list[j]
            else:
                df_dct[exp_files[i]] = df
        return df_dct

    @property
    def get_experiment_times(self):
        d = {}
        time_marker = False
        for i in self.experimental_data:
            d[i] = {}
            for j in self.experimental_data[i].keys():
                if j.lower() == 'time':
                    time_marker = True
                    d[i] = self.experimental_data[i][j]

        ## Protect against not having time column labelled correctly
        if not time_marker:
            raise errors.InputError('Column in data file called \'time\' or \'Time\' not '
                                    ' detected. Please check your experiment file. The first '
                                    'column should be labelled Time for time course.' )
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
            d[i] = self.parse(TC, log10=False, copasi_file=self.copasi_file)
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
                    legend=self.legend,
                )
                

                if parameter in self.observables:
                    for df in self.experimental_data.values():
                        if parameter in df.keys():
                            if df.columns[0] == 'time':
                                df = df.rename(columns={'time': 'Time'})

                            # plt.figure()
                            ax2 = plt.plot(list(df['Time']), list(df[parameter]), '--', color=self.exp_color,
                                           label='Exp', alpha=0.4, marker='o')


                    if self.legend:
                        sim_patch = mpatches.Patch(color=self.color, label='Sim', alpha=0.4)
                        exp_patch = mpatches.Patch(color=self.exp_color, label='Exp', alpha=0.4)
                        plt.legend(handles=[sim_patch, exp_patch], loc=(1, 0.5))

                if self.despine:
                    seaborn.despine(ax=ax1, top=True, right=True)

                if self.title is None:
                    plt.title('{} (n={})'.format(parameter, self.data.shape[0]))

                else:
                    plt.title(self.title)

                if self.ylabel is None:
                    plt.ylabel('{}/{}'.format(self.cls.model.quantity_unit,
                                              self.cls.model.volume_unit)+'$^{-1}$')

                else:
                    plt.ylabel(self.ylabel)

                if self.xlabel is None:
                    plt.xlabel('Time ({})'.format(self.cls.model.time_unit))

                else:
                    plt.xlabel(self.xlabel)
                    
                if self.ymin is not None:
                    plt.ylim(ymin=self.ymin)

                if self.ymax is not None:
                    plt.ylim(ymax=self.ymax)

                if self.savefig:
                    self.results_directory = self.create_directory()
                    fname = os.path.join(self.results_directory, '{}.{}'.format(
                        misc.RemoveNonAscii(parameter).filter, self.ext))
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
            'dpi': 400,
            'context': 'talk',
            'font_scale': 1.5,
            'rc': None,
            'copasi_file': None,
        }

        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        raise NotImplementedError

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)


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

        ## defaults to metabolites andglobal quantities with assignments
        default_y = [i.name for i in self.cls.model.metabolites] + [i.name for i in self.cls.model.global_quantities if i.simulation_type == 'Assignment']
        self.default_properties = {
            'y': default_y,
            'savefig': False,
            'results_directory': None,
            'title': 'TimeCourse',
            'xlabel': None,
            'ylabel': None,
            'show': False,
            'filename': None,
            'dpi': 400,
            'log10': False,
            'context': 'talk',
            'font_scale': 1.5,
            'rc': None,
            'copasi_file': None,
        }
        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(),'{} is not a keyword argument for "PlotParameterEstimation"'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)


        self.data = self.parse(self.cls, self.log10, copasi_file=self.copasi_file)

        self.exp_data = self.read_experimental_data()
        self.sim_data = self.simulate_time_course()

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
        if not isinstance(self.y, list):
            self.y = [self.y]

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

        for i in self.exp_data:
            dct[i] = self.exp_data[i]['Time'].max()
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
        for exp in time_dct:
            indep_dct = {}
            for exp_key in self.exp_data[exp].keys():
                if exp_key[-6:] == '_indep':
                    indep_dct[exp_key[:-6]] = self.exp_data[exp][exp_key].iloc[0]

                ## Insert independent vars
                model.InsertParameters(self.cls.model, parameter_dict=indep_dct, inplace=True)


            TC = tasks.TimeCourse(
                self.cls.model, end=time_dct[exp], step_size=step_size,
                intervals=time_dct[exp]/step_size,
            )
            d[exp] = self.parse(TC, self.log10, copasi_file=self.copasi_file)

        return d

    def plot(self):
        """
        plot experimental data versus best parameter sets
        :return:
        """
        ## filter out y values which are not in the data file
        for y in self.y:
            if y not in self.read_experimental_data().values()[0].keys():
                raise errors.InputError('"{0}" not in "{1}". "{0}" is being ignored'.format(y, self.read_experimental_data().values()[0].keys()))

        for exp in self.exp_data:
            for sim in self.sim_data:
                if exp == sim:

                    for key in self.y:

                        plt.figure()
                        plt.plot(
                            self.exp_data[exp]['Time'], self.exp_data[exp][key],
                            label='Exp', linestyle=self.linestyle,
                            marker=self.marker, linewidth=self.linewidth,
                            markersize=self.markersize,
                            alpha=0.5,
                            color='#0E00FA',
                        )
                        plt.plot(
                            self.sim_data[sim]['Time'], self.sim_data[sim][key],
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
                                   'dpi': 400,
                                   'show': False,
                                   'despine': True,
                                   'ext': 'png',
                                   'context': 'talk',
                                   'font_scale': 1.5,
                                   'rc': None,
                                   'copasi_file': None,
                                   'filename': 'boxplot'
                                   }
        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(),'{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)

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
            fig = plt.figure()#
            data = self.data[labels[label_set]]
            seaborn.boxplot(data=data )
            plt.xticks(rotation=self.xtick_rotation)
            if self.despine:
                seaborn.despine(fig=fig, top=True, right=True)
            if self.title is not None:
                plt.title(self.title+'(n={})'.format(data.shape[0]))
            plt.ylabel(self.ylabel)
            if self.savefig:
                self.results_directory = self.create_directory()
                fle = os.path.join(self.results_directory,
                                   '{}{}.{}'.format(self.filename, label_set, self.ext))
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
@mixin(SeabornContextMixin)
class LikelihoodRanks(PlotKwargs):
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
        # self.plot_kwargs = self.plot_kwargs()


        self.default_properties = {'log10': False,
                                   'truncate_mode': 'percent',
                                   'theta': 100,
                                   'xtick_rotation': 'horizontal',
                                   'ylabel': None,
                                   'title': 'Likelihood-Ranks Plot',
                                   'savefig': False,
                                   'results_directory': None,
                                   'dpi': 400,
                                   'show': False,
                                   'filename': 'LikelihoodRanks',
                                   'despine': True,
                                   'ext': 'png',
                                   'line_transparency': 1, ##passed to matplotlib alpha parameter
                                   'marker_transparency': 0.7,
                                   'color': '#004ADF',
                                   'markercolor': '#FF9709',
                                   'linewidth': 3,
                                   'markersize': 10,
                                   'context': 'talk',
                                   'font_scale': 1.5,
                                   'rc': None,
                                   'copasi_file': None,
                                   }

        # self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for RssVsIterations'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        # self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)

        self.plot()

    def _do_checks(self):
        """

        :return:
        """
        if self.log10:
            self.ylabel = 'log10 RSS'
            self.xlabel = 'log10 Rank of Best Fit'
        else:
            self.ylabel = 'RSS'
            self.xlabel = 'Rank of Best Fit'




    def create_directory(self):
        """
        create a directory for the results
        :return:
        """
        if self.results_directory is None:
            if type(self.cls) == Parse:
                self.results_directory = os.path.join(os.path.dirname(self.cls.copasi_file), 'RssVsIterations')
            else:
                self.results_directory = os.path.join(
                    self.cls.model.root, 'LikelihoodRank'
                )

        if not os.path.isdir(self.results_directory):
            os.makedirs(self.results_directory)
        return self.results_directory

    def plot(self):
        """
        Plot Rss Vs rank of best fit
        :return:
            None
        """
            
        fig = plt.figure()
        if self.log10:
            x = numpy.log10(range(self.data['RSS'].shape[0]))
        else:
            x = range(self.data['RSS'].shape[0])

        plt.plot(x,
                 self.data['RSS'].sort_values(ascending=True),
                 color=self.color, linewidth=self.linewidth,
                 alpha=self.line_transparency,
                 )

        plt.plot(x,
                 self.data['RSS'].sort_values(ascending=True), 'o',
                 color=self.markercolor, markersize=self.markersize,
                 alpha=self.marker_transparency
                 )

        plt.xticks(rotation=self.xtick_rotation)
        if self.title is not None:
            plt.title(self.title+'(n={})'.format(self.data.shape[0]))
        plt.ylabel(self.ylabel)
        plt.xlabel('Rank of Best Fit')
        if self.despine:
            seaborn.despine(fig=fig, top=True, right=True)
        if self.savefig:
            self.results_directory = self.create_directory()
            fle = os.path.join(self.results_directory, '{}.{}'.format(self.filename, self.ext))
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
                                 'dpi': 400,
                                 'n_components': 2,
                                 'by': 'iterations', ##iterations or parameters
                                 'legend_position': None, ##Horizontal, verticle, line spacing
                                 'legend_fontsize': 25,
                                 'cmap': 'viridis',
                                 'annotate': False,
                                 'annotation_fontsize': 25,
                                 'show': False,
                                 'despine': True,
                                 'ext': 'png',
                                 'context': 'talk',
                                 'font_scale': 1.5,
                                 'rc': None,
                                 'copasi_file': None,
                                 }


        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Pca'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
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
        # if self.title is None:
        #     if self.by is 'parameters':
        #         title = 'PCA by Parameters (n={})'.format(len(labels))
        #     elif self.by is 'iterations':
        #         title = 'PCA by Iterations (n={})'.format(len(labels))

        if self.by not in ['parameters','iterations']:
            raise errors.InputError('{} not in {}'.format(
                self.by, ['parameters','iterations']))

        # if self.results_directory is None:
        #     self.results_directory = self.create_directory()

        if self.ylabel==None:
            if self.log10==False:
                self.ylabel = 'PC2'
            elif self.log10==True:
                self.ylabel = 'log10 PC2'
            else:
                raise errors.SomethingWentHorriblyWrongError('{} not in {}'.format(
                    self.ylabel, [True, False]))
        
        if self.xlabel==None:
            if self.log10==False:
                self.xlabel = 'PC1'
            elif self.log10==True:
                self.xlabel = 'log10 PC1'
            else:
                raise errors.SomethingWentHorriblyWrongError(
                    '{} not in {}'.format(self.ylabel, [True, False]))
 
        
        LOG.info('plotting PCA {}'.format(self.by))
        
        if self.by == 'parameters':
            self.annotate = True
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
            sc = ax.scatter(projected[0], projected[1])


        else:
            projected = pca.fit(self.data).transform(self.data)
            projected = pandas.DataFrame(projected, index=self.data.index)
            labels = list(self.data.index)
            projected = pandas.concat([rss, projected], axis=1)
            sc = ax.scatter(projected[0], projected[1], c=projected['RSS'], cmap=self.cmap)
            cb = plt.colorbar(sc)
            cb.ax.set_title('RSS')

        if self.despine:
            seaborn.despine(fig=fig, top=True, right=True)
            
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.title(self.title)
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
            fle = os.path.join(self.results_directory, 'Pca_by_{}.{}'.format(self.by, self.ext))
            plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')

        if self.show:
            plt.show()

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
                                   'title': True, ##boolean here as title is inferred from parameter
                                   'savefig': False,
                                   'results_directory': None,
                                   'dpi': 400,
                                   'title_fontsize': 35,
                                   'show': False,
                                   'despine': True,
                                   'ext': 'png',
                                   'color': 'green',
                                   'hist': True,
                                   'kde': False,
                                   'rug': False,
                                   'context': 'talk',
                                   'font_scale': 1.5,
                                   'rc': None,
                                   'copasi_file': None,
                                   }

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Histograms'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
        LOG.info('plotting histograms')
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.plot()
        # self.coloured_plot()


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
            fig = plt.figure()
            seaborn.distplot(
                self.data[parameter], color=self.color, kde=self.kde, rug=self.rug,
                hist=self.hist
                )
            if self.log10:
                plt.ylabel("{}".format(self.ylabel))
                plt.xlabel("log10 {}".format(parameter))
            else:
                plt.ylabel(self.ylabel)
                plt.xlabel(parameter)
            if self.title is True:
                plt.title('{},n={}'.format(parameter, self.data[parameter].shape[0]),
                      fontsize=self.title_fontsize)

            if self.despine:
                seaborn.despine(fig=fig, top=True, right=True)

            if self.savefig:
                self.create_directory(self.results_directory)
                fname = os.path.join(self.results_directory,
                                     misc.RemoveNonAscii(parameter).filter+'.{}'.format(self.ext))
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                LOG.info('plot save to "{}"'.format(fname))
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

        bins = numpy.arange(self.data[parameter].min(), self.data[parameter].max(),
                            bins_size)#width/num_bins
        ## calculate the density of RSS

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
            'x': 'RSS',
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
            'dpi': 400,
            'title_fontsize': 35,
            'title': True,  #Either True or None/False
            'show': False,
            'ext': 'png',
            'despine': True,
            'color_bar_pad': 0.1,   #padding for color bar. Dist between bar and axes
            'context': 'talk',
            'font_scale': 1.5,
            'rc': None,
            'copasi_file': None,
        }

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for Scatters'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)


        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
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

        if self.y == 'all' or self.y == ['all']:
            self.y = self.data.keys()

        if self.x == 'all' or self.x == ['all']:
            self.x = self.data.keys()


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
                fig = plt.figure()
                plt.scatter(
                    self.data[x_var], self.data[y_var],
                    cmap=self.cmap, c=self.data['RSS'],
                )
                cb = plt.colorbar(pad=self.color_bar_pad)

                if self.title:
                    title = 'Scatter graph of\n {} Vs {}.(n={})'.format(
                        x_var, y_var, self.data.shape[0]
                    )

                if self.log10:
                    cb.set_label('log10 RSS')
                    plt.xlabel('log$_{10}$'+'[{}]'.format(x_var))
                    plt.ylabel('log$_{10}$'+'[{}]'.format(y_var))
                else:
                    cb.set_label('RSS')
                    plt.xlabel(x_var)
                    plt.ylabel(y_var)

                if self.despine:
                    seaborn.despine(fig=fig, top=True, right=True)

                if self.savefig:
                    x_dir = os.path.join(self.results_directory, x_var)
                    self.create_directory(x_dir)
                    fle = os.path.join(x_dir, '{}.{}'.format(y_var, self.ext))
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
            'scores_title': None,
            'coef_title': None,
            'savefig': False,
            'results_directory': None,
            'dpi': 400,
            'title_fontsize': 35,
            'show': False,
            'n_alphas': 100,
            'max_iter': 20000,
            'ext': 'png',
            'despine': True,
            'context': 'talk',
            'font_scale': 1.5,
            'rc': None,
            'copasi_file': None,
        }

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for LinearRegression'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
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

        if self.scores_title is None:
            pass
        if self.log10:
            self.scores_title = 'Model Fitting Test and Train Scores (Log10)'

        else:
            self.scores_title = 'Model Fitting Test and Train Scores'


        if self.coef_title is None:
            if self.log10:
                self.coef_title = 'Coefficients (Log10)'
            else:
                self.coef_title = 'Coefficients'



    def compute1coef(self, parameter):
        """
        Compute coefficients for a single parameter
        using self['lin_model'] from sklearn
        """
        y = numpy.array(self.data[parameter])
        X = self.data.drop(parameter, axis=1)
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y)

        try:
            lin_model = self.lin_model(fit_intercept=True, n_alphas=self.n_alphas,
                    max_iter=self.max_iter)
        except TypeError:
            lin_model = self.lin_model(fit_intercept=True)

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
        fig = plt.figure()
        seaborn.heatmap(self.scores)
        if self.despine:
            seaborn.despine(fig=fig, top=True, right=True)

        plt.title(self.scores_title, fontsize=self.title_fontsize)
        if self.savefig:
            self.create_directory(self.results_directory)
            fname = os.path.join(self.results_directory, 'linregress_scores.{}'.format(self.ext))
            plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')


    def plot_rss(self):
        fig = plt.figure()
        seaborn.heatmap(self.coef.RSS.sort_values(by='RSS', ascending=False))
        plt.title('Lasso Regression \n(Y=RSS) (n={})'.format(self.data.shape[0]), fontsize=self.title_fontsize)
        if self.despine:
            seaborn.despine(fig=fig, top=True, right=True)
        if self.savefig:
            self.create_directory(self.results_directory)
            fname = os.path.join(self.results_directory, 'linregress_RSS.{}'.format(self.ext))
            plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')


    def plot_coef(self):
        """

        :return:
        """
        self.coef.columns = self.coef.columns.droplevel(0)
        self.coef = self.coef.drop('RSS', axis=1)
        self.coef = self.coef.drop('RSS', axis=0)
        fig = plt.figure()
        seaborn.heatmap(self.coef, cbar_kws={'pad': 0.2})
        if self.despine:
            seaborn.despine(fig=fig, top=True, right=True)

        plt.title(self.coef_title)
        plt.xlabel('')
        if self.savefig:
            self.create_directory(self.results_directory)
            fname = os.path.join(self.results_directory, 'linregress_parameters.{}'.format(self.ext))
            plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')


@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class ModelSelectionOld(object):
    """
    Calculate model selection criteria AIC (corrected) and
    BIC for a selection of models that have undergone fitting
    using the :py:class:`tasks.MultiModelFit` class. Plot as
    boxplots and histograms.
    """

    def __init__(self, multi_model_fit, **kwargs):
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


        self.default_properties = {
            'lin_model': linear_model.LinearRegression,
            'savefig': False,
            'results_directory': None,
            'dpi': 400,
            'log10': False,
            'filename': None,
            'pickle': None,
            'despine': True,
            'ext': 'png',
            'title': True,
            'context': 'poster',
            'font_scale': 2,
            'rc': None,
            'bins': None,
            'hist': True,
            'kde': False,
            'rug': False,
            'fit': None,
            'hist_kws': None,
            'kde_kws': None,
            'rug_kws': None,
            'color': None,
            'palette': None,
            'saturation': 0.75,
            'vertical': None,
            'norm_hist': False,
            'axlabel': None,
            'model_labels': None,
            'label': None,
            'ax': None,
            'legend': True,
            'legend_loc': (0, -0.5),
            'show': False
        }

        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for ModelSelection'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)

        self._do_checks()

        ## do model selection stuff
        self.results_folder_dct = self._get_results_directories()
        self.model_dct = self._get_model_dct()


        ## code for having default legend labels
        self.default_model_labels = {os.path.split(i)[1][:-6]: os.path.split(i)[1][:-6] for i in [j.copasi_file for j in self.model_dct.values()]}


        if self.model_labels is not None:
            if type(self.model_labels) is not dict:
                raise errors.InputError('model labels should be a dict')

            for label in self.model_labels:
                if label not in self.default_model_labels:
                    raise errors.InputError('keys of the model_labels dict should be one of '
                                            '"{}"'.format(self.default_model_labels))
        elif self.model_labels is None:
            self.model_labels = self.default_model_labels

        self.data_dct = self._parse_data()
        self.number_model_parameters = self._get_number_estimated_model_parameters()
        self.number_observations = self._get_n()
        self.model_selection_data = self.calculate_model_selection_criteria()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)



        # self.boxplot()
        # self.histogram()
        self.violin()
        self.to_csv()


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
        if self.results_directory is None:
            self.results_directory = self.multi_model_fit.project_dir


        if self.filename is None:
            save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
            self.filename = os.path.join(save_dir, 'ModelSelectionCriteria.csv')

    def _get_results_directories(self):
        '''
        Find the results directories embedded within MultimodelFit
        and RunMutliplePEs.
        '''
        return self.multi_model_fit.results_folder_dct

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
        dct = {}
        for MPE in self.multi_model_fit:

            ## get the first cps file configured for eastimation in each MMF obj
            cps_1 = glob.glob(
                os.path.join(
                    os.path.dirname(MPE.results_directory),
                    '*_0.cps')
            )[0]
            dct[MPE.results_directory] = model.Model(cps_1)
        return dct

    def _parse_data(self):
        if self.pickle is not None:
            #     self.pickle = os.path.splitext(self.filename)[0]+'.pickle'
            return pandas.read_pickle(self.pickle)
        else:
            dct={}
            for cps, MPE in self.multi_model_fit.items():
                cps_0 = cps[:-4]+'_0.cps'
                dct[cps_0] = Parse(MPE.results_directory, copasi_file=cps_0, log10=self.log10)
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
        """
        Calculate AIC corrected and BIC
        :return:
            pandas.DataFrame
        """
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
            aic = pandas.DataFrame.from_dict(aic_dct, orient='index')
            rss = pandas.DataFrame(rss)
            bic = pandas.DataFrame.from_dict(bic_dct, orient='index')
            df = pandas.concat([rss, aic, bic], axis=1)
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
            fig = plt.figure()
            seaborn.boxplot(data=data[data['Metric'] == metric],
                            x='Model', y='Score')
            plt.xticks(rotation='vertical')
            if self.title:
                plt.title('{} Scores'.format(metric))
            plt.xlabel(' ')
            if self.despine:
                seaborn.despine(fig=fig, top=True, right=True)

            if self.savefig:
                save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
                if os.path.isdir(save_dir) is not True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, 'boxplot_{}.{}'.format(metric, self.ext))
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
            fig = plt.figure()
            for label2, df2 in df.groupby(by='Model'):

                plot_data = df2['Score'].dropna()
                ax = seaborn.distplot(
                    plot_data,
                    bins=self.bins,
                    hist=self.hist, kde=self.kde, rug=self.rug, fit=None,
                    hist_kws=self.hist_kws, kde_kws=self.kde_kws, rug_kws=self.rug_kws,
                    color=self.color, vertical=self.vertical, norm_hist=self.norm_hist,
                    axlabel=self.axlabel, label=self.model_labels[label2], ax=self.ax)
                if self.title:
                    plt.title("{} Score (n={})".format(label, plot_data.shape[0]))
                plt.ylabel("Frequency")
                plt.xlabel("Score".format(label, plot_data.shape[0]))
                if self.despine:
                    seaborn.despine(fig=fig, top=True, right=True)

                if self.legend:
                    plt.legend(loc=(self.legend_loc))

            if self.savefig:
                save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
                if os.path.isdir(save_dir) != True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, 'Histogram_{}_{}.{}'.format(label2, label, self.ext))
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                LOG.info('histograms saved to : "{}"'.format(fname))
                self.to_csv(self.filename)

            if self.show:
                plt.show()

    def violin(self):
        seaborn.set_context(context='poster')
        data = self.model_selection_data

        data = data.unstack()
        data = data.reset_index()
        data = data.rename(columns={'level_0': 'Model',
                                    'level_1': 'Metric',
                                    0: 'Score'})
        for metric in data['Metric'].unique():
            fig = plt.figure()
            seaborn.violinplot(data=data[data['Metric'] == metric],
                               x='Model',
                               y='Score',
                               color=self.color,
                               palette=self.palette,
                               saturation=self.saturation,
                               axlabel=self.axlabel,
                               ax=self.ax)
            plt.xticks(rotation='vertical')
            if self.title:
                plt.title('{} Scores'.format(metric))
            plt.xlabel(' ')
            if self.despine:
                seaborn.despine(fig=fig, top=True, right=True)

            if self.savefig:
                save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
                if os.path.isdir(save_dir) is not True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, 'ViolinPlot_{}.{}'.format(metric, self.ext))
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                LOG.info('Violin plot saved to : "{}"'.format(fname))

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
        plt.ylabel('log10 parameter_value,Err=SEM')
        if filename!=None:
            plt.savefig(filename,dpi=200,bbox_inches='tight')


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

    def __init__(self, multi_model_fit, **kwargs):
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


        self.default_properties = {
            'savefig': False,
            'results_directory': None,
            'dpi': 400,
            'log10': False,
            'filename': None,
            'pickle': None,
            'despine': True,
            'ext': 'png',
            'title': True,
            'context': 'poster',
            'font_scale': 2,
            'rc': None,
            'color': None,
            'palette': None,
            'saturation': 0.75,
            'model_labels': None,
            'label': None,
            'ax': None,
            'show': False
        }

        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for ModelSelection'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)

        self._do_checks()

        ## do model selection stuff
        self.results_folder_dct = self._get_results_directories()
        self.model_dct = self._get_model_dct()


        ## code for having default legend labels
        self.default_model_labels = {os.path.split(i)[1][:-6]: os.path.split(i)[1][:-6] for i in [j.copasi_file for j in self.model_dct.values()]}


        if self.model_labels is not None:
            if type(self.model_labels) is not dict:
                raise errors.InputError('model labels should be a dict')

            for label in self.model_labels:
                if label not in self.default_model_labels:
                    raise errors.InputError('keys of the model_labels dict should be one of '
                                            '"{}"'.format(self.default_model_labels))
        elif self.model_labels is None:
            self.model_labels = self.default_model_labels

        self.data_dct = self._parse_data()
        self.number_model_parameters = self._get_number_estimated_model_parameters()
        self.number_observations = self._get_n()
        self.model_selection_data = self.calculate_model_selection_criteria()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)



        # self.boxplot()
        # self.histogram()
        self.violin()
        self.to_csv()


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
        if self.results_directory is None:
            self.results_directory = self.multi_model_fit.project_dir


        if self.filename is None:
            save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
            self.filename = os.path.join(save_dir, 'ModelSelectionCriteria.csv')

    def _get_results_directories(self):
        '''
        Find the results directories embedded within MultimodelFit
        and RunMutliplePEs.
        '''
        return self.multi_model_fit.results_folder_dct

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
        dct = {}
        for MPE in self.multi_model_fit:

            ## get the first cps file configured for eastimation in each MMF obj
            cps_1 = glob.glob(
                os.path.join(
                    os.path.dirname(MPE.results_directory),
                    '*_0.cps')
            )[0]
            dct[MPE.results_directory] = model.Model(cps_1)
        return dct

    def _parse_data(self):
        if self.pickle is not None:
            #     self.pickle = os.path.splitext(self.filename)[0]+'.pickle'
            return pandas.read_pickle(self.pickle)
        else:
            dct={}
            for cps, MPE in self.multi_model_fit.items():
                cps_0 = cps[:-4]+'_0.cps'
                dct[cps_0] = Parse(MPE.results_directory, copasi_file=cps_0, log10=self.log10)
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
        """
        Calculate AIC corrected and BIC
        :return:
            pandas.DataFrame
        """
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
            aic = pandas.DataFrame.from_dict(aic_dct, orient='index')
            rss = pandas.DataFrame(rss)
            bic = pandas.DataFrame.from_dict(bic_dct, orient='index')
            df = pandas.concat([rss, aic, bic], axis=1)
            df.columns = ['RSS', 'AICc', 'BIC']
            df.index.name = 'RSS Rank'
            df_dct[os.path.split(cps_key)[1][:-6]] = df
        df = pandas.concat(df_dct, axis=1)
        return df

    def violin(self):
        seaborn.set_context(context='poster')
        data = self.model_selection_data

        data = data.unstack()
        data = data.reset_index()
        data = data.rename(columns={'level_0': 'Model',
                                    'level_1': 'Metric',
                                    0: 'Score'})

        new_names = []
        for mod in data['Model']:
            for j in self.model_labels:
                if mod == j:
                    new_names.append(self.model_labels[j])

        data['Model'] = new_names
        for metric in data['Metric'].unique():
            fig = plt.figure()
            seaborn.violinplot(data=data[data['Metric'] == metric],
                               x='Model',
                               y='Score',
                               color=self.color,
                               palette=self.palette,
                               saturation=self.saturation,
                               ax=self.ax)
            plt.xticks(rotation='vertical')
            if self.title:
                plt.title('{} Scores'.format(metric))
            plt.xlabel(' ')
            if self.despine:
                seaborn.despine(fig=fig, top=True, right=True)

            if self.savefig:
                save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
                if os.path.isdir(save_dir) is not True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, 'ViolinPlot_{}.{}'.format(metric, self.ext))
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                LOG.info('Violin plot saved to : "{}"'.format(fname))

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
        plt.ylabel('log10 parameter_value,Err=SEM')
        if filename!=None:
            plt.savefig(filename,dpi=200,bbox_inches='tight')

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
                                   'y': None, #can equal all
                                   'index': None,
                                   'log10': True,
                                   'savefig': False,
                                   'results_directory': None,
                                   'dpi': 400,
                                   'plot_cl': True,
                                   'alpha': 0.95,
                                   'title': None,
                                   'xlabel': None,
                                   'ylabel': None,
                                   'legend': False,
                                   'legend_loc': None,
                                   'show': False,
                                   'separate': True,
                                   'filename': None,
                                   'despine': True,
                                   'ext': 'png',
                                   'show_best_rss': True,
                                   'best_rss_marker': 'k*', ##Any matplotlib marker
                                   'ylim': None,
                                   'xlim': None,
                                   'interpolation': None,
                                   'interpolation_resolution': 1000, #number of steps to interpolate
                                   'context': 'talk',
                                   'font_scale': 1,
                                   'rc': None,
                                   'multiplot': False,
                                   'same_axis': False,
                                   }

        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for PlotProfileLikelihood'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        ## parse data
        self.data = Parse(self.cls, log10=self.log10, alpha=self.alpha).data

        ## do some checks
        self._do_checks()

        ## do plotting
        if self.same_axis:
            self.plot_same_axis()
        else:
            self.plot()
        ##todo implement ability to change confidence level from Plot.
        ##at the moment the CL is conputer by Parse. This is not optimal

    def _do_checks(self):
        """

        :return:
        """
        ## todo put original estimatd values on non rss graphs as well
        if self.ylim is not None:
            if not isinstance(self.ylim, tuple):
                raise errors.InputError('ylim arg should be tuple. Got "{}"'.format(type(self.ylim)))

            if len(self.ylim) is not 2:
                raise errors.InputError('ylim arg should be tuple of length 2. '
                                        'See "https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.ylim.html" '
                                        'for details')

        if self.xlim is not None:
            if not isinstance(self.xlim, tuple):
                raise errors.InputError('xlim arg should be tuple. Got "{}"'.format(type(self.xlim)))

            if len(self.xlim) is not 2:
                raise errors.InputError('xlim arg should be tuple of length 2. '
                                        'See "https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.xlim.html" '
                                        'for details')

        interpolation_kinds = ['linear', 'nearest', 'zero',
                               'slinear', 'quadratic', 'cubic']

        if self.interpolation is not None:
            if self.interpolation not in interpolation_kinds:
                raise errors.InputError('"{}" is not in "{}"'.format(
                    self.interpolation, interpolation_kinds
                ))

        if type(self.cls) == tasks.ProfileLikelihood:
            self.results_directory = self.cls.results_directory
        else:
            LOG.warning('cls not of type tasks.ProfileLikelihood')

        if isinstance(self.data, pandas.core.frame.DataFrame) != True:
            raise errors.InputError('"{}" should be a dataframe not "{}".'.format(self.data, type(self(data))))

        self.parameter_list = sorted(list(self.data.columns))

        if self.separate == False:

            self.legend = True

        if self.index is None:
            self.index = 0

        if not isinstance(self.index, list):
            self.index = [self.index]

        if self.x == None:
            self.x = [i for i in self.parameter_list if i is not 'RSS']
            # raise errors.InputError('x cannot be None')

        if self.y == None:
            self.y = 'RSS'

        if self.y == 'all':
            self.y = self.parameter_list

        if self.x == 'all':
            self.x = [i for i in self.parameter_list if i != 'RSS']

        if self.y == None:
            raise errors.InputError('y cannot be None')

        if isinstance(self.y, str):
            self.y = [self.y]

        if isinstance(self.y, list):
            for y_param in self.y:
                if y_param not in self.parameter_list:
                    raise errors.InputError('{} not in {}'.format(y_param, self.parameter_list))

        if isinstance(self.x, str):
            self.x = [self.x]

        if isinstance(self.x, list):
            for x_param in self.x:
                if x_param not in self.parameter_list:
                    raise errors.InputError('{} not in {}'.format(x_param, self.parameter_list))

        if self.filename is not None:
            if not os.path.isabs(self.filename):
                self.filename = os.path.join(self.results_directory, self.filename)

            self.data.to_csv(self.filename)
            LOG.info('Profile likelihood data saved to "{}"'.format(self.filename))

    def plot_same_axis(self):
        """

        :return:
        """
        fig = plt.figure()
        for x in self.x:
            for y in self.y:
                for i in self.index:
                    plot_data = self.data.loc[x, i][y]
                    if type(plot_data) == pandas.Series:
                        plot_data = pandas.DataFrame(plot_data)

                    plot_data = plot_data.reset_index()

                    x_plot = plot_data['Parameter Of Interest Value']
                    y_plot = plot_data[y]

                    if self.interpolation is not None:
                        f = interp1d(x_plot, y_plot, kind=self.interpolation)
                        minimum = x_plot.min()
                        maximum = x_plot.max()
                        step = (maximum - minimum) / self.interpolation_resolution
                        xnew = numpy.arange(start=minimum, stop=maximum, step=step)
                        ynew = f(xnew)
                        plt.plot(xnew, ynew, 'k')
                        plt.plot(x_plot, y_plot, 'ro', label=y, linewidth=2)  # linestyle='o', color='red')
                    else:
                        plt.plot(x_plot, y_plot, label=y)

                    if y is 'RSS':
                        plt.plot(plot_data['Parameter Of Interest Value'],
                             plot_data['Confidence Level'], linewidth=3,
                             linestyle='--', color='green', label='CL')

                    if self.show_best_rss:
                        if y is 'RSS':
                            best_rss = list(set(plot_data['Best RSS Value']))
                            best_param_val = list(set(plot_data['Best Parameter Value']))
                            plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
                                     markersize=12)

                    if self.legend:
                        if self.legend_loc is not None:
                            plt.legend(loc=self.legend_loc)
                        else:
                            plt.legend(loc='best')

                    if self.despine:
                        seaborn.despine(fig=fig, top=True, right=True)

                    if self.title is None:
                        self.title = 'Profile Likelihoods for\n{} ' \
                                     'against {} (index={})'.format(x, y, i)

                    elif self.title is 'profile':
                        self.title = x

                    plt.title(self.title)

                    if self.log10:
                        plt.ylabel(r'$log_{10}$[{}]'.format(y))
                        plt.xlabel(r'$log_{10}$[{}]'.format(x))
                    else:
                        plt.ylabel(y)
                        plt.xlabel(x)

                    if self.ylim is not None:
                        plt.ylim(self.ylim)

                    if self.xlim is not None:
                        plt.xlim(self.xlim)

                    if self.savefig:
                        d = os.path.join(self.results_directory, str(i))
                        d = os.path.join(d, x)
                        self.create_directory(d)
                        fname = os.path.join(d, misc.RemoveNonAscii(y).filter + '.{}'.format(self.ext))

                        plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                        LOG.info('saved to --> {}'.format(fname))

                    if self.show:
                        plt.show()

    def plot(self):
        """

        :return:
        """
        for x in self.x:
            for y in self.y:
                if self.multiplot:
                    fig = plt.figure()
                for i in self.index:
                    plot_data = self.data.loc[x, i][y]
                    if type(plot_data) == pandas.Series:
                        plot_data = pandas.DataFrame(plot_data)

                    if not self.multiplot:
                        fig = plt.figure()

                    plot_data = plot_data.reset_index()

                    x_plot = plot_data['Parameter Of Interest Value']
                    y_plot = plot_data[y]

                    if self.interpolation is not None:
                        f = interp1d(x_plot, y_plot, kind=self.interpolation)
                        minimum = x_plot.min()
                        maximum = x_plot.max()
                        step = (maximum - minimum) / self.interpolation_resolution
                        xnew = numpy.arange(start=minimum, stop=maximum, step=step)
                        ynew = f(xnew)
                        plt.plot(xnew, ynew, 'k')
                        plt.plot(x_plot, y_plot, 'ro', label=y, linewidth=2)  # linestyle='o', color='red')
                    else:
                        plt.plot(x_plot, y_plot, label=y, marker='o')

                    if y is 'RSS':
                        plt.plot(plot_data['Parameter Of Interest Value'],
                             plot_data['Confidence Level'], linewidth=3,
                             linestyle='--', color='green', label='CL')


                    if self.show_best_rss:
                        if y == 'RSS':
                            best_rss = list(set(plot_data['Best RSS Value']))
                            best_param_val = list(set(plot_data['Best Parameter Value']))
                            plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
                                     markersize=12)

                    if self.legend:
                        if self.legend_loc is not None:
                            plt.legend(loc=self.legend_loc)
                        else:
                            plt.legend(loc='best')

                    if self.despine:
                        seaborn.despine(fig=fig, top=True, right=True)

                    # LOG.debug('title is --> {}'.format(self.title))
                    if self.title is None:
                        self.title = 'Profile Likelihoods for\n{} ' \
                                 'against {} (index={})'.format(x, y, i)


                    # elif self.title is 'profile':
                    #     self.title = x

                    plt.title(self.title)

                    if self.log10:
                        plt.ylabel(r'log$_{10}$'+'[{}]'.format(y))
                        plt.xlabel(r'log$_{10}$'+'[{}]'.format(x))
                    else:
                        plt.ylabel(y)
                        plt.xlabel(x)

                    if self.ylim is not None:
                        plt.ylim(self.ylim)

                    if self.xlim is not None:
                        plt.xlim(self.xlim)

                    if self.savefig:
                        d = os.path.join(self.results_directory, str(i))
                        d = os.path.join(d, x)
                        self.create_directory(d)
                        fname = os.path.join(d, misc.RemoveNonAscii(y).filter + '.{}'.format(self.ext))

                        plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                        LOG.info('saved to --> {}'.format(fname))

                    if self.show:
                        plt.show()

    def plot_pdf(self):
        """

        :return:
        """
        raise NotImplementedError
        # with PdfPages()
        for x in self.x:
            for y in self.y:
                if self.multiplot:
                    fig = plt.figure()
                for i in self.index:
                    plot_data = self.data.loc[x, i][y]
                    if type(plot_data) == pandas.Series:
                        plot_data = pandas.DataFrame(plot_data)

                    if not self.multiplot:
                        fig = plt.figure()

                    plot_data = plot_data.reset_index()

                    x_plot = plot_data['Parameter Of Interest Value']
                    y_plot = plot_data[y]

                    if self.interpolation is not None:
                        f = interp1d(x_plot, y_plot, kind=self.interpolation)
                        minimum = x_plot.min()
                        maximum = x_plot.max()
                        step = (maximum - minimum) / self.interpolation_resolution
                        xnew = numpy.arange(start=minimum, stop=maximum, step=step)
                        ynew = f(xnew)
                        plt.plot(xnew, ynew, 'k')
                        plt.plot(x_plot, y_plot, 'ro', label=y, linewidth=2)  # linestyle='o', color='red')
                    else:
                        plt.plot(x_plot, y_plot, label=y, marker='o')

                    if y is 'RSS':
                        plt.plot(plot_data['Parameter Of Interest Value'],
                             plot_data['Confidence Level'], linewidth=3,
                             linestyle='--', color='green', label='CL')


                    if self.show_best_rss:
                        best_rss = list(set(plot_data['Best RSS Value']))
                        best_param_val = list(set(plot_data['Best Parameter Value']))
                        plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
                                 markersize=12)

                    if self.legend:
                        if self.legend_loc is not None:
                            plt.legend(loc=self.legend_loc)
                        else:
                            plt.legend(loc='best')

                    if self.despine:
                        seaborn.despine(fig=fig, top=True, right=True)

                    if self.title is None:
                        self.title = 'Profile Likelihoods for\n{} ' \
                                     'against {} (index={})'.format(x, y, i)

                    elif self.title is 'profile':
                        self.title = x

                    else:
                        plt.title(self.title)

                    if self.log10:
                        plt.ylabel('log10 {}'.format(y))
                        plt.xlabel('log10 {}'.format(x))
                    else:
                        plt.ylabel(y)
                        plt.xlabel(x)

                    if self.ylim is not None:
                        plt.ylim(self.ylim)

                    if self.xlim is not None:
                        plt.xlim(self.xlim)

                    if self.savefig:
                        d = os.path.join(self.results_directory, str(i))
                        d = os.path.join(d, x)
                        self.create_directory(d)
                        fname = os.path.join(d, misc.RemoveNonAscii(y).filter + '.{}'.format(self.ext))

                        plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                        LOG.info('saved to --> {}'.format(fname))

                    if self.show:
                        plt.show()

@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class PlotProfileLikelihood3d(object):
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
                                   'y': None, #can equal all
                                   'z': None,
                                   'index': None,
                                   'log10': True,
                                   'savefig': False,
                                   'results_directory': None,
                                   'dpi': 400,
                                   'plot_cl': True,
                                   'alpha': 0.95,
                                   'title': None,
                                   'xlabel': None,
                                   'ylabel': None,
                                   'legend': False,
                                   'legend_loc': None,
                                   'show': False,
                                   'separate': True,
                                   'filename': None,
                                   'despine': True,
                                   'ext': 'png',
                                   'show_best_rss': True,
                                   'best_rss_marker': 'k*', ##Any matplotlib marker
                                   'ylim': None,
                                   'xlim': None,
                                   'interpolation': None,
                                   'interpolation_resolution': 1000, #number of steps to interpolate
                                   'context': 'talk',
                                   'font_scale': 1,
                                   'rc': None,
                                   'multiplot': False,
                                   'same_axis': False,
                                   }
        # raise NotImplementedError('Not yet implemented')

        ## todo - colour plots by RSS
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for PlotProfileLikelihood'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.update_properties(self.default_properties)
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        ## parse data
        self.data = Parse(self.cls, log10=self.log10, alpha=self.alpha).data

        ## do some checks
        self._do_checks()

        ## do plotting
        if self.same_axis:
            self.plot_same_axis()
        else:
            self.plot()
        ##todo implement ability to change confidence level from Plot.
        ##at the moment the CL is conputer by Parse. This is not optimal

    def _do_checks(self):
        """

        :return:
        """
        ## todo put original estimatd values on non rss graphs as well
        if self.ylim is not None:
            if not isinstance(self.ylim, tuple):
                raise errors.InputError('ylim arg should be tuple. Got "{}"'.format(type(self.ylim)))

            if len(self.ylim) is not 2:
                raise errors.InputError('ylim arg should be tuple of length 2. '
                                        'See "https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.ylim.html" '
                                        'for details')

        if self.xlim is not None:
            if not isinstance(self.xlim, tuple):
                raise errors.InputError('xlim arg should be tuple. Got "{}"'.format(type(self.xlim)))

            if len(self.xlim) is not 2:
                raise errors.InputError('xlim arg should be tuple of length 2. '
                                        'See "https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.xlim.html" '
                                        'for details')

        interpolation_kinds = ['linear', 'nearest', 'zero',
                               'slinear', 'quadratic', 'cubic']

        if self.interpolation is not None:
            if self.interpolation not in interpolation_kinds:
                raise errors.InputError('"{}" is not in "{}"'.format(
                    self.interpolation, interpolation_kinds
                ))

        if type(self.cls) == tasks.ProfileLikelihood:
            self.results_directory = self.cls.results_directory
        else:
            LOG.warning('cls not of type tasks.ProfileLikelihood')

        if isinstance(self.data, pandas.core.frame.DataFrame) != True:
            raise errors.InputError('"{}" should be a dataframe not "{}".'.format(self.data, type(self(data))))

        self.parameter_list = sorted(list(self.data.columns))

        if self.separate == False:

            self.legend = True

        if self.index is None:
            self.index = 0

        if not isinstance(self.index, list):
            self.index = [self.index]

        if self.x == None:
            self.x = [i for i in self.parameter_list if i is not 'RSS']
            # raise errors.InputError('x cannot be None')

        if self.y == None:
            self.y = 'RSS'

        if self.y == 'all':
            self.y = self.parameter_list

        if self.x == 'all':
            self.x = [i for i in self.parameter_list if i != 'RSS']

        if self.y == None:
            raise errors.InputError('y cannot be None')

        if isinstance(self.y, str):
            self.y = [self.y]

        if isinstance(self.y, list):
            for y_param in self.y:
                if y_param not in self.parameter_list:
                    raise errors.InputError('{} not in {}'.format(y_param, self.parameter_list))

        if isinstance(self.x, str):
            self.x = [self.x]

        if isinstance(self.x, list):
            for x_param in self.x:
                if x_param not in self.parameter_list:
                    raise errors.InputError('{} not in {}'.format(x_param, self.parameter_list))

        if self.filename is not None:
            if not os.path.isabs(self.filename):
                self.filename = os.path.join(self.results_directory, self.filename)

            self.data.to_csv(self.filename)
            LOG.info('Profile likelihood data saved to "{}"'.format(self.filename))

    def plot_same_axis(self):
        """

        :return:
        """
        fig = plt.figure()
        for x in self.x:
            for y in self.y:
                for i in self.index:
                    plot_data = self.data.loc[x, i][y]
                    if type(plot_data) == pandas.Series:
                        plot_data = pandas.DataFrame(plot_data)

                    plot_data = plot_data.reset_index()

                    x_plot = plot_data['Parameter Of Interest Value']
                    y_plot = plot_data[y]

                    if self.interpolation is not None:
                        f = interp1d(x_plot, y_plot, kind=self.interpolation)
                        minimum = x_plot.min()
                        maximum = x_plot.max()
                        step = (maximum - minimum) / self.interpolation_resolution
                        xnew = numpy.arange(start=minimum, stop=maximum, step=step)
                        ynew = f(xnew)
                        plt.plot(xnew, ynew, 'k')
                        plt.plot(x_plot, y_plot, 'ro', label=y, linewidth=2)  # linestyle='o', color='red')
                    else:
                        plt.plot(x_plot, y_plot, label=y)

                    if y is 'RSS':
                        plt.plot(plot_data['Parameter Of Interest Value'],
                             plot_data['Confidence Level'], linewidth=3,
                             linestyle='--', color='green', label='CL')

                    if self.show_best_rss:
                        best_rss = list(set(plot_data['Best RSS Value']))
                        best_param_val = list(set(plot_data['Best Parameter Value']))
                        plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
                                 markersize=12)

                    if self.legend:
                        if self.legend_loc is not None:
                            plt.legend(loc=self.legend_loc)
                        else:
                            plt.legend(loc='best')

                    if self.despine:
                        seaborn.despine(fig=fig, top=True, right=True)

                    if self.title is None:
                        self.title = 'Profile Likelihoods for\n{} ' \
                                     'against {} (index={})'.format(x, y, i)

                    elif self.title is 'profile':
                        self.title = x

                    plt.title(self.title)

                    if self.log10:
                        plt.ylabel('log10 {}'.format(y))
                        plt.xlabel('log10 {}'.format(x))
                    else:
                        plt.ylabel(y)
                        plt.xlabel(x)

                    if self.ylim is not None:
                        plt.ylim(self.ylim)

                    if self.xlim is not None:
                        plt.xlim(self.xlim)

                    if self.savefig:
                        d = os.path.join(self.results_directory, str(i))
                        d = os.path.join(d, x)
                        self.create_directory(d)
                        fname = os.path.join(d, misc.RemoveNonAscii(y).filter + '.{}'.format(self.ext))

                        plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                        LOG.info('saved to --> {}'.format(fname))

                    if self.show:
                        plt.show()

    def plot(self):
        """

        :return:
        """
        for x in self.x:
            for y in self.y:
                if self.multiplot:
                    fig = plt.figure()
                for i in self.index:
                    plot_data = self.data.loc[x, i][y]
                    if type(plot_data) == pandas.Series:
                        plot_data = pandas.DataFrame(plot_data)

                    if not self.multiplot:
                        fig = plt.figure()

                    plot_data = plot_data.reset_index()

                    x_plot = plot_data['Parameter Of Interest Value']
                    y_plot = plot_data[y]

                    if self.interpolation is not None:
                        f = interp1d(x_plot, y_plot, kind=self.interpolation)
                        minimum = x_plot.min()
                        maximum = x_plot.max()
                        step = (maximum - minimum) / self.interpolation_resolution
                        xnew = numpy.arange(start=minimum, stop=maximum, step=step)
                        ynew = f(xnew)
                        plt.plot(xnew, ynew, 'k')
                        plt.plot(x_plot, y_plot, 'ro', label=y, linewidth=2)  # linestyle='o', color='red')
                    else:
                        plt.plot(x_plot, y_plot, label=y, marker='o')

                    if y is 'RSS':
                        plt.plot(plot_data['Parameter Of Interest Value'],
                             plot_data['Confidence Level'], linewidth=3,
                             linestyle='--', color='green', label='CL')


                    if self.show_best_rss:
                        best_rss = list(set(plot_data['Best RSS Value']))
                        best_param_val = list(set(plot_data['Best Parameter Value']))
                        plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
                                 markersize=12)

                    if self.legend:
                        if self.legend_loc is not None:
                            plt.legend(loc=self.legend_loc)
                        else:
                            plt.legend(loc='best')

                    if self.despine:
                        seaborn.despine(fig=fig, top=True, right=True)

                    # LOG.debug('title is --> {}'.format(self.title))
                    # if self.title is None:
                    self.title = 'Profile Likelihoods for\n{} ' \
                                 'against {} (index={})'.format(x, y, i)

                    # elif self.title is 'profile':
                    #     self.title = x

                    plt.title(self.title)

                    if self.log10:
                        plt.ylabel('log10 {}'.format(y))
                        plt.xlabel('log10 {}'.format(x))
                    else:
                        plt.ylabel(y)
                        plt.xlabel(x)

                    if self.ylim is not None:
                        plt.ylim(self.ylim)

                    if self.xlim is not None:
                        plt.xlim(self.xlim)

                    if self.savefig:
                        d = os.path.join(self.results_directory, str(i))
                        d = os.path.join(d, x)
                        self.create_directory(d)
                        fname = os.path.join(d, misc.RemoveNonAscii(y).filter + '.{}'.format(self.ext))

                        plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                        LOG.info('saved to --> {}'.format(fname))

                    if self.show:
                        plt.show()

    def plot_pdf(self):
        """

        :return:
        """
        raise NotImplementedError
        # with PdfPages()
        for x in self.x:
            for y in self.y:
                if self.multiplot:
                    fig = plt.figure()
                for i in self.index:
                    plot_data = self.data.loc[x, i][y]
                    if type(plot_data) == pandas.Series:
                        plot_data = pandas.DataFrame(plot_data)

                    if not self.multiplot:
                        fig = plt.figure()

                    plot_data = plot_data.reset_index()

                    x_plot = plot_data['Parameter Of Interest Value']
                    y_plot = plot_data[y]

                    if self.interpolation is not None:
                        f = interp1d(x_plot, y_plot, kind=self.interpolation)
                        minimum = x_plot.min()
                        maximum = x_plot.max()
                        step = (maximum - minimum) / self.interpolation_resolution
                        xnew = numpy.arange(start=minimum, stop=maximum, step=step)
                        ynew = f(xnew)
                        plt.plot(xnew, ynew, 'k')
                        plt.plot(x_plot, y_plot, 'ro', label=y, linewidth=2)  # linestyle='o', color='red')
                    else:
                        plt.plot(x_plot, y_plot, label=y, marker='o')

                    if y is 'RSS':
                        plt.plot(plot_data['Parameter Of Interest Value'],
                             plot_data['Confidence Level'], linewidth=3,
                             linestyle='--', color='green', label='CL')


                    if self.show_best_rss:
                        best_rss = list(set(plot_data['Best RSS Value']))
                        best_param_val = list(set(plot_data['Best Parameter Value']))
                        plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
                                 markersize=12)

                    if self.legend:
                        if self.legend_loc is not None:
                            plt.legend(loc=self.legend_loc)
                        else:
                            plt.legend(loc='best')

                    if self.despine:
                        seaborn.despine(fig=fig, top=True, right=True)

                    if self.title is None:
                        self.title = 'Profile Likelihoods for\n{} ' \
                                     'against {} (index={})'.format(x, y, i)

                    elif self.title is 'profile':
                        self.title = x

                    else:
                        plt.title(self.title)

                    if self.log10:
                        plt.ylabel('log10 {}'.format(y))
                        plt.xlabel('log10 {}'.format(x))
                    else:
                        plt.ylabel(y)
                        plt.xlabel(x)

                    if self.ylim is not None:
                        plt.ylim(self.ylim)

                    if self.xlim is not None:
                        plt.xlim(self.xlim)

                    if self.savefig:
                        d = os.path.join(self.results_directory, str(i))
                        d = os.path.join(d, x)
                        self.create_directory(d)
                        fname = os.path.join(d, misc.RemoveNonAscii(y).filter + '.{}'.format(self.ext))

                        plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
                        LOG.info('saved to --> {}'.format(fname))

                    if self.show:
                        plt.show()


@mixin(tasks.UpdatePropertiesMixin)
@mixin(ParseMixin)
@mixin(TruncateDataMixin)
@mixin(CreateResultsDirectoryMixin)
class PearsonsCorrelation(PlotKwargs):
    """

    ========    =================================================
    kwarg       Description
    ========    =================================================
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
            'x': 'RSS',
            'y': None,
            'sep': '\t',
            'log10': False,
            'truncate_mode': 'percent',
            'theta': 100,
            'xtick_rotation': 'horizontal',
            'ylabel': 'Frequency',
            'savefig': False,
            'results_directory': None,
            'dpi': 400,
            'title_fontsize': 35,
            'title': True,  #Either True or None/False
            'show': False,
            'ext': 'png',
            'color_bar_pad': 0.1,   #padding for color bar. Dist between bar and axes
            'context': 'talk',
            'font_scale': 1.5,
            'rc': None,
            'copasi_file': None,
            'cmap': 'BrBG_r',
            'center': None,
            'robust': False,
            'annot': None,
            'fmt': '.2g',
            'annot_kws': None,
            'linewidths':0,
            'linecolor': 'white',
            'cbar': True,
            'cbar_kws': None,
            'cbar_ax': None,
            'square' : False,
            'xticklabels': 'auto',
            'yticklabels': 'auto',
            'mask': None,
            'ax': None,
        }

        self.default_properties.update(self.plot_kwargs)
        for i in kwargs.keys():
            assert i in self.default_properties.keys(), '{} is not a keyword argument for PearsonsHeatMap'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)


        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)


        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)

        self.combinations = self.get_combinations()
        self.pearsons, self.p_val = self.do_pearsons()
        self.heatmap()

    def _do_checks(self):
        """

        :return:
        """
        if isinstance(self.cls, str):
            if self.copasi_file is None:
                raise ValueError('When first argument is a string '
                                 'pointing to parameter estimation data '
                                 'specify an argument to copasi_file')
        if self.results_directory is None:
            try:
                self.results_directory = os.path.join(self.cls.model.root, 'PearsonsCorrelation')
            except AttributeError as e:
                self.results_directory = os.path.join(
                    os.path.dirname(self.copasi_file), 'PearsonsCorrelation'
                )

    def get_combinations(self):
        return permutations(list(self.data.keys()), 2)

    def do_pearsons(self):
        """

        :return:
        """
        dct = {}
        for x, y in self.combinations:
            dct[(x, y)] = pearsonr(self.data[x], self.data[y])

        df = pandas.DataFrame(dct).transpose()#, index=['r2', 'p-val']).transpose()
        df.columns = ['r2', 'p-val']
        df.index.name = ['x', 'y']
        df = df.unstack()
        df = df.fillna(value=numpy.nan)
        return df['r2'], df['p-val']

    def heatmap(self):
        seaborn.set_context(context=self.context, font_scale=self.font_scale)
        data = self.pearsons

        data = data.drop('RSS', axis=0)
        data = data.drop('RSS', axis=1)

        plt.figure()
        fig = seaborn.heatmap(data=data,
                              cmap=self.cmap,
                              vmin=-1, vmax=1,
                              center=self.center,
                              robust=self.robust,
                              annot=self.annot,
                              fmt=self.fmt,
                              annot_kws=self.annot_kws,
                              linewidths=self.linewidths,
                              linecolor=self.linecolor,
                              cbar=self.cbar,
                              cbar_kws=self.cbar_kws,
                              cbar_ax=self.cbar_ax,
                              square=self.square,
                              xticklabels=self.xticklabels,
                              yticklabels=self.yticklabels,
                              mask=self.mask,
                              ax=self.ax,
                              )

        if self.log10:
            plt.title('Pearsons Correlation (Log10)')

        else:
            plt.title('Pearsons Correlation')

        if self.savefig:
            self.create_directory(self.results_directory)
            fname = os.path.join(self.results_directory, 'PearsonsHeatmap' + '.{}'.format(self.ext))

            plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
            LOG.info('saved to --> {}'.format(fname))
            pearsons_data_file = os.path.join(self.results_directory, 'r2_data.csv')
            p_val_file = os.path.join(self.results_directory, 'p_val_data.csv')
            self.pearsons.to_csv(pearsons_data_file, sep='\t')
            self.p_val.to_csv(p_val_file, sep='\t')

        if self.show:
            plt.show()


if __name__=='__main__':
    pass
#    execfile('/home/b3053674/Documents/pycotools/pycotools/pycotoolsTutorial/Test/testing_kholodenko_manually.py')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




















