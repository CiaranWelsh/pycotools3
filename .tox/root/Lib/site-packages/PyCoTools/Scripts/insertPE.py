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


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
Insert parameters into a copasi file
"""

import PyCoTools
import argparse



#f=r'D:\MPhil\Model_Building\Models\2016\11_Nov\TGFbModel\Modules\Fit5\ReceptorModule42.cps'
#d=r'D:\MPhil\Model_Building\Models\2016\11_Nov\TGFbModel\Modules\Fit5\Results'
parser=argparse.ArgumentParser(description='Insert Parameters into COPASI file')
parser.add_argument('copasi_file',help='full path to a copasi model corresponding to the parameter estimation data you want to insert')
parser.add_argument('path',help='Path to parameter estimation data file or folder of parameter estimation data files')
parser.add_argument('-i','--Index',type=int,help='Which rank of PE data to insert from path.')
args=parser.parse_args()



#===============================================================================


if args.Index==None:
    args.Index=0

IP=PyCoTools.pycopi.InsertParameters(args.copasi_file,ParameterPath=args.path,Index=args.Index)

print IP.parameters.transpose()





