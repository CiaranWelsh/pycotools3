from . import viz
from . import tasks
from . import errors
from . import misc
from . import model
from . import munch
import os
from sys import version_info, platform

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

# import logging
#
# logging.basicConfig()
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

# global LOG_FILENAME
# LOG_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                'logging_config.conf')
#
# if os.path.isfile(LOG_CONFIG_FILE) is not True:
#     raise Exception
# logging.config.fileConfig(LOG_CONFIG_FILE,
#                           disable_existing_loggers=False)

# LOG = logging.getLogger(__name__)
# LOG.setLevel(logging.WARNING)

## define the list of modules imported with the "from pycotools3 import *" statement
__all__ = ['tasks', 'model', 'viz', 'utils']




# global __version__
# #version
# MAJOR = 1
# MINOR = 0
# MICRO = 3
#
# __version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
