# -*-coding: utf-8 -*-
"""
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
import pandas
# from pandas.parser import CParserError
import matplotlib.pyplot as plt
import scipy
import os
from . import tasks, errors, utils, model
import seaborn
import logging
import glob
import re
import numpy
from .cached_property import cached_property
from math import exp as exponential_function
import math
from scipy.stats.mstats import pearsonr
from cycler import cycler
from collections import OrderedDict
import roadrunner
import tellurium as te

LOG = logging.getLogger(__name__)


class _Plotter:
    """base  for all plotter classes"""

    def plot_kwargs(self):
        """ """
        plot_kwargs = {
            'linestyle': '-',
            'marker': 'o',
            'linewidth': 3,
            'markersize': 8,
            'alpha': 0.5
        }
        return plot_kwargs

    def context(context='talk', font_scale=1, rc=None):
        """

        Args:
          context:  (Default value = 'talk')
          font_scale:  (Default value = 1)
          rc:  (Default value = None)

        Returns:

        """
        seaborn.set_context(
            context=context, font_scale=font_scale, rc=rc
        )

    @staticmethod
    def save_figure(directory, filename, dpi=300):
        """

        Args:
          directory: 
          filename: 
          dpi:  (Default value = 300)

        Returns:

        """
        if not os.path.isdir(directory):
            os.mkdir(directory)
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')

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
        rc = kwargs.get('rc')
        if rc is not None:
            import matplotlib
            matplotlib.rcParams.update(rc)

    @staticmethod
    def parse(cls, log10, copasi_file=None):
        """Mixin method interface to parse class
        :return:

        Args:
          log10: 
          copasi_file:  (Default value = None)

        Returns:

        """
        if type(cls) == Parse:

            if log10:
                return numpy.log10(cls.data)
            else:
                return cls.data
        else:
            return Parse(cls, log10=log10, copasi_file=copasi_file).data

    @staticmethod
    def truncate(data, mode, theta):
        """mixin method interface to truncate data

        Args:
          data: 
          mode: 
          theta: 

        Returns:

        """
        df = TruncateData(data,
                          mode=mode,
                          theta=theta).data
        return df

    @staticmethod
    def create_directory(results_directory):
        """create directory for results and switch to it

        Args:
          results_directory: return:

        Returns:

        """
        if not os.path.isdir(results_directory):
            os.makedirs(results_directory)
        os.chdir(results_directory)
        return results_directory


class _ParameterEstimationPlotter(_Plotter):

    def create_directory(self, cls, data_dict, dirname):
        """
        Create a directory to house some simulation output graphs.
        Args:
            cls: the first argument to the Parse class.
            data_dict: Output from parameter estimation
            dirname: Name of directory

        Returns: Dict

        """
        dct = {}
        for model_name in self.data:
            if self.results_directory is None:
                if type(self.cls) == Parse:
                    dct[model_name] = os.path.join(
                        os.path.dirname(
                            self.cls.config.models[model_name].model.copasi_file
                        ), dirname)
                else:
                    dct[model_name] = os.path.join(
                        self.cls.models[model_name].model.root, 'Boxplots')
                if not os.path.isdir(dct[model_name]):
                    os.makedirs(dct[model_name])
        return dct


class TruncateData(_Plotter):
    """
    Truncates a parameter estimation dataset for a model

    A dict like object containing model names as keys and
    dataframes of truncated parameter estimation data as values.

    Examples:
        Truncate the data to get the top 50% and do not convert to logspace
        >>> data = TruncateData(data, mode='percent', theta=50, log10=False)

        ## truncate using ranks of best fit. Get top 10 and convert to log space
        >>> data = TruncateData(data, mode='ranks', theta=range(10), log10=True)

        ## Choose a number, in log10 space and return all data below thie value
        >>> data = TruncateData(data, mode='below_theta', theta=3.5, log10=True)
    """

    def __init__(self, data, mode='percent', theta=100, log10=False):
        """

        Args:
            data(pandas.DataFrame):
                A dataframe to truncate
            mode (str):
                Either 'percent', 'ranks' or 'below_theta'
            theta (numeric):
                Numeric. A percentage (i.e. 50), the number of ranks or a number
            log10 (bool):
                Whether to return data in log10 space
        """
        self.data = data
        self.mode = mode
        self.theta = theta
        self.log10 = log10
        assert self.mode in ['below_theta', 'percent', 'ranks']

        self.data = self.truncate()

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def below_theta(self):
        """remove data which is not below theta
        :return:
            :py:class:'pandas.DataFrame`

        Args:

        Returns:

        """
        for model_name in self.data:
            data = self.data[model_name]
            assert data.shape[0] != 0, 'There are no data with RSS below {}. Choose a higher number'.format(self.theta)
            self.data[model_name] = self.data[model_name][self.data[model_name]['RSS'] < self.theta]
        return self.data

    def top_theta_percent(self):
        """Remove data not in top theta percent
        :return:
            :py:class:'pandas.DataFrame`

        Args:

        Returns:

        """
        if self.theta > 100 or self.theta < 1:
            raise errors.InputError('{} should be between 0 and 100')
        for model_name in self.data:
            theta_quantile = int(numpy.round(self.data[model_name].shape[0] * \
                                             (float(self.theta) / 100.0)))
            if theta_quantile == 0:
                raise ValueError(
                    f'Cannot get the {self.theta} quantile of this dataset as it is 0. Choose another quantile'
                )
            self.data[model_name] = self.data[model_name].iloc[:theta_quantile]
        return self.data

    def ranks(self):
        """Remove data which is not in the top ranks
        parameter estimation data
        :return:
            :py:class:'pandas.DataFrame`

        Args:

        Returns:

        """
        ## need to reset the index after sorting just in case some of the RSS
        ## values are identical. In this case there is no guarentee that
        ## self.data is in ascending order and breaks with .iloc[0].
        for model_name in self.data:
            self.data[model_name] = self.data[model_name].sort_values(by='RSS').reset_index(drop=True)
            self.data[model_name] = self.data[model_name].iloc[self.theta]
        return self.data

    def truncate(self):
        """:return:"""
        if self.mode == 'below_theta':
            return self.below_theta()  # self.data
        elif self.mode == 'percent':
            return self.top_theta_percent()
        elif self.mode == 'ranks':
            return self.ranks()


class Parse:
    """General class for parsing copasi output into Python.

    First argument is an instance of a pycotools3 class.

    ==================================          ===========================
    instance                                       Description
    ==================================          ===========================
    tasks.TimeCourse                            Parse time course data from
                                                TC.report_name into pandas.df
    tasks.ParameterEstimation                   Parse parameter estimation
                                                data from PE.report_name into pandas.df
    tasks.Scan                                  Parse scan data from scan.report_name
    Parse                                       enable parsing from a parse instance.
                                                Just returns itself
    str                                         Parse data from folder of parameter
                                                estimation data into pandas.df. Requires
                                                the copasi file argument.
    ==================================          ===========================

    Args:

    Returns:

    """

    def __init__(self, cls_instance, log10=False, copasi_file=None, alpha=0.95,
                 rss_value=None, num_data_points=None):
        """

        :param cls_instance:
            A instance of pycotools3 class

        :param log10:
            `bool`. Whether to work on log10 scale

        :param copasi_file:
            `str`. Optional but necessary when cls_instance
            is string. Must be the copasi_file which produced
            the parameter estimation data as Parse extracts
            data headers from the copasi file
        :param rss_value: float
            When cls is a profile likelihood with the current_parameters setting,
             rss_value may not be empty. It is not automatically inferable from
             the COPASI model and must be specified separetly.
        :param num_data_points: int
            When cls is a profile likelihood with current paraemters setting,
            the number of data points cannot be automatically inferred for the calculation
            of likelihood ratio based confidence intervals. Therefore, this must be specified
            by the user.
        """
        self.cls_instance = cls_instance
        self.log10 = log10
        self.copasi_file = copasi_file
        self.model = None
        self.alpha = alpha
        self.rss_value = rss_value
        self.num_data_points = num_data_points

        if self.copasi_file is not None:
            self.model = model.Model(self.copasi_file)

        accepted_types = [tasks.TimeCourse,
                          tasks.Scan,
                          tasks.ParameterEstimation,
                          str,
                          Parse,
                          pandas.DataFrame,
                          ]

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

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def __delitem__(self, key):
        return self.data.__delitem__(key)

    def __iter__(self):
        return self.data.__iter__()

    def __next__(self):
        return self.data.__next__()

    def parse(self):
        """determine class type of self.cls_instance
        and call the appropirate method for
        parsing the data type
        :return:

        Args:

        Returns:

        """
        data = None

        if isinstance(self.cls_instance, tasks.TimeCourse):
            data = self.from_timecourse()

        # elif type(self.cls_instance) == tasks.ParameterEstimation:
        #     data = self.from_parameter_estimation

        elif type(self.cls_instance) == tasks.ParameterEstimation:
            data = self.from_multi_parameter_estimation(self.cls_instance)

        elif type(self.cls_instance) == Parse:
            data = self.cls_instance.data

        elif type(self.cls_instance) == pandas.core.frame.DataFrame:
            data = self.cls_instance
            if 'RSS' not in list(data.keys()):
                raise errors.InputError('DataFrame should have an RSS column. Your '
                                        'df only has these: "{}"'.format(data.columns))
            data = data.sort_values(by='RSS')

        ##They are all strings. So only do this last
        elif type(self.cls_instance == str):
            data = self.from_folder()

        if self.log10:
            for model_name, df in data.items():
                data[model_name] = numpy.log10(data[model_name])
        return data

    def from_timecourse(self):
        """read time course data into pandas dataframe. Remove
        copasi generated square brackets around the variables
        :return: pandas.DataFrame

        Args:

        Returns:

        """

        df = pandas.read_csv(self.cls_instance.report_name, sep='\t')
        try:
            headers = [re.findall('(Time)|\[(.*)\]', i)[0] for i in list(df.columns)]
            time = headers[0][0]
            headers = [i[1] for i in headers]
            headers[0] = time
            df.columns = headers
        except IndexError as e:
            if e.message == 'list index out of range':
                pass
        return df

    def parse_scan(self):
        """read scan data into pandas Dataframe.
        :return: pandas.DataFrame

        Args:

        Returns:

        """
        df = pandas.read_csv(
            self.cls_instance.report_name,
            sep='\t',
            skip_blank_lines=False,
        )
        return NotImplementedError('scan plotting features are not yet implemented')

    @cached_property
    def from_parameter_estimation(self):
        """Parse parameter estimation data. Store the data in
        a cache.
        :return:

        Args:

        Returns:

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
            names = self.cls_instance.model.fit_item_order + ['RSS']
            data.columns = names
            os.remove(self.cls_instance.report_name)
            data.to_csv(self.cls_instance.report_name,
                        sep='\t',
                        index=False)
            return data

    @staticmethod
    def from_multi_parameter_estimation(cls_instance):
        """Results come without headers - parse the results
        give them the proper headers then overwrite the file again

        Args:
          cls_instance: instance of MultiParameterEstiamtion
          folder: afternative folder to parse from. Useful for tests (Default value = None)

        Returns:

        """

        def read1(folder):
            tmp_dct = {}
            for report_name in folder:
                report_name = os.path.abspath(report_name)
                if not os.path.isfile(report_name):
                    raise FileNotFoundError('"{}" does not exist'.format(report_name))

                try:
                    data = pandas.read_csv(report_name,
                                           sep='\t',
                                           header=None, skiprows=[0])
                except:
                    LOG.warning(f'No data are available in parameter estimation data file '
                                f' "{os.path.split(report_name)[1]}". Since it is empty, it will be '
                                f'skipped.')
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
                    tmp_dct[report_name] = data
                else:
                    data = data.drop(data.columns[[0, -2]], axis=1)
                    data.columns = list(range(data.shape[1]))
                    ### parameter of interest has been removed.
                    names = mod.fit_item_order + ['RSS']
                    if mod.fit_item_order == []:
                        raise errors.SomethingWentHorriblyWrongError('Parameter Estimation task is empty')

                    if len(names) != data.shape[1]:
                        raise errors.SomethingWentHorriblyWrongError(
                            f'The shape of parameter estimation data ({data.shape}) does not '
                            f'match the number of parameters that were estimated ({len(names)}). You might be '
                            f'using an old parameter set on a new model? ')

                    if os.path.isfile(report_name):
                        os.remove(report_name)
                    data.columns = names
                    data.to_csv(report_name, sep='\t', index=False)
                    tmp_dct[report_name] = data
            return tmp_dct

        dct = {}
        for model_name in cls_instance.models:
            mod = cls_instance.models[model_name].model
            ##set default
            folder = cls_instance.results_directory[model_name]

            ## I need to split this function into two because
            ## of the nested for loop and skipping files if they are
            ## empty using continue. (i.e. continue will continue over both loops, not one
            tmp_dct = read1(glob.glob(folder + r'/*.txt'))

            df = pandas.concat(tmp_dct, sort=True)
            columns = df.columns
            ## reindex, drop and sort by RSS
            df = df.reset_index().drop(['level_0', 'level_1'], axis=1).sort_values(by='RSS')

            dct[model_name] = df.reset_index(drop=True)
        return dct

    # @cached_property
    def from_chaser_estimations(self, cls_instance, folder=None):
        """:return:

        Args:
          cls_instance:
          folder:  (Default value = None)

        Returns:

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
                d.append(data)

            except ValueError as e:
                if str(e) == 'No columns to parse from file':
                    LOG.info('Empty file "{}". Skipping'.format(report_name))

        df = pandas.concat(d)
        df = df.sort_values(by='RSS').reset_index(drop=True)
        return df.apply(pandas.to_numeric)  # astype('float')

    def from_folder(self):
        """

        Args:
          folder: return:

        Returns:

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
                                    ' parameter estimation data. This is a common error when '
                                    'shifting data to and from a cluster. In this case, set '
                                    '"run_mode" to False and use the _setup method of '
                                    'ParameterEstimation, MultiParameterEstimation or '
                                    'MultiModelFit classes. ')

        d = {}
        for report_name in glob.glob(os.path.join(self.cls_instance, '*.txt')):
            report_name = os.path.abspath(report_name)
            if os.path.isfile(report_name) != True:
                raise errors.FileDoesNotExistError('"{}" does not exist'.format(report_name))

            try:
                data = pandas.read_csv(report_name, sep='\t', header=None, skiprows=[0])
                read_type = 'multi_parameter_estimation'
            except ValueError as e:
                if e == 'No columns to parse from file':
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
                        raise ValueError(
                            """
                            pandas raised the following error \n {} \n while trying
                            to read from "{}". It is likely that for some reason not all your
                            data files are uniform in shape. Perhaps this has occured
                            because more than one parameter estimation iterations have tried
                            to write to the same file?
                            """.format(e, report_name)
                        )

            # except CParserError:
            #     raise CParserError('Parameter estimation data file is empty')

            if read_type == 'multi_parameter_estimation':
                bracket_columns = data[data.columns[[0, -2]]]
                if bracket_columns.iloc[0].iloc[0] != '(':
                    data = pandas.read_csv(report_name, sep='\t')
                    d[report_name] = data
                else:
                    data = data.drop(data.columns[[0, -2]], axis=1)
                    data.columns = list(range(data.shape[1]))
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
        if d == {}:
            raise ValueError(f'There is no parameter '
                             f'estimation data to read.')
        df = pandas.concat(d)
        columns = df.columns
        ## reindex, drop and sort by RSS
        df = df.reset_index().drop(['level_0', 'level_1'], axis=1).sort_values(by='RSS')

        return df.reset_index(drop=True)

    def from_profile_likelihood(self):
        """Parse data from :py:class:`tasks.ProfileLikelihood`
        :return:
            :py:class:`pandas.DataFrame`

        Args:

        Returns:

        """
        print('invoked')
        # def get_results():
        #     """Get results files as dict
        #     :return:
        #         2 element `tuple`.
        #         First element:
        #             dict[model_number][parameter] = path/to/results.csv
        #
        #         Second element:
        #             dict[model_number][parameter] = fit item order for that model
        #
        #     Args:
        #
        #     Returns:
        #
        #     """
        #     results_dirs = {}
        #     fit_item_order_dirs = {}
        #     param_of_interest_dict = {}
        #
        #     ## iterate over models in ProfileLikelihood task
        #     for model in self.cls_instance.model_dct:
        #
        #         ## create dict's for collection of results
        #         results_dirs[model] = {}
        #         fit_item_order_dirs[model] = {}
        #         param_of_interest_dict[model] = {}
        #
        #         ## iterate over parameters in models
        #         for param in self.cls_instance.model_dct[model]:
        #
        #             ## get the copasi file from that model
        #             copasi_file = self.cls_instance.model_dct[model][param].copasi_file
        #
        #             ## infer the results file from copasi file
        #             results_file = os.path.splitext(copasi_file)[0] + '.csv'
        #
        #             ## ensure it exists
        #             if not os.path.isfile(results_file):
        #                 raise errors.InputError('file does not exist: "{}"'.format(results_file))
        #
        #             ## assign to dict
        #             results_dirs[model][param] = results_file
        #
        #             ## collect fit items
        #             fit_item_order_dirs[model][param] = self.cls_instance.model_dct[model][param].fit_item_order
        #     return results_dirs, fit_item_order_dirs
        #
        # def experiment_files_in_use(mod):
        #     """Search the model specified by mod for experiment
        #     files defined in the parameter estimation task
        #
        #     Args:
        #       mod: py:class:`model.Model`. The
        #     still configured model that was used
        #     to generate parameter estimation data
        #
        #     Returns:
        #       list` of experiment files
        #
        #     """
        #     query = '//*[@name="File Name"]'
        #     l = []
        #     for i in mod.xml.xpath(query):
        #         f = os.path.abspath(i.attrib['value'])
        #         if os.path.isfile(f) != True:
        #             raise errors.InputError(
        #                 'Experimental files in use cannot be automatically '
        #                 ' determined. Please give a list of experiment file '
        #                 'paths to the experiment_files keyword'.format())
        #         l.append(os.path.abspath(i.attrib['value']))
        #     return l
        #
        # def dof(mod):
        #     """Return degrees of freedom. This is the
        #     number of estimated parameters minus 1
        #
        #     Args:
        #       mod: py:class:`model.Model`. The
        #     still configured model that was used
        #     to generate parameter estimation data
        #
        #     Returns:
        #
        #     """
        #     return len(mod.fit_item_order) - 1
        #
        # def num_data_points(experiment_files):
        #     """number of data points in your data files. Relies on
        #     being able to locate the experiment files from the
        #     copasi file
        #
        #     :return:
        #         `int`.
        #
        #     Args:
        #       experiment_files:
        #
        #     Returns:
        #
        #     """
        #     experimental_data = [pandas.read_csv(i, sep='\t') for i in experiment_files]
        #     l = []
        #     for i in experimental_data:
        #         l.append(i.shape[0] * (i.shape[1] - 1))
        #     s = sum(l)
        #     if s == 0:
        #         raise errors.InputError('Number of data points cannot be 0. '
        #                                 'Experimental data is inferred from the '
        #                                 'parameter estimation task definition. '
        #                                 'It might be that copasi_file refers to a '
        #                                 'fresh copy of the model. Try redefining the '
        #                                 'same parameter estimation problem that you '
        #                                 'used in the profile likelihood, using the '
        #                                 '_setup method but not running the '
        #                                 'parameter estimation before trying again.')
        #     return s
        #
        # def confidence_level(cls):
        #     """Get confidence level using ChiSquaredStatistics
        #
        #     :return:
        #         dict[index][confidence_level]
        #
        #     Args:
        #
        #     Returns:
        #
        #     """
        #     CL_dct = {}
        #     if cls.index == 'current_parameters':
        #         rss_value = self.rss_value
        #         experiment_files = experiment_files_in_use(cls.model)
        #         CL_dct[0] = float(ChiSquaredStatistics(rss_value, dof(cls.model),
        #                                                num_data_points(experiment_files), self.alpha).CL)
        #     else:
        #         for index in cls.parameters:
        #             rss_value = cls.parameters[index]['RSS']
        #             experiment_files = experiment_files_in_use(cls.model)
        #             CL_dct[index] = float(ChiSquaredStatistics(rss_value, dof(cls.model),
        #                                                        num_data_points(experiment_files), self.alpha).CL)
        #     return CL_dct
        #
        # def parse_data(results_dict, fit_item_order_dict):
        #     """Parse data from profile likelihood analysis
        #     into :py:class`pandas.DataFrame`
        #
        #     Args:
        #       results_dict: dict[model][param] = path/to/csv.
        #     First element of output from get_results
        #       fit_item_order_dict: dict[model][param] = model.fit_item_order.
        #     second element from output of get_results
        #
        #     Returns:
        #       py:class:`pandas.DataFrame`. Results in
        #       formatted pandas Dataframe
        #
        #     """
        #     res = {}
        #     df_list = []
        #     for index in results_dict:
        #         res[index] = {}
        #         for param in results_dict[index]:
        #             df = pandas.read_csv(results_dict[index][param],
        #                                  sep='\t', skiprows=1, header=None)
        #             bracket_indices = [1, -2]
        #             df = df.drop(df.columns[bracket_indices], axis=1)
        #             df.columns = list(range(len(df.columns)))
        #             items = ['Parameter Of Interest Value'] + fit_item_order_dict[index][param] + ['RSS']
        #             df.columns = items
        #             if self.log10:
        #                 df_list2 = []
        #                 for key in list(df.keys()):
        #                     l = []
        #                     for i in range(df[key].shape[0]):
        #                         l.append(numpy.log10(df[key].iloc[i]))
        #                     df_list2.append(pandas.DataFrame(l, columns=[key]))
        #                 df = pandas.concat(df_list2, axis=1)
        #             CL = confidence_level(self.cls_instance)
        #
        #             if self.cls_instance.index == 'current_parameters':
        #                 """
        #                 This is a patch over what was here originally to
        #                 get the current parameters index working.
        #                 """
        #                 ## set index name to current parameters
        #                 # self.cls_instance.parameters['best_parameter_set'] = 0#'current_parameters'
        #                 # self.cls_instance.parameters.set_index('best_parameter_set', drop=True, inplace=True)
        #
        #                 if self.log10:
        #                     ## get best parameters
        #                     df['Best Parameter Value'] = math.log10(
        #                         float(self.cls_instance.parameters.loc[index][param]))
        #                     df['Best RSS Value'] = math.log10(float(self.rss_value))
        #                     ## This is the old version::
        #                     # CL[index] = math.log10(CL[index])
        #                     CL[index] = math.log10(CL[index])
        #                 else:
        #                     df['Best Parameter Value'] = float(self.cls_instance.parameters.loc[index][param])
        #                     df['Best RSS Value'] = float(self.rss_value)
        #             else:
        #                 if self.log10:
        #                     df['Best Parameter Value'] = math.log10(float(self.cls_instance.parameters[index][param]))
        #                     df['Best RSS Value'] = math.log10(float(self.cls_instance.parameters[index]['RSS']))
        #                     CL[index] = math.log10(CL[index])
        #
        #                 else:
        #                     df['Best Parameter Value'] = float(self.cls_instance.parameters[index][param])
        #                     df['Best RSS Value'] = float(self.cls_instance.parameters[index]['RSS'])
        #
        #             ## end of patch
        #             ## with index works with from file but not from current_parameters
        #             df['Confidence Level'] = CL[index]
        #             # df['Confidence Level'] = CL[param]
        #             df['Best Fit Index'] = index
        #             df['Parameter Of Interest'] = param
        #             df = df.set_index(['Parameter Of Interest', 'Best Fit Index', 'Confidence Level',
        #                                'Best Parameter Value', 'Best RSS Value',
        #                                'Parameter Of Interest Value'], drop=True)
        #             df_list.append(df)
        #     df = pandas.concat(df_list)
        #     return df
        #
        # print('asdfasdjfnalisdcli')
        # print(get_results())
        # results, fit_item_order = get_results()

        # return parse_data(results, fit_item_order)

    def concat(self):
        return pandas.concat(self.data)


