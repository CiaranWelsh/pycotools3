# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 16:51:43 2016

@author: b3053674
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





