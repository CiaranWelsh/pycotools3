#$
import bioservices
import os
import PyCoTools
from lxml import etree
import re
import string
import time
import pandas

#d=r'/sharedlustre/users/b3053674/2016/08August/Models'


'''
This script will download all curated models from the BioModels DataBase. 
This script relys on bioservices which can be installed using 
'pip install bioservices' from the command line if you have pip available
'''


def replace_non_ascii(st):
    for j in st:
        if j  not in string.ascii_letters+string.digits+'_-[]':
            st=re.sub('\{\}'.format(j),'_',st) 
    return st
    
    
def download_models():
    bio=bioservices.BioModels()
    print 'The number of models in biomodels right now is {}'.format(len(bio))
    m=bio.getAllCuratedModelsId()
    print 'The number of curated models in biomodels is: {}'.format(len(m))
    model_dct={}
    skipped=0
    for i in m:
        os.chdir(d)
        dire=os.path.join(d,i)
        if os.path.isdir(dire)==False:
            os.mkdir(dire)   
        else:
            skipped+=1
            continue
        models_to_skip=['BIOMD0000000241','BIOMD0000000148']
        if i in models_to_skip:
            '''
            This file is broken and doesn't simulate with CopasiSE
            '''
            continue
        try:
            name=bio.getModelNameById(i)
            strings='\[\]_\{\}'
            name=re.sub(strings,'_',name)
            model_dct[name]=bio.getModelSBMLById(i)
            print 'downloading {}:\t{}'.format(i,name.encode('utf8'))
            fle=os.path.join(dire,name+'.xml')
            if os.path.isfile(fle)!=True:
                with open(fle,'w') as f:
                    f.write(model_dct[name].encode('utf8'))
            time.sleep(0.25)
        except:
            continue
    print 'You have downloaded {} out of {} models'.format(len(model_dct.keys()),len(m))
    print 'you have skipped {} models because you already have a folder for them'.format(skipped)
    df=pandas.DataFrame.from_dict(model_dct.keys())
    xlsx=os.path.join(d,'ModelsMap.xlsx')
    df.to_excel(xlsx,index=True,header=True)
    return df

if __name__=='__main__':
    d=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    if os.path.isdir(d)!=True:
        os.mkdir(d)
    os.chdir(d)
    
    download_models()
    os.chdir('..')
    
#    print write_files(models)






























