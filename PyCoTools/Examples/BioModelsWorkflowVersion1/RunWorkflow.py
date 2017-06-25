import os


#class WrongDirError(Exception):
#    pass

#d=os.path.join(os.getcwd(),'PydentifyingBiomodels')
#os.chdir(d)
#
#if os.path.split(os.getcwd())[1]=='PydentifyingBiomodels':
current_dir=os.getcwd()
#else:
#    raise WrongDirError('Your not in the right directory')
    
#execfile(os.path.join(current_dir,'DownloadCuratedmodelsFromBiomodels.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'ConvertmodelsToCps.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'MedianNumberOfParameter.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'runTimeCourseForEachmodel.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'AddNoiseToTimeCourseData.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'plotSpaceSpaceForEachmodel.py'))
#os.chdir(current_dir)
execfile(os.path.join(current_dir,'runParameterEstimationForEachmodel.py'))
os.chdir(current_dir)
#execfile(os.path.join(current_dir,'PrunePEDataHeaders.py'))
#

'''
These two not ready yet 
'''
#execfile('runProfileLikelihoodOnEachmodel.py')
#
#execfile('plotPLs.py')




















