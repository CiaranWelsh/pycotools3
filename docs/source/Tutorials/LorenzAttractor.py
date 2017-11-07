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
mod = pycotools.model.Model(cps, new_model=True)

mod.add('compartment', 'space')
mod.open()
# mod.save()
# mod.add('metabolite', 'X')
# mod.add('metabolite', 'Y')
# mod.add('metabolite', 'Z')
#
# mod.set('metabolite', 'concentration', 'X', 10)
# mod.set('metabolite', 'concentration', 'Y', 15)
# mod.set('metabolite', 'concentration', 'Z', 20)
#
# mod.save()
# mod.open()

# X = pycotools.model.Reaction('X', '-> X', 'sigma*(Y-X)')
#Y = pycotools.model.Reaction('X', '-> X', 'sigma*(Y-X)')
#X = pycotools.model.Reaction('X', '-> X', 'sigma*(Y-X)')














