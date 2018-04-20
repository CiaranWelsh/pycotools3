#! -*- coding: utf-8 -*-
"""

 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.




 Object:
 
Setup tools for PyCoTools


 $Author: Ciaran Welsh
 $Date: 22-01-2017
 Time:  12:29

"""

#from distutils.core import setup
from setuptools import setup


#version
MAJOR = 0
MINOR = 0
MICRO = 90


##test version
#MAJOR = 0
#MINOR = 0
#MICRO = 52




__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

setup(
  name='pycotools',
  packages=['pycotools'], # this must be the same as the name above
  version=__version__,
  description='A python toolbox for COPASI',
  author='Ciaran Welsh',
  requires=['lxml', 'argparse', 'pandas', 'numpy', 'scipy',
            'matplotlib', 'scipy', 'seaborn', 'sklearn',
            'retrying'],
  package_data={'pycotools':['*.py',
                             'Licence.txt',
                             'Tests/*.py',
                             'logging_config.conf'],
                # 'docs': ['build/*'],
                # 'Tests': ['*.py']
                },
  author_email='c.welsh2@newcastle.ac.uk',
  url='https://github.com/CiaranWelsh/PyCoTools',

  keywords=['systems biology', 'modelling', 'biological',
            'networks', 'copasi', 'identifiability analysis', 'profile likelihood'],

  license='GPL4',
  install_requires=['pandas', 'numpy', 'scipy', 'matplotlib',
                    'lxml', 'seaborn', 'sklearn', 'openpyxl', 'xlrd'],
  long_description='A python package for enhancing mathematical'
                   ' modelling using COPASI. See github and docs for more details'
)











