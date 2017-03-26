import PEAnalysis
import pycopi
import pydentify2
import Errors
import os



import logging.config
global LOG_FILENAME
LOG_CONFIG_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'logging_config.conf')
logging.config.fileConfig(LOG_CONFIG_FILE,disable_existing_loggers=False)


LOG=logging.getLogger('root')
LOG.info('Initializing PyCoTools')
LOG.info('Initializing Logging System')
LOG.info('logging config file at: {}'.format(LOG_CONFIG_FILE))





