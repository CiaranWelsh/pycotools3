# import viz
# import tasks
# import errors
# import misc
# import model
import os

import logging.config

global LOG_FILENAME
LOG_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'logging_config.conf')

if os.path.isfile(LOG_CONFIG_FILE) is not True:
    raise Exception
logging.config.fileConfig(LOG_CONFIG_FILE,
                          disable_existing_loggers=False)

LOG = logging.getLogger('root')



global __version__
#version
MAJOR = 1
MINOR = 0
MICRO = 2

__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
