| Title | Badge |
|-------|-------|
| master        | [![Build Status](https://travis-ci.org/CiaranWelsh/pycotools3.svg?branch=master)](https://travis-ci.org/CiaranWelsh/pycotools3)   [![Documentation Status](https://readthedocs.org/projects/pycotools3/badge/?version=latest)](https://pycotools3.readthedocs.io/en/latest/?badge=latest)| 
| develop | [![Build Status](https://travis-ci.org/CiaranWelsh/pycotools3.svg?branch=develop)](https://travis-ci.org/CiaranWelsh/pycotools3) [![Documentation Status](https://readthedocs.org/projects/pycotools3/badge/?version=develop)](https://pycotools3.readthedocs.io/en/latest/?badge=develop)|
|Version|[![PyPI version](https://badge.fury.io/py/pycotools3.svg)](https://badge.fury.io/py/pycotools3)|
| Downloads | [![Downloads](https://pepy.tech/badge/pycotools3)](https://pepy.tech/project/pycotools3) [![Downloads](https://pepy.tech/badge/pycotools3/month)](https://pepy.tech/project/pycotools3)|

# Pycotools3

Pycotools3 is a set of tools for interacting with [COPASI simulation software](http://copasi.org/) from Python 3. The old repository supports Python 2 only, can be found [here](https://github.com/CiaranWelsh/pycotools) and is the version that is described in detail in the [bioinformatics publication](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/bty409/5001390). 

Since publication, the pycotools project has moved to this pycotools3 repository, which is maintained separetly from pycotools. Since moving, the interface to COPASI's parameter estimation task has been significantly improved including inherent multi-model configuration and profile likelihood support - please refer to the **[pycotools3 documentation](http://pycotools3.readthedocs.io/en/latest/)** for more detail. Despite these improvements, there still a few things left to implement, namely full support for visualisation facilities.  For now, users are advised to checkout [matplotlib](https://matplotlib.org/contents.html) and [seaborn](https://seaborn.pydata.org/).

## Support 
I get email notificatons fror stackoverflow questions tagged with `pycotools` so you can ask a question there. Additionally, you may contact me directly or post an issue.

## Contributions
Contributions, ideas, suggestions, feature requests or anything generally geared towards improving the package are welcome. 

## Citations
- Welsh CM, Fullard N, Proctor CJ, Martinez-Guimera A, Isfort RJ, Bascom CC, Tasseff R, Przyborski SA, Shanley DP. PyCoTools: a Python toolbox for COPASI. Bioinformatics. 2018 May 22;34(21):3702-10.

Since this package relies heavily on COPASI and tellurium please also cite 

- Hoops, S., Sahle, S., Gauges, R., Lee, C., Pahle, J., Simus, N., Singhal, M., Xu, L., Mendes, P. and Kummer, U., 2006. COPASI—a complex pathway simulator. Bioinformatics, 22(24), pp.3067-3074.


- Medley, J.K., Choi, K., König, M., Smith, L., Gu, S., Hellerstein, J., Sealfon, S.C. and Sauro, H.M., 2018. Tellurium notebooks—An environment for reproducible dynamical modeling in systems biology. PLoS computational biology, 14(6), p.e1006220.


