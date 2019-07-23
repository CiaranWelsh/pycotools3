Working from the model.Model class directly
===========================================

The pycotools3 tasks module contains classes for a bunch of copasi tasks that can be configured from python using pycotools. To simplify some of these tasks, wrappers have been build around these task classes in the :py:class:`model.Model` class so that they can be used like a regular method. Here I demonstrate some of these.

We first configure a model for the demonstration

.. code-block:: python

    import os, glob
    import pandas, numpy
    import matplotlib.pyplot as plt
    import seaborn
    from pycotools3 import model, tasks, viz
    seaborn.set_context(context='talk')

    ## Choose a directory for our model and analysis
    working_directory = os.path.abspath('')

    ## In this model, A gets reversibly converted to B but the backwards reaction is additionally regulated by C.
    ## B is reversibly converted into C.
    antimony_string = """
    model simple_parameter_estimation()
        compartment Cell = 1;

        A in Cell;
        B in Cell;
        C in Cell;

        // reactions
        R1: A => B ; Cell * k1 * A;
        R2: B => A ; Cell * k2 * B * C;
        R3: B => C ; Cell * k3 * B;
        R4: C => B ; Cell * k4 * C;

        // initial concentrations
        A = 100;
        B = 1;
        C = 1;

        // reaction parameters
        k1 = 0.1;
        k2 = 0.1;
        k3 = 0.1;
        k4 = 0.1;
    end
    """

    copasi_file = os.path.join(working_directory, 'example_model.cps')

    ## build model
    mod = model.loada(antimony_string, copasi_file)

    assert isinstance(mod, model.Model)


Inserting parameters
--------------------


.. code-block:: python

   dct = {
     'k1': 55,
     'k2': 36
   }
   mod.insert_parameters(parameter_dict=dct, inplace=True)

or

.. code-block:: python

   mod = mod.insert_parameters(parameter_dict=dct)

or

.. code-block:: python

   import pandas
   df = pandas.DataFrame(dct, index=[0])
   mod.insert_parameters(df=df, inplace=True)

or if the dataframe `df` has more than one parameter set we can specify the rank using the `index` argument.

.. code-block:: python

   import pandas
   ##insert second best parameter set
   mod.insert_parameters(df=df, inplace=True, index=1)


.. note::

   This is most useful when using :py:class:`viz.Parse` output dataframes, which are :py:class:`pandas.DataFrame` objects containing parameters in the columns and parameter sets in the rows, sorted by best RSS

or, assuming the variable `results_directory` is a directory to a folder containing parameter estimation results.

.. code-block:: python

   mod.insert_parameters(parameter_path=results_directory, inplace=True)


Simulating a time course
------------------------

.. code-block:: python

   data = mod.simulate(0, 10, 11)

Simulates a deterministic time course, 11 time points between 0 and 10. `data` contains a :py:class:`pandas.DataFrame` object with variables along the columns and time points down the rows.

.. code-block:: python

   fname = os.path.join(os.path.dirname(__file__), 'simulation_data.csv')
   ## write data to file named fname
   data = mod.simulate(0, 10, 11, report_name=fname)

Like with the other shortcuts, arguments for the :py:class:`tasks.TimeCourse` class are pass on.

.. code-block:: python

   data = mod.simulate(0, 10, 11, method='direct')

.. code-block:: python

   fname = ps.path.join(os.path.dirname(__file__), 'scan_results.csv')
   mod.scan(variable='A', minimum=5, maximum=10, report_name=fname)

By default the scan type is set to 'scan'. We can change this

.. code-block:: python

   fname = ps.path.join(os.path.dirname(__file__), 'scan_results.csv')
   mod.simulate(0, 10, 11, method='direct', run_mode=False)
   mod.scan(variable='A', scan_type='repeat',
            number_of_steps=10, report_name=fname,
            subtask='timecourse')

.. note::

   In the `mod.simulate` we configure copasi to run a stochastic time course but do not execute. We then configure the repeat scan task to run the stochastic time course 10 times.


Sensitivities
-------------


.. code-block:: python

   sens = mod.sensitivities(
               subtask='steady_state', cause='all_parameters',
               effect='all_variables'
          )
