class PlotTimeCourse(_Plotter):
    """Plot time course data

    Time course kwargs:

    ================    ======================================
    kwarg               Description
    ================    ======================================
    x                   `str`. Parameter to go on x axis.
                        defaults to 'Time'. If not 'Time'
                        then  plot is a phase space plot. Required.
    y                   `str` or `list` of `str`. Parameters
                        for the y axis. Required.
    log10               `bool` plot on log10 scale
    separate            bool` separate time courses onto
                        different axes. Default: True
    **kwargs            See :ref:`kwargs` for more options
    ================    ======================================

    Args:

    Returns:

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

        # TODO implement `separate` keyword as `share` insteady

        self.default_properties = {
            'x': 'time',
            'y': None,
            'log10': False,
            'separate': True,
            'savefig': False,
            'results_directory': None,
            'title': None,
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
        for i in list(kwargs.keys()):
            assert i in list(self.default_properties.keys()), '{} is not a keyword ' \
                                                              'argument for PlotTimeCourse'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs())
        self.update_properties(self.default_properties)
        self._do_checks()

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.fig = self.plot()

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
        """:return:"""
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
        """:return:"""
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
            if i not in list(self.data.keys()):
                raise errors.InputError('{} not in {}'.format(i, list(self.data.keys())))

        if self.x == 'time':
            self.x = 'Time'
        if self.x not in list(self.data.keys()):
            raise errors.InputError('{} not in {}'.format(self.x, list(self.data.keys())))

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


class PlotTimeCourseEnsemble(_Plotter):
    """Plot a time course ensemble from a model and
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
    multiple times if you have multiple _experiments measuring the same varibale.

    Args:

    Returns:

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
                   'color': 'husl',
                   'err_style': 'ci_band',
                   'err_palette': None,
                   'err_kws': None,
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
                   'legend_loc': (1, 0.1),
                   'legend_labels': None,
                   'ext': 'png',
                   'context': 'talk',
                   'font_scale': 1.5,
                   'rc': None,
                   'copasi_file': None,
                   'normalize_y_axis': False,
                   'ymin': None,
                   'ymax': None,
                   }

        for i in list(kwargs.keys()):
            assert i in list(options.keys()), '{} is not a keyword argument for ParameterEnsemble'.format(i)
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

        ## set seaborn and matplotlib colours
        colours = sorted(seaborn.color_palette('husl', len(self.experimental_data)))
        plt.rc('axes', prop_cycle=cycler('color', colours))
        seaborn.set_palette(colours)

        self.exp_times = self.get_experiment_times

        self.independent_vars_dct = (self.collect_independent_vars())
        self.ensemble_data = self.simulate_ensemble()
        self.ensemble_data.index = self.ensemble_data.index.rename(['Experiment', 'Index', 'Time'])

        if self.data_filename is not None:
            self.ensemble_data.to_csv(self.data_filename)
            LOG.info('Data written to {}'.format(self.data_filename))
        self.plot_per_observable()

    def create_directory(self):
        """create a directory for the results
        :return:

        Args:

        Returns:

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
        """:return:"""
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

            self.experiment_files = sorted(self.experiment_files)

    @property
    def parse_experimental_files(self):
        """:return:"""
        df_dct = OrderedDict()
        if type(self.cls) == Parse:
            exp_files = self.experiment_files

        elif type(self.cls) is pandas.core.frame.DataFrame:
            exp_files = self.experiment_files

        else:
            exp_files = self.cls.experiment_files

        if exp_files is None:
            raise errors.InputError('if input class is Parse or pandas.DataFrame object '
                                    'experiment_files argument cannot be None')
        exp_files = sorted(exp_files)
        ## if exp_files is empty then read_csv would not be called
        for i in range(len(exp_files)):
            df = pandas.read_csv(exp_files[i],
                                 sep='\t', skip_blank_lines=False, header=None)
            ## mangle dupe cols
            df = df.rename(columns=df.iloc[0], copy=False).iloc[1:].reset_index(drop=True)
            df = df.astype(float)
            df = df.dropna(axis=0)

            is_null = df.isnull().all(1)
            from collections import Counter
            count = Counter(is_null)
            if count[True] > 0:
                df_list = numpy.split(df, df[df.isnull().all(1)].index)
                df_list = [j.dropna(how='all') for j in df_list]
                for j in range(len(df_list)):
                    if df_list[j].empty:
                        raise ValueError('Empty parameter set. ')

                    else:
                        df_dct[exp_files[i] + str(j)] = df_list[j]
            else:
                df_dct[exp_files[i]] = df
        return df_dct

    @property
    def get_experiment_times(self):
        """ """
        d = OrderedDict()
        time_marker = False
        for i in sorted(self.experimental_data):
            d[i] = OrderedDict()
            for j in list(self.experimental_data[i].keys()):
                if j.lower() == 'time':
                    time_marker = True
                    d[i] = self.experimental_data[i][j]

        ## Protect against not having time column labelled correctly
        if not time_marker:
            raise errors.InputError('Column in data file called \'time\' or \'Time\' not '
                                    ' detected. Please check your experiment file. The first '
                                    'column should be labelled Time for time course.')
        times = OrderedDict()
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

    def collect_independent_vars(self):
        """If experiment file has independant vars (_indep) defined, go and get them
        :return:

        Args:

        Returns:

        """
        d = OrderedDict()
        for i in sorted(self.experimental_data):
            d[i] = OrderedDict()
            for j in sorted(list(self.experimental_data[i].keys())):
                if j[-6:] == '_indep':

                    val = list(set(self.experimental_data[i][j]))
                    if len(val) is not 1:
                        raise ValueError('Independant values should be unique in a single data column, '
                                         'i.e. the column should be a single number. '
                                         'Found "{}" distinct numbers. Please amend input data file'.format(len(val)))
                    d[i][j] = val
        return d

    def simulate_ensemble(self):
        """ """
        ## collect end times for each experiment
        ##in order to find the biggest
        end_times = []
        for i in self.exp_times:
            ## start creating a results dict while were at it
            end_times.append(self.exp_times[i]['end'])
        intervals = max(end_times) / self.step_size
        d = OrderedDict()
        df_dct = OrderedDict()
        for exp_file in sorted(self.independent_vars_dct):
            indep_vars = self.independent_vars_dct[exp_file]
            ## indep_vars now contains a list of indep vars in the file
            ## I need to change all of the independent values per file at once
            indep_vars = {i[:-6]: v for i, v in list(indep_vars.items())}

            I = model.InsertParameters(self.cls.model, parameter_dict=indep_vars, inplace=True)
            d[exp_file] = OrderedDict()
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
                d[exp_file][i] = self.parse(TC, log10=False, copasi_file=self.copasi_file)
            df_dct[os.path.split(exp_file)[1][:-4]] = pandas.concat(d[exp_file])
        return pandas.concat(df_dct)

    @property
    def observables(self):
        """

        Args:

        Returns:
          :return:

        """
        obs = []
        for i in self.experimental_data:
            obs += list(self.experimental_data[i].keys())
        return sorted(list(set([i for i in obs if str(i).lower() != 'time'])))

    def plot_per_observable(self):
        """Plot observables with _experiments on same graph.
        i.e. variable x in treated and control conditions
        will be plotted together.

        Args:

        Returns:

        """
        if self.y == None:
            self.y = [i for i in list(self.observables) if i in list(self.ensemble_data.keys())]

        if isinstance(self.y, list) != True:
            self.y = [self.y]

        for param in self.y:
            if param not in list(self.ensemble_data.keys()):
                raise errors.InputError('{} not in your data set. {}'.format(param, sorted(self.ensemble_data.keys())))

        # data = {i.reset_index(level=1, drop=True) for i in self.ensemble_data}
        data = self.ensemble_data[sorted(self.ensemble_data.keys())]  # .reset_index()
        ## remove the existing time column so we can get it back again by resetting index
        data = data.drop('Time', axis=1)
        data = data.reset_index(level=[1, 2])

        experiments = sorted(list(set(data.index)))

        for parameter in sorted(self.y):
            if parameter not in ['ParameterFitIndex', 'Time']:
                LOG.info('Plotting "{}"'.format(parameter))
                fig, ax = plt.subplots()
                plot_data = data.reset_index()

                ax1 = seaborn.tsplot(
                    data=plot_data,
                    time='Time',
                    value=parameter,
                    condition='Experiment',
                    unit='Index',
                    err_style=self.err_style,
                    err_palette=self.err_palette,
                    err_kws=self.err_kws,
                    estimator=self.estimator,
                    n_boot=self.n_boot,
                    ci=self.ci,
                    legend=self.legend,
                )

                for exp in sorted(self.experimental_data):
                    df = self.experimental_data[exp]
                    exp = os.path.split(exp)[1][:-4]
                    if parameter in list(df.keys()):
                        if df.columns[0] == 'time':
                            df = df.rename(columns={'time': 'Time'})
                        # plt.figure()
                        df_keys = list(df[parameter].keys())

                        if len(df_keys) > 1:
                            # for i in range(len(df_keys)):
                            plt.plot(list(df['Time']), df[parameter], '--',
                                     label=exp, alpha=0.4, marker='o')
                        else:
                            plt.plot(list(df['Time']), sorted(list(df[parameter])), '--',
                                     label=exp, alpha=0.4, marker='o')
                if self.legend:
                    # sim_patch = mpatches.Patch(color=self.color, label='Sim', alpha=0.4)
                    # exp_patch = mpatches.Patch(color=self.exp_color, label='Exp', alpha=0.4)
                    # plt.legend(handles=[sim_patch, exp_patch], loc=(1, 0.5))
                    plt.legend(loc=self.legend_loc)
                    if self.legend_labels is not None:
                        handle, labels = ax1.get_legend_handles_labels()
                        new_labels = []
                        for lab in labels:
                            if lab in self.legend_labels:
                                new_labels.append(self.legend_labels[lab])

                            else:
                                new_labels.append(lab)
                        assert len(labels) == len(new_labels)

                        plt.legend(handle, new_labels, loc=self.legend_loc)

            if self.despine:
                seaborn.despine(ax=ax1, top=True, right=True)

            if self.title is None:
                plt.title('{} (n={})'.format(parameter, self.data.shape[0]))

            else:
                plt.title(self.title)

            if self.ylabel is None:
                plt.ylabel('{}/{}'.format(self.cls.model.quantity_unit,
                                          self.cls.model.volume_unit) + '$^{-1}$')

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
                    utils.RemoveNonAscii(parameter).filter, self.ext))
                plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
            if self.show:
                plt.show()


class PlotScan(_Plotter):
    """TODO: Create visualization facilities for parameter scans."""

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

        for i in list(kwargs.keys()):
            assert i in list(self.default_properties.keys()), '{} is not a keyword argument for Boxplot'.format(i)
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


class Boxplots(_Plotter):
    """Plot a boxplot for multi parameter estimation data.

    ============    =================================================
    kwarg           Description
    ============    =================================================
    num_per_plot    Number of parameter per plot. Remainder
                    fills up another plot.
    **kwargs        see :ref:`kwargs`  options
    ============    =================================================

    Args:

    Returns:

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
        for i in list(kwargs.keys()):
            assert i in list(self.default_properties.keys()), '{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)

        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
        self.divide_data()
        if self.savefig:
            self.results_directory = self.create_directory()
        self.plot()

    def _do_checks(self):
        """ """
        pass

    def create_directory(self):
        """:return:"""
        dct = {}
        for model_name in self.data:
            if self.results_directory is None:
                dct[model_name] = os.path.join(
                    os.path.dirname(self.cls.models_dir[model_name]), 'Boxplots')

                if not os.path.isdir(dct[model_name]):
                    os.makedirs(dct[model_name])
        return dct

    def plot(self):
        """Plot multiple parameter estimation data as boxplot
        :return:

        Args:

        Returns:

        """
        for model_name in self.data:
            data = self.data[model_name]
            labels = self.divide_data()[model_name]
            for label_set in range(len(labels)):
                fig = plt.figure()  #
                plot_data = data[labels[label_set]]
                seaborn.boxplot(data=plot_data)
                plt.xticks(rotation=self.xtick_rotation)
                if self.despine:
                    seaborn.despine(fig=fig, top=True, right=True)
                if self.title is not None:
                    plt.title(self.title + '(n={})'.format(data.shape[0]))
                plt.ylabel(self.ylabel)
                if self.savefig:
                    fle = os.path.join(self.results_directory[model_name],
                                       '{}{}.{}'.format(self.filename, label_set, self.ext))
                    plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
        if self.show:
            plt.show()

    def divide_data(self):
        """split data into multi plot
        :return:

        Args:

        Returns:

        """
        dct = {}
        for model_name in self.data:
            data = self.data[model_name]
            n_vars = len(list(data.keys()))
            n_per_plot = self.num_per_plot
            #        assert n_per_plot<n_vars,'number of variables per plot must be smaller than the number of variables'
            int_division = n_vars // n_per_plot
            remainder = n_vars - (n_per_plot * int_division)

            l = []
            for i in range(int_division):
                l.append(list(list(data.keys())[i * n_per_plot:(i + 1) * n_per_plot]))
            if remainder is not 0:
                l.append(list(list(data.keys())[-remainder:]))
            dct[model_name] = l
        return dct


