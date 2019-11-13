import subprocess
import os
from sys import version_info, platform

from . import viz
from . import tasks
from . import errors
from . import misc
from . import model
from . import bunch

if version_info[0] < 3:
    raise RuntimeError('On python version >3 you must use "import pycotools3" rather '
                       'than "import pycotools". To install pycotools3 '
                       ' use "pip install pycotools3". Please note'
                       ' that improvements will only be made to pycotools3 in '
                       'future. ')

import logging
import logging.config
import warnings

warnings.filterwarnings("ignore", message=".*numpy.dtype.*")
warnings.filterwarnings("ignore", message=".*numpy.ufunc.*")

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.WARNING)

## define the list of modules imported with the "from pycotools3 import *" statement
__all__ = ['tasks', 'model', 'viz', 'utils']


import matplotlib
try:
    matplotlib.use('Qt5Agg')
except Exception:
    try:
        matplotlib.use('Qt4Agg')
    except Exception:
        try:
            matplotlib.use('TkAgg')
        except Exception:
            pass


#todo fix logging
#todo implements the steady state task
#todo steady state documentation
#todo documentation on sensitivity analysis
#todo you have both a Bunch and a DotDict which as far as I can tell does the same thing. Fix
#todo build interface to sbmlviz from tellurium
#todo modify the models section of the parameter estimation config
#todo explain the concept of fit and Problem within parameter estimoatin settings and working directory
#todo build a proper queing system for running models in parallel. This can be done by creating N lists, like the bioinformatics problem.
#todo provide a list of both parameter estimation algorithms and solvers that are available
#todo Think about clearing up some of the unused arguments
#todo explain the concept of running parameter estimations through scan task for NxP runs
#todo enable giving explicit parameters as strings to the Context
#todo deprecate BuildAntimony class
#todo restructure the docs to remove distinction between tutorials and examples.
#todo think more about global/local chasers.
