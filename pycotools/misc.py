
'''

 This file is part of pycotools.

 pycotools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools.  If not, see <http://www.gnu.org/licenses/>.


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
Miscellaneous bunch of useful classes and functions
'''

import os
import string
import pandas,numpy
import re
import time
import subprocess
import threading
import pickle
import logging

LOG=logging.getLogger(__name__)

def convert_particles_to_molar(particles,mol_unit,compartment_volume):#,vol_unit):
    '''
    Converts particle numbers to Molarity. 
    particles=number of particles you want to convert
    mol_unit=one of, 'fmol, pmol, nmol, umol, mmol or mol'
    '''
    mol_dct={
        'fmol':1e-15,
        'pmol':1e-12,
        'nmol':1e-9,
        u'\xb5mol':1e-6,
        'mmol':1e-3,
        'mol':float(1),
        'dimensionless':float(1),
        '#':float(1)}
    mol_unit_value=mol_dct[mol_unit]
    avagadro=6.02214179e+023
    molarity=float(particles)/(avagadro*mol_unit_value*compartment_volume)
    if mol_unit=='dimensionless':
        molarity=float(particles)
    if mol_unit=='#':
        molarity=float(particles)
    return round(molarity,33)

def convert_molar_to_particles(moles,mol_unit,compartment_volume):
    '''
    Converts particle numbers to Molarity. 
    particles=number of particles you want to convert
    mol_unit=one of, 'fmol, pmol, nmol, umol, mmol or mol'
    '''
    if isinstance(compartment_volume,(float,int))!=True:
        raise Errors.InputError('compartment_volume is the volume of the compartment for species and must be either a float or a int')

    mol_dct={
        'fmol':1e-15,
        'pmol':1e-12,
        'nmol':1e-9,
        u'\xb5mol':1e-6,
        'mmol':1e-3,
        'mol':float(1),
        'dimensionless':1,
        '#':1}
    mol_unit_value=mol_dct[mol_unit]
    avagadro=6.02214179e+023
    particles=float(moles)*avagadro*mol_unit_value*compartment_volume
    if mol_unit=='dimensionless':# or '#':
        particles=float(moles)
    if mol_unit=='#':
        particles=float(moles)
    return particles        

def setup_logger_deprecated(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(funcName)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)
    
    
def run_parallel(commands):
    length = len(commands)
    x = 0
    while x < length:
        exec("threading.Thread(target = "+commands[x]+").start()")
        x = x+1
    return True

    
class RemoveNonAscii():
    def __init__(self,non_ascii_str):
        self.non_ascii_str=non_ascii_str
        self.filter=self.remove_non_ascii()
        
        
    def remove_non_ascii(self):
        for i in self.non_ascii_str:
            if i not in string.ascii_letters+string.digits+r'[]-_().\:/':
                self.non_ascii_str=self.non_ascii_str.replace(i,'_')
        return self.non_ascii_str
                



def add_noise(f, noise_factor=0.05):
    '''
    Add noise to time course data
    
    f:
        Single experiment file to add noise too
    
    noise_factor:
        limits the amount of noise to add. Must be float between 0 and 1
        . default is 0.05 for 5% 
        
    ==========
    Returns: pandas.DataFrame containing noisy data 
    
    '''
    ## check file is real file
    assert os.path.isfile(f),'{} is not a file'.format(f)
    ## read into pandas
    df=pandas.read_csv(f,sep='\t')
    ## Count number of data points to add noise too
    ## remember to account for the time varible by minus 1 from column dimension 
    number_of_data_points= df.shape[0]*(df.shape[1]-1)
    ## sample from uniform distribution 'number_of_data_points' times and assign to u vector
    u= numpy.random.uniform(1-noise_factor,1+noise_factor,number_of_data_points)
    ## reshape u vector
    u_matrix= u.reshape(df.shape[0],df.shape[1]-1)
    ## remove the time colum but save as 't' variable for later
    try:
        
        t=df['Time']
        df.drop('Time',axis=1,inplace=True)
        df_noise=pandas.DataFrame(u_matrix,columns=df.columns)
    except KeyError:
        return None
    ## Check we have the corect shape for matrix
    assert df.shape==df_noise.shape
    ## Perform dot multiplication on two matrices to get noisy matrix
    noise= df_noise.rmul(df,axis=0)
    ## change index to be time
    noise.index=t
    ## return noisy vector
    return noise