class Violinplots(_Plotter):
    """Plot a Violinplots for multi parameter estimation data.

    ============    =================================================
    kwarg           Description
    ============    =================================================
    num_per_plot    Number of parameter per plot. Remainder
                    fills up another plot.
    **kwargs        see :ref:`kwargs`  options
    ============    =================================================

    Args:

    Returns:

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
                                   'filename': 'violinplot',
                                   }
        self.default_properties.update(self.plot_kwargs)
        for i in list(kwargs.keys()):
            assert i in list(self.default_properties.keys()), '{} is not a keyword argument for Boxplot'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)

        self._do_checks()

        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)

        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
        self.divide_data()
        if self.savefig:
            self.results_directory = self.create_directory()
        self.plot()

    def _do_checks(self):
        """ """
        pass

    def create_directory(self):
        """:return:"""
        dct = {}
        for model_name in self.data:
            if self.results_directory is None:
                dct[model_name] = os.path.join(
                    os.path.dirname(self.cls.models_dir[model_name]), 'ViolinPlots')

                if not os.path.isdir(dct[model_name]):
                    os.makedirs(dct[model_name])
        return dct

    def plot(self):
        """Plot multiple parameter estimation data as violin
        :return:

        Args:

        Returns:

        """
        for model_name in self.data:
            data = self.data[model_name]
            labels = self.divide_data()[model_name]
            for label_set in range(len(labels)):
                fig = plt.figure()  #
                plot_data = data[labels[label_set]]
                seaborn.violinplot(data=plot_data, **self.kwargs)
                plt.xticks(rotation=self.xtick_rotation)
                if self.despine:
                    seaborn.despine(fig=fig, top=True, right=True)
                if self.title is not None:
                    plt.title(self.title + '(n={})'.format(data.shape[0]))
                plt.ylabel(self.ylabel)
                if self.savefig:
                    fle = os.path.join(self.results_directory[model_name],
                                       '{}{}.{}'.format(self.filename, label_set, self.ext))
                    plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
        if self.show:
            plt.show()

    def divide_data(self):
        """split data into multi plot
        :return:

        Args:

        Returns:

        """
        dct = {}
        for model_name in self.data:
            data = self.data[model_name]
            n_vars = len(list(data.keys()))
            n_per_plot = self.num_per_plot
            #        assert n_per_plot<n_vars,'number of variables per plot must be smaller than the number of variables'
            int_division = n_vars // n_per_plot
            remainder = n_vars - (n_per_plot * int_division)

            l = []
            for i in range(int_division):
                l.append(list(list(data.keys())[i * n_per_plot:(i + 1) * n_per_plot]))
            if remainder is not 0:
                l.append(list(list(data.keys())[-remainder:]))
            dct[model_name] = l
        return dct


class ChiSquaredStatistics(object):
    def __init__(self, rss, dof, num_data_points, alpha,
                 plot_chi2=False, show=False):
        self.alpha = alpha
        self.dof = dof
        if self.dof == 0 :
            raise ValueError('Degrees of freedom cannot be 0')
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
        table = list(zip(nums, scipy.stats.chi2.cdf(nums, self.dof)))
        chi2_df_alpha = None
        for i in table:
            if i[1] <= alpha:
                chi2_df_alpha = i[0]
        assert chi2_df_alpha is not None
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


class WaterfallPlot(_Plotter):
    """Plot the ordered residual sum of squares (RSS) objective
    function value against the RSS's rank of best fit.
    See :ref:`kwargs` for list of keyword arguments.

    Args:

    Returns:

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
                                   'filename': 'WaterfallPlot',
                                   'despine': True,
                                   'ext': 'png',
                                   'line_transparency': 1,  ##passed to matplotlib alpha parameter
                                   'marker_transparency': 0.7,
                                   'color': 'grey',
                                   'markercolor': 'black',
                                   'marker': '.',
                                   'linewidth': 3,
                                   'markersize': 10,
                                   'context': 'talk',
                                   'font_scale': 1.5,
                                   'rc': None,
                                   'copasi_file': None,
                                   }

        # self.default_properties.update(self.plot_kwargs)
        for i in list(kwargs.keys()):
            assert i in list(self.default_properties.keys()), '{} is not a keyword argument for RssVsIterations'.format(
                i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        # self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()
        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
        self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)

        self.fig = self.plot()

    def _do_checks(self):
        """:return:"""
        if self.log10:
            self.ylabel = 'log$_{10}$ RSS'
            self.xlabel = 'log$_{10}$ Rank of Best Fit'
        else:
            self.ylabel = 'RSS'
            self.xlabel = 'Rank of Best Fit'

    def create_directory(self):
        """
        Create a directory to house some simulation output graphs.
        """

        dct = {}
        for model_name in self.data:
            if self.results_directory is None:
                dct[model_name] = os.path.join(
                    self.cls.models_dir[model_name], 'WaterfallPlots')
                if not os.path.isdir(dct[model_name]):
                    os.makedirs(dct[model_name])
        return dct

    def plot(self):
        """Plot Rss Vs rank of best fit
        :return:
            None

        Args:

        Returns:

        """
        figs = {}
        for label, df in self.data.items():
            figs[label] = plt.figure()
            if self.log10:
                x = numpy.log10(list(range(df['RSS'].shape[0])))
            else:
                x = list(range(df['RSS'].shape[0]))

            plt.plot(x,
                     df['RSS'].sort_values(ascending=True),
                     color=self.color, linewidth=self.linewidth,
                     alpha=self.line_transparency,
                     )

            plt.plot(x,
                     df['RSS'].sort_values(ascending=True), self.marker,
                     color=self.markercolor, markersize=self.markersize,
                     alpha=self.marker_transparency
                     )

            plt.xticks(rotation=self.xtick_rotation)
            if self.title is not None:
                plt.title(self.title + '(n={})'.format(df.shape[0]))
            plt.ylabel(self.ylabel)
            plt.xlabel('Rank of Best Fit')
            if self.despine:
                seaborn.despine(fig=figs[label], top=True, right=True)
            if self.savefig:
                self.results_directory = self.create_directory()
                for model_name, folder in self.results_directory.items():
                    fle = os.path.join(folder, '{}_{}.{}'.format(self.filename, model_name, self.ext))
                    plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
                    print('Saved to {}'.format(fle))

            if self.show:
                plt.show()

        return figs


