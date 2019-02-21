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
"""
import pandas
import os
import logging
import re
from collections import OrderedDict, Mapping
import json
import sys
from . import model
import yaml, json
LOG = logging.getLogger(__name__)


def format_timecourse_data(report_name):
    """read time course data into pandas dataframe. Remove
    copasi generated square brackets around the variables
    and write to file again.

    Modifies the file inplace

    Args:
      report_name (str): path to a copasi time course simulation results file

    Returns:
        pandas.DataFrame

    """

    df = pandas.read_csv(report_name, sep='\t')
    headers = [re.findall('(Time)|\[(.*)\]', i)[0] for i in list(df.columns)]
    time = headers[0][0]
    headers = [i[1] for i in headers]
    headers[0] = time
    df.columns = headers
    os.remove(report_name)
    df.to_csv(report_name, sep='\t', index=False)
    return df



def load_copasi():
    """ """
    COPASI_DIR = os.path.join(os.path.dirname(__file__), 'COPASI')
    assert os.path.isdir(COPASI_DIR)

    if sys.platform == 'linux':
        LINUX_DIR = os.path.join(COPASI_DIR, 'linux')

        if not os.path.isdir(LINUX_DIR):
            raise ValueError(f"{LINUX_DIR} is not a directory")

        BIN_DIR = os.path.join(LINUX_DIR, 'bin')
        if not os.path.isdir(BIN_DIR):
            raise ValueError(f"{BIN_DIR} is not a directory")

        COPASISE = os.path.join(BIN_DIR, 'CopasiSE')

        if not os.path.isfile(COPASISE):
            raise ValueError(f"{COPASISE} is not a file")

        COPASIUI = os.path.join(BIN_DIR, 'CopasiUI')

        if not os.path.isfile(COPASIUI):
            raise ValueError(f"{COPASIUI} is not a file")

    elif sys.platform == 'win32':
        COPASI_DIR = os.path.join(COPASI_DIR, 'windows')
        COPASISE = os.path.join(COPASI_DIR, 'CopasiSE.exe')
        COPASIUI = os.path.join(COPASI_DIR, 'CopasiUI.exe')

    elif sys.platform == 'os2':
        COPASI_DIR = os.path.join(COPASI_DIR, 'mac')

    return COPASISE, COPASIUI


class ParameterEstimationConfiguration:
    """ """

    def __init__(self,
                 experiment_files=[],
                 validation_files=[],
                 fit_items=[],
                 constraint_items=[],
                 copy_number=1,
                 pe_number=1,
                 overwrite_config_file=False,
                 results_directory=None,
                 config_filename=None,
                 randomize_start_values=False,
                 create_parameter_sets=False,
                 calculate_statistics=False,
                 settings_kw={},
                 experiments_kw={},
                 validations_kw={},
                 fit_item_kw={},
                 constraint_item_kw={},
                 report_kw={}
                 ):
        self.experiment_files = experiment_files
        self.validation_files = validation_files
        self.fit_items = fit_items
        self.constraint_items = constraint_items
        self.copy_number = copy_number
        self.pe_number = pe_number
        self.overwrite_config_file = overwrite_config_file
        self.results_directory = results_directory
        self.config_filename = config_filename
        self.randomize_start_values = randomize_start_values
        self.create_parameter_sets = create_parameter_sets
        self.calculate_statistics = calculate_statistics

        self.experiments_kw = experiments_kw
        self.validations_kw = validations_kw
        self.settings_kw = settings_kw
        self.fit_item_kw = fit_item_kw
        self.constraint_item_kw = constraint_item_kw
        self.report_kw = report_kw

        self.all_kw = [self.experiments_kw, self.settings_kw,
                       self.fit_item_kw, self.constraint_item_kw,
                       self.report_kw]

        for i in self.all_kw:
            if not isinstance(i, dict):
                raise TypeError('All inputs should be '
                                'of type dict. Got "{}"'.format(
                    type(i)
                ))

        self.experiments = self._ExperimentsKW(self.experiment_files, **self.experiments_kw)
        self.validations = self._ValidationKW(self.validation_files, **self.validations_kw)
        self.fit_items = self._FitItemKW(self.fit_items, **self.fit_item_kw)
        self.constraint_items = self._ConstraintItemKW(self.constraint_items, **self.constraint_item_kw)
        self.report = self._ReportKW(**self.report_kw)

    class _KW:
        """ """
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def update_recursive(self, orig_dict, new_dict):
            """

            Args:
              orig_dict: 
              new_dict: 

            Returns:

            """
            for key, val in new_dict.items():
                if isinstance(val, Mapping):
                    tmp = self.update(orig_dict.get(key, {}), val)
                    orig_dict[key] = tmp
                elif isinstance(val, list):
                    orig_dict[key] = (orig_dict.get(key, []) + val)
                else:
                    orig_dict[key] = new_dict[key]
            return orig_dict

        def pretty_print(self, sort_keys=False):
            """

            Args:
              sort_keys:  (Default value = False)

            Returns:

            """
            return json.dumps(self.kwargs, indent=4, sort_keys=sort_keys)

        def validate_kwargs(self, dct, valid_kwargs):
            """

            Args:
              dct: 
              valid_kwargs: 

            Returns:

            """
            for k in dct:
                if k not in self.valid_kwargs:
                    raise ValueError(
                        '"{}" is not a valid key. '
                        'Valid kwargs are "{}"'.format(
                            k, valid_kwargs))

        def __str__(self):
            return self.pretty_print()

    class _ExperimentsKW(_KW):
        """ """
        valid_kwargs = ['filename', 'normalize_weights_per_experiment',
                        'weight_method', 'separator']

        def __init__(self, experiment_files, **kwargs):
            super().__init__(**kwargs)
            dct = OrderedDict()
            for i in experiment_files:
                experiment_name = os.path.split(i)[1][:-4]
                dct[experiment_name] = OrderedDict()
                dct[experiment_name]['filename'] = i
                dct[experiment_name]['normalize_weights_per_experiment'] = True
                dct[experiment_name]['weight_method'] = 'mean_squared'
                dct[experiment_name]['separator'] = '\t'

            dct = self.update_recursive(dct, kwargs)

            self.kwargs = dct

            for k, v in self.kwargs.items():
                self.validate_kwargs(v, self.valid_kwargs)
                setattr(self, k, v)

            setattr(self, 'experiment_names', list(self.kwargs.keys()))

        def __len__(self):
            return len(self.kwargs)

        # def __str__(self):
        #     return self.pretty_print()

    class _ValidationKW(_KW):
        """ """
        valid_kwargs = [
            'filename',
            'normalize_weights_per_experiment',
            'weight_method',
            'separator',
            'validation_weight',
            'validation_threshold'
        ]

        def __init__(self, validation_files, **kwargs):
            super().__init__(**kwargs)

            dct = OrderedDict()
            for i in validation_files:
                experiment_name = os.path.split(i)[1][:-4]
                dct[experiment_name] = OrderedDict()
                dct[experiment_name]['filename'] = i
                dct[experiment_name]['normalize_weights_per_experiment'] = True
                dct[experiment_name]['weight_method'] = 'mean_squared'
                dct[experiment_name]['separator'] = '\t'
                dct[experiment_name]['validation_weight'] = 1
                dct[experiment_name]['validation_threshold'] = 5

            dct = self.update_recursive(dct, kwargs)

            self.kwargs = dct

            for k, v in self.kwargs.items():
                self.validate_kwargs(v, self.valid_kwargs)
                setattr(self, k, v)

            setattr(self, 'validation_names', list(self.kwargs.keys()))

        def __len__(self):
            return len(self.kwargs)

    class _FitItemKW(_KW):
        """ """
        valid_kwargs = [
            'lower_bound',
            'upper_bound',
            'start_value',
            'lower_bound_dct',
            'upper_bound_dct',
            'affected_experiments',
            'affected_validation_experiments',
        ]

        def __init__(self, fit_items, **kwargs):
            super().__init__(**kwargs)
            dct = OrderedDict()
            for item in fit_items:
                dct[item] = OrderedDict()
                dct[item]['lower_bound'] = 1e-6
                dct[item]['upper_bound'] = 1e6
                dct[item]['start_value'] = 'model_value'
                dct[item]['lower_bound_dct'] = {}
                dct[item]['upper_bound_dct'] = {}
                dct[item]['affected_experiments'] = {}
                dct[item]['affected_validation_experiments'] = {}

            dct = self.update_recursive(dct, kwargs)

            self.kwargs = dct

            for k, v in self.kwargs.items():
                self.validate_kwargs(v, self.valid_kwargs)
                setattr(self, k, v)

            setattr(self, 'fit_items', list(self.kwargs.keys()))

    class _ConstraintItemKW(_KW):
        """ """
        valid_kwargs = [
            'lower_bound',
            'upper_bound',
            'start_value',
            'lower_bound_dct',
            'upper_bound_dct',
            'affected_experiments',
            'affected_validation_experiments',
        ]

        def __init__(self, constraint_items, **kwargs):
            super().__init__(**kwargs)

            dct = OrderedDict()
            for constr in constraint_items:
                dct[constr] = OrderedDict()
                dct[constr]['lower_bound'] = 1e-6
                dct[constr]['upper_bound'] = 1e6
                dct[constr]['start_value'] = 'model_value'
                dct[constr]['lower_bound_dct'] = {}
                dct[constr]['upper_bound_dct'] = {}
                dct[constr]['affected_experiments'] = {}
                dct[constr]['affected_validation_experiments'] = {}

            dct = self.update_recursive(dct, kwargs)

            self.kwargs = dct

            for k, v in self.kwargs.items():
                self.validate_kwargs(v, self.valid_kwargs)
                setattr(self, k, v)

            setattr(self, 'constraint_items', list(self.kwargs.keys()))

    class _ReportKW(_KW):
        """ """
        valid_kwargs = [
            'report_name',
            'append',
            'confirm_overwrite',
        ]

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            dct = OrderedDict()
            dct['report_name'] = ''
            dct['append'] = False
            dct['confirm_overwrite'] = False

            dct = self.update_recursive(dct, kwargs)

            self.kwargs = dct

            self.validate_kwargs(self.kwargs, self.valid_kwargs)
            for i in self.kwargs:
                setattr(self, i, self.kwargs[i])

        def __str__(self):
            return self.pretty_print()


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    # yaml_tag = '!DotDict'
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, kwargs, recursive=False):
        super().__init__(kwargs)

        if recursive:
            for k in self:
                if isinstance(self[k], dict):
                    self[k] = DotDict(self[k], recursive=recursive)

    def __getattr__(self, item):
        ans = self.get(item)
        if ans is None:
            raise ValueError(f'"{item}" is not a valid attribute of this DotDict "{self}"')

        return ans



    @staticmethod
    def pretty_print(dct, sort_keys=False):
        """Use json to pretty print a nested dictionary

        Args:
          sort_keys: return: (Default value = False)
          dct: 

        Returns:

        """
        if dct is None:
            raise ValueError('Cannot pretty print Null')

        def stringify(dct):
            """recursively convert all objects of nested dct
            to strings before printing

            Args:
              dct: return:

            Returns:

            """
            for k, v in dct.items():
                if isinstance(v, dict):
                    stringify(dct[k])
                else:
                    if isinstance(v, model.Model):
                        dct[k] = str(v)
            return dct

        return json.dumps(stringify(dct), indent=4, sort_keys=sort_keys)

    def __str__(self):
        return self.pretty_print(self)

    def __repr__(self):
        return self.__str__()



