import os
import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir('/home/b3053674/Documents/PyCoTools/Tests')

import PyCoTools
import TestModels
import lxml.etree
import logging



<<<<<<< HEAD
RMPE = PyCoTools.pycopi.runMultiplePEs(f,data,method = 'CurrentSolutionStatistics',
                                       randomize_start_values = 'false',
                                       copy_number = 5,pe_number = 4)
=======
MODEL_STRING = TestModels.TestModels.get_model1()
>>>>>>> 429c10cf87dc359d74434f80ea107ba8d837c4c9



dire='/home/b3053674/Documents/PyCoTools/PyCoTools/Tests'
model = os.path.join(dire,'test_model.cps')
data = os.path.join(dire,'TimeCourse1.txt')

if os.path.isfile(model)!=True:
    with open(model,'w') as f:
        f.write(MODEL_STRING)



#
<<<<<<< HEAD
# I=PyCoTools.pycopi.InsertParameters(f,parameter_dict=d)
# print I.parameters.transpose()
=======
>>>>>>> 429c10cf87dc359d74434f80ea107ba8d837c4c9
#
# # RMPE = PyCoTools.pycopi.RunMultiplePEs(f,data,Method = 'CurrentSolutionStatistics',
# #                                        RandomizeStartValues = 'false',
# #                                        CopyNumber = 5,NumberOfPEs = 4)
# #
# # RMPE.write_config_template()
# # RMPE.set_up()
# # RMPE.run()
#
#
#
#
#
GMQ = PyCoTools.pycopi.GetModelQuantities(model)



d = {'two':15, '(reaction_3).k1':10, 'B':5}
logging.info('Original parameters'.format(d))



I=PyCoTools.pycopi.InsertParameters(model,ParameterDict=d)

GMQ = PyCoTools.pycopi.GetModelQuantities(model)
logging.info('Parameters after insertion: {}'.format(I.parameters.transpose))


os.system('CopasiUI {}'.format(model))

#
#
#
#
#
#
#
