import os
from lxml import etree 
import argparse
import shutil
import pandas
import glob
import re
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


 $Author: Ciaran Welsh
 $Date: 12-09-2016 
 Time:  14:50
 
 
This script will take an appropiately configured copasi file and submit 
a copasi parameter estimation(s) as a job in SunGridEngine (the job scheduler that Newcastle fms cluster uses)

An appropiately configured copasi file conforms to the following:
    1) You must set up a scan task with a repeat item. Even if you are just submiting one parameter estimation it must be submitted via the parameter scan task
    2) To get the resutls you need to define a report. The default parameter estimation report will work but it gives a little too much information. I instead tend to define a new report in the output specifications containing all parameters I am estimating plus the best value (from the expert mode)
    3) now use the report you've just defined in the parameter scan window. Set 'append' and 'confirm overwrite' to off (optional but this is how I like it)
    4) ensure parameter estimation is set as subtask and the 'executable' box is checked in the top right hand corner of the parameter scan task
    5) go to the parameter estimation task and configure your estimation however you like
    6) Save and close
    
    
This script works as 1) command line program or 2) as a stand-alone python module

    1) Use 'python submit_copasi_multijob -h' to see input arguments that are required
    2) At the SGE terminal, from the directory where you have placed this file
    type 'python' to call the interpreter, then:
            >>> import submit_copasi_multijob # bring classes into name space
            >>> copasi_filename='<full path to copasi file'> #define necessary variables
            >>> output_name='<name of output text files>'
            >>> n=<'number of times you want to submit'>
            >>> submit_copasi_multijob.Submit_Copasi_Multijob(copasi_filename, output_name,n) #submit


'''

class Submit_Copasi_Job(object):
    '''
    Submit a properly formatted copasi file to sun grid engine
    '''
    def __init__(self,copasi_file,report_name):
        self.copasi_file=copasi_file
        self.copasiML_str=self._read_copasiML_as_string()
        self.report_name=report_name
        self.submit_copasi_job_SGE()

    def _read_copasiML_as_string(self):
        '''
        Read a copasiML file as string 
        '''
        assert os.path.exists(self.copasi_file), "{} does not exist!".format(self.copasi_file)
        with open(self.copasi_file) as f:
            fle = f.read()
        return fle
    
    def change_scan_report_name(self):
        '''
        Takes copasi_file and a name for a copasi 'Scan' report
        (usually for use in parameter estimation) as input and outputs
        a copy of the Copasi file with the predefined scan report name changed
        to report_name
        '''
        copasiML=etree.fromstring(self.copasiML_str)            
        query = "//*[@name='Scan']" and "//*[@type='scan']"
        for i in copasiML.xpath(query): 
            for j in i.getchildren():
                for k in j.attrib.keys():
                    if k=='target':
                        j.attrib['target']=self.report_name
        os.remove(self.copasi_file) #remove original and replace with new copasiML
        with open(self.copasi_file,'w') as f:
            f.write(etree.tostring(copasiML))
                  
    def submit_copasi_job_SGE(self):
        '''
        Will run a job on the fms cluster by submitting to sun grid engine
        '''
        self.change_scan_report_name()
        if args.e:
            with open('{}.sh'.format(self.report_name),'w') as f:
                f.write('#!/bin/bash\n#$ -M c.welsh2@newcastle.ac.uk -m es -V -cwd\nmodule add apps/COPASI/4.16.104-Linux-64bit\nCopasiSE {}'.format(self.copasi_file))
        else:
            with open('{}.sh'.format(self.report_name),'w') as f:
                f.write('#!/bin/bash\n#$ -V -cwd\nmodule add apps/COPASI/4.16.104-Linux-64bit\nCopasiSE {}'.format(self.copasi_file))
        ## -N is the current job name option
        os.system('qsub {} -N {} '.format('{}.sh'.format(self.report_name),self.report_name))
        os.remove('{}.sh'.format(self.report_name))
        
#---------------------------------------------------------------------
        
        
class Submit_Copasi_Multijob(Submit_Copasi_Job):
    '''
    submit copasi file to SGE n times
    copasi_file: a copasi_file
    report_name: name ouput report name
    n: number of times to submit
    '''
    def __init__(self,copasi_file,report_name,n=None):
        self.copasi_file=copasi_file
        self.report_name=report_name
        self.n=n
        self.submit_jobs()
        
    def submit_jobs(self):
        if self.n==None:
            Submit_Copasi_Job(self.copasi_file,self.report_name)
        else:
            for i in range(self.n):
                new_file=self.copasi_file[:-4]+'_temp'+str(i)+'.cps'
                new_report_name=self.report_name[:-4]+'_{}.txt'.format(i)
                shutil.copy(self.copasi_file,new_file)
                Submit_Copasi_Job(new_file,new_report_name)
#                os.remove(new_file) #can't remove the file or SGE wont be able to read it!!!!




if __name__=='__main__':
    #------------------------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='''Submit copasi jobs to SGE  \n ''')
    parser.add_argument('copasi_file',help='A appropiately configured Copasi_file')
    parser.add_argument('report_name',help='Name of the report')
    parser.add_argument('-e',help='email when finished. Floods your email!',action='store_true')
    parser.add_argument('-n',type=int,help='Number of times to submit. If \'-n\' omitted, default set to 1')
    parser.add_argument('-c',type=int,help='Count number of PEs already completed. Takes number of expected PEs as argument')
    args = parser.parse_args()
    #-----------------------------------------------------------------------------------------------
    Submit_Copasi_Multijob(args.copasi_file,args.report_name,args.n)
        
        

        
        
        
        
        
        