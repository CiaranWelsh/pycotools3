.. getting-started:

.. testsetup:: *

   from pycotools3 import model, vis, tasks

Getting Started
===============
As PyCoTools only provides an alternative interface into some of COPASI's tasks, if you are unfamiliar with `COPASI <http://copasi.org/>`_ then it is a good idea to become acquainted, prior to proceeding. As much as possible, arguments to PyCoTools functions follow the corresponding option in the COPASI user interface.

In addition to COPASI, PyCoTools depends on `tellurium <http://tellurium.analogmachine.org/>`_ which is a Python package for modelling biological systems. While tellurium and COPASI have some of the same features, generally they are complementary and productivity is enhanced by using both together, particularly when using PyCoTools.

More specifically, tellurium uses `antimony <http://tellurium.analogmachine.org/antimony-tutorial/>`_ strings to define a model which is then converted into SBML. PyCoTools provides a the :class:`model.BuildAntimony` class which is essentially a wrapper around this tellurium feature, create a Copasi model and parses it into a PyCoTools :class:`model.Model`


.. autoclass:: pycotools3.model.BuildAntimony
   :members:



















