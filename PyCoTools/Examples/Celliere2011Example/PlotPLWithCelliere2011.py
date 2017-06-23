# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy


import FilePaths

K=FilePaths.KholodenkoExample()

PyCoTools.pydentify2.plot(K.kholodenko_model, #full path to the model
                           parameter_path=K.local_PEData_dir, #full path to the PEData
                           index=[0,1],
                           log10='true',
                           savefig='true')
#                           RSS=618.648)
                           






































