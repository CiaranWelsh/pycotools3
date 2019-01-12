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
delete sun grid engine jobs
'''
import os
import argparse

parser = argparse.ArgumentParser(description='''\n\n Delete range of SGE jobs \n ''')
parser.add_argument('lower',help='lower number',type=int)
parser.add_argument('upper',help='upper number',type=int)
args = parser.parse_args()

job_IDs=list(range(args.lower,args.upper+1))
for i in job_IDs:
    os.system('qdel {}'.format(i))

