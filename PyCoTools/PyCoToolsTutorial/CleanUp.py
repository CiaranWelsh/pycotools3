# -*- coding: utf-8 -*-
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


 $Author: Ciaran Welsh
 $Date: 12-09-2016
 Time:  14:50


This file is for use after runnnig code in the tutorials
in order to 'clean up' the extra files produced by running
the examples.

"""

import os
import glob



for i in glob.glob('*.txt'):
    os.remove(i)


for i in glob.glob('*.xlsx'):
    os.remove(i)



for i in glob.glob('*.cps'):
    if i != 'Kholodenko.cps':
        os.remove(i)

for i in glob.glob('*.pickle'):
    if i != 'Kholodenko.cps':
        os.remove(i)

for i in glob.glob('*.log'):
    if i != 'Kholodenko.cps':
        os.remove(i)


import shutil

p = os.path.join(os.getcwd(),'MultipleParameterEsimationAnalysis')
if os.path.isdir(p):
    shutil.rmtree(p)



p = os.path.join(os.getcwd(),'ProfileLikelihood')
if os.path.isdir(p):
    shutil.rmtree(p)