class PlotProfileLikelihoods(_Plotter):
    def __init__(self, mod, pl, rss, alpha=0.95):
        self.rss = rss
        self.pl = pl
        self.alpha = alpha
        data = Parse(pl).data
        if not isinstance(data, dict):
            raise TypeError('expected a dictionary object but got a {}'.format(type(data)))

        for k, v in data.items():
            if not isinstance(v, pandas.DataFrame):
                raise TypeError('expected a pandas.DataFrame object but got a {}'.format(type(v)))

        self.mod = mod
        self.data = data
        self.data = pandas.concat(self.data, sort=False)

    def _get_number_of_estimated_parameters(self):
        """
        Counts the number of parameters that are present in the parameter estimation task
        Returns:

        """
        query = '//*[@name="FitItem"]'
        c = 0
        for i in self.mod.xml.xpath(query):
            c += 1
        return c

    def get_best_original_parameter_set(self):
        """
        From pe class
        Returns:

        """
        cols = [i for i in self.data.columns if i != 'RSS']
        params = pandas.DataFrame(self.mod.get_parameters_as_dict(), index=[0])
        return params[cols]

    def get_experiment_files(self):
        experiments = self.pl.config.experiments
        dct = {}
        for name in experiments:
            dct[name] = experiments[name].filename
        return dct

    def dof(self):
        """Return degrees of freedom. This is the
        number of estimated parameters minus 1
        Args:
          mod: py:class:`model.Model`. The
        still configured model that was used
        to generate parameter estimation data
        Returns:
        """
        return self._get_number_of_estimated_parameters() - 1

    def num_data_points(self):
        """number of data points in your data files. Relies on
        being able to locate the experiment files from the
        copasi file
        Returns:
        """
        experimental_data = [pandas.read_csv(i, sep='\t') for i in list(self.get_experiment_files().values())]
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
                                    '_setup method but not running the '
                                    'parameter estimation before trying again.')
        return s

    def compute_x(self):
        lb = self.pl.config.settings.pl_lower_bound
        ub = self.pl.config.settings.pl_upper_bound
        parameters = self.get_best_original_parameter_set()
        num_steps = self.pl.config.settings.pe_number
        dct = {}
        for i in parameters:
            val = parameters.loc[0, i]
            low = numpy.log10(val / lb)
            high = numpy.log10(val * ub)
            dct[i] = pandas.Series(numpy.logspace(low, high, num_steps).flatten())
        df = pandas.concat(dct, axis=1)

        return df

    def plot(self, x, y='RSS', ncol=3,
             filename=None, wspace=0.1,
             hspace=1.0, figsize=(12, 8),
             marker='.', **kwargs):
        # validate input
        if not isinstance(y, str):
            raise ValueError('y must be a string')
        if not isinstance(x, (str, list)):
            raise ValueError('x must be a string or a list of strings')
        if x == 'all':
            x = [i for i in self.data.columns if i not in ['RSS', x]]
        if isinstance(x, str):
            x = [x]
        for i in x:
            if not isinstance(i, str):
                raise ValueError('y must be a string or list of strings.')
        if y not in self.data.columns:
            raise ValueError(f'Cannot find parameter "{y}" in your '
                             f'profile likelihood analysis. These '
                             f'are your options {list(sorted(self.data.columns))}')
        if not isinstance(ncol, int):
            raise ValueError('ncol argument must be of type int')
        cl = float(ChiSquaredStatistics(
            self.rss, self.dof(),
            self.num_data_points(), self.alpha).CL)
        # print(self.confidence_level())
        # compute number of rows needed for len(x) plots
        N = len(x)
        if N < ncol:
            ncol = N
        nrow = N // ncol
        r = N % ncol
        if r > 0:
            nrow += 1

        # select plot data
        # if self.data.shape[0] % 2 == 0 :
        #     mid_point = self.data.shape[0] / 2
        #     best_parameters = self.get_best_original_parameter_set()
        #     best_parameters['RSS'] = self.rss
        # best_parameters = pandas.concat(
        #     [self.data.iloc[:mid_point], best_parameters, self.data.iloc[mid_point:]]).reset_index(drop=True)
        ydata = self.data.loc[x, [y]].unstack(level=0)[y]
        xdata = self.compute_x()[x]
        seaborn.set_context('talk')
        from matplotlib.gridspec import GridSpec
        fig = plt.figure(figsize=figsize)
        gs = GridSpec(nrow, ncol, wspace=wspace,
                      hspace=hspace)
        for i, xi in enumerate(x):
            ax = fig.add_subplot(gs[i])
            xplt = numpy.log10(xdata[xi])
            yplt = ydata[xi]
            ax.plot(xplt, yplt, color='grey',
                    label=xi, marker=marker, **kwargs)
            if y == 'RSS':
                ax.plot(xplt, [cl]*len(xplt), color='black', ls='--')
            seaborn.despine(ax=ax, top=True, right=True)
            # plt.xlabel('log10({})'.find(xi))
            plt.ylabel(y)
            plt.title(xi)
        plt.subplots_adjust(hspace=hspace, wspace=wspace)
        if filename is not None:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print('saved figure to "{}"'.find(filename))
        else:
            plt.show()


