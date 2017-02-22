import PyCoTools as P
import argparse
import os

parser=argparse.ArgumentParser(description='Plot Parameter Estimation Data')
parser.add_argument('path',help='Path to parameter estimation data file or folder of parameter estimation data files')
parser.add_argument('-o',help='output directory',default=None)
parser.add_argument('-l','--Log10',action='store_false',help='plot in log10 space')
parser.add_argument('-t','--TruncateMode',help='either percent or below_x')
parser.add_argument('-x',help='value to use for data truncation',type=float)

parser.add_argument('-b','--Bins',help='Number of bins for histogram',type=int)
parser.add_argument('-n','--NumPerPlot',help='Number of bars per plot',type=int)
#parser.add_argument()

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
    args.o=os.path.join(os.path.dirname(args.path),os.path.split(args.path)[1]+'Results')
if os.path.isdir(args.o)!=True:
    os.mkdir(args.o)
os.chdir(args.o)

P.PEAnalysis.EvaluateOptimizationPerformance(args.path,SaveFig='true',Log10=args.Log10)
P.PEAnalysis.PlotHistogram(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,Bins=args.Bins,Log10=args.Log10)
P.PEAnalysis.PlotScatters(args.path,SaveFig='true',Log10=args.Log10,TruncateMode=args.TruncateMode,X=args.x)
P.PEAnalysis.PlotBoxplot(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,NumPerPlot=args.NumPerPlot)
P.PEAnalysis.PlotHexMap(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,Mode='RSS')
P.PEAnalysis.PlotHexMap(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,Mode='count')











