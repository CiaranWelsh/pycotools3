# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 10:40:12 2017

@author: b3053674
"""
import os
import sys
'''
Change the 'self.current_directory' string variable below to the directory containing 
your own Celliere2011Example folder. The if statement is there to enable use
of the same script on both linux and windows machines without modification
(i.e. for use with a linux based SGE cluster). If you do not have this facility 
available, just ignore it. 

 
'''

class Celliere2011Example():
    def __init__(self):
        ## path to folder containing kholodenko example
        if sys.platform=='win32':
            self.current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\Celliere2011Example'
        else:
            self.current_directory=r'//sharedlustre/users/b3053674/2017/Jan/Celliere2011Example'
        
        ## Kholodenko filename
        self.copasi_filename=r'Celliere2011.cps'
        ## full path to kholodenko model
        self.celliere2011_model=os.path.join(self.current_directory,self.copasi_filename)
        ## full path to the time course output
        self.timecourse_report=os.path.join(self.current_directory,'Celliere2011TimeCourseOutput.txt')
        ## full path to the noisy time course output
        self.noisy_timecourse_report=os.path.join(self.current_directory,'NoisyCelliere2011TimeCourseOutput.txt')
        ## Full path to parameter estimation results file
        self.PEData_file=os.path.join(self.current_directory,'PEResultsFile.txt')
        ## Full path to a folder containing all data from initial multiple global parameter estimations
        self.PEData_dir=os.path.join(self.current_directory,'PEResults')
        ## Full path to file containing secondary local parameter estimation (starting with best values from self.PEData_dir)
#        self.local_PEData_file=os.path.join(self.current_directory,'LocalPEData.txt')
        self.local_PEData_dir=os.path.join(self.current_directory,'LocalPEDataResults')