class PlotParameterEstimation(_ParameterEstimationPlotter):
    """Visualize parameter estimation runs against a single
    parameter estimation. Similar to PlotTimeCourseEnsemble
    but for a single parameter estimation run.



    =========================================       =========================================
    kwarg                                           Description
    =========================================       =========================================
    y                                               `str` or list of `str`. Parameter for plotting
                                                    on y axis. Defaults to all estimated parameters.
    **savefig_kwargs                                see savefig_kwargs for savefig options
    =========================================       =========================================

    Args:

    Returns:

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

        ## defaults to metabolites and global quantities with assignments
        # default_y_dct = {}
        # for model_name in self.cls.models:
        #     default_y_dct[model_name] = [i.name for i in self.cls.models[model_name].model.metabolites] + [i.name for i in self.cls.models[model_name].model.global_quantities if
        #                                                             i.simulation_type == 'Assignment']
        self.default_properties = {
            'y': None,
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
            'font_scale': 1,
            'rc': None,
            'copasi_file': None,
        }
        self.default_properties.update(self.plot_kwargs)
        for i in list(kwargs.keys()):
            assert i in list(
                self.default_properties.keys()), '{} is not a keyword argument for "PlotParameterEstimation"'.format(i)
        self.kwargs = self.default_properties
        self.default_properties.update(kwargs)
        self.default_properties.update(self.plot_kwargs)
        self.update_properties(self.default_properties)
        self._do_checks()

        seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)

        self.data = self.parse(self.cls, self.log10, copasi_file=self.copasi_file)

        self.cls.models = self.update_parameters()
        self.exp_data = self.read_experimental_data()
        self.sim_data = self.simulate()

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
        """ """

        if not isinstance(self.cls, tasks.ParameterEstimation):
            raise errors.InputError('first argument should be ParameterEstimation calss. Got {}'.format(type(self.cls)))

        if self.results_directory is None:
            dct = {}
            for model_name in self.cls.models:
                dct[model_name] = os.path.join(
                    os.path.join(
                        os.path.join(
                            self.cls.models[model_name].model.root, self.cls.config.settings.problem),
                        f'Fit{self.cls.config.settings.fit}',
                        'ParameterEstimationPlots')
                )
            self.results_directory = dct
        # if not isinstance(self.y, list):
        #     self.y = [self.y]

    def update_parameters(self):
        """Use the InsertParameters class to insert estimated

        Args:
          return: Model

        Returns:

        """
        for model_name in self.cls.models:
            self.cls.models[model_name].model.insert_parameters(df=self.data[model_name], inplace=True)
        return self.cls.models

    def create_directories(self):
        """
        create a place for parameter estiamtion plots on disk

        """
        directories = {}
        for model_name in self.cls.models:
            directories[model_name] = {}
            for fle in self.cls.config.experiment_filenames:
                _, fle = os.path.split(fle)
                directories[model_name][fle] = os.path.join(self.results_directory[model_name], fle[:-4])
                if not os.path.isdir(directories[model_name][fle]):
                    os.makedirs(directories[model_name][fle])
        return directories

    def read_experimental_data(self):
        """read the experimental data in order to figure
        out how long a time course we need to simulate
        with the new parameters
        :return:

        Args:

        Returns:

        """

        import csv
        sniffer = csv.Sniffer()

        dct = {}
        for model_name in self.cls.models:
            dct[model_name] = {}
            experiment_files = [self.cls.config.experiments[i].filename for i in self.cls.config.experiments]
            for i in experiment_files:
                with open(i) as f:
                    line = f.readline()
                delimiter = sniffer.sniff(line).delimiter
                df = pandas.read_csv(i, sep=delimiter)
                dct[model_name][i] = df.rename(columns={'Time': 'time'})
        return dct

    def get_time(self):
        """get dict of _experiments and max time
        :return:

        Args:

        Returns:

        """
        dct = {}
        for k, v in self.exp_data.items():
            dct[k] = {}
            for filename, data in v.items():
                if 'time'.lower() not in [i.lower() for i in data]:
                    dct[k][filename] = None
                else:
                    dct[k][filename] = (min(data['time']), max(data['time']))
        return dct

    def simulate(self):
        """simulate a timecourse or steady state for each experiment, using the time column as a flag

        Returns:

        """
        d = {}
        time_dct = self.get_time()
        # iterate over models
        for model_name in self.cls.models:
            mod = self.cls.models[model_name].model
            step_size = 1
            d[model_name] = {}
            # first make sure conditions of the parameter estimation are replicated
            #  by changing independent variables to that specified in the experimental data
            for experiment_file, time in time_dct[model_name].items():
                indep_dct = {}
                for exp_key in list(self.exp_data[model_name][experiment_file].keys()):
                    if exp_key[-6:] == '_indep' and exp_key[:-6] in mod:
                        indep_dct[exp_key[:-6]] = self.exp_data[model_name][experiment_file][exp_key].iloc[0]
                    ## Insert independent vars
                    mod.insert_parameters(parameter_dict=indep_dct, inplace=True)

                # now simulate a steady state or timeseries depending on whether the time column exists in the
                #  experimental data or not
                if time is None:
                    # simulate steady state using tellurium, since steadystate is not yet supported in pycotools
                    te_mod = mod.to_tellurium()
                    te_mod.reset()
                    te_mod.conservedMoietyAnalysis = True
                    te_mod.steadyStateSolver.allow_precomputation = True
                    te_mod.steadyStateSolver.allow_approx = True

                    # add global parameters to ss selections
                    te_mod.steadyStateSelections += te_mod.getGlobalParameterIds()

                    te_mod.steadyState()
                    ss = dict(zip(
                        [i.replace('[', '').replace(']', '') for i in te_mod.steadyStateSelections],
                        te_mod.getSteadyStateValues(),
                    ))
                    d[model_name][experiment_file] = pandas.DataFrame(ss, index=[0])
                else:
                    # simulate time series
                    d[model_name][experiment_file] = mod.simulate(
                        time[0], time[1], step_size,
                        variables='gm'
                    )

        return d

    def plot(self):
        """plot experimental data versus best parameter sets
        :return:

        Args:

        Returns:

        """

        for model_name in self.cls.models:
            newy = []
            for exp in self.exp_data[model_name]:
                for sim in self.sim_data[model_name]:
                    if exp == sim:
                        plot_data_exp = self.exp_data[model_name][exp]
                        plot_data_sim = self.sim_data[model_name][sim]

                        if plot_data_sim is None:
                            continue

                        plot_data_exp = plot_data_exp.rename(columns={'Time': 'time'})
                        plot_data_sim = plot_data_sim.rename(columns={'Time': 'time'})

                        if 'time' in plot_data_exp:

                            for y in plot_data_exp.columns:
                                # sometimes we have data in file that doesn't have a matching simulated variable
                                #  and vice versa. In this situation just continue with a warning
                                if y not in plot_data_exp:
                                    LOG.warning(f'Skipping "{y}" as it is not in the experimental data.')
                                    continue

                                if y not in plot_data_sim:
                                    LOG.warning(f'Skipping "{y}" as it is not in your model.')
                                    continue

                                # do not plot time
                                if y.lower() == 'time':
                                    continue

                                fig = plt.figure()
                                plt.plot(
                                    plot_data_exp['time'], plot_data_exp[y],
                                    label='Exp', linestyle=self.linestyle,
                                    marker=self.marker, linewidth=self.linewidth,
                                    markersize=self.markersize,
                                    alpha=0.7,
                                    color='black',
                                )
                                plt.plot(
                                    plot_data_sim.index, plot_data_sim[y],
                                    label='Sim', linestyle=self.linestyle,
                                    linewidth=self.linewidth,
                                    alpha=0.7,
                                    color='red'
                                )

                                plt.legend(loc=(1, 0.5))
                                plt.title(y)
                                plt.xlabel('Time({})'.format(self.cls.models[model_name].model.time_unit))
                                plt.ylabel('Abundance\n({})'.format(self.cls.models[model_name].model.quantity_unit))
                                seaborn.despine(fig=fig, top=True, right=True)
                                if self.savefig:
                                    dirs = self.create_directories()
                                    exp_key = os.path.split(exp)[1]
                                    fle = os.path.join(dirs[model_name][exp_key], '{}.png'.format(y))
                                    plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
                                    print('figure saved to "{}"'.format(fle))

                        else:
                            for y in plot_data_exp.columns:
                                # sometimes we have data in file that doesn't have a matching simulated variable
                                #  and vice versa. In this situation just continue with a warning
                                if y not in plot_data_exp:
                                    LOG.warning(f'Skipping "{y}" as it is not in the experimental data.')
                                    continue

                                if y not in plot_data_sim:
                                    LOG.warning(f'Skipping "{y}" as it is not in your model.')
                                    continue

                            # get only variables that exist in both
                            ys_in_both = sorted(
                                list(set(plot_data_sim.columns).intersection(set(plot_data_exp.columns))))
                            plot_data_exp = plot_data_exp[ys_in_both]
                            plot_data_sim = plot_data_sim[ys_in_both]

                            ss_df = pandas.concat({'exp': plot_data_exp, 'sim': plot_data_sim})
                            ss_df.index = ss_df.index.droplevel(1)
                            # ss_df.index.name = 'type'
                            ss_df = pandas.DataFrame(ss_df.stack(), columns=['amount'])
                            ss_df.index.names = ['type', 'variable']
                            ss_df = ss_df.reset_index()

                            fig = plt.figure()
                            seaborn.barplot(x='variable', y='amount', hue='type', data=ss_df, edgecolor='black',
                                            linewidth=2, palette='Greys')
                            seaborn.despine(fig=fig, top=True, right=True)
                            plt.xticks(rotation=90, fontsize=12)
                            plt.xlabel('')
                            plt.legend(loc=(1, 0.1))
                            if self.savefig:
                                dirs = self.create_directories()
                                exp_key = os.path.split(exp)[1]
                                fle = os.path.join(dirs[model_name][exp_key], '{}.png'.format(y))
                                plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
                                print('figure saved to "{}"'.format(fle))

    def plot_waterfall(self):
        pass

    def plot_vs_exp(self):
        pass

    def plot_histograms(self):
        pass

    def plot_scatters(self, x, y):
        pass

# class Pca(_Viz, PlotKwargs):
#     """Use the :py:class:`PCA` function to conduct
#     a principle component analysis on the parameter
#     estimation data.
#
#     ===================   ====================
#     kwargs                Description
#     ===================   ====================
#     by                    `str` either Determine which axes of parameter estimation
#                           data to undergoe data reduction. When ``by='iterations'``
#                           the data is reduced to one data point per parameter estimation
#                           run. When ``by='parameters'``, data is reduced to one data point
#                           per parameter.
#     legend_position       `tuple`. When ``by='parameters`` specify the (horizontal, verticle,
#                           line spacing) parameter for the legend location and formatting
#     cmap                  `str` a valid matplotlib colour map
#     annotate              `bool` annotate. Automatically on when ``by='parameters'``
#     annotation_fontsize   `int` or `float`. fontsize for annotation
#     **kwargs              See :ref:`kwargs for more options
#     ===================   ====================
#
#     Args:
#
#     Returns:
#
#     """
#
#     def __init__(self, cls, **kwargs):
#         self.cls = cls
#         self.kwargs = kwargs
#         self.plot_kwargs = self.plot_kwargs()
#
#         self.default_properties = {'sep': '\t',
#                                    'truncate_mode': 'percent',
#                                    'theta': 100,
#                                    'log10': False,
#                                    'ylabel': None,
#                                    'xlabel': None,
#                                    'title': None,
#                                    'savefig': False,
#                                    'results_directory': None,
#                                    'dpi': 400,
#                                    'n_components': 2,
#                                    'by': 'iterations',  ##iterations or parameters
#                                    'legend_position': None,  ##Horizontal, verticle, line spacing
#                                    'legend_fontsize': 25,
#                                    'cmap': 'viridis',
#                                    'annotate': False,
#                                    'annotation_fontsize': 25,
#                                    'show': False,
#                                    'despine': True,
#                                    'ext': 'png',
#                                    'context': 'talk',
#                                    'font_scale': 1.5,
#                                    'rc': None,
#                                    'copasi_file': None,
#                                    }
#
#         self.default_properties.update(self.plot_kwargs)
#         for i in list(kwargs.keys()):
#             assert i in list(self.default_properties.keys()), '{} is not a keyword argument for Pca'.format(i)
#         self.kwargs = self.default_properties
#         self.default_properties.update(kwargs)
#         self.default_properties.update(self.plot_kwargs)
#         self.update_properties(self.default_properties)
#         self._do_checks()
#         seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)
#
#         self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
#         self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
#         self.pca()
#
#     def create_directory(self):
#         """create a directory for the results
#         :return:
#
#         Args:
#
#         Returns:
#
#         """
#         if self.results_directory is None:
#             if type(self.cls) == Parse:
#                 self.results_directory = os.path.join(os.path.dirname(self.cls.copasi_file),
#                                                       'PCA')
#             else:
#                 self.results_directory = os.path.join(self.cls.model.root,
#                                                       'PCA')
#
#         if not os.path.isdir(self.results_directory):
#             os.makedirs(self.results_directory)
#         return self.results_directory
#
#     def _do_checks(self):
#         """varify integrity of user input
#         :return:
#
#         Args:
#
#         Returns:
#
#         """
#         # if self.title is None:
#         #     if self.by is 'parameters':
#         #         title = 'PCA by Parameters (n={})'.format(len(labels))
#         #     elif self.by is 'iterations':
#         #         title = 'PCA by Iterations (n={})'.format(len(labels))
#
#         if self.by not in ['parameters', 'iterations']:
#             raise errors.InputError('{} not in {}'.format(
#                 self.by, ['parameters', 'iterations']))
#
#         # if self.results_directory is None:
#         #     self.results_directory = self.create_directory()
#
#         if self.ylabel == None:
#             if self.log10 == False:
#                 self.ylabel = 'PC2'
#             elif self.log10 == True:
#                 self.ylabel = 'log10 PC2'
#             else:
#                 raise errors.SomethingWentHorriblyWrongError('{} not in {}'.format(
#                     self.ylabel, [True, False]))
#
#         if self.xlabel == None:
#             if self.log10 == False:
#                 self.xlabel = 'PC1'
#             elif self.log10 == True:
#                 self.xlabel = 'log10 PC1'
#             else:
#                 raise errors.SomethingWentHorriblyWrongError(
#                     '{} not in {}'.format(self.ylabel, [True, False]))
#
#         LOG.info('plotting PCA {}'.format(self.by))
#
#         if self.by == 'parameters':
#             self.annotate = True
#             if self.legend_position == None:
#                 LOG.critical(
#                     'When data reduction is by \'parameters\' you should specify an argument to legend_position. i.e. legend_position=(10,10,1.5) for horizontal, vertical and linespacing')
#
#         if self.legend_position is None:
#             self.legend_position = (1, 1, 0.5)  ##horizontal, verticle, linespacing
#
#     def pca(self):
#         """ """
#         pca = PCA(n_components=self.n_components)
#         rss = self.data.RSS
#         self.data = self.data.drop('RSS', axis=1)
#         fig, ax = plt.subplots()
#         if self.by == 'parameters':
#             projected = pca.fit(self.data.transpose()).transform(self.data.transpose())
#             projected = pandas.DataFrame(projected, index=self.data.columns)
#             labels = self.data.columns
#             sc = ax.scatter(projected[0], projected[1])
#
#
#         else:
#             projected = pca.fit(self.data).transform(self.data)
#             projected = pandas.DataFrame(projected, index=self.data.index)
#             labels = list(self.data.index)
#             projected = pandas.concat([rss, projected], axis=1)
#             sc = ax.scatter(projected[0], projected[1], c=projected['RSS'], cmap=self.cmap)
#             cb = plt.colorbar(sc)
#             cb.ax.set_title('RSS')
#
#         if self.despine:
#             seaborn.despine(fig=fig, top=True, right=True)
#
#         plt.ylabel(self.ylabel)
#         plt.xlabel(self.xlabel)
#         plt.title(self.title)
#         # TODO connect copasi with the python community
#         # TODO mjor selling point for pycoools.
#         # TODO interafce with pysces, pyDStools and sloppycell
#         for i, txt in enumerate(labels):
#             if self.annotate:
#                 ax.annotate(str(i), (projected[0][i], projected[1][i]),
#                             fontsize=self.annotation_fontsize)
#             if self.by == 'parameters':
#                 ax.text(self.legend_position[0],
#                         self.legend_position[1] - i * self.legend_position[2],
#                         '{}: {}'.format(i, txt), fontsize=self.legend_fontsize)
#         if self.savefig:
#             self.create_directory()
#             fle = os.path.join(self.results_directory, 'Pca_by_{}.{}'.format(self.by, self.ext))
#             plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
#
#         if self.show:
#             plt.show()
#
#
# class Histograms(_Viz, PlotKwargs):
#     """Plot a Histograms for multi parameter estimation data.
#
#     See :ref:`kwargs` for more options.
#
#     Args:
#
#     Returns:
#
#     """
#
#     def __init__(self, cls, **kwargs):
#         """
#
#         :param cls:
#             Instance of :py:class:`tasks.MultiParameterEstimation`
#             Same as :py:class:`PlotTimeCourseEnsemble`
#
#         :param kwargs:
#         """
#         self.cls = cls
#         self.kwargs = kwargs
#         self.plot_kwargs = self.plot_kwargs()
#
#         self.default_properties = {'sep': '\t',
#                                    'log10': False,
#                                    'truncate_mode': 'percent',
#                                    'theta': 100,
#                                    'xtick_rotation': 'horizontal',
#                                    'ylabel': 'Frequency',
#                                    'title': True,  ##boolean here as title is inferred from parameter
#                                    'savefig': False,
#                                    'results_directory': None,
#                                    'dpi': 400,
#                                    'title_fontsize': 35,
#                                    'show': False,
#                                    'despine': True,
#                                    'ext': 'png',
#                                    'color': 'green',
#                                    'hist': True,
#                                    'kde': False,
#                                    'rug': False,
#                                    'context': 'talk',
#                                    'font_scale': 1.5,
#                                    'rc': None,
#                                    'bins': None,
#                                    'copasi_file': None,
#                                    }
#
#         self.default_properties.update(self.plot_kwargs)
#         for i in list(kwargs.keys()):
#             assert i in list(self.default_properties.keys()), '{} is not a keyword argument for Histograms'.format(i)
#         self.kwargs = self.default_properties
#         self.default_properties.update(kwargs)
#         self.default_properties.update(self.plot_kwargs)
#         self.update_properties(self.default_properties)
#         self._do_checks()
#
#         self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
#         self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
#         LOG.info('plotting histograms')
#         seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)
#
#         self.plot()
#         # self.coloured_plot()
#
#     def _do_checks(self):
#         """:return:"""
#         if self.results_directory is None:
#             if type(self.cls) == Parse:
#                 self.results_directory = os.path.join(os.path.dirname(self.cls.copasi_file), 'Histograms')
#             else:
#                 self.results_directory = os.path.join(self.cls.model.root, 'Histograms')
#
#     def plot(self):
#         """ """
#         for parameter in list(self.data.keys()):
#             fig = plt.figure()
#             seaborn.distplot(
#                 self.data[parameter], color=self.color, kde=self.kde, rug=self.rug,
#                 hist=self.hist,
#                 bins=self.bins
#             )
#             if self.log10:
#                 plt.ylabel("{}".format(self.ylabel))
#                 plt.xlabel("log$_{10}$" + "[{}]".format(parameter))
#             else:
#                 plt.ylabel(self.ylabel)
#                 plt.xlabel(parameter)
#             if self.title is True:
#                 plt.title('{},n={}'.format(parameter, self.data[parameter].shape[0]),
#                           fontsize=self.title_fontsize)
#
#             if self.despine:
#                 seaborn.despine(fig=fig, top=True, right=True)
#
#             if self.savefig:
#                 self.create_directory(self.results_directory)
#                 fname = os.path.join(self.results_directory,
#                                      utils.RemoveNonAscii(parameter).filter + '.{}'.format(self.ext))
#                 plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#                 LOG.info('plot save to "{}"'.format(fname))
#
#     def coloured_plot(self):
#         """:return:"""
#         # for parameter in self.data.keys():
#         raise NotImplementedError('this is an attempt to colour bars '
#                                   'of histogram by RSS but the code does not '
#                                   'work. ')
#         parameter = 'Ski'
#         num_bins = 10
#         width = self.data[parameter].max() - self.data[parameter].min()
#         iqr = scipy.stats.iqr(self.data[parameter])
#         bins_size = 2 * (iqr / (self.data[parameter].shape[0] ** 1.0 / 3.0))
#
#         bins = numpy.arange(self.data[parameter].min(), self.data[parameter].max(),
#                             bins_size)  # width/num_bins
#         ## calculate the density of RSS
#
#         groups = self.data.groupby([pandas.cut(self.data[parameter], bins), 'RSS'])
#         data = groups.size().reset_index([parameter, 'RSS'])
#         data2 = data.groupby(parameter)[0].sum()
#         data3 = data.groupby(parameter)['RSS'].mean()
#         data5 = pandas.concat([data2, data3], axis=1)
#         data5['Density'] = data5[0] / (numpy.sum(data5[0].fillna(0).values * numpy.diff(bins)))
#
#         ## colours
#         norm = plt.Normalize(numpy.nanmin(data5['RSS'].values),
#                              numpy.nanmax(data5['RSS'].values))
#         colours = plt.cm.plasma(norm(data5['RSS'].fillna(0).values))
#
#         fig, ax = plt.subplots()
#
#         ax.bar(bins[:-1], data5.fillna(0)['Density'], width=width, color=colours, align='edge')
#
#         # seaborn.kdeplot(data[parameter], ax=ax, color='k', lw=2)
#
#         sm = plt.cm.ScalarMappable(cmap='plasma', norm=norm)
#         sm.set_array([])
#         fig.colorbar(sm, ax=ax, label='RSS')
#         ax.set_ylabel('Density')
#         ax.set_xlabel(parameter)
#         plt.show()
#
#
# class Scatters(_Viz, PlotKwargs):
#     """Plot scatter graphs. When 'x' and 'y' are lists, 2 way
#     combinations are automatically plotted and organized into
#     folders (when ``savefig=True``). Data is automatically
#     coloured by RSS.
#
#     ========        =================================================
#     kwarg           Description
#     ========        =================================================
#     x               `str` or `list` of `str`. Variable(s) to plot on x
#                     axis. Defaults to ``RSS``
#     y               `str` or `list` of `str`. Variable(s) to plot on
#                     y axis. Defaults to all parameters in data set.
#     cmap            `str` a valid matplotlib colour map
#     colorbar_pad    Default=0.2. Distance of color bar from plot.
#     **kwargs        see :ref:`kwargs` for more options
#     ========        =================================================
#
#     Args:
#
#     Returns:
#
#     """
#
#     def __init__(self, cls, **kwargs):
#         """
#
#         :param cls:
#             Instance of :py:class:`tasks.MultiParameterEstimation`
#             Same as :py:class:`PlotTimeCourseEnsemble`
#
#         :param kwargs:
#         """
#         self.cls = cls
#         self.kwargs = kwargs
#         self.plot_kwargs = self.plot_kwargs()
#
#         self.default_properties = {
#             'x': 'RSS',
#             'y': None,
#             'sep': '\t',
#             'log10': False,
#             'cmap': 'jet_r',
#             'truncate_mode': 'percent',
#             'theta': 100,
#             'xtick_rotation': 'horizontal',
#             'ylabel': 'Frequency',
#             'savefig': False,
#             'results_directory': None,
#             'dpi': 400,
#             'title_fontsize': 35,
#             'title': True,  # Either True or None/False
#             'show': False,
#             'ext': 'png',
#             'despine': True,
#             'colorbar_pad': 0.2,  # padding for color bar. Dist between bar and axes
#             'context': 'talk',
#             'font_scale': 1.5,
#             'rc': None,
#             'copasi_file': None,
#         }
#
#         self.default_properties.update(self.plot_kwargs)
#         for i in list(kwargs.keys()):
#             assert i in list(self.default_properties.keys()), '{} is not a keyword argument for Scatters'.format(i)
#         self.kwargs = self.default_properties
#         self.default_properties.update(kwargs)
#         self.default_properties.update(self.plot_kwargs)
#         self.update_properties(self.default_properties)
#         self._do_checks()
#         seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)
#
#         self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
#         self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
#         self.plot()
#
#     def _do_checks(self):
#         """:return:"""
#         if isinstance(self.x, str):
#             self.x = [self.x]
#
#         if self.results_directory is None:
#             self.results_directory = os.path.join(self.cls.model.root, 'Scatters')
#
#     def plot(self):
#         """:return:"""
#         if self.y is None:
#             self.y = list(self.data.keys())
#
#         if (self.y == 'all') or (self.y == ['all']):
#             self.y = list(self.data.keys())
#
#         if self.x == 'all' or self.x == ['all']:
#             self.x = list(self.data.keys())
#
#         for x_var in self.x:
#             if x_var not in sorted(list(self.data.keys())):
#                 raise errors.InputError('"{}" invalid. These are valid: "{}"'.format(
#                     x_var, list(self.data.keys())
#                 ))
#             for y_var in self.y:
#                 if x_var not in sorted(list(self.data.keys())):
#                     raise errors.InputError('"{}" invalid. These are valid: "{}"'.format(
#                         y_var, list(self.data.keys())
#                     )
#                     )
#                 LOG.info('Plotting "{}" Vs "{}"'.format(x_var, y_var))
#                 fig = plt.figure()
#                 plt.scatter(
#                     self.data[x_var], self.data[y_var],
#                     cmap=self.cmap, c=self.data['RSS'],
#                 )
#                 # c_ax = plt.subplot(199)
#                 # cb = matplotlib.colorbar.ColorbarBase(c_ax, orientation='vertical')
#                 # c_ax.yaxis.set_ticks_position('right')
#                 cb = plt.colorbar(pad=self.colorbar_pad)
#                 # cb.set_
#
#                 if self.title:
#                     title = 'Scatter graph of\n {} Vs {}.(n={})'.format(
#                         x_var, y_var, self.data.shape[0]
#                     )
#
#                 if self.log10:
#                     cb.set_label('log10 RSS')
#                     plt.xlabel('log$_{10}$' + '[{}]'.format(x_var))
#                     plt.ylabel('log$_{10}$' + '[{}]'.format(y_var))
#                 else:
#                     cb.set_label('RSS')
#                     plt.xlabel(x_var)
#                     plt.ylabel(y_var)
#
#                 if self.despine:
#                     seaborn.despine(fig=fig, top=True, right=True)
#
#                 if self.savefig:
#                     x_dir = os.path.join(self.results_directory, x_var)
#                     self.create_directory(x_dir)
#                     fle = os.path.join(x_dir, '{}.{}'.format(y_var, self.ext))
#                     plt.savefig(fle, dpi=self.dpi, bbox_inches='tight')
#
#         if self.show:
#             plt.show()
#
#
# class LinearRegression(_Viz, PlotKwargs):
#     """Perform multiple linear regression using
#     :py:module:`sklearn.linear_model`.
#
#     ========    =================================================
#     kwarg       Description
#     ========    =================================================
#     lin_model   `func`. default=LassoCV. Any linear model supported
#                 by :py:module:`sklearn.linear_model`. see `here`
#
#                 .. _here: http://scikit-learn.org/stable/modules/linear_model.html
#
#     n_alphas    `int` number of alphas
#     max_iter    `int`. Number of iterations.
#     **kwargs    see :ref:`kwargs` for more options
#     ========    =================================================
#
#     Args:
#
#     Returns:
#
#     """
#
#     def __init__(self, cls, **kwargs):
#         """
#
#         :param cls:
#             Instance of :py:class:`tasks.MultiParameterEstimation`
#             Same as :py:class:`PlotTimeCourseEnsemble`
#
#         :param kwargs:
#         """
#         self.cls = cls
#         self.kwargs = kwargs
#         self.plot_kwargs = self.plot_kwargs()
#
#         self.default_properties = {
#             'lin_model': linear_model.LassoCV,
#             'log10': False,
#             'truncate_mode': 'percent',
#             'theta': 100,
#             'xtick_rotation': 'horizontal',
#             'ylabel': 'Frequency',
#             'scores_title': None,
#             'coef_title': None,
#             'savefig': False,
#             'results_directory': None,
#             'dpi': 400,
#             'title_fontsize': 35,
#             'show': False,
#             'n_alphas': 100,
#             'max_iter': 20000,
#             'ext': 'png',
#             'despine': True,
#             'context': 'talk',
#             'font_scale': 1.5,
#             'rc': None,
#             'copasi_file': None,
#         }
#
#         self.default_properties.update(self.plot_kwargs)
#         for i in list(kwargs.keys()):
#             assert i in list(
#                 self.default_properties.keys()), '{} is not a keyword argument for LinearRegression'.format(i)
#         self.kwargs = self.default_properties
#         self.default_properties.update(kwargs)
#         self.default_properties.update(self.plot_kwargs)
#         self.update_properties(self.default_properties)
#         self._do_checks()
#         seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)
#
#         self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
#         self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
#
#         self.scores, self.coef = self.compute_coefficients()
#         self.coef = self.coef.fillna(value=0)
#
#         self.plot_rss()
#         self.plot_scores()
#         self.plot_coef()
#
#     def _do_checks(self):
#         """:return:"""
#         if self.results_directory is None:
#             self.results_directory = os.path.join(self.cls.model.root, 'LinearRegression')
#
#         if self.scores_title is None:
#             pass
#         if self.log10:
#             self.scores_title = 'Model Fitting Test and Train Scores (Log10)'
#
#         else:
#             self.scores_title = 'Model Fitting Test and Train Scores'
#
#         if self.coef_title is None:
#             if self.log10:
#                 self.coef_title = 'Coefficients (Log10)'
#             else:
#                 self.coef_title = 'Coefficients'
#
#     def compute1coef(self, parameter):
#         """Compute coefficients for a single parameter
#         using self['lin_model'] from sklearn
#
#         Args:
#           parameter:
#
#         Returns:
#
#         """
#         y = numpy.array(self.data[parameter])
#         X = self.data.drop(parameter, axis=1)
#         X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y)
#
#         try:
#             lin_model = self.lin_model(fit_intercept=True, n_alphas=self.n_alphas,
#                                        max_iter=self.max_iter)
#         except TypeError:
#             lin_model = self.lin_model(fit_intercept=True)
#
#         lin_model.fit(X_train, y_train)
#         df = pandas.DataFrame(lin_model.coef_, index=X.columns, columns=[parameter])  # .sort_values(by='Coefficients')
#         df['abs_values'] = numpy.absolute(df[parameter])
#         df = df.sort_values(by='abs_values', ascending=False)
#         df = df.drop('abs_values', axis=1)
#         scores = [lin_model.score(X_train, y_train), lin_model.score(X_test, y_test)]
#         scores = pandas.DataFrame(scores, index=['TrainScore', 'TestScore'])
#         return scores, df
#
#     def compute_coefficients(self):
#         """ """
#         parameters = list(self.data.columns)
#         df_dct = {}
#         score_dct = {}
#         for y in parameters:
#             score_dct[y], df_dct[y] = self.compute1coef(y)
#
#         df1 = pandas.concat(score_dct, axis=1).transpose().sort_values(by='TestScore',
#                                                                        ascending=False)
#         df2 = pandas.concat(df_dct, axis=1)
#         return df1, df2
#
#     def plot_scores(self):
#         """ """
#         fig = plt.figure()
#         seaborn.heatmap(self.scores)
#         if self.despine:
#             seaborn.despine(fig=fig, top=True, right=True)
#
#         plt.title(self.scores_title, fontsize=self.title_fontsize)
#         if self.savefig:
#             self.create_directory(self.results_directory)
#             fname = os.path.join(self.results_directory, 'linregress_scores.{}'.format(self.ext))
#             plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#
#     def plot_rss(self):
#         """ """
#         fig = plt.figure()
#         seaborn.heatmap(self.coef.RSS.sort_values(by='RSS', ascending=False))
#         plt.title('Lasso Regression \n(Y=RSS) (n={})'.format(self.data.shape[0]), fontsize=self.title_fontsize)
#         if self.despine:
#             seaborn.despine(fig=fig, top=True, right=True)
#         if self.savefig:
#             self.create_directory(self.results_directory)
#             fname = os.path.join(self.results_directory, 'linregress_RSS.{}'.format(self.ext))
#             plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#
#     def plot_coef(self):
#         """:return:"""
#         self.coef.columns = self.coef.columns.droplevel(0)
#         self.coef = self.coef.drop('RSS', axis=1)
#         self.coef = self.coef.drop('RSS', axis=0)
#         fig = plt.figure()
#         seaborn.heatmap(self.coef, cbar_kws={'pad': 0.2})
#         if self.despine:
#             seaborn.despine(fig=fig, top=True, right=True)
#
#         plt.title(self.coef_title)
#         plt.xlabel('')
#         if self.savefig:
#             self.create_directory(self.results_directory)
#             fname = os.path.join(self.results_directory, 'linregress_parameters.{}'.format(self.ext))
#             plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#


