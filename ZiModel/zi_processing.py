import site
site.addsitedir('/home/b3053674/Documents/pycotools')

from  pycotools import *



cps_file = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012.cps'


zi = model.Model(cps_file)


# # print [i.name for i in zi.metabolites]
# r = model.Reaction(zi_copy, name='smad7_prod', expression='Smads_Complex_c -> Smads_Complex_c + Smad7', rate_law='k1*Smads_Complex_c')
#
# #zi.add_local_parameter(r.parameters[0])
#
#
# zi_copy = zi_copy.add_reaction(r)
# # zi.open()
# # #
# zi_copy.save()
# print zi_copy.reactions
# # zi.open()

# print zi.metabolites[0]

metab = model.Metabolite(zi, 'x')
zi = zi.add_metabolite(metab)
zi = zi.set('metabolite', 'x', 1234, 'name', 'concentration')
print zi.get('metabolite', 'x')
# print zi.set('metabolite', 'x', 'y')
# print model.Product(zi, 'smad')
# print zi.get('metabolite', 'Smad3n', by='name')
# print model.Reaction(zi, 'reaction1', expression='A -> B',
#                      rate_law='k*A')


# from beaker.cache import CacheManager
# from beaker.util import parse_cache_config_options
#
# cache_opts = {
#     'cache.type': 'file',
#     'cache.data_dir': '/home/b3053674/Documents/pycotools/ZiModel/data',
#     'cache.lock_dir': '/home/b3053674/Documents/pycotools/ZiModel/lock'
# }
# cache = CacheManager(**parse_cache_config_options(cache_opts))
# print cache


























