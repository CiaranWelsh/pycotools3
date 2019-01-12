'''
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
 
Visualize parameter estimation data 
 
'''
import PyCoTools as P
import argparse
import os


parser=argparse.ArgumentParser(description='plot Parameter Estimation Data')
parser.add_argument('path',help='Path to parameter estimation data file or folder of parameter estimation data files')
parser.add_argument('-o',help='output directory',default=None)
parser.add_argument('-l','--log10',action='store_false',help='do not plot in log10 space')
parser.add_argument('-t','--truncate_model',help='either percent or below_x')
parser.add_argument('-x',help='value to use for data truncation',type=float)

parser.add_argument('-b','--bins',help='Number of bins for histogram',type=int)
parser.add_argument('-n','--NumPerplot',help='Number of bars per plot',type=int)
parser.add_argument('-g','--grid_size',help='size of hex grids',type=int,default=25)
parser.add_argument('-fs','--font_size',help='size of font',type=int,default=22)
parser.add_argument('-as','--axis_size',help='size of axes labels',type=int,default=18)
parser.add_argument('-tol','-tolerance',help='tolerance parameter',type=float,default=0.01)

args=parser.parse_args()
#===============================================================================
PD=P.PEAnalysis.ParsePEData(args.path)
print(('Number of PE runs: {}'.format(PD.data.shape[0])))

if args.truncate_model==None:
    args.truncate_model='tolerance'
    
if args.x==None:
    args.x=100
    
if args.bins==None:
    args.bins=100
    
if args.log10==True:
    args.log10='true'
elif args.log10==False:
    args.log10='false'
    
    
if args.o==None:
    if os.path.isfile(args.path):
        args.o=os.path.join(os.path.dirname(args.path),os.path.split(args.path)[1]+'FitAnalysisOutput')
    if os.path.isdir(args.path):
        args.o=os.path.join(os.path.dirname(args.path),os.path.split(args.path)[1]+'FitAnalysisOutput')
        
        
if os.path.isdir(args.o)!=True:
    os.mkdir(args.o)
os.chdir(args.o)

l=[]
for i in['OptimizationPerformance','Histograms','Scatters','Boxplots','HexMapRSS','HexMapCounts']:
    l.append(os.path.join(args.o,i))


print(args)
P.PEAnalysis.EvaluateOptimizationPerformance(args.path,
                                             savefig='true',
                                             log10=args.log10,
                                             results_directory=l[0],
                                             font_size=args.font_size,
                                             axis_size=args.axis_size,
                                             tolerance=args.tol)

P.PEAnalysis.plotHistogram(args.path,savefig='true',
                           tolerance=args.tol,
                           truncate_model=args.truncate_model,
                           x=args.x,
                           bins=args.bins,
                           log10=args.log10,
                           results_directory=l[1],
                           font_size=args.font_size,
                           axis_size=args.axis_size)

P.PEAnalysis.plotScatters(args.path,
                          savefig='true',
                          log10=args.log10,
                          truncate_model=args.truncate_model,
                          x=args.x,results_directory=l[2],
                          font_size=args.font_size,
                          axis_size=args.axis_size,
                          tolerance=args.tol)

P.PEAnalysis.plotBoxplot(args.path,
                         savefig='true',
                         truncate_model=args.truncate_model,
                         x=args.x,
                         NumPerplot=args.NumPerplot,
                         results_directory=l[3],
                         log10='true',
                         font_size=args.font_size,
                         axis_size=args.axis_size,
                         Tolernce=args.tol)

P.PEAnalysis.plotHexMap(args.path,
                        savefig='true',
                        truncate_model=args.truncate_model,
                        x=args.x,
                        mode='RSS',
                        results_directory=l[4],
                        log10='true',
                        grid_size=args.grid_size,
                        font_size=args.font_size,
                        axis_size=args.axis_size,
                        tolerance=args.tol)


P.PEAnalysis.plotHexMap(args.path,
                        savefig='true',
                        truncate_model=args.truncate_model,
                        x=args.x,
                        mode='counts',
                        results_directory=l[5],
                        log10='true',
                        grid_size=args.grid_size,
                        font_size=args.font_size,
                        axis_size=args.axis_size,
                        tolerance=args.tol)


for i in l:
    print(i)








