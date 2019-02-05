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
from pathlib2 import Path
from . import tasks, errors, misc, model
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
import seaborn
import logging
import glob
import re
import numpy
from .mixin import Mixin, mixin
from .cached_property import cached_property
from multiprocessing import Process, Queue
import pylatex
from collections import OrderedDict

LOG = logging.getLogger(__name__)

def format_timecourse_data(report_name):
    """
    read time course data into pandas dataframe. Remove
    copasi generated square brackets around the variables
    and write to file again.
    :return: pandas.DataFrame
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













