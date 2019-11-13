Working with an existing copasi model
=====================================

You can create a new model using the antimony language. Sometimes however, you have already built a model using the CoapsiUI and want to use pycotools3 with this model. This example shows you how to use the :py:class:`pycotools3.model.Model` class directly. 

Create a PyCoTools model from an existing model
-----------------------------------------------

.. highlight:: python

    from pycotools3 import model
    
    # remember to input the string to your own model here
    copasi_file = <'string/to/model.cps'>

    mod = model.Model(copasi_file)

    assert isinstance(mod, model.Model)

Extracting the antimony string associated with a copasi model
-------------------------------------------------------------

It is often useful to have an antimony string generated directly from a copasi model. 

.. code-block:: python

    ant_string = mod.to_antimony()
    print(ant_string)

 
