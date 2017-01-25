import PyCoTools
import os
import subprocess
import shutil

from AddNoiseToTimeCourseData import add_noise1

'''
Replace the directory below with the absolute path to the directory of the 
Goldbetter copasi file on your own machine
'''
copasi_file=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\Goldbetter1995\Goldbeter1995_CircClock.cps'

d=os.path.dirname(copasi_file)

TC=PyCoTools.pycopi.TimeCourse(copasi_file,End=100,
                                  StepSize=10,Intervals=10,
                                  Plot='true',SaveFig='true')




#PyCoTools.pycopi.PhaseSpacePlots(copasi_file,
#                                    End=1000,StepSize=0.1,
#                                    Intervals=10000,
#                                    SaveFig='true')

'''
write noisy data to file
'''
noisy_data=os.path.join(d,'data_with_noise.txt')
#noise= add_noise1(TC.kwargs.get('ReportName'))
#noise.to_csv(noisy_data,sep='\t')
#

report=os.path.join(d,'parameter_est_data.txt')


#import pandas
#df=pandas.DataFrame.from_csv(noisy_data,sep='\t')
#print df
#for i in df:
#    print i
#    import matplotlib.pyplot as plt
#    plt.figure()
#    plt.plot(df.index,df[i])
#
PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,noisy_data,
                                           Method='HookeJeeves',
                                           IterationLimit=10,
                                           RandomizeStartValues='false',
                                           SaveFig='true',
                                           UpdateModel='false',
                                           Plot='true',
                                           ReportName=report,
                                           )
PE.write_item_template()
PE.set_up()
PE.run()
#print PE.PL.parameters
#
#
#import pandas
#
#df= pandas.DataFrame.from_csv(report,sep='\t').iloc[-1]
#print df


f=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\Goldbetter1995\Goldbeter1995_CircClock.cps'
d=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\Goldbetter1995\noisy_data.txt'
w=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\Goldbetter1995\parameter_est_data.txt'
#PyCoTools.pycopi.PlotPEData(copasi_file,noisy_data,PE.kwargs.get('ReportName'),SaveFig='true')




PyCoTools.pycopi.PlotPEData(f,d,w,SaveFig='true')






