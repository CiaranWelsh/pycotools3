import site
site.addsitedir('/home/b3053674/Documents/pycotools')
import pandas
from  pycotools import *



cps_file1 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012.cps'
cps_file2 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012_2.cps'
cps_file3 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012_3.cps'

zi = model.Model(cps_file1)


TC1 = tasks.TimeCourse(zi, end=1000, step_size=100,
                                      intervals=10, report_name='report1.txt')

# zi.set('metabolite', 'Smad3c', 150, match_field='name', change_field='concentration')
#
# TC2 = tasks.TimeCourse(zi, end=1000, step_size=100,
#                                       intervals=10, report_name='report2.txt')



misc.correct_copasi_timecourse_headers(TC1.report_name)
# misc.correct_copasi_timecourse_headers(TC2.report_name)


PE = tasks.MultiParameterEstimation(
    zi, TC1.report_name, method='genetic_algorithm',
    population_size=350, number_of_generations=400,
    metabolites=[], local_parameters=[], lower_bound=0.1,
    upper_bound=100, copy_number=1, pe_number=3, results_directory='FitFake',

)
if os.path.isfile(PE.config_filename):
    os.remove(PE.config_filename)

PE.write_config_file()
PE.setup()
# # # # PE.model.open()
# # PE.run()
#
#
#
viz.EnsembleTimeCourse(PE, y='Smad3c',
                       savefig=True,
                       step_size=10, data_filename='data_file.csv')


# f = r'/home/b3053674/Documents/pycotools/ZiModel/data_file.csv'
# import pandas
# import seaborn
# import matplotlib.pyplot as plt
# df = pandas.read_csv(f)
# plt.figure()
# print seaborn.tsplot(data=df, unit='Index', time='Time', value='Smad3n', ci=95)
#
# plt.show()

# report= 'parameter_estimation_synthetic_data.txt'
# TC = tasks.TimeCourse(
#     zi, start=0, end=1000, intervals=10, step_size=100, report_name=report
# )
#
# ## validate that its worked
# pandas.read_csv(TC.report_name,sep='\t').head()
#
# data1 = TC.report_name
#
# misc.correct_copasi_timecourse_headers(data1)
# # Set getetic algorithm parameters to low for speed of demonstration
# PE = tasks.ParameterEstimation(zi, data1, method='genetic_algorithm',
#                              population_size=15, number_of_generations=10,
#                              metabolites=[])

# if os.path.isfile(PE.config_filename):
#     os.remove(PE.config_filename)
# PE.write_config_file()
# PE.setup()
# PE.run()

# viz.PlotParameterEstimation(PE, savefig=True)
# PE.model.open()

# print zi.constants

# zi.open()












































