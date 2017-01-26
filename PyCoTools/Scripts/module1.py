

'''
Run time course from command line

'''

import argparse
import PyCoTools


'''
parser=argparse.ArgumentParser(description='Script to run time course using COPASI from command line')
parser.add_argument('copasi_file',help='Path to copasi file you want to run')
parser.add_argument('-l','--Log10',action='store_false',help='plot in log10 space')
parser.add_argument('-t','--TruncateMode',help='either percent or below_x')
parser.add_argument('-x',help='value to use for data truncation',type=float)

parser.add_argument('-b','--Bins',help='Number of bins for histogram',type=int)
parser.add_argument('-n','--NumPerPlot',help='Number of bars per plot',type=int)

'''

f="D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Scripts\Goldbeter1995_CircClock.cps"

PyCoTools.pycopi.TimeCourse(f,**kwargs)





















