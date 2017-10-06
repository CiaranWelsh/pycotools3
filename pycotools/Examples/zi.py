import os
import site
site.addsitedir('/home/b3053674/Documents/pycotools')
from pycotools.Tests import test_models
from pycotools import model
import os

zi_model_string = test_models.TestModels().zi_model()

## get a working directory. Change this to change this to wherever you like
directory = r'/home/b3053674/Documents/pycotools/pycotools/Examples'

## choose path to zi model
zi_path = os.path.join(directory, 'zi2012.cps')
my_zi_path = os.path.join(directory, 'my_zi2012.cps')

##write model to file
with open(zi_path, 'w') as f:
    f.write(zi_model_string)

## check file exists
if not os.path.isfile(zi_path):
    raise Exception


from shutil import copy
copy(zi_path, my_zi_path)
assert os.path.isfile(my_zi_path)



my_zi = model.Model(my_zi_path)


my_zi = my_zi.remove('reaction', 'R26_LRC_Cave_degradation')




r = model.Reaction(my_zi, 'Smad7NegFB', 'LRC_Cave -> ;Smad7', 'k*LRC_Cave*Smad7')
my_zi = my_zi.add('reaction', r)

# r = model.Reaction(my_zi, 'Smad7 Prod', 'Smads_Complex_n -> Smads_Complex_n + Smad7', 'kSmad7Prod*Smads_Complex_n')
# my_zi = my_zi.add('reaction', r)

my_zi.open()

















