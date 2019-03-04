import subprocess
import os
from sys import version_info, platform

def download_copasi():
    """
    Download COPASI 4.24 from my github.

    It is conventient for the user to not have to download
    copasi themselves but it is not possible to include in pypi
    because of file sizes. A workaround is to download the
    COPASI folder manually, the first time pycotools3 is run. That
    is what is function does.
    """
    # write some code to handle the case where copasi is not installed
    try:
        ## check whether there is a directory next to __init__.py called COAPSI
        copasi_directory = os.path.join(os.path.dirname(__file__), 'COPASI')
        ## if present, assume this function has been run before
        assert os.path.isdir(copasi_directory)
    except AssertionError:
        print('For convenience, COPASI is distributed with pycotools3 and sits '
              'next to the pycotools installation. Please wait while we configure'
              ' for you. This is only necessary the first time you use pycotools3 '
              'after installing with pip.')
        import requests
        import zipfile
        import shutil

        filename = os.path.join(os.path.dirname(__file__), 'pycotools.zip')

        url = 'https://github.com/CiaranWelsh/pycotools3/archive/master.zip'

        if not os.path.isfile(filename):
            print('downloading the pycotools3 repository...')
            r = requests.get(url)
            with open(filename, 'wb') as f:
                f.write(r.content)


        print('decompressing pycotools3 repository...')
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(os.path.dirname(__file__))
        zip_ref.close()

        extracted_dir = os.path.join(os.path.dirname(__file__), 'pycotools3-master')
        if not os.path.isdir(extracted_dir):
            raise NotADirectoryError(extracted_dir)

        extracted_pycotools3_dir = os.path.join(extracted_dir, 'pycotools3')
        extracted_copasi_dir = os.path.join(
            extracted_pycotools3_dir, 'COPASI')

        if not os.path.isdir(extracted_copasi_dir):
            raise NotADirectoryError(extracted_copasi_dir)

        print('copying COPASI files ...')
        shutil.copytree(extracted_copasi_dir, os.path.join(os.path.dirname(__file__), 'COPASI'))

        print('Removing downloaded files..')
        shutil.rmtree(extracted_pycotools3_dir)
        shutil.rmtree(extracted_dir)
        os.remove(filename)
        print('configuration complete.')


download_copasi()

from . import viz
from . import tasks
from . import errors
from . import misc
from . import model
from . import munch

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
