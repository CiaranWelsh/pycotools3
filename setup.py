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

from distutils.core import setup
import  setuptools 


#version
MAJOR = 3
MINOR = 3
MICRO = 65

#=======
__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

setup(
  name = 'PyCoTools',
  packages = ['PyCoTools'], # this must be the same as the name above
  version = __version__,
  description = 'A python copasi toolbox',
  author = 'Ciaran Welsh',
  requires=['lxml','argparse','pandas','numpy','scipy','matplotlib.pyplot'],
  package_data={'PyCoTools':['*.py','Documentation/*.pdf',
                             'logging_config.conf',
                             'Documentation/*.html','Licence.txt',
                             'ReadMe.md',
                             'Examples/KholodenkoExample/*',
                             'Examples/BioModelsWorkflowVersion1/*',
                             'Scripts/*.py',
                             'Tests/*.py',
                             'Tests/*.cps',
                             'PyCoToolsTutorial/*.pickle',
                             'PyCoToolsTutorial/*.py',
                             'PyCoToolsTutorial/*.ipynb',
                             'PyCoToolsTutorial/*.html',
                             'PyCoToolsTutorial/*.cps']},
  author_email = 'c.welsh2@newcastle.ac.uk',
  url = 'https://github.com/CiaranWelsh/PyCoTools', # use the URL to the github repo
#  download_url = 'https://github.com/b3053674/pydentify/tarball/0.1',
  keywords = ['systems biology','modelling','biological','networks','copasi','identifiability analysis','profile likelihood'],
#  include_package_data=False,
  license='GPL4',
#  platform=['windows','linux'],
  install_requires=['pandas','numpy','scipy','matplotlib',
                    'lxml'],
  long_description='''Tools for using Copasi via Python and calculating profile likelihoods. See Github page for more details''')











