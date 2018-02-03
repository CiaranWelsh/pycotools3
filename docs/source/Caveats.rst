Caveats
=======

This is a list of known problems currently in Pycotools

Non-Ascii Characters
--------------------

* Are not supported
* Do not use unusual characters or naming systems (i.e. A reaction name called "A -> B" will break pycotools)

Parameter Estimation
--------------------

Currently we cannot setup:

* Affected experiments in parameter estimations 

Units
=====

Not all quantity units are supported. 
Supported units are:

* fmol, pmol, nmol, mmol, mol, dimensionless and `#` (latter for particle numbers)

Assignments
===========

Assignments are not currently supported but will be in a future release. Again, here simply use the COPASI user interface instead. 

Duplicate Names
===============

In COPASI we can have (say) a global quantity and a metaboltie
with the same name because they are different entities. This is not
supported in Pycotools and you must use unique names for every model
component

Known Bugs
==========
* viz.PlotTimeCourseEnsembles doesn't work properly if user is fitting multiple experiments with multiple conditions (i.e. defined by independent variables)


