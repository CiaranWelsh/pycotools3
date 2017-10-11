import os
# import site
# site.addsitedir('/home/b3053674/Documents/pycotools')
from pycotools import *
import pycotools.Examples.zi_model_varients as zi
import pandas
import matplotlib.pyplot as plt
import seaborn
import numpy
import copy
import shutil
import argparse
import inspect

## setup command line interface
parser = argparse.ArgumentParser(description='Run multiple parameter estimations'
                                             ' on three extended model variants '
                                             'of the published model on TGFb '
                                             'dynamics by zi et. al., 2012')

parser.add_argument('model_directory', help='directory where model files are stored', type=str)

parser.add_argument('--fit_directory', help='directory where multi model fitting occurs', type=str)

parser.add_argument('--configure', help='configure models and data into a '
                                        ' MultiModelFit style directory structure',
                    default=False, action='store_true')

parser.add_argument('--run', help='run the parameter estimations. Use --run_mode to specify '
                                  'how to run them', default=False, action='store_true')

parser.add_argument('--plot', help='Plot the parameter estimations as time course ensemble. '
                                   'Remember that parameter estimations from --run must'
                                   'be complete before this option can be used. Therefore do not'
                                   'use the --plot and --run flags at the same time', default=False,
                    action='store_true')

parser.add_argument('--run_mode', help='multiprocess or sge(for sun grid engine scheduled cluster',
                    type=str, default='multiprocess')

parser.add_argument('--copy_number', help='number of times to copy the copasi model '
                                          'before running them all simultaneously using pythons'
                                          'multiprocessing module or sun grid engine (depending on --run_mode flag)',
                    default=2, type=int)
parser.add_argument('--pe_number', help='number of repeat parameter estimation to perform per copied model. '
                                        'i.e. total parameter estimations = copy_number * pe_number',
                    default=1, type=int)

## parse args from command line
args = parser.parse_args()


##if not directory exists create
if not os.path.isdir(args.model_directory):
    os.makedirs(args.model_directory)

##default fit directory
if args.fit_directory is None:
    args.fit_directory = os.path.join(args.model_directory, 'ExtendedZi2002Fit')

## make if not exists
if not os.path.isdir(args.fit_directory):
    os.makedirs(args.fit_directory)


if (args.configure is False) and (args.plot is False) and (args.run is False):
    raise Exception('at least one of configure, plot or run flags must be specified')

if (args.run is True) and (args.plot is True):
    raise Exception('Cannot use run and plot flags at the same time. Parameter estimations '
                    'take time.')



## define some useful functions specific for this parameter estimation problem


def move_data_into_model_directory(dire):
    """
    We have data in the examples folder of pycotools distribution.
    Copy this data into args.model_directory
    :return:
    """
    data_dire = os.path.dirname(zi.__file__)
    smad7_data_path = os.path.join(data_dire, 'smad7_pcr_data.csv')
    ski_data_path = os.path.join(data_dire, 'ski_pcr_data.csv')
    new_smad7_data_path = os.path.join(dire, 'smad7_pcr_data.csv')
    new_ski_data_path = os.path.join(dire, 'ski_pcr_data.csv')
    shutil.copy(smad7_data_path, new_smad7_data_path)
    shutil.copy(ski_data_path, new_ski_data_path)
    return new_smad7_data_path, new_ski_data_path


def get_models(directory):
    """
    Get models from Models class and save as cps
    files in a directory of users choosing.

    :param directory: where to save the model varients
    :return: dict[model_id] = FullPathToModel
    """
    ## if directory not exists create it
    if not os.path.isdir(directory):
        os.makedirs(directory)

    ## get all methods of the Models class
    all_methods = dir(zi.Models)

    ## remove magic methods
    all_model_methods = [i for i in all_methods if i[:2] != '__']
    all_model_methods = [i for i in all_methods if i != 'published_zi']

    M = zi.Models()
    dct = {}
    for model_id in all_model_methods:
        m = getattr(zi.Models, model_id)
        if type(m) == property:
            model_str = m.fget(M)
            cps_file = os.path.join(directory, '{}.cps'.format(model_id))
            dct[model_id] = cps_file

            ## if already exists remove
            if os.path.isfile(cps_file):
                os.remove(cps_file)

            ## write file
            with open(cps_file, 'w') as f:
                f.write(model_str)

            ## raise error if not exists
            if not os.path.isfile(cps_file):
                raise Exception
    return dct

