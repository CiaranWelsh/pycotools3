# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 13:24:41 2017

@author: b3053674
"""

import os
import glob
if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for i in glob.glob('*.py'):
        print(i)
