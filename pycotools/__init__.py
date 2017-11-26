import viz
import tasks
import errors
import os
import misc
import model
import models

import logging
import logging.config

global LOG_FILENAME
LOG_CONFIG_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'logging_config.conf')

if os.path.isfile(LOG_CONFIG_FILE) is not True:
    raise Exception
logging.config.fileConfig(LOG_CONFIG_FILE,
                          disable_existing_loggers=False)

LOG = logging.getLogger('root')












