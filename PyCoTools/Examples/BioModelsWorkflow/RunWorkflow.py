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
    
#execfile(os.path.join(current_dir,'DownloadCuratedModelsFromBioModels.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'ConvertModelsToCps.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'MedianNumberOfParameter.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'RunTimeCourseForEachModel.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'AddNoiseToTimeCourseData.py'))
#os.chdir(current_dir)
#execfile(os.path.join(current_dir,'PlotSpaceSpaceForEachModel.py'))
#os.chdir(current_dir)
execfile(os.path.join(current_dir,'RunParameterEstimationForEachModel.py'))
os.chdir(current_dir)
#execfile(os.path.join(current_dir,'PrunePEDataHeaders.py'))
#

'''
These two not ready yet 
'''
#execfile('RunProfileLikelihoodOnEachModel.py')
#
#execfile('PlotPLs.py')




