def read_models_into_pycotools(files_dct):
    dct = {}
    for v in files_dct.values():
        dct[v] = model.Model(v)
    return dct

def read_data_file(fle):
    """
    read data into pandas dataframe for each
    data set
    """
    data = pandas.read_csv(fle)
    data = data.set_index(['Cell Type', 'Repeat'])
    time = [int(i) * 60 for i in data.columns]
    data.columns = time
    return data

def make_smad_protein_data(df):
    ## deep copy for reproducability
    data = copy.deepcopy(df)
    time = [i + 30 for i in data.columns]
    data.columns = time

    ## add 0 time point = 75% of time 30
    data[0] = 0.75 * data[30]
    data = data[sorted(data.columns)]
    return data * 100


seaborn.set_context(context='notebook')

def plot_experimental(data, title):
    for label, df in data.groupby(level=0):
        plt.figure()
        ax = df.transpose().plot()
        ax.legend(loc=(1, 0.5))
        plt.title('{}: {}'.format(title, label))
        plt.ylabel('Signal (AU)')
        plt.xlabel('Time(h)')

def format_copasi(data, data_directory, data_name, truncate_number):
    file_dct = {}
    ## iterate over cell types
    for label, df in data.groupby(level=0):
        ## nested dict for resutls collection

        file_dct[label] = {}
        ## reset index, transpose and rename index
        df = df.reset_index(drop='True')
        df = df.transpose()
        df.index.name = 'Time'

        ##iterate over each column
        for i in df.columns:
            ##create subdirectory for each cell type
            dir2 = os.path.join(data_directory, label)
            if not os.path.isdir(dir2):
                os.makedirs(dir2)

            ## get experimental repeat
            smad7 = pandas.DataFrame(df[i])
            smad7 = smad7.astype(float)
            smad7 = smad7.reset_index()

            ## relabel to match model variable
            smad7.columns = ['Time', data_name]

            ## ensure consistent time units
            smad7 = smad7.iloc[:truncate_number]

            ## write to file
            fle = os.path.join(dir2, '{}_{}_data.csv'.format(i, data_name))
            file_dct[label][i] = fle
            smad7.to_csv(fle, index=False, sep='\t')
    return file_dct

def set_initial_values(all_models, cell_type):
    new_models = []
    for mod in all_models.values():
        mod = mod.set('global_quantity', 'Smad7mRNAInitial',
                      float(smad7_mRNA_starting_values.loc[cell_type]), match_field='name',
                      change_field='initial_value')

        mod = mod.set('global_quantity', 'SkiInitial',
                      float(ski_starting_values.loc[cell_type]), match_field='name', change_field='initial_value')

        mod = mod.set('global_quantity', 'Smad7ProteinInitial',
                      float(smad7_protein_starting_values.loc[cell_type]), match_field='name',
                      change_field='initial_value')

        new_models.append(mod)
    return new_models


if args.configure:
    LOG.info('configuring parameter estimations')
    ## get models and save into user specified directory
    model_paths = get_models(args.model_directory)

    print model_paths

    ##get model.Model instance per model
