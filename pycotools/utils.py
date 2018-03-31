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
"""

import tasks, errors, misc, model
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
from mixin import Mixin, mixin
from cached_property import cached_property
from multiprocessing import Process, Queue
import pylatex

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


class Latex(object):
    def __init__(self, filename):
        self.filename = filename
        
        
    def prepare_model_selection(self, directory):
        """
        
        :return: 
        """
        ## first get a list of files to compile
        files = []
        for i in ['*.pdf', '*.jpg', '*.png']:
            patterns = os.path.join(directory, i)
            for j in glob.glob(patterns):
                if j is not []:
                    files.append(j)

        print files
        # doc = pylatex.Document(self.filename)













































