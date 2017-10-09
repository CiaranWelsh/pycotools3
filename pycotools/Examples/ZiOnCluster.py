import os
import site
site.addsitedir('/home/b3053674/Documents/pycotools')
from pycotools import *
from zi_model_varients import Models


WRITE_NEW_ZI = False
WRITE_TIME_COURSE = True
DO_PE = False

zi_path = r'/home/b3053674/Documents/pycotools/pycotools/Examples/zi_model2012.cps'
zi_str = Models.published_zi()

if WRITE_NEW_ZI:
    with open(zi_path, 'w') as f:
        f.write(zi_str)


m = model.Model(zi_path)


TC = tasks.TimeCourse(m, end=1000, step_size=100, intervals=10)
misc.format_timecourse_data(TC.report_name)

PE = tasks.MultiParameterEstimation(m, TC.report_name,
                                    method='genetic_algorithm',
                                    population_size=10,
                                    number_of_generations=10,
                                    copy_number=2,
                                    pe_number=2,
                                    metabolites=[],
                                    overwrite_config_file=True)

PE.write_config_file()
# PE.setup()
# PE.run()

viz.PlotTimeCourseEnsemble(PE, savefig=True)


































































