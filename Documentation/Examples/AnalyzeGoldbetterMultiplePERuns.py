import PyCoTools
import os



current_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
os.chdir(current_dir)

goldbetter_dir=os.path.join(current_dir,'Goldbetter1995')
PEresults_dir=os.path.join(goldbetter_dir,'PE_results_dir')

cps=os.path.join(goldbetter_dir,'Goldbeter1995_CircClock.cps')


noisy=os.path.join(goldbetter_dir,'noisy_data.txt')

#'''
#Plot boxplots histograms and scatters
#'''
PE=PyCoTools.PEAnalysis.PlotBoxplot(PEresults_dir,SaveFig='true',Log10='true',ExtraTitle='Log10')
PE=PyCoTools.PEAnalysis.PlotHistogram(PEresults_dir,SaveFig='true')


PE=PyCoTools.PEAnalysis.PlotScatters(PEresults_dir,SaveFig='true')


PE=PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(PEresults_dir,SaveFig='true')
#
#
#
#
#'''
#Do the same thing on log scale
#'''
#
#PE=PyCoTools.PEAnalysis.PlotBoxplot(PEresults_dir,SaveFig='true',
#                                    Log10='true',ExtraTitle='Log10')
#                                    
#PE=PyCoTools.PEAnalysis.PlotHistogram(PEresults_dir,SaveFig='true',
#                                      Log10='true',ExtraTitle='Log10')
#                                      
#PE=PyCoTools.PEAnalysis.PlotScatters(PEresults_dir,SaveFig='true',
#                                     Log10='true',ExtraTitle='Log10')
#                                     
#PE=PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(PEresults_dir,
#                                                        SaveFig='true',
#                                                        Log10='true',
#                                                        ExtraTitle='Log10')
##
#




PyCoTools.PEAnalysis.PlotPEData(cps,noisy,PEresults_dir,Index=0)



















