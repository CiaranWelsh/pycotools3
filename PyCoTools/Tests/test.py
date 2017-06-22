import os
import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
import PyCoTools
dire='/home/b3053674/Documents/PyCoTools/PyCoTools/Tests'
f = os.path.join(dire,'test_model.cps')
data = os.path.join(dire,'TimeCourse1.txt')



RMPE = PyCoTools.pycopi.runMultiplePEs(f,data,method = 'CurrentSolutionStatistics',
                                       randomize_start_values = 'false',
                                       copy_number = 5,pe_number = 4)

RMPE.write_config_template()
RMPE.set_up()
RMPE.run()





# GMQ = PyCoTools.pycopi.GetModelQuantities(f)
# print GMQ.get_all_model_variables().keys()
# d = {'two':15, '(reaction_3).k1':10, 'B':5}
#
# I=PyCoTools.pycopi.InsertParameters(f,parameter_dict=d)
# print I.parameters.transpose()
#
# os.system('CopasiUI {}'.format(f))








