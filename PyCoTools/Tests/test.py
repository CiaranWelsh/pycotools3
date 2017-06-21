import PyCoTools
import os

dire='/home/b3053674/Documents/PyCoTools/PyCoTools/Tests'
f = os.path.join(dire,'test_model.cps')
data = os.path.join(dire,'TimeCourse1.txt')



RMPE = PyCoTools.pycopi.RunMultiplePEs(f,data,Method = 'CurrentSolutionStatistics',
                                       RandomizeStartValues = 'false',
                                       CopyNumber = 3,NumberOfPEs = 4)

RMPE.write_config_template()
RMPE.set_up()
RMPE.run()
