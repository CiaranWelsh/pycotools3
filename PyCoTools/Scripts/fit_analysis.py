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


parser=argparse.ArgumentParser(description='Plot Parameter Estimation Data')
parser.add_argument('path',help='Path to parameter estimation data file or folder of parameter estimation data files')
parser.add_argument('-o',help='output directory',default=None)
parser.add_argument('-l','--Log10',action='store_false',help='do not plot in log10 space')
parser.add_argument('-t','--TruncateMode',help='either percent or below_x')
parser.add_argument('-x',help='value to use for data truncation',type=float)

parser.add_argument('-b','--Bins',help='Number of bins for histogram',type=int)
parser.add_argument('-n','--NumPerPlot',help='Number of bars per plot',type=int)
parser.add_argument('-g','--GridSize',help='size of hex grids',type=int,default=25)
parser.add_argument('-fs','--FontSize',help='size of font',type=int,default=22)
parser.add_argument('-as','--AxisSize',help='size of axes labels',type=int,default=18)


args=parser.parse_args()
#===============================================================================
PD=P.PEAnalysis.ParsePEData(args.path)
print 'Number of PE Runs: {}'.format(PD.data.shape[0])

if args.TruncateMode==None:
    args.TruncateMode='percent'
    
if args.x==None:
    args.x=100
    
if args.Bins==None:
    args.Bins=100
    
if args.Log10==True:
    args.Log10='true'
elif args.Log10==False:
    args.Log10='false'
    
    
if args.o==None:
    if os.path.isfile(args.path):
        args.o=os.path.join(os.path.dirname(args.path),os.path.split(args.path)[1]+'FitAnalysisOutput')
    if os.path.isdir(args.path):
        args.o=os.path.join(os.path.dirname(args.path),os.path.split(args.path)[1]+'FitAnalysisOutput')
        
        
if os.path.isdir(args.o)!=True:
    os.mkdir(args.o)
os.chdir(args.o)

l=[]
for i in['OptimizationPerformance','Histograms','Scatters','BoxPlots','HexMapRSS','HexMapCounts']:
    l.append(os.path.join(args.o,i))


print args
P.PEAnalysis.EvaluateOptimizationPerformance(args.path,SaveFig='true',Log10=args.Log10,ResultsDirectory=l[0],FontSize=args.FontSize,AxisSize=args.AxisSize)
P.PEAnalysis.PlotHistogram(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,Bins=args.Bins,Log10=args.Log10,ResultsDirectory=l[1],
                            FontSize=args.FontSize,AxisSize=args.AxisSize)
P.PEAnalysis.PlotScatters(args.path,SaveFig='true',Log10=args.Log10,TruncateMode=args.TruncateMode,X=args.x,ResultsDirectory=l[2],
                            FontSize=args.FontSize,AxisSize=args.AxisSize)
P.PEAnalysis.PlotBoxplot(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,NumPerPlot=args.NumPerPlot,ResultsDirectory=l[3],Log10='true',
                               FontSize=args.FontSize,AxisSize=args.AxisSize)
P.PEAnalysis.PlotHexMap(args.path,SaveFig='true',
                        TruncateMode=args.TruncateMode,X=args.x,Mode='RSS',
                        ResultsDirectory=l[4],Log10='true',
                        GridSize=args.GridSize,
                        FontSize=args.FontSize,AxisSize=args.AxisSize)
P.PEAnalysis.PlotHexMap(args.path,SaveFig='true',
                        TruncateMode=args.TruncateMode,X=args.x,Mode='counts',
                        ResultsDirectory=l[5],Log10='true',GridSize=args.GridSize,
                        FontSize=args.FontSize,AxisSize=args.AxisSize)


for i in l:
    print i








