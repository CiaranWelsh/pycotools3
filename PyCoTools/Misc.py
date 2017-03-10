import os
import string
import pandas,numpy
import re
import time
import subprocess
import threading
import pickle

class RemoveNonAscii():
    def __init__(self,non_ascii_str):
        self.non_ascii_str=non_ascii_str
        self.filter=self.remove_non_ascii()
        
        
    def remove_non_ascii(self):
        for i in self.non_ascii_str:
            if i not in string.ascii_letters+string.digits+'[]-_().\\:':
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



def download_models(directory,percent=100):
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
    ## get BioModels service 
    bio=bioservices.BioModels()
    print 'The number of models in biomodels right now is {}'.format(len(bio))
    model=bio.getAllCuratedModelsId()
    print 'The number of curated models in biomodels is: {}'.format(len(model))
    per=len(model)//100*percent
    print per
    model_dct={}
    model_files=[]
    skipped=0
    for i in model[:per]:
        os.chdir(directory)
        dire=os.path.join(directory,i)
        if os.path.isdir(dire)==False:
            os.mkdir(dire)   
        else:
            skipped+=1
            continue
        models_to_skip=['BIOMD0000000241','BIOMD0000000148'] #these cause python to crash
        if i in models_to_skip:
            '''
            These file is broken and doesn't simulate with CopasiSE
            '''
            continue
        try:
            name=bio.getModelNameById(i)
            name=RemoveNonAscii(name).filter
#            strings='\[\]_\{\}'
#            name=re.sub(strings,'_',name)
            model_dct[name]=bio.getModelSBMLById(i)
            print 'downloading {}:\t{}'.format(i,name.encode('utf8'))
            
            fle=os.path.join(dire,name+'.xml')
            if os.path.isfile(fle)!=True:
                with open(fle,'w') as f:
                    f.write(model_dct[name].encode('utf8'))
            time.sleep(0.25)
            model_files.append(fle)
            print 'saved to : {}'.format(fle)
        except:
            continue
    print 'You have downloaded {} out of {} models'.format(len(model_dct.keys()),len(model))
    print 'you have skipped {} models because you already have a folder for them'.format(skipped)
    df=pandas.DataFrame(model_files)
#    df=pandas.DataFrame.from_dict(model_dct.keys())
#    xlsx=os.path.join(directory,'ModelsMap.xlsx')
#    df.to_excel(xlsx,index=True,header=True)
    pickle_file=os.path.join(directory,'BioModelsFilesPickle.pickle')
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
























