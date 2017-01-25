import os
import argparse

parser = argparse.ArgumentParser(description='''\n\n Delete range of SGE jobs \n ''')
parser.add_argument('lower',help='lower number',type=int)
parser.add_argument('upper',help='upper number',type=int)
args = parser.parse_args()

job_IDs=range(args.lower,args.upper+1)
for i in job_IDs:
    os.system('qdel {}'.format(i))

