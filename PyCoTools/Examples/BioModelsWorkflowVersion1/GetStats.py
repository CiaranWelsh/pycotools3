import PyCoTools
import pickle
import os

class FileDoesNotExistError(Exception):
    pass


class FolderDoesNotExistError(Exception):
    pass

time_course_data_pickle=os.path.join(os.getcwd(),'timecourseResultPickle.pickle')

noisy_data_pickle=os.path.join(os.getcwd(),'NoisySimulatedDataPickle.pickle')
cps_dirs_pickle=os.path.join(os.getcwd(),'cps_file_pickle.pickle')



model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
os.chdir(model_dir)
PE_data_pickle=os.path.join(model_dir,'PEDataFilesPickle.pickle')
PL_pickle=os.path.join(model_dir,'PLResultPathsPickle.pickle')

    
with open(cps_dirs_pickle ) as f:
   cps= pickle.load(f)

#print cps,len(cps)

for i in cps:
    print os.path.abspath(i)

#for i in cps:
#    assert os.path.isfile(i)
    
    
    
#
#
#
#
#if os.path.isfile(time_course_data_pickle)!=True:
#    raise FileDoesNotExistError('Make sure you have run all the scripts in the correct order, as described in the read me file')
    
    

#
#if os.path.isfile(noisy_data_pickle)!=True:
#    raise FileDoesNotExistError('Make sure you have run all the scripts in the correct order, as described in the read me file')
#    
#    
#    
#    
#
#if os.path.isdir(model_dir)!=True:
#    raise FolderDoesNotExistError('Make sure you have run all the scripts in the correct order, as described in the read me file')
#    
#    
#    
#    
#
#if os.path.isfile(PE_data_pickle)!=True:
#    raise FileDoesNotExistError('Make sure you have run all the scripts in the correct order, as described in the read me file')
#    
#    
#    
#    
#
#if os.path.isfile(PL_pickle)!=True:
#    raise FileDoesNotExistError('Make sure you have run all the scripts in the correct order, as described in the read me file')
#    
    
    
#    
#with open(time_course_data_pickle) as f:
##    TC= pickle.load(f)
##    
#print TC[0].keys()
#print len(TC[0]['successful'].keys())    
#print len(TC[0]['KeyboardInterrupt'].keys())    
#print len(TC[0]['CopasiError'].keys())    
#print len(TC[0]['NometabolitesError'].keys())    
#print len(TC[0]['IncompatibleStringError'].keys())    
#print len(TC[0]['OverNSpecies'].keys())    
#



'''
convert to cps

Total number of models downloaded: 618
Number that converted to copasi files without error: 597

Reason for loss - use of non-ascii strings in file paths


TimeCourse
'''





