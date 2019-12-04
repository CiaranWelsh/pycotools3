Organising parameter estimation runs
====================================
It is very rare that you get the parameter estimation settings
correct the first time. PyCoTools has a way of organising
sequential parameter estimations runs by using the `problem` and
`fit` arguments.

Setup a model for parameter estimation
--------------------------------------

.. code-block:: python

    import os, glob
    import pandas, numpy
    import matplotlib.pyplot as plt
    import seaborn
    from pycotools3 import model, tasks, viz
    seaborn.set_context(context='talk')		# set seaborn context for formatting output of plots

    ## Choose a directory for our model and analysis. Note this can be anywhere. 
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

    # Create a path to a copasi file
    copasi_file = os.path.join(working_directory, 'example_model.cps')

    ## build model
    mod = model.loada(antimony_string, copasi_file)
    assert isinstance(mod, model.Model)

    ## simulate some data, returns a pandas.DataFrame
    data = mod.simulate(0, 20, 1)

    ## write data to file
    experiment_filename = os.path.join(working_directory, 'experiment_data.txt')
    data.to_csv(experiment_filename)

    ## We now have a model and some experimental data and can
    ## configure a parameter estimation


Incrementing parameter estimation runs
--------------------------------------
In the :py:class:`pycotools3.tasks.ParameterEstimation.Config.settings`
there are two arguments called `problem` and `fit`. Both of these
default to 1. When you run a parameter estimation, the results
are placed in a directory called `Problem1/Fit1`. By changing
either argument, you effectively change the location of the
results directory.

The `problem` directory is generally used for major changes
in the model which make previous parameter estimations
incompatable with the current model. For instance a major
change would be adding a reaction, changing which parameter
are estimated or modifying the experimental data.

The `fit` directory is generally used for minor changes, such as
using a different algorithm or changing hyperparameters.

Example
-------

You could setup the following estimation

.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, experiment_filename, context='s', parameters='g') as context:
        context.set('separator', ',')
        context.set('run_mode', True)
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 100)
        context.set('lower_bound', 1e-1)
        context.set('upper_bound', 1e1)
        context.set('problem', 'Problem1')  # default
        context.set('fit', 1)               # default

        config = context.get_config()

    pe = tasks.ParameterEstimation(config)

Decide to add a reaction to your model string and then
change the configuration to


.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, experiment_filename, context='s', parameters='g') as context:
        context.set('separator', ',')
        context.set('run_mode', True)
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 100)
        context.set('lower_bound', 1e-1)
        context.set('upper_bound', 1e1)
        context.set('problem', 'Problem2')  # default
        context.set('fit', 1)               # default
        config = context.get_config()

    pe = tasks.ParameterEstimation(config)

If your parameter estimiation doesn't converge you could
modify the algorthm and increment the fit argument.


.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, experiment_filename, context='s', parameters='g') as context:
        context.set('separator', ',')
        context.set('run_mode', True)
        context.set('randomize_start_values', True)
        context.set('method', 'particle_swarm')
        context.set('swarm_size', 100)
        context.set('lower_bound', 1e-2)
        context.set('upper_bound', 1e3)
        context.set('problem', 'Problem2')  # default
        context.set('fit', 2)               # default
        config = context.get_config()

    pe = tasks.ParameterEstimation(config)

