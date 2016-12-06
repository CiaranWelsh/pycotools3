import PyCoTools
import os
import shutil
import multiprocessing
from functools import partial
import subprocess


'''
get current directory
'''
current_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
os.chdir(current_dir)

'''
Copy the Goldbetter model to another file to work with 
'''
old_dir=os.path.join(current_dir,'BIOMD0000000016')
new_dir=os.path.join(current_dir,'Goldbetter1995')
if os.path.isdir(new_dir)==False:
    shutil.copytree(old_dir,new_dir)


'''
Get handle to the copasi file in new dir
'''
copasi_file=os.path.join(new_dir,'Goldbeter1995_CircClock.cps')
data_file=os.path.join(new_dir,'data_with_noise.txt')





'''
Copy the copasi file and run n parameter 
estimations using 4 separate CopasiSE processes for
speed. 

To do this we first set up parameter estimation for each file
'''
copasi_file_list=[]
for i in range(4):
    new_copasi_file=copasi_file[:-4]+str(i)+'.cps'
    copasi_file_list.append(new_copasi_file)

    if os.path.isfile(new_copasi_file):
        os.remove(new_copasi_file)
        shutil.copy(copasi_file,new_copasi_file)
    '''
    create a results directory
    '''
    results_dir=os.path.join(os.path.dirname(new_copasi_file),'PE_results_dir')
    if os.path.isdir(results_dir)==False:
        os.mkdir(results_dir)
    
    PE=PyCoTools.pycopi.ParameterEstimation(new_copasi_file,data_file,
                                               ReportName='',
                                               RandomizeStartValues='true',
                                               Run='false',
                                               Plot='false',
                                               Scheduled='false')
    PE.write_item_template()
    PE.set_up()
    
    
'''
The we use Scan to set up a repeat item with 25 iterations
using the parameter estimation subtask. Also set Run to false
otherwise they will run back to back in the same process.
'''


n=1000
    
for i in range(len(copasi_file_list)):
    PE_data_file=os.path.join(results_dir,'PEData_{}.txt'.format(str(i)))
    kwargs={'ScanType':'repeat',
            'NumberOfSteps':1000,
            'ReportName':PE_data_file,
            'SubTask':'parameter_estimation',
            'ReportType':'parameter_estimation',
            'Run':'false'}
    PyCoTools.pycopi.Scan(copasi_file_list[i],**kwargs)
    '''
    Use the Run class to set all executable boxes to false except for 
    the scan task. Set 'Run' to 'false' will just check the box instead of 
    processing the file using CopasiSE. 
    '''
    PyCoTools.pycopi.Run(copasi_file_list[i],Run='false',Task='scan')
    
    
'''
Now we can use subprocess.Popen to run all the CopasiSE files at once. 

Warning: Increasing the number of copasi files run simultaneously will
make your computer unusable until the files are processed
'''

for i in copasi_file_list:
    subprocess.Popen('CopasiSE {}'.format(i))

    
    
ListOfExperimentFiles=[]


PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,
                                           ListOfExperimentFiles,
                                           Method='ParticleSwarm',
                                           SwarmSize=100,
                                           RandomizeStartValues='true',
                                           Plot='true')
PE.write_item_template()

PE.set_up()
PE.run()


PE_data_file=[]
#
#PL=PyCoTools.pydentify2.ProfileLikelihood(copasi_file,
#                                          Index=0,
#                                          ParameterPath=PE_data_file,
#                                          UpperBoundMultiplier=1000,
#                                          LowerBoundMultiplier=1000,
#                                          NumberOfSteps=50,
#                                          Log='true',
#                                          Run='SGE')
#
#
#P=PyCoTools.pydentify2.Plot(copasi_file,
#                            ParameterPath=PE_data_file,
#                            Index=0,
#                            SaveFig='true')
#
#



