# class ModelSelection(_Viz):
#     """Calculate model selection criteria AIC (corrected) and
#     BIC for a selection of models that have undergone fitting
#     using the :py:class:`tasks.MultiModelFit` class. Plot as
#     boxplots and histograms.
#
#     Args:
#
#     Returns:
#
#     """
#
#     def __init__(self, multi_model_fit, **kwargs):
#         """
#
#         :param multi_model_fit:
#             a :py:class:`tasks.MultiModelFit` object
#
#         :param filename:
#             `str` file to save model selection data to
#
#         :param pickle:
#             `str` pickle path to save data too
#         """
#         self.multi_model_fit = multi_model_fit
#         self.number_models = self.get_num_models()
#
#         self.default_properties = {
#             'savefig': False,
#             'results_directory': None,
#             'dpi': 400,
#             'log10': False,
#             'filename': None,
#             'pickle': None,
#             'despine': True,
#             'ext': 'png',
#             'title': True,
#             'context': 'poster',
#             'font_scale': 2,
#             'rc': None,
#             'color': None,
#             'palette': None,
#             'saturation': 0.75,
#             'model_labels': None,
#             'label': None,
#             'ax': None,
#             'show': False,
#             'order': None,
#             'figsize': (8, 6),
#             'violin_kwargs': {},
#         }
#
#         for i in list(kwargs.keys()):
#             assert i in list(self.default_properties.keys()), '{} is not a keyword argument for ModelSelection'.format(
#                 i)
#         self.kwargs = self.default_properties
#         self.default_properties.update(kwargs)
#         self.update_properties(self.default_properties)
#
#         self._do_checks()
#
#         ## do model selection stuff
#         self.results_folder_dct = self._get_results_directories()
#         self.model_dct = self._get_model_dct()
#
#         ## code for having default legend labels
#         self.default_model_labels = {i.name: i.name for i in list(self.model_dct.values())}
#
#         if self.model_labels is not None:
#             if type(self.model_labels) is not dict:
#                 raise errors.InputError('model labels should be a dict')
#
#             for label in self.model_labels:
#                 if label not in self.default_model_labels:
#                     raise errors.InputError('keys of the model_labels dict should be one of '
#                                             '"{}"'.format(list(self.default_model_labels.keys())))
#         elif self.model_labels is None:
#             self.model_labels = self.default_model_labels
#
#         self.data_dct = self._parse_data()
#         self.number_model_parameters = self._get_number_estimated_model_parameters()
#         self.number_observations = self._get_n()
#         self.model_selection_data = self.calculate_model_selection_criteria()
#         seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)
#
#         # self.boxplot()
#         # self.histogram()
#         self.fig = self.violin()
#         self.to_csv()
#
#     def __iter__(self):
#         for MPE in self.multi_model_fit:
#             yield MPE
#
#     def __getitem__(self, item):
#         return self.multi_model_fit[item]
#
#     def __setitem__(self, key, value):
#         self.multi_model_fit[key] = value
#
#     def __delitem__(self, key):
#         del self.multi_model_fit[key]
#
#     def keys(self):
#         """ """
#         return list(self.multi_model_fit.keys())
#
#     def values(self):
#         """ """
#         return list(self.multi_model_fit.values())
#
#     def items(self):
#         """ """
#         return list(self.multi_model_fit.items())
#
#     def _do_checks(self):
#         """:return:"""
#         if self.results_directory is None:
#             self.results_directory = self.multi_model_fit.project_dir
#
#         if self.filename is None:
#             save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
#             self.filename = os.path.join(save_dir, 'ModelSelectionCriteria.csv')
#
#     def _get_results_directories(self):
#         """Find the results directories embedded within MultimodelFit
#         and RunMutliplePEs.
#
#         Args:
#
#         Returns:
#
#         """
#         return self.multi_model_fit.results_folder_dct
#
#     def get_num_models(self):
#         """ """
#         return len(self.multi_model_fit.cps_files)
#
#     def to_excel(self, filename=None):
#         """
#
#         Args:
#           filename:  (Default value = None)
#
#         Returns:
#
#         """
#         if filename is None:
#             filename = self.filename[:-4] + '.xlsx'
#         self.model_selection_data.to_excel(filename)
#
#     def to_csv(self, filename=None):
#         """
#
#         Args:
#           filename:  (Default value = None)
#
#         Returns:
#
#         """
#         if filename is None:
#             filename = self.filename
#         LOG.info('model selection data saved to {}'.format(filename))
#         self.model_selection_data.to_csv(filename)
#
#     def to_pickle(self, filename=None):
#         """
#
#         Args:
#           filename:  (Default value = None)
#
#         Returns:
#
#         """
#         if filename is None:
#             filename = os.path.splitext(self.filename)[0] + '.pickle'
#
#         LOG.info('model selection pickle saved to {}'.format(filename))
#         self.model_selection_data.to_pickle(filename)
#
#     def _get_model_dct(self):
#         """Get a model dct. The model must be a configured model
#         (i.e. not the original and with a number after it)
#         :return:
#
#         Args:
#
#         Returns:
#
#         """
#         dct = {}
#         for MPE in self.multi_model_fit:
#             ## get the first cps file configured for eastimation in each MMF obj
#             cps_1 = sorted(glob.glob(
#                 os.path.join(
#                     os.path.dirname(MPE.results_directory),
#                     '*.cps')
#             ))[0]
#             dct[MPE.results_directory] = model.Model(cps_1)
#         return dct
#
#     def _parse_data(self):
#         """ """
#         if self.pickle is not None:
#             #     self.pickle = os.path.splitext(self.filename)[0]+'.pickle'
#             return pandas.read_pickle(self.pickle)
#         else:
#             dct = {}
#             for cps, MPE in list(self.multi_model_fit.items()):
#                 cps_0 = cps[:-4] + '.cps'
#                 dct[cps_0] = Parse(MPE.results_directory, copasi_file=cps_0, log10=self.log10)
#             return dct
#
#     def _get_number_estimated_model_parameters(self):
#         """ """
#         k_dct = {}
#         for mod in list(self.model_dct.values()):
#             k_dct[mod.copasi_file] = len(mod.fit_item_order)
#         return k_dct
#
#     def _get_n(self):
#         """get number of observed data points for AIC calculation"""
#         n = {}
#         for exp in self.multi_model_fit.exp_files:
#             data = pandas.read_csv(exp, sep='\t')
#             l = []
#             for key in list(data.keys()):
#                 if key.lower() != 'time':
#                     if key[-6:] != '_indep':
#                         l.append(int(data[key].shape[0]))
#             n[exp] = sum(l)
#         n = sum(n.values())
#         return n
#
#     def calculate1AIC(self, RSS, K, n):
#         """Calculate the corrected AIC:
#
#             AICc = -2*ln(RSS/n) + 2*K + (2*K*(K+1))/(n-K-1)
#
#             or if likelihood function used instead of RSS
#
#             AICc = -2*ln(likelihood) + 2*K + (2*K*(K+1))/(n-K-1)
#
#         Where:
#             RSS:
#                 Residual sum of squares for model fit
#             n:
#                 Number of observations collectively in all data files
#
#             K:
#                 Number of model parameters
#
#         Args:
#           RSS:
#           K:
#           n:
#
#         Returns:
#
#         """
#         return n * numpy.log((RSS / n)) + 2 * K + (2 * K * (K + 1)) / (n - K - 1)
#
#     def calculate1BIC(self, RSS, K, n):
#         """Calculate the bayesian information criteria
#             BIC = -2*ln(likelihood) + k*ln(n)
#
#                 Does this then go to:
#
#             BIC = -2*ln(RSS/n) + k*ln(n)
#
#         Args:
#           RSS:
#           K:
#           n:
#
#         Returns:
#
#         """
#         return (n * numpy.log(RSS / n)) + K * numpy.log(n)
#
#     def calculate_model_selection_criteria(self):
#         """Calculate AIC corrected and BIC
#         :return:
#             pandas.DataFrame
#
#         Args:
#
#         Returns:
#
#         """
#         df_dct = {}
#         for model_num in range(len(self.model_dct)):
#             keys = list(self.model_dct.keys())
#             cps_key = self.model_dct[keys[model_num]].copasi_file
#
#             k = self.number_model_parameters[cps_key]
#             n = self.number_observations  # constant throughout analysis
#             rss = self.data_dct[cps_key].data.RSS
#             aic_dct = {}
#             bic_dct = {}
#             for i in range(len(rss)):
#                 aic = self.calculate1AIC(rss.iloc[i], k, n)
#                 bic = self.calculate1BIC(rss.iloc[i], k, n)
#                 aic_dct[i] = aic
#                 bic_dct[i] = bic
#             aic = pandas.DataFrame.from_dict(aic_dct, orient='index')
#             rss = pandas.DataFrame(rss)
#             bic = pandas.DataFrame.from_dict(bic_dct, orient='index')
#             df = pandas.concat([rss, aic, bic], axis=1)
#             df.columns = ['RSS', 'AICc', 'BIC']
#             df.index.name = 'RSS Rank'
#             # df_dct[os.path.split(cps_key)[1][:-6]] = df
#             df_dct[self.model_dct[keys[model_num]].name] = df
#         df = pandas.concat(df_dct, axis=1)
#         return df
#
#     def violin(self):
#         """ """
#         # seaborn.set_context(context='poster')
#         data = self.model_selection_data
#
#         data = data.unstack()
#         data = data.reset_index()
#         data = data.rename(columns={'level_0': 'Model',
#                                     'level_1': 'Metric',
#                                     0: 'Score'})
#
#         new_names = []
#         for mod in data['Model']:
#             for j in self.model_labels:
#                 if mod == j:
#                     new_names.append(self.model_labels[j])
#
#         figs = []
#         data['Model'] = new_names
#         for metric in data['Metric'].unique():
#             fig = plt.figure(figsize=self.figsize)
#             seaborn.violinplot(data=data[data['Metric'] == metric],
#                                x='Model',
#                                y='Score',
#                                color=self.color,
#                                palette=self.palette,
#                                saturation=self.saturation,
#                                ax=self.ax,
#                                order=self.order,
#                                **self.violin_kwargs
#                                )
#             plt.xticks(rotation='vertical')
#             if self.title:
#                 plt.title('{} Scores'.format(metric))
#             plt.xlabel(' ')
#             if self.despine:
#                 seaborn.despine(fig=fig, top=True, right=True)
#
#             if self.savefig:
#                 save_dir = os.path.join(self.results_directory, 'ModelSelectionGraphs')
#                 if os.path.isdir(save_dir) is not True:
#                     os.mkdir(save_dir)
#                 os.chdir(save_dir)
#                 fname = os.path.join(save_dir, 'ViolinPlot_{}.{}'.format(metric, self.ext))
#                 plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#                 LOG.info('Violin plot saved to : "{}"'.format(fname))
#
#             figs.append(fig)
#         return figs
#
#     def chi2_lookup_table(self, alpha):
#         """Looks at the cdf of a chi2 distribution at incriments of
#         0.1 between 0 and 100.
#
#         Returns the x axis value at which the alpha interval has been crossed,
#         i.e. gets the cut off point for chi2 dist with DOF and alpha .
#
#         Args:
#           alpha:
#
#         Returns:
#
#         """
#         nums = numpy.arange(0, 100, 0.1)
#         table = list(zip(nums, scipy.stats.chi2.cdf(nums, self.kwargs.get('DOF'))))
#         for i in table:
#             if i[1] <= alpha:
#                 chi2_df_alpha = i[0]
#         return chi2_df_alpha
#
#     def get_chi2_alpha(self):
#         """ """
#         dct = {}
#         alphas = numpy.arange(0, 1, 0.01)
#         for i in alphas:
#             dct[round(i, 3)] = self.chi2_lookup_table(i)
#         return dct[0.05]
#
#     def compare_sim_vs_exp(self):
#         """ """
#         LOG.info('Visually comparing simulated Versus Experiemntal data.')
#
#         for cps, res in list(self.multi_model_fit.results_folder_dct.items()):
#             tasks.InsertParameters(cps, parameter_path=res, index=0)
#             PE = tasks.ParameterEstimation(cps, self.multi_model_fit.exp_files,
#                                            randomize_start_values=False,
#                                            method='CurrentSolutionStatistics',
#                                            plot=True, savefig=True,
#                                            )
#             PE.set_up()
#             PE.run()
#             PE.format_results()
#
#     def get_best_parameters(self, filename=None):
#         """
#
#         Args:
#           filename:  (Default value = None)
#
#         Returns:
#
#         """
#         df = pandas.DataFrame()
#         for cps, res in list(self.multi_model_fit.results_folder_dct.items()):
#             df[os.path.split(cps)[1]] = ParsePEData(res).data.iloc[0]
#
#         if filename == None:
#             return df
#         else:
#             df.to_excel(filename)
#             return df
#
#     def compare_model_parameters(self, parameter_list, filename=None):
#         """Compare all the parameters accross multiple models
#         in a bar chart averaging and STD for a parameter accross
#         all models.
#
#         May have a problem with different models have different
#
#         Args:
#           parameter_list:
#           filename:  (Default value = None)
#
#         Returns:
#
#         """
#         best_parameters = self.get_best_parameters()
#         data = best_parameters.loc[parameter_list].transpose()
#         f = seaborn.barplot(data=numpy.log10(data))
#         f.set_xticklabels(parameter_list, rotation=90)
#         plt.legend(loc=(1, 1))
#         plt.title('Barplot Comparing Parameter Estimation Results for specific\nParameters accross all models')
#         plt.ylabel('log10 parameter_value,Err=SEM')
#         if filename != None:
#             plt.savefig(filename, dpi=200, bbox_inches='tight')


