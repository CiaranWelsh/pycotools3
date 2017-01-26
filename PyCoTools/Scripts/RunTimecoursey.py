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
 

'''





if __name__=='__main__':
    #------------------------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='''Submit copasi jobs to SGE  \n ''')
    parser.add_argument('copasi_file',help='A copasi for running deterministic time course on')
    parser.add_argument('report_name',help='Name of the report')
    parser.add_argument('-e',help='email when finished. Floods your email!',action='store_true')
    parser.add_argument('-n',type=int,help='Number of times to submit. If \'-n\' omitted, default set to 1')
    parser.add_argument('-c',type=int,help='Count number of PEs already completed. Takes number of expected PEs as argument')
    args = parser.parse_args()
    #-----------------------------------------------------------------------------------------------
    Submit_Copasi_Multijob(args.copasi_file,args.report_name,args.n)
        
        

        
        
        
        
        
        