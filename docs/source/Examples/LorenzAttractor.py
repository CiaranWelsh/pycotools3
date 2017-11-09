import site
site.addsitedir(r'C:\Users\Ciaran\Documents\pycotools')
from pycotools import model, viz, tasks
import os

"""
The Lorenz attractor system
===========================

d[X] / dt = sigma * (Y - X)
d[Y] / dt = -X*Z + r*X -Y
d[Z] / dt = XY - b*Z 

"""

cps = r'C:\Users\Ciaran\Documents\pycotools\docs\source\Tutorials\lorenz_attractor.cps'
if os.path.isfile(cps):
    os.remove(cps)

##Use the Build context manager to build the model
with model.Build(cps) as mod:
    ## name
    mod.name = 'LorenzSystem'

    ## Add a compartment - Step can be ommited if you
    ## don't mind having your compartment called
    ## NewCompartment
    mod.add('compartment', 'space')

    ## Add metabolites to model
    mod.add('metabolite', 'X')
    mod.add('metabolite', 'Y')
    mod.add('metabolite', 'Z')

    ## Set initial concentrations of metabolites
    mod.set('metabolite', 'X', 10, 'name', 'concentration')
    mod.set('metabolite', 'Y', 10, 'name', 'concentration')
    mod.set('metabolite', 'Z', 10, 'name', 'concentration')

    ## create reaction objects
    X = model.Reaction(mod, 'X', '-> X; Y', 'sigma*(Y-X)')
    Y = model.Reaction(mod, 'Y', '-> Y; Z X', '-X*Z + r*X -Y')
    Z = model.Reaction(mod, 'Z', '-> Z; X Y', 'X*Y - b*Z ')

    ##add reaction objects to the model
    mod.add('reaction', X)
    mod.add('reaction', Y)
    mod.add('reaction', Z)


## Get handle to the model
mod = model.Model(cps)

## Change parameters
model.InsertParameters(mod, parameter_dict={
    '(X).sigma': 10,
    '(Y).r': 46.92,
    '(Z).b': 4,
})

## Run and plot time course
viz.PlotTimeCourse(
    tasks.TimeCourse(
        mod, end=100,
        step_size=1, intervals=100
    ),
    savefig=True, show=True, separate=False,
    filename='lorenz.png')
















