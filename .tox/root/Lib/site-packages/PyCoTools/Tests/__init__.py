# -*- coding: utf-8 -*-
import PyCoTools
import unittest
import os
from lxml import etree
import glob
import sys
# sys.path.insert(0, os.path.abspath("."))

__all__=[]
for i in glob.glob('*.py'):
    mod = i[:-3]
    __all__.append(mod)

#print __all__