def download_models(directory,percent=100,SKIP_ALREADY_DOWNLOADED=True):
    '''
    download curated models from biomodels curated section
    
    args:
        directory:
            Name of directory to download models too
    
    ===============================================================
    Returns:
        df:
            containing models
        pickle:
            save to file and contains models
        
    '''
    if percent>100 or percent <0 :
        raise TypeError('percent should be between 0 and 100')
    try:
        import bioservices
    except ImportError:
        ## install bioservices if it doesn't already exist
        ##May need to do this with admin rights
        os.system('pip install bioservices')
        import bioservices 
    except WindowsError:
        raise ImportError( 'Need bioservices module to download biomodels database. Use pip install bioservices with admin rights')

        
    ## create directory if not exist    
    if os.path.isdir(directory)!=True:
        os.makedirs(directory)
    ## change to directory
    os.chdir(directory)
    ## get Biomodels service 
    bio=bioservices.Biomodels()
    print 'The number of models in biomodels right now is {}'.format(len(bio))
    model=bio.getAllCuratedmodelsId()
    print 'The number of curated models in biomodels is: {}'.format(len(model))
    per=len(model)//100.0*percent
    print 'You are about to download {} models'.format(per)
    model_dct={}
    model_files=[]
    skipped=0
    if percent==100:
        models=model
    else:
        models=model[:int(per)]
    for i in enumerate(models):
        os.chdir(directory)
        author=bio.getAuthorsBymodelId(i[1])
        author=RemoveNonAscii(author[0]).filter
        dire=os.path.join(directory,i[1]+author)
#        if SKIP_ALREADY_DOWNLOADED:
        if os.path.isdir(dire)==False:
            os.mkdir(dire)   
        else:
            if SKIP_ALREADY_DOWNLOADED:
                skipped+=1
                continue
        models_to_skip=['BIOMD0000000241','BIOMD0000000148'] #these cause python to crash
        if i[1] in models_to_skip:
            '''
            These file is broken and doesn't simulate with CopasiSE
            '''
            continue
        try:

            model_dct[author]=bio.getmodelSBMLById(i[1])
            print 'downloading model {} of {}: {}:\t{}'.format(i[0],per,i[1],author.encode('utf8'))
            fle=os.path.join(dire,author+'.xml')
            print fle
            if os.path.isfile(fle)!=True:
                with open(fle,'w') as f:
                    f.write(model_dct[author].encode('utf8'))
            time.sleep(0.25)
            model_files.append(fle)
            print 'saved to : {}'.format(fle)
        except UnicodeEncodeError:
            print 'model with author {} skipped as the name contains non-ascii characters'.format(author)
            continue
    print 'You have downloaded {} out of {} models'.format(len(model_dct.keys()),len(model))
    print 'you have skipped {} models because you already have a folder for them'.format(skipped)
    df=pandas.DataFrame(model_files)
    pickle_file=os.path.join(directory,'BiomodelsFilesPickle.pickle')
    df.to_pickle(pickle_file)    
    return df





    
        
def xml2cps(paths):
    '''
    use CopasiSE to convert the xml into copasi files
    
    paths:
        dictionary dict[sbml filename]=copasi filename
    '''
    
    def worker(path):
        return subprocess.check_call('CopasiSE -i "{}"'.format(path),shell=True)
        
    start=time.time()
    jobs=[]
    for i in paths:
        print i
        p=threading.Thread(target=worker,args=(paths['successful'][i],))
        jobs.append(p)
        p.start()
        p.join()
#        subprocess.check_call('CopasiSE -i "{}"'.format(paths['successful'][i]))
    return 'program took {}s'.format(time.time()-start)



def correct_copasi_timecourse_headers(report_name):
    """
    read time course data into pandas dataframe. Remove
    copasi generated square brackets around the variables
    and write to file again.
    :return: pandas.DataFrame
    """

    df = pandas.read_csv(report_name, sep='\t')
    headers = [re.findall('(Time)|\[(.*)\]', i)[0] for i in list(df.columns)]
    time = headers[0][0]
    headers = [i[1] for i in headers]
    headers[0] = time
    df.columns = headers
    os.remove(report_name)
    df.to_csv(report_name, sep='\t', index=False)
    return df




