#     models = read_models_into_pycotools(model_paths)
#
#     ##move experimental data into user specified directory
#     smad7_mRNA_data_file, ski_data_file = move_data_into_model_directory(args.model_directory)
#
#     ## read data files
#     smad7_mRNA_data = read_data_file(smad7_mRNA_data_file)
#     ski_data = read_data_file(ski_data_file)
#
#     ## manafacture some smad7 protein level data from the mRNA level
#     smad7_protein_data = make_smad_protein_data(smad7_mRNA_data)
#
#     ## Create directories for data files
#     smad7_protein_data_directory = os.path.join(args.model_directory, 'Smad7ProteinDataDirectory')
#     ski_data_directory = os.path.join(args.model_directory, 'SkiDataDirectory')
#     smad7_mRNA_directory = os.path.join(args.model_directory, 'Smad7mRNADataDirectory')
#
#     ## format and write the data files into these directories
#     smad7_protein_data_files = format_copasi(smad7_protein_data, smad7_protein_data_directory, 'Smad7Obs', truncate_number=6)
#     ski_data_files = format_copasi(ski_data, ski_data_directory, 'SkiObs', truncate_number=6)
#     smad7_mRNA_data_files = format_copasi(smad7_mRNA_data, smad7_mRNA_directory, 'Smad7mRNAObs', truncate_number=6)
#
#     ## copy data files into a 'fit project directory'
#     for i in [smad7_protein_data_files, ski_data_files, smad7_mRNA_data_files]:
#         for j in i['Neonatal']:
#             shutil.copy(i['Neonatal'][j], args.fit_directory)
#
#     ## get averages of the repeated experiment as start values
#     smad7_mRNA_starting_values = pandas.DataFrame(smad7_mRNA_data[0].groupby(level=0).agg(numpy.mean))
#     ski_starting_values = pandas.DataFrame(ski_data[0].groupby(level=0).agg(numpy.mean))
#     smad7_protein_starting_values = pandas.DataFrame(smad7_protein_data[0].groupby(level=0).agg(numpy.mean))
#
#     ##set the initial concentrations of smad7 and ski to the average of the repeat data
#     models = set_initial_values(models, 'Neonatal')
#
#     ##save the model
#     [i.save() for i in models]
#
# print 'fit directory --> ', args.fit_directory
#
# ## create instance of MultiModelFit.
# ## This is needed to setup, run and plot
# PE = tasks.MultiModelFit(
#     args.fit_directory,
#     # smad7_mRNA_data_files['Neonatal'].values() + smad7_protein_data_files['Neonatal'].values() + ski_data_files['Neonatal'].values(),
#     metabolites=['Ski'], global_quantities=['Smad7SF', 'SkiSF'],
#     overwrite_config_file=True,
#     method='genetic_algorithm', population_size=150, number_of_generations=300,
#     upper_bound=1e4, run_mode=args.run_mode, copy_number=args.copy_number, pe_number=args.pe_number,
# )
# PE.write_config_file()
# PE.setup()

if args.run:
    LOG.info('running parameter estimations')
    PE.run()

if args.plot:
    LOG.info('Plotting parameter estimations')
    for m in PE:
        TCM = viz.PlotTimeCourseEnsemble(m, y=['Smad7', 'Smad7Obs', 'Ski',
                                               'Smad7_mRNA', 'Ski_mRNA',
                                               'SkiObs', 'Smad7mRNAObs'],
                                         savefig=True, run_mode=args.run_mode)
























































































#
# if ZI_PUB:
#
#     zi_path = r'/home/b3053674/Documents/pycotools/pycotools/Examples/zi_model2012.cps'
#     zi_str = Models.published_zi()
#
#     with open(zi_path, 'w') as f:
#         f.write(zi_str)
#
#
#     m = model.Model(zi_path)
#
#
#     TC = tasks.TimeCourse(m, end=1000, step_size=100, intervals=10)
#     misc.format_timecourse_data(TC.report_name)
#
#     PE = tasks.MultiParameterEstimation(m, TC.report_name,
#                                         method='genetic_algorithm',
#                                         population_size=10,
#                                         number_of_generations=10,
#                                         copy_number=2,
#                                         pe_number=2,
#                                         metabolites=[],
#                                         overwrite_config_file=True)
#
#     PE.write_config_file()
#     # PE.setup()
#     # PE.run()
#
#     viz.PlotTimeCourseEnsemble(PE, savefig=True)
#
#
#
#
#
#
#



























































