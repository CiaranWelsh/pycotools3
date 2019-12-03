.. Pycotools documentation master file, created by
   sphinx-quickstart on Wed Oct 11 11:46:06 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: bash(code)
   :language: bash

.. role:: python(code)
   :language: python

.. _home-page:

PyCoTools
=========
PyCoTools is a python package that was developed
as an alternative interface into
`COPASI <http://copasi.org/>`_, simulation software
for modelling biochemical systems. The PyCoTools
paper can be found `here <https://academic.oup.com/bioinformatics/article/34/21/3702/5001390>`_ and describes in detail the intentions and functionality of PyCoTools. There are some important differences between the PyCoTools version that is described in the publication and the current version. The first is that PyCoTools is now a python 3 only package. If using Python 2.7 you should create a virtual Python 3.6 environment using `conda <https://salishsea-meopar-docs.readthedocs.io/en/latest/work_env/python3_conda_environment.html>`_ or `virtualenv <https://virtualenv.pypa.io/en/latest/>`_.
My preference is conda. The other major difference
is the interface to COPASI's parameter estimation task which is described in the tutorials and examples.

.. note::

   I am in the process of improving this documentation.
   Although still valid, content in the
   `Tutorials <https://pycotools3.readthedocs.io/en/latest/Tutorials/tutorials.html>`_ page
   is quite old and is in the process of being replaced by content
   in the `examples <https://pycotools3.readthedocs.io/en/latest/Examples/examples.html>`_.

Installation
------------

First make sure you use a Python 3.6 environment.

.. warning::

   Using Python 3.7 or 3.8 will not work at this time due to dependency issues
   (which are unfortunately out of my control).

Then use:

.. code-block:: bash

   $ pip install pycotools3

Remember to :bash:`source activate` your python 3.6 environment if you need to.

To install from `source <https://github.com/CiaranWelsh/pycotools3.git>`_:

.. code-block:: bash

  $ git clone https://github.com/CiaranWelsh/pycotools3.git
  $ cd pycotools3
  $ python setup.py install

The procedure is the same in linux, mac and windows.

Troubleshooting
---------------

### PyCoTools3 will not install

Pycotools3 is only supported in Python 3 to Python 3.6. If you are using Python 2.7 or Python 3.7 please create a new conda Python3.7 environment. 

.. code-block:: bash

    $ conda create -n py36 python=3.6
    $ conda activate py36
    $ pip install pycotools3

The same commands should work cross platform. 

### You get errors when trying to build a model using :py:func:`pycotools3.model.loada`
Make sure you have installed `Copasi <http://copasi.org/Download/>`_ and added the `Copasi/bin` directory to
the path variable.

- `On Linux <https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path>`_
- `On Windows <https://stackoverflow.com/questions/9546324/adding-directory-to-path-environment-variable-in-windows>`_
- `On Mac <https://stackoverflow.com/questions/7703041/editing-path-variable-on-mac>`_

Documentation
-------------
This is a guide to PyCoTools version >2.0.1.

.. toctree::
   :maxdepth: 2
   :name: master-toc
   :hidden:

   self
   getting_started
   Tutorials/tutorials
   Examples/examples
   API/modules


Support
-------
Users can post a question on stack-overflow using the :code:`pycotools` tag. I get email notifications for these questions and will respond.

People
------
PyCoTools has been developed by Ciaran Welsh in Daryl Shanley's lab at Newcastle University.

Caveats
=======
* Non-ascii characters are minimally supported and can break PyCoTools
* Do not use unusual characters or naming systems (i.e. A reaction name called "A -> B" will break pycotools)
* In COPASI we can have (say) a global quantity and a metaboltie with the same name because they are different entities. This is not supported in Pycotools and you must use unique names for every model component


Citing PyCoTools
----------------
If you made use of PyCoTools, please cite `this <https://academic.oup.com/bioinformatics/article/34/21/3702/5001390>`_ article using:

  - Welsh, C.M., Fullard, N., Proctor, C.J., Martinez-Guimera, A., Isfort, R.J., Bascom, C.C., Tasseff, R., Przyborski, S.A. and Shanley, D.P., 2018. PyCoTools: a Python toolbox for COPASI. Bioinformatics, 34(21), pp.3702-3710.

And also please remember to cite `COPASI <http://copasi.org/>`_:

  - Hoops, S., Sahle, S., Gauges, R., Lee, C., Pahle, J., Simus, N., Singhal, M., Xu, L., Mendes, P. and Kummer, U., 2006. COPASI—a complex pathway simulator. Bioinformatics, 22(24), pp.3067-3074.

and `tellurium <http://tellurium.analogmachine.org/>`_:

  - Medley, J.K., Choi, K., König, M., Smith, L., Gu, S., Hellerstein, J., Sealfon, S.C. and Sauro, H.M., 2018. Tellurium notebooks—An environment for reproducible dynamical modeling in systems biology. PLoS computational biology, 14(6), p.e1006220.















