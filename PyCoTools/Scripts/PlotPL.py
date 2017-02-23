# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 13:50:49 2017

@author: b3053674
"""

import PyCoTools
import argparse

##==============================================================================

parser=argparse.ArgumentParser(description='Plot Profile likelihood data ')

parser.add_argument('Model',help='Model to run profile likelihood analysis on')

parser.add_argument('Index',nargs='+',
                    help='''-1 for parameters already in model, integer value for
                    index of best fit (0 is best) or list of integers for multiple''',
                    type=int,
                    default=None)

parser.add_argument('--ParameterPath',
                    help='Full path to parameter results file or folder of results files from the same problem',
                    type=str,
                    default=None)

parser.add_argument('--RSS',
                    help='value for RSS. Only used when index = -1',
                    type=int,
                    default=None)

parser.add_argument('--Log10',help='Sample in log10 space',default='true',choices=['true','false'])
parser.add_argument('--SaveFig',help='Sample in log10 space',default='true',choices=['true','false'])
parser.add_argument('--MultiPlot',help='Plot multiple runs on the same canvas',default='true',choices=['true','false'])
parser.add_argument('--UsePickle',help='Parse estimation data using pickled data file',default='false',choices=['true','false'])
parser.add_argument('--OverwritePickle',help='Overwrite the automatically produced pickle file',default='false',choices=['true','false'])

args=parser.parse_args()






##==============================================================================

if args.Index==-1 and args.RSS==None:
    raise PyCoTools.Errors.InputError('if Index=-1, a value to RSS must be specified')
    
    
if args.Index==-1:
    PyCoTools.pydentify2.Plot(args.Model,
                           ParameterPath=args.ParameterPath,
                           RSS=args.RSS,
                           Index=args.Index,
                           Log10=args.Log10,
                           SaveFig=args.SaveFig,
                           MultiPlot=args.MultiPlot,
                           UsePickle=args.UsePickle,
                           OverwritePickle=args.OverwritePickle)
else:
    PyCoTools.pydentify2.Plot(args.Model, 
                           ParameterPath=args.ParameterPath,
                           Index=args.Index,
                           Log10=args.Log10,
                           SaveFig=args.SaveFig,
                           MultiPlot=args.MultiPlot,
                           UsePickle=args.UsePickle,
                           OverwritePickle=args.OverwritePickle



























