import PyCoTools
import os
import shutil






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


'''
Get handle to the copasi file in new dir
'''
copasi_file=os.path.join(new_dir,'Goldbeter1995_CircClock0.cps')
data_files=os.path.join(new_dir,'PE_results_dir')






f=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\Goldbetter1995\Goldbeter1995_CircClock0.cps'
p=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\Goldbetter1995\PE_results_dir'


#
#PL=PyCoTools.pydentify2.ProfileLikelihood(copasi_file,ParameterPath=data_files,
#                                          Index=0,
#                                          UpperBoundMultiplier=1000,
#                                          LowerBoundMultiplier=1000,
#                                          Log='true',
#                                          Run='slow',
#                                          NumProcesses=6)




PyCoTools.pydentify2.Plot(f,ParameterPath=p,Index=0,
                          SaveFig='true',Mode='all',
                          )










