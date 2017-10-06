import os




CLUSTER = False

if CLUSTER:
    directory = r'/sharedlustre/users/b3053674/2017/10_Oct/ModellingSmad7WithZi/Fit1Dir'
    if not os.path.isdir(directory):
        raise Exception('Your not running on the cluster')

else:
    directory = r'/home/b3053674/Documents/pycotools/pycotools/Examples/Fit1Dir'
    import site
    site.addsitedir('/home/b3053674/Documents/pycotools')
    if not os.path.isdir(directory):
        raise Exception('Your are running on the cluster')

from pycotools import *
from pycotools.Tests import test_models



# PE = tasks.ParameterEstimation(
#     m1,
#     smad7_mRNA_data_files['Neonatal'].values() + smad7_protein_data_files['Neonatal'].values() + ski_data_files['Neonatal'].values(),
#     metabolites=['Ski'], global_quantities=['Smad7SF', 'SkiSF'],
#     local_parameters=[i.global_name for i in m1.local_parameters], overwrite_config_file=True,
#     method='genetic_algorithm', population_size=100, number_of_generations=300,
#     upper_bound=1e4
# )



PE = tasks.MultiModelFit(
    directory,
    metabolites=['Ski'], global_quantities=['Smad7SF', 'SkiSF'],
    overwrite_config_file=True,
    method='genetic_algorithm', population_size=5, number_of_generations=5,
    upper_bound=1e4,
    copy_number=1, pe_number=1, run_mode='sge'
)

# print PE.default_properties
#
# print PE.config_filename
# PE.write_config_file()
# PE.setup()
# PE.run()
MS = viz.ModelSelection(PE)
# MS.to_csv()

k = MS.keys()

viz.EnsembleTimeCourse(MS[k[0]], savefig=True)





