# class PlotProfileLikelihood(_Viz):
#     """ """
#
#     def __init__(self, cls, data=None, **kwargs):
#         """
#         Plot profile likelihoods
#         :param data:
#         :param kwargs:
#         """
#         self.cls = cls
#
#         self.default_properties = {'x': None,
#                                    'y': None,  # can equal all
#                                    'index': None,
#                                    'rss_value': None,
#                                    'log10': True,
#                                    'savefig': False,
#                                    'results_directory': None,
#                                    'dpi': 400,
#                                    'plot_cl': True,
#                                    'alpha': 0.95,
#                                    'title': None,
#                                    'xlabel': None,
#                                    'ylabel': None,
#                                    'color': None,  # if RSS, colour plots by RSS
#                                    'cmap': 'jet_r',
#                                    'legend': False,
#                                    'legend_loc': None,
#                                    'show': False,
#                                    'separate': True,
#                                    'filename': None,
#                                    'despine': True,
#                                    'ext': 'png',
#                                    'show_best_rss': True,
#                                    'best_rss_marker': 'k*',  ##Any matplotlib marker
#                                    'ylim': None,
#                                    'xlim': None,
#                                    'interpolation': None,
#                                    'interpolation_resolution': 1000,  # number of steps to interpolate
#                                    'context': 'talk',
#                                    'font_scale': 1,
#                                    'rc': None,
#                                    'multiplot': False,
#                                    'same_axis': False,
#                                    'colorbar_pad': 0.2,
#                                    }
#
#         for i in list(kwargs.keys()):
#             assert i in list(
#                 self.default_properties.keys()), '{} is not a keyword argument for PlotProfileLikelihood'.format(i)
#         self.kwargs = self.default_properties
#         self.default_properties.update(kwargs)
#         self.update_properties(self.default_properties)
#         seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)
#
#         ## parse data
#         self.data = Parse(self.cls, log10=self.log10,
#                           alpha=self.alpha, rss_value=self.rss_value).data
#
#         ## do some checks
#         self._do_checks()
#
#         ## do plotting
#         if self.same_axis:
#             self.plot_same_axis()
#         else:
#             self.plot()
#         ##todo implement ability to change confidence level from Plot.
#         ##at the moment the CL is conputer by Parse. This is not optimal
#
#     def _do_checks(self):
#         """:return:"""
#         ## todo put original estimatd values on non rss graphs as well
#         if self.ylim is not None:
#             if not isinstance(self.ylim, tuple):
#                 raise errors.InputError('ylim arg should be tuple. Got "{}"'.format(type(self.ylim)))
#
#             if len(self.ylim) is not 2:
#                 raise errors.InputError('ylim arg should be tuple of length 2. '
#                                         'See "https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.ylim.html" '
#                                         'for details')
#
#         if self.xlim is not None:
#             if not isinstance(self.xlim, tuple):
#                 raise errors.InputError('xlim arg should be tuple. Got "{}"'.format(type(self.xlim)))
#
#             if len(self.xlim) is not 2:
#                 raise errors.InputError('xlim arg should be tuple of length 2. '
#                                         'See "https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.xlim.html" '
#                                         'for details')
#
#         interpolation_kinds = ['linear', 'nearest', 'zero',
#                                'slinear', 'quadratic', 'cubic']
#
#         if self.interpolation is not None:
#             if self.interpolation not in interpolation_kinds:
#                 raise errors.InputError('"{}" is not in "{}"'.format(
#                     self.interpolation, interpolation_kinds
#                 ))
#
#         if type(self.cls) == tasks.ProfileLikelihood:
#             self.results_directory = self.cls.results_directory
#         else:
#             LOG.warning('cls not of type tasks.ProfileLikelihood')
#
#         if isinstance(self.data, pandas.core.frame.DataFrame) != True:
#             raise errors.InputError('"{}" should be a dataframe not "{}".'.format(self.data, type(self(data))))
#
#         self.parameter_list = sorted(list(self.data.columns))
#
#         if self.separate == False:
#             self.legend = True
#
#         if self.index is None:
#             self.index = 0
#
#         if not isinstance(self.index, list):
#             self.index = [self.index]
#
#         if self.x == None:
#             self.x = [i for i in self.parameter_list if i is not 'RSS']
#             # raise errors.InputError('x cannot be None')
#
#         if self.y == None:
#             self.y = 'RSS'
#
#         if self.y == 'all':
#             self.y = self.parameter_list
#
#         if self.x == 'all':
#             self.x = [i for i in self.parameter_list if i != 'RSS']
#
#         if self.y == None:
#             raise errors.InputError('y cannot be None')
#
#         if isinstance(self.y, str):
#             self.y = [self.y]
#
#         if isinstance(self.y, list):
#             for y_param in self.y:
#                 if y_param not in self.parameter_list:
#                     raise errors.InputError('{} not in {}'.format(y_param, self.parameter_list))
#
#         if isinstance(self.x, str):
#             self.x = [self.x]
#
#         if isinstance(self.x, list):
#             for x_param in self.x:
#                 if x_param not in self.parameter_list:
#                     raise errors.InputError('{} not in {}'.format(x_param, self.parameter_list))
#
#         if self.filename is not None:
#             if not os.path.isabs(self.filename):
#                 self.filename = os.path.join(self.results_directory, self.filename)
#
#             self.data.to_csv(self.filename)
#             LOG.info('Profile likelihood data saved to "{}"'.format(self.filename))
#
#     def plot_same_axis(self):
#         """:return:"""
#         fig = plt.figure()
#         for x in self.x:
#             for y in self.y:
#                 colorbar_present = False
#                 for i in self.index:
#                     if y == 'RSS':
#                         plot_data = self.data.loc[x, i][y]
#                     else:
#                         plot_data = self.data.loc[x, i][[y, 'RSS']]
#                     if type(plot_data) == pandas.Series:
#                         plot_data = pandas.DataFrame(plot_data)
#
#                     plot_data = plot_data.reset_index()
#
#                     x_plot = plot_data['Parameter Of Interest Value']
#                     y_plot = plot_data[y]
#
#                     if self.color == 'RSS':
#                         c = plot_data['RSS']
#                     elif self.color is None:
#                         c = 'r'
#
#                     if self.interpolation is not None:
#                         f = interp1d(x_plot, y_plot, kind=self.interpolation)
#                         minimum = x_plot.min()
#                         maximum = x_plot.max()
#                         step = (maximum - minimum) / self.interpolation_resolution
#                         xnew = numpy.arange(start=minimum, stop=maximum, step=step)
#                         ynew = f(xnew)
#                         plt.plot(xnew, ynew, 'k')
#                         plt.scatter(x_plot, y_plot, c=c, cmap=self.cmap,
#                                     marker='o', label=y, linewidth=2)  # linestyle='o', color='red')
#                     else:
#                         plt.scatter(x_plot, y_plot, c=c, cmap=self.cmap,
#                                     marker='o', label=y, linewidth=2)
#
#                     if self.color == 'RSS':
#                         if not colorbar_present:
#                             cb = plt.colorbar(pad=self.colorbar_pad)
#                             colorbar_present = True
#
#                     if y is 'RSS':
#                         plt.plot(plot_data['Parameter Of Interest Value'],
#                                  plot_data['Confidence Level'], linewidth=3,
#                                  linestyle='--', color='green', label='CL')
#
#                     if self.show_best_rss:
#                         if y is 'RSS':
#                             best_rss = list(set(plot_data['Best RSS Value']))
#                             best_param_val = list(set(plot_data['Best Parameter Value']))
#                             plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
#                                      markersize=12)
#
#                     if self.legend:
#                         if self.legend_loc is not None:
#                             plt.legend(loc=self.legend_loc)
#                         else:
#                             plt.legend(loc='best')
#
#                     if self.despine:
#                         seaborn.despine(fig=fig, top=True, right=True)
#
#                     if self.title is None:
#                         self.title = 'Profile Likelihoods for\n{} ' \
#                                      'against {} (index={})'.format(x, y, i)
#
#                     elif self.title is 'profile':
#                         self.title = x
#
#                     if self.title is not False:
#                         plt.title(self.title)
#
#                     if self.log10:
#                         plt.ylabel(r'$log_{10}$[{}]'.format(y))
#                         plt.xlabel(r'$log_{10}$[{}]'.format(x))
#                         if self.color == 'RSS':
#                             cb.set_label('log_${10}$[RSS]')
#                     else:
#                         plt.ylabel(y)
#                         plt.xlabel(x)
#                         if self.color == 'RSS':
#                             cb.set_label('RSS')
#
#                     if self.ylim is not None:
#                         plt.ylim(self.ylim)
#
#                     if self.xlim is not None:
#                         plt.xlim(self.xlim)
#
#                     if self.savefig:
#                         d = os.path.join(self.results_directory, str(i))
#                         d = os.path.join(d, x)
#                         self.create_directory(d)
#                         fname = os.path.join(d, utils.RemoveNonAscii(y).filter + '.{}'.format(self.ext))
#
#                         plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#                         LOG.info('saved to --> {}'.format(fname))
#
#                     if self.show:
#                         plt.show()
#
#     def plot(self):
#         """:return:"""
#         for x in self.x:
#             for y in self.y:
#                 ##indicator var for colorbar
#                 colorbar_present = False
#                 if self.multiplot:
#                     fig = plt.figure()
#                 for i in self.index:
#                     if y == 'RSS':
#                         plot_data = self.data.loc[x, i][y]
#                     else:
#                         plot_data = self.data.loc[x, i][[y, 'RSS']]
#                     if type(plot_data) == pandas.Series:
#                         plot_data = pandas.DataFrame(plot_data)
#
#                     if not self.multiplot:
#                         fig = plt.figure()
#
#                     plot_data = plot_data.reset_index()
#
#                     x_plot = plot_data['Parameter Of Interest Value']
#                     y_plot = plot_data[y]
#
#                     if self.color == 'RSS':
#                         c = plot_data['RSS']
#                     elif self.color is None:
#                         c = 'r'
#
#                     if self.interpolation is not None:
#                         f = interp1d(x_plot, y_plot, kind=self.interpolation)
#                         minimum = x_plot.min()
#                         maximum = x_plot.max()
#                         step = (maximum - minimum) / self.interpolation_resolution
#                         xnew = numpy.arange(start=minimum, stop=maximum, step=step)
#                         ynew = f(xnew)
#                         plt.plot(xnew, ynew, 'k')
#                         plt.scatter(x_plot, y_plot, c=c,
#                                     marker='o', label=y, linewidth=2,
#                                     )
#                     else:
#                         plt.scatter(x_plot, y_plot, c=c, cmap=self.cmap,
#                                     label=y, marker='o')
#
#                     if self.color == 'RSS':
#                         if not colorbar_present:
#                             cb = plt.colorbar(pad=self.colorbar_pad)
#                             colorbar_present = True
#
#                     if y is 'RSS':
#                         plt.plot(plot_data['Parameter Of Interest Value'],
#                                  plot_data['Confidence Level'], linewidth=3,
#                                  linestyle='--', color='green', label='CL')
#
#                     if self.show_best_rss:
#                         if y == 'RSS':
#                             best_rss = list(set(plot_data['Best RSS Value']))
#                             best_param_val = list(set(plot_data['Best Parameter Value']))
#                             plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
#                                      markersize=12)
#
#                     if self.legend:
#                         if self.legend_loc is not None:
#                             plt.legend(loc=self.legend_loc)
#                         else:
#                             plt.legend(loc='best')
#
#                     if self.despine:
#                         seaborn.despine(fig=fig, top=True, right=True)
#
#                     if self.title is None:
#                         self.title = 'Profile Likelihoods for\n{} ' \
#                                      'against {} (index={})'.format(x, y, i)
#
#                     # elif self.title is 'profile':
#                     #     self.title = x
#
#                     # plt.title(self.title)
#
#                     if self.log10:
#                         plt.ylabel(r'log$_{10}$' + '[{}]'.format(y))
#                         plt.xlabel(r'log$_{10}$' + '[{}]'.format(x))
#                         if self.color == 'RSS':
#                             cb.set_label('log$_{10}$[RSS]')
#                     else:
#                         plt.ylabel(y)
#                         plt.xlabel(x)
#                         if self.color == 'RSS':
#                             cb.set_label('RSS')
#
#                     if self.ylim is not None:
#                         plt.ylim(self.ylim)
#
#                     if self.xlim is not None:
#                         plt.xlim(self.xlim)
#
#                     if self.savefig:
#                         d = os.path.join(self.results_directory, str(i))
#                         d = os.path.join(d, x)
#                         self.create_directory(d)
#                         fname = os.path.join(d, utils.RemoveNonAscii(y).filter + '.{}'.format(self.ext))
#
#                         plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#                         LOG.info('saved to --> {}'.format(fname))
#
#                     if self.show:
#                         plt.show()
#
#     def plot_pdf(self):
#         """:return:"""
#         raise NotImplementedError
#         # with PdfPages()
#         for x in self.x:
#             for y in self.y:
#                 if self.multiplot:
#                     fig = plt.figure()
#                 for i in self.index:
#                     plot_data = self.data.loc[x, i][y]
#                     if type(plot_data) == pandas.Series:
#                         plot_data = pandas.DataFrame(plot_data)
#
#                     if not self.multiplot:
#                         fig = plt.figure()
#
#                     plot_data = plot_data.reset_index()
#
#                     x_plot = plot_data['Parameter Of Interest Value']
#                     y_plot = plot_data[y]
#
#                     if self.interpolation is not None:
#                         f = interp1d(x_plot, y_plot, kind=self.interpolation)
#                         minimum = x_plot.min()
#                         maximum = x_plot.max()
#                         step = (maximum - minimum) / self.interpolation_resolution
#                         xnew = numpy.arange(start=minimum, stop=maximum, step=step)
#                         ynew = f(xnew)
#                         plt.plot(xnew, ynew, 'k')
#                         plt.plot(x_plot, y_plot, 'ro', label=y, linewidth=2)  # linestyle='o', color='red')
#                     else:
#                         plt.plot(x_plot, y_plot, label=y, marker='o')
#
#                     if y is 'RSS':
#                         plt.plot(plot_data['Parameter Of Interest Value'],
#                                  plot_data['Confidence Level'], linewidth=3,
#                                  linestyle='--', color='green', label='CL')
#
#                     if self.show_best_rss:
#                         best_rss = list(set(plot_data['Best RSS Value']))
#                         best_param_val = list(set(plot_data['Best Parameter Value']))
#                         plt.plot(best_param_val, best_rss, self.best_rss_marker, linewidth=5,
#                                  markersize=12)
#
#                     if self.legend:
#                         if self.legend_loc is not None:
#                             plt.legend(loc=self.legend_loc)
#                         else:
#                             plt.legend(loc='best')
#
#                     if self.despine:
#                         seaborn.despine(fig=fig, top=True, right=True)
#
#                     if self.title is None:
#                         self.title = 'Profile Likelihoods for\n{} ' \
#                                      'against {} (index={})'.format(x, y, i)
#
#                     elif self.title is 'profile':
#                         self.title = x
#
#                     else:
#                         plt.title(self.title)
#
#                     if self.log10:
#                         plt.ylabel('log10 {}'.format(y))
#                         plt.xlabel('log10 {}'.format(x))
#                     else:
#                         plt.ylabel(y)
#                         plt.xlabel(x)
#
#                     if self.ylim is not None:
#                         plt.ylim(self.ylim)
#
#                     if self.xlim is not None:
#                         plt.xlim(self.xlim)
#
#                     if self.savefig:
#                         d = os.path.join(self.results_directory, str(i))
#                         d = os.path.join(d, x)
#                         self.create_directory(d)
#                         fname = os.path.join(d, utils.RemoveNonAscii(y).filter + '.{}'.format(self.ext))
#
#                         plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#                         LOG.info('saved to --> {}'.format(fname))
#
#                     if self.show:
#                         plt.show()


