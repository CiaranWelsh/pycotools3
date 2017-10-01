import site
site.addsitedir('/home/b3053674/Documents/pycotools')
import pandas
from  pycotools import *



cps_file1 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012.cps'
cps_file2 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012_2.cps'
cps_file3 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012_3.cps'

zi = model.Model(cps_file1)


report= 'parameter_estimation_synthetic_data.txt'
TC=tasks.TimeCourse(
    zi, start=0, end=1000, intervals=1000, step_size=1, report_name=report
)

## validate that its worked
pandas.read_csv(TC.report_name,sep='\t').head()

data1 = TC.report_name

misc.correct_copasi_timecourse_headers(data1)
## Set getetic algorithm parameters to low for speed of demonstration
# PE=tasks.ParameterEstimation(zi, data1, method='genetic_algorithm',
#                              population_size=15, number_of_generations=10)
# PE.write_config_file()
#
# PE.setup()
# PE.model.open()

print zi.constants2

# zi.open()












































