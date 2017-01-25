import PyCoTools as P
import argparse
import multiprocessing

parser=argparse.ArgumentParser(description='Plot Parameter Estimation Data')
parser.add_argument('path',help='Path to parameter estimation data file or folder of parameter estimation data files')
parser.add_argument('-l','--Log10',action='store_false',help='plot in log10 space')
parser.add_argument('-t','--TruncateMode',help='either percent or below_x')
parser.add_argument('-x',help='value to use for data truncation',type=float)

parser.add_argument('-b','--Bins',help='Number of bins for histogram',type=int)
parser.add_argument('-n','--NumPerPlot',help='Number of bars per plot',type=int)
#parser.add_argument()

args=parser.parse_args()
#===============================================================================
print args
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
    

#def EOP():
P.PEAnalysis.EvaluateOptimizationPerformance(args.path,SaveFig='true',Log10=args.Log10)
#def PH():
P.PEAnalysis.PlotHistogram(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,Bins=args.Bins,Log10=args.Log10)
#def PS():
P.PEAnalysis.PlotScatters(args.path,SaveFig='true',Log10=args.Log10)
#def PB():
P.PEAnalysis.PlotBoxplot(args.path,SaveFig='true',TruncateMode=args.TruncateMode,X=args.x,NumPerPlot=args.NumPerPlot)

#if __name__=='__main__':
#    multiprocessing.freeze_support()
#    p1=multiprocessing.Process(target=EOP)
#    p2=multiprocessing.Process(target=PH)
#    p3=multiprocessing.Process(target=PS)
#    p4=multiprocessing.Process(target=PB)
#    
#    p1.start()
#    p1.join()
#
#    p2.start()
#    p2.join()
#    
#    p3.start()
#    p3.join()
#    
#    p4.start()
#    p4.join()
#t1=threading.Thread(target=EOP)
#t2=threading.Thread(target=PH)
#t3=threading.Thread(target=PS)
#t4=threading.Thread(target=PB)
#
#
#t1.start()
#t1.join()
#t2.start()
#t2.join()
#t3.start()
#t3.join()
#t4.start()
#t4.join()