# class PearsonsCorrelation(_Viz):
#     """========    =================================================
#     kwarg       Description
#     ========    =================================================
#     **kwargs    see :ref:`kwargs` for more options
#     ========    =================================================
#
#     Args:
#
#     Returns:
#
#     """
#
#     def __init__(self, cls, **kwargs):
#         """
#
#         :param cls:
#             Instance of :py:class:`tasks.MultiParameterEstimation`
#             Same as :py:class:`PlotTimeCourseEnsemble`
#
#         :param kwargs:
#         """
#         self.cls = cls
#         self.kwargs = kwargs
#         self.plot_kwargs = self.plot_kwargs()
#
#         self.default_properties = {
#             'x': 'RSS',
#             'y': None,
#             'sep': '\t',
#             'log10': False,
#             'truncate_mode': 'percent',
#             'theta': 100,
#             'xtick_rotation': 'horizontal',
#             'ylabel': 'Frequency',
#             'savefig': False,
#             'results_directory': None,
#             'dpi': 400,
#             'title_fontsize': 35,
#             'title': True,  # Either True or None/False
#             'show': False,
#             'ext': 'png',
#             'colorbar_pad': 0.1,  # padding for color bar. Dist between bar and axes
#             'context': 'talk',
#             'font_scale': 1.5,
#             'rc': None,
#             'copasi_file': None,
#             'cmap': 'BrBG_r',
#             'center': None,
#             'robust': False,
#             'annot': None,
#             'fmt': '.2g',
#             'annot_kws': None,
#             'linewidths': 0,
#             'linecolor': 'white',
#             'cbar': True,
#             'cbar_kws': None,
#             'cbar_ax': None,
#             'square': False,
#             'xticklabels': 'auto',
#             'yticklabels': 'auto',
#             'mask': None,
#             'ax': None,
#         }
#
#         self.default_properties.update(self.plot_kwargs)
#         for i in list(kwargs.keys()):
#             assert i in list(self.default_properties.keys()), '{} is not a keyword argument for PearsonsHeatMap'.format(
#                 i)
#         self.kwargs = self.default_properties
#         self.default_properties.update(kwargs)
#         self.default_properties.update(self.plot_kwargs)
#         self.update_properties(self.default_properties)
#         self._do_checks()
#         seaborn.set_context(context=self.context, font_scale=self.font_scale, rc=self.rc)
#
#         self.data = self.parse(self.cls, log10=self.log10, copasi_file=self.copasi_file)
#
#         self.data = self.truncate(self.data, mode=self.truncate_mode, theta=self.theta)
#
#         self.combinations = self.get_combinations()
#         self.pearsons, self.p_val = self.do_pearsons()
#         self.heatmap()
#
#     def _do_checks(self):
#         """:return:"""
#         if isinstance(self.cls, str):
#             if self.copasi_file is None:
#                 raise ValueError('When first argument is a string '
#                                  'pointing to parameter estimation data '
#                                  'specify an argument to copasi_file')
#         if self.results_directory is None:
#             try:
#                 self.results_directory = os.path.join(self.cls.model.root, 'PearsonsCorrelation')
#             except AttributeError as e:
#                 self.results_directory = os.path.join(
#                     os.path.dirname(self.copasi_file), 'PearsonsCorrelation'
#                 )
#
#     def get_combinations(self):
#         """ """
#         return permutations(list(self.data.keys()), 2)
#
#     def do_pearsons(self):
#         """:return:"""
#         dct = {}
#         for x, y in self.combinations:
#             dct[(x, y)] = pearsonr(self.data[x], self.data[y])
#
#         df = pandas.DataFrame(dct).transpose()  # , index=['r2', 'p-val']).transpose()
#         df.columns = ['r2', 'p-val']
#         df.index.name = ['x', 'y']
#         df = df.unstack()
#         df = df.fillna(value=numpy.nan)
#         return df['r2'], df['p-val']
#
#     def heatmap(self):
#         """ """
#         seaborn.set_context(context=self.context, font_scale=self.font_scale)
#         data = self.pearsons
#
#         data = data.drop('RSS', axis=0)
#         data = data.drop('RSS', axis=1)
#
#         plt.figure()
#         fig = seaborn.heatmap(data=data,
#                               cmap=self.cmap,
#                               vmin=-1, vmax=1,
#                               center=self.center,
#                               robust=self.robust,
#                               annot=self.annot,
#                               fmt=self.fmt,
#                               annot_kws=self.annot_kws,
#                               linewidths=self.linewidths,
#                               linecolor=self.linecolor,
#                               cbar=self.cbar,
#                               cbar_kws=self.cbar_kws,
#                               cbar_ax=self.cbar_ax,
#                               square=self.square,
#                               xticklabels=self.xticklabels,
#                               yticklabels=self.yticklabels,
#                               mask=self.mask,
#                               ax=self.ax,
#                               )
#
#         if self.log10:
#             plt.title('Pearsons Correlation (Log10)')
#
#         else:
#             plt.title('Pearsons Correlation')
#
#         if self.savefig:
#             self.create_directory(self.results_directory)
#             fname = os.path.join(self.results_directory, 'PearsonsHeatmap' + '.{}'.format(self.ext))
#
#             plt.savefig(fname, dpi=self.dpi, bbox_inches='tight')
#             LOG.info('saved to --> {}'.format(fname))
#             pearsons_data_file = os.path.join(self.results_directory, 'r2_data.csv')
#             p_val_file = os.path.join(self.results_directory, 'p_val_data.csv')
#             self.pearsons.to_csv(pearsons_data_file, sep='\t')
#             self.p_val.to_csv(p_val_file, sep='\t')
#
#         if self.show:
#             plt.show()
