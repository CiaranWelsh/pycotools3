import viz
import tasks
import pydentify
import Errors
import os
# import model
# import _base

import logging
import logging.config
import subprocess
import re






global LOG_FILENAME
LOG_CONFIG_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'logging_config.conf')
if os.path.isfile(LOG_CONFIG_FILE)!=True:
    raise Exception
logging.config.fileConfig(LOG_CONFIG_FILE,disable_existing_loggers=False)


LOG=logging.getLogger('root')
LOG.info('Initializing pycotools')
LOG.info('Initializing logging System')
LOG.info('logging config file at: {}'.format(LOG_CONFIG_FILE))












