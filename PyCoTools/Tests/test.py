import os
import site
site.addsitedir(r'C:\Users\Ciaran\Documents\PyCoTools')

import PyCoTools
import TestModels
import lxml.etree
import logging



f =r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\Tests\test_model.cps'

#PyCoTools.pycopi.Reports(f,report_type = 'parameter_estimation')
#
#
#

#
#os.system('CopasiUI {}'.format(f))
TC = PyCoTools.pycopi.TimeCourse(f,end=1000,step_size=100, intervals = 10)
PE=PyCoTools.pycopi.ParameterEstimation(f,TC.kwargs['report_name'],population_size =20)
PE.write_config_template()
PE.setup()
PE.run()


#GMQ = PyCoTools.pycopi.GetModelQuantities(f)

#





















