# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:14:25 2016

@author: b3053674
"""

from distutils.core import setup
import  setuptools 


#version
MAJOR = 2
MINOR = 1
MICRO = 9
#=======
__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

setuptools.setup(
  name = 'PyCoTools',
  packages = ['PyCoTools'], # this must be the same as the name above
  include_package_data=True,

  version = __version__,
  description = 'A python copasi toolbox',
  author = 'Ciaran Welsh',
  requires=['lxml','argparse','pandas','numpy','scipy','matplotlib.pyplot'],
  package_data={'PyCoTools':['*.py','Documentation/*.pdf',
                             'Documentation/*.html',
                             'Documentation/*.py',
                             'Documentation/Examples/*.py',
                             'Documentation/Examples/*.txt',
                             'Licence.txt',
                             'Tests/*.py']},#,'Examples':['*.pdf' ,'*.txt' ,'*.cps' ,'*.py', '*.jpeg' ,'*.png', '*.tiff']},
  author_email = 'c.welsh2@newcastle.ac.uk',
  url = 'https://github.com/CiaranWelsh/PyCoTools', # use the URL to the github repo
#  download_url = 'https://github.com/b3053674/pydentify/tarball/0.1',
  keywords = ['systems biology','modelling','biological','networks','copasi','identifiability analysis','profile likelihood'],
#  include_package_data=False,
  license='GPLv3',
#  platform=['windows','linux'],
  install_requires=['pandas','numpy','scipy','matplotlib',
                    'lxml'],
  long_description='''
  
  
  
  
''')