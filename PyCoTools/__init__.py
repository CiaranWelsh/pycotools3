import PEAnalysis
import pycopi
import pydentify
import Errors
import os


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
LOG.info('Initializing PyCoTools')
LOG.info('Initializing log10ging System')
LOG.info('logging config file at: {}'.format(LOG_CONFIG_FILE))












