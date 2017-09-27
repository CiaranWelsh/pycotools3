import site
site.addsitedir('/home/b3053674/Documents/pycotools')

from  pycotools import *



cps_file = r'/home/b3053674/Documents/pycotools/ZiModel/Zi2012.cps'
cps_file2 = r'/home/b3053674/Documents/pycotools/ZiModel/Zi2012_2.cps'


from copy import deepcopy
zi = model.Model(cps_file)

zi_copy = deepcopy(zi)


# print [i.name for i in zi.metabolites]
r = model.Reaction(zi_copy, name='smad7_prod', expression='Smads_Complex_c -> Smads_Complex_c + Smad7', rate_law='k1*Smads_Complex_c')

#zi.add_local_parameter(r.parameters[0])


zi_copy = zi_copy.add_reaction(r)
# zi.open()
# #
zi_copy.save()
print zi_copy.reactions
# zi.open()



























