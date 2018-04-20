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
from pathlib2 import Path
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


class Latex(object):
    def __init__(self, filename, file_types='.png'):
        self.filename = filename
        self.file_types = file_types

        if self.filename.endswith('.pdf'):
            self.filename = os.path.splitext(self.filename)[0]

    def search_recursive(self, directory):
        """
        recursively add all png, pdf or jpg
        files to a list
        :param directory:
        :return:
        """

        files = OrderedDict()
        for i in sorted(os.listdir(directory)):
            fname = os.path.join(directory, i)
            if os.path.isfile(fname):
                if os.path.splitext(fname)[1] in self.file_types:
                    key = os.path.dirname(fname)
                    if key in files.keys():
                        files[key] = files[key] + [fname]
                    elif key not in files.keys():
                        files[key] = [fname]
                    else:
                        raise Exception
            elif os.path.isdir(fname):
                files.update(self.search_recursive(fname))
        return files

    def search(self, directory):
        file_types = ['*.{}'.format(i) for i in self.file_types]
        files = []
        for i in self.file_types:
            patterns = os.path.join(directory, i)
            for j in glob.glob(patterns):
                if j is not []:
                    files.append(j)
        return files
        
    def prepare_document(self, directory, subdirs=False, file_types='.png'):
        """
        compile any pdf, jpg and png files
        in directory into a latex pdf document
        :return:
        """
        if subdirs not in [True, False]:
            raise errors.InputError('subdirs argument should be either True or False')

        if isinstance(file_types, str):
            file_types = [file_types]


        if subdirs:
            files = self.search_recursive(directory)

        else:
            files = self.search()

        if files is []:
            raise errors.InputError(
                '''Cannot locate pdf, jpg or png files in "{}". Please 
                give the full path to where your model selection results are
                 plotted. 
                '''.format(directory)
            )
        doc = pylatex.Document(self.filename, documentclass='article')

        for k, v in files.items():
            assert isinstance(v, list)
            if v is not None:
                with doc.create(pylatex.Section(os.path.join(*Path(k).parts[-1:]))):
                    doc.append(k)
                    doc.append(pylatex.NoEscape(r'\\*'))
                    if len(v) == 1:
                        with doc.create(
                                pylatex.Figure(
                                    position='htbp!',
                                    width=pylatex.NoEscape(r'0.3\linewidth'))
                        ) as fig:
                            
                            fig.add_image(v[0])
                            fig.add_caption(os.path.join(*Path(v[0]).parts[-2:]))
                            # fig.add_label(v[0])
                    else:
                        with doc.create(pylatex.Figure(
                                position='htbp!',
                                width=pylatex.NoEscape(r'\linewidth'),
                                )
                        ) as fig:
                            for i in range(len(v)):
                                with doc.create(
                                        pylatex.SubFigure(
                                            width=pylatex.NoEscape(r'0.3\linewidth')
                                        )
                                ) as sub:
                                    sub.add_image(v[i])
                                    # sub.add_caption('')
                                if i % 3 == 0:
                                    doc.append(pylatex.NoEscape(r'\break'))
                                    # sub.add_label(i)
                            fig.add_caption(os.path.join(*Path(v[i]).parts[-3:-1]))
                    doc.append(pylatex.NoEscape(r'\hfill'))


        doc.generate_pdf()
        LOG.info('PDF generated at "{}"'.format(doc.default_filepath))

    def profile_likelihood(self, pl_directory, size=0.3, num_per_row=3):
        """
        compile any pdf, jpg and png files
        in directory into a latex pdf document
        :return:
        """
        if isinstance(self.file_types, str):
            self.file_types = [self.file_types]

        files = self.search_recursive(pl_directory)

        if files is []:
            raise errors.InputError(
                '''Cannot locate pdf, jpg or png files in "{}". Please 
                give the full path to where your model selection results are
                 plotted. 
                '''.format(pl_directory)
            )
        doc = pylatex.Document(self.filename, documentclass='article')

        for k, v in files.items():
            assert isinstance(v, list)
            if v is not None:
                with doc.create(pylatex.Figure(
                        position='htbp!',
                        width=pylatex.NoEscape(r'\linewidth'))) as fig:
                    # [fig.add_image(i) for i in v]
                    for i in range(len(v)):
                        with doc.create(pylatex.SubFigure(
                                width=pylatex.NoEscape(str(size) + r'\linewidth'))) as sub:
                            sub.add_image(v[i])
                            sub.add_caption(os.path.split(v[i])[1])
                        if i is not 0 and i % num_per_row is 0:
                            doc.append(pylatex.NoEscape(r'\break'))
                            # sub.add_label(i)
                            #         # fig.add_caption(os.path.join(*Path(v[i]).parts[-3:-1]))

                        doc.append(pylatex.NoEscape(r'\hfill'))
                    fig.add_caption(os.path.split(k)[1])

        doc.generate_pdf()
        LOG.info('PDF generated at "{}"'.format(doc.default_filepath))






































