import site
site.addsitedir(r'C:\Users\Ciaran\Documents\pycotools')
import pycotools
import os, glob




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

mod = pycotools.model.Model(cps, new=True)
mod.add('compartment', 'space')

mod.add('metabolite', 'X')
mod.add('metabolite', 'Y')
mod.add('metabolite', 'Z')

mod.set('metabolite', 'X', 10, 'name', 'concentration')
mod.set('metabolite', 'Y', 15, 'name', 'concentration')
mod.set('metabolite', 'Z', 20, 'name', 'concentration')

X = pycotools.model.Reaction(mod, 'X', '-> X; Y', 'sigma*(Y-X)')
Y = pycotools.model.Reaction(mod, 'Y', '-> Y; Z X', '-X*Z + r*X -Y')
Z = pycotools.model.Reaction(mod, 'Z', '-> Z; X Y', 'X*Y - b*Z ')

mod.add_reaction(X)

mod.save()
mod.open()













