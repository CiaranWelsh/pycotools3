import os, glob
import site
site.addsitedir(r'/home/ncw135/Documents/pycotools3')
site.addsitedir('D:\pycotools3')
from pycotools3 import viz, model, misc, tasks, models
from io import StringIO
import pandas


working_directory = os.path.abspath('')

copasi_file = os.path.join(working_directory, 'negative_feedback.cps')

with model.BuildAntimony(copasi_file) as loader:
    mod = loader.load(
        """
        model negative_feedback
            compartment cell = 1.0
            var A in cell
            var B in cell

            vAProd = 0.1
            kADeg = 0.2
            kBProd = 0.3
            kBDeg = 0.4
            A = 0
            B = 0

            AProd: => A; cell*vAProd
            ADeg: A =>; cell*kADeg*A*B
            BProd: => B; cell*kBProd*A
            BDeg: B => ; cell*kBDeg*B
        end
        """
    )

## open model in copasi
#mod.open()
mod


experimental_data = StringIO(
    """
Time,A,B
 0, 0.000000, 0.000000
 1, 0.099932, 0.013181
 2, 0.199023, 0.046643
 3, 0.295526, 0.093275
 4, 0.387233, 0.147810
 5, 0.471935, 0.206160
 6, 0.547789, 0.265083
 7, 0.613554, 0.322023
 8, 0.668702, 0.375056
 9, 0.713393, 0.422852
10, 0.748359, 0.464639
    """.strip()
)

df = pandas.read_csv(experimental_data, index_col=0)

fname = os.path.join(os.path.abspath(''), 'experimental_data.csv')
df.to_csv(fname)

assert os.path.isfile(fname)


config = tasks.ParameterEstimation.Config(
    models=dict(
        negative_feedback=dict(
            copasi_file=copasi_file
        )
    ),
    datasets=dict(
        experiments=dict(
            first_dataset=dict(
                filename=fname,
                separator=','
            )
        )
    ),
    items=dict(
        fit_items=dict(
            A={},
            B={},
        )
    ),
    settings=dict(
        working_directory=working_directory,
        run_mode=True
    )
)
config


# PE = tasks.ParameterEstimation(config)


# config.settings.run_mode = True
# PE = tasks.ParameterEstimation(config)
# viz.Parse(PE)['negative_feedback']
# config

# config.settings.copy_number = 4
# config.settings.pe_number = 2
# config.settings.run_mode = True

##why hasn;t the first dataset been removed???
PE = tasks.ParameterEstimation(config)

with tasks.ParameterEstimation.Context(mod, fname, context='s', parameters='g') as context:
    context.set('method', 'genetic_algorithm')
    context.set('population_size', 25)
    context.set('copy_number', 4)
    context.set('pe_number', 2)
    context.set('run_mode', True)
    context.set('separator', ',')
    config = context.get_config()

## when begining parameter estimation we need to go through and remove and existing experiments
print(config)

pe = tasks.ParameterEstimation(config)
print(pe.config)
pe.models.negative_feedback.model.open()


data = viz.Parse(pe)
print(data)







