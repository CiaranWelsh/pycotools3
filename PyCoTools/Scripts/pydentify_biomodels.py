# -*- coding: utf-8 -*-
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
 
Optionally download a percentage of models from BioModels using the -d flag. 
Specify the percentage of models to download via the -p flag. 
Process these models through a workflow demonstrating PyCoTools capability. 
See 'pydentify_model.py' for more details on the workflow.
'''
import PyCoTools
import os
import sys
import subprocess
import threading
import pickle
import pandas
import time
import argparse
import logging

 
  


##==============================================================================

parser=argparse.ArgumentParser()

parser.add_argument('-d', help='Stores True. Use -d to download models before pydentifying',action='store_true')
parser.add_argument('-p',help='Percent of curated models to download',type=int,default=100)
args=parser.parse_args()

##==============================================================================

if sys.platform=='win32':
    DOWNLOAD_DIRECTORY=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PydentifyingBiomodelFoldersFromPyCoTools\PydentifyingBiomodels4'
    CLUSTER=False
else:
    DOWNLOAD_DIRECTORY=r'/sharedlustre/users/b3053674/12_Dec/PydentifyingBiomodelsAgain'
    CLUSTER=True
    
log_file=os.path.join(DOWNLOAD_DIRECTORY,'log.log')
PyCoTools.Misc.setup_logger(__name__,log_file)
LOG=logging.getLogger(__name__)

class FilePaths():
    def __init__(self):
        self.wd=DOWNLOAD_DIRECTORY
        if os.path.isdir(self.wd)!=True:
            raise PyCoTools.Errors.InputError('{} doesn\'t exist'.format(self.wd))
        
        self.model_downloads_pickle=os.path.join(self.wd,'BioModelsFilesPickle.pickle')
        self.cps_files_pickle=os.path.join(self.wd,'cpsFilesPickle.pickle')

        self.models_downloads_xlsx=os.path.join(self.wd,'ModelsMap.xlsx')
        
    
def xml2cps(model_pickle,cps_pickle):
    '''
    use CopasiSE to convert the xml into copasi files
    
    model_pickle:
        pickle file produced by PyCoTools.Misc.download_models
        
    cps_pickle:
        Path to name cps pickle output
    =================
    returns:
        list of copasi files
    '''
    LOG.info('Converting XML to COPASI')
    paths= pandas.read_pickle(model_pickle)
    LOG.debug('sbml pickle file has following dimenions: {} '.format(paths.shape))

#    print pandas.read_excel(models,header=0,index_col=0)
    def worker(path,output_path):
        return subprocess.check_call('CopasiSE -i "{}" -s {}'.format(path,output_path),shell=True)
        
    start=time.time()
    jobs=[]
    cps_files=[]
    for i in paths.index:
        path= paths.iloc[i][0]
        LOG.debug('sbml file: {}'.format(path))
#        print path
        cps_path=PyCoTools.Misc.RemoveNonAscii(os.path.splitext(path)[0]).filter+'.cps'
        LOG.debug('cps file: {}'.format(cps_path.decode('utf8')))
               
        if os.path.isfile(cps_path):
            continue
        LOG.debug('Performing conversion')
        p=threading.Thread(target=worker,args=(path,cps_path))
        jobs.append(p)
        p.start()
        p.join()
        cps_files.append(cps_path) 
    df=pandas.DataFrame( cps_files)
    df.to_pickle(cps_pickle)
    LOG.debug('cps pickle file has following shape: {}'.format(df.shape))
    LOG.info( '...Finished. Full SBML to cps conversion took {}s'.format(time.time()-start))

    return df
#    
    
def pydentify_biomodels(cps_pickle):
    '''
    cps_pickle:
        Input to function. This is the pickle file containing copasi file paths
        produced by xml2cps function
        
    pydentify_model_file:
        Full path to script called pydentify_model.py distributed with 
        PyCoTools under the scripts folder. 
    '''
    
    failures_path=os.path.join(os.path.dirname(cps_pickle),'ErrorCopasiImport.pickle')
    failures=[]
    copasi_files=pandas.read_pickle(cps_pickle)
    LOG.debug('Starting the Pydentification process')
    LOG.debug('cps_pickle passed to pydentify_biomodels has the following shape: {}'.format(copasi_files.shape))
    for i in copasi_files.index:
        LOG.debug('pydentifying: {}'.format(copasi_files.iloc[i][0]))
        cps_file= copasi_files.iloc[i][0]
        if os.path.isfile(cps_file)==False:
            LOG.warning('{} does not exist'.format(cps_file))
            failures.append((cps_file,'SBML conversion Error'))

        dire,fle=os.path.split(cps_file)
        try:
            if CLUSTER:
                sh_file=os.path.join(dire,fle[:-4]+'_sh_file.sh')
                err_file=os.path.join(dire,fle[:-4]+'_errorStream.txt')
                out_file=os.path.join(dire,fle[:-4]+'outputStream.txt')
                with open(sh_file,'w') as f:
                    f.write('module load apps/python27/2.7.8\nmodule load apps/COPASI/4.16.104-Linux-64bit\npython -m PyCoTools.Scripts.pydentify_model "{}"'.format(cps_file))
                
                os.system('qsub {} '.format(sh_file,err_file,out_file))
            else:   
                subprocess.call('python -m PyCoTools.Scripts.pydentify_model "{}"'.format(cps_file),shell=True)

        except:
            LOG.warning('skipped: {}'.format(cps_file))
            failures.append((cps_file,'skipped, already exists'))
    failures=pandas.DataFrame(failures)
    failures.to_pickle(failures_path)
    return failures
            



if __name__=='__main__':
    LOG.info('Logger has been saved to {}'.format(log_file))
    F=FilePaths()
    if args.d:
        PyCoTools.Misc.download_models(F.wd,percent=args.p,SKIP_ALREADY_DOWNLOADED=False)
    
    cps_files=xml2cps(F.model_downloads_pickle,F.cps_files_pickle)
        
    print pydentify_biomodels(F.cps_files_pickle)
    
    


















        
        
