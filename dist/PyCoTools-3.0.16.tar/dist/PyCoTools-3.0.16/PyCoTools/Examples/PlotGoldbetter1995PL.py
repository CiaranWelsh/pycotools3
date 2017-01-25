# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 17:29:50 2016

@author: b3053674
"""

import PyCoTools
import os

class InputError(Exception):
    pass



current_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
os.chdir(current_dir)

goldbetter_dir=os.path.join(current_dir,'Goldbetter1995')
PEresults_dir=os.path.join(goldbetter_dir,'PE_results_dir')


if os.path.isdir(current_dir)!=True:
    raise InputError
    
    
    
if os.path.isdir(goldbetter_dir)!=True:
    raise InputError
    

if os.path.isdir(PEresults_dir)!=True:
    raise InputError


copasi_file=os.path.join(goldbetter_dir,'Goldbeter1995_CircClock0.cps')

if os.path.isfile(copasi_file)!=True:
    raise InputError
    
    
PL=PyCoTools.pydentify2.Plot(copasi_file,ParameterPath=PEresults_dir,
                                          Index=0,Run='slow')

