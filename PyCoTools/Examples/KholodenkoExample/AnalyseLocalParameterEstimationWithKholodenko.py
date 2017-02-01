# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:23:46 2017

@author: b3053674
"""

import PyCoTools
import os
import FilePaths

K=FilePaths.KholodenkoExample()





PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(K.local_PEData_dir)






PyCoTools.PEAnalysis.PlotBoxplot(K.local_PEData_dir)



PyCoTools.PEAnalysis.PlotHistogram(K.local_PEData_dir,Log10='true',
                                   Bins=5)
















