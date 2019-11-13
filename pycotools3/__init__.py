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
#todo steady state documentation
#todo make explicit how  pe works
#todo documentation on sensitivity analysis