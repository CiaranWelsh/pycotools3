from pycotools import model, viz, tasks, misc
import os
import pandas
import seaborn
# seaborn.set_style('white')
# seaborn.set_context('notebook')
#
# working_directory = r'/home/b3053674/Documents/Models/2018/01_Jan/PyCoToolsQuickStart'
# copasi_file = os.path.join(working_directory, 'quick_start_model.cps')
#
# if os.path.isfile(copasi_file):
#     os.remove(copasi_file)
#
# antimony_string = """
# model michaelis_menten()
#     compartment cell = 1.0
#     var E in cell
#     var S in cell
#     var ES in cell
#     var P in cell
#
#     kf = 0.1
#     kb = 1
#     kcat = 0.3
#     E = 75
#     S = 1000
#
#     SBindE: S + E => ES; kf*S*E
#     ESUnbind: ES => S + E; kb*ES
#     ProdForm: ES => P + E; kcat*ES
# end
# """
#
# with model.BuildAntimony(copasi_file) as loader:
#     michaelis_menten = loader.load(antimony_string)
#
# TC = tasks.TimeCourse(michaelis_menten, end=100,
#                       step_size=1, intervals=100,
#                       report_name='MM-time-course.csv')
#
#
# viz.PlotTimeCourse(TC, separate=False, show=True)



