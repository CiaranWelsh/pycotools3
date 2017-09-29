import site
site.addsitedir('/home/b3053674/Documents/pycotools')

from  pycotools import *



cps_file1 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012.cps'
cps_file2 = r'/home/b3053674/Documents/pycotools/ZiModel/zi20122.cps'
cps_file3 = r'/home/b3053674/Documents/pycotools/ZiModel/zi20123.cps'

def reset(cps1, cps2):
    '''
    resplace m1 with m2
    :param cps1:
    :param cps2:
    :return:
    '''
    m = model.Model(cps1)
    m.save(cps2)


zi = model.Model(cps_file2)
# # print zi.save(cps_file2)
# print len(zi.reactions)
# for i in zi.functions:
#     for j in i.list_of_parameter_descriptions:
#         print j, j.key
#
# '''
# ParameterDescription(name="A", role="substrate") FunctionParameter_37652982
# ParameterDescription(name="k", role="constant") FunctionParameter_58009604
# '''
r = model.Reaction(zi, 'A2B2', expression='A -> B',
                     rate_law='k*A')
zi = zi.add('reaction', r)
#
# # r = model.Reaction(zi, 'A2B3', expression='A -> B',
# #                      rate_law='k*A')
# # zi = zi.add('reaction', r)
#
# # print len(zi.reactions)
#
zi.open(cps_file2)
#
#
# zi.open()
# from lxml import etree
# print etree.tostring(r.to_xml(), pretty_print=True)

# zi.open()
# for i in r.rate_law.list_of_parameter_descriptions:
#     print i

# print zi.reactions
# print zi.functions

#

# def __init__(self, model, name='function_1', expression=None,
#              type=None, key=None, reversible=None,
#              list_of_parameter_descriptions=[],
#              roles={}):


# f = model.Function(zi, name='funct', expression='k*A', roles={'k': 'parameter',
#                                                               'A': 'substrate'})
# for i in f.list_of_parameter_descriptions:
#     print i


# print r.rate_law
# print model.Expression(r.rate_law).to_list()

# print zi.reactions

# print r.to_xml()
# zi.add('reaction', r)

























