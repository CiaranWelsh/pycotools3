Parameter Estimation using Prefix Argument
==========================================

Sometimes we would like to select a set of parameters to estimate and leave the rest fixed. One way to do this is to compile a list of parameters you would like to estimate and enter them into the :py:class:`ParameterEstimation.Config` class. A quicker alternative is to use the `prefix` setting.

.. code-block:: python

    import os, glob
    import pandas, numpy
    import matplotlib.pyplot as plt
    import seaborn
    from pycotools3 import model, tasks, viz
    seaborn.set_context(context='talk')

    ## Choose a directory for our model and analysis
    working_directory = os.path.abspath('')

The `prefix` argument will setup the configuration of a parameter estimation containing only parameters that start with `prefix`. While this can be anything, its quite useful to use the `_` character and then add an `_` to any parameters that you want estimated. In this way you can keep your estimated parameters marked.

.. code-block:: python

    antimony_string = """
    model simple_parameter_estimation()
        compartment Cell = 1;

        A in Cell;
        B in Cell;
        _C in Cell;

        // reactions
        R1: A => B ; Cell * _k1 * A;
        R2: B => A ; Cell * k2 * B * _C;
        R3: B => C ; Cell * _k3 * B;
        R4: C => B ; Cell * k4 * _C;

        // initial concentrations
        A = 100;
        B = 1;
        _C = 1;

        // reaction parameters
        _k1 = 0.1;
        k2 = 0.1;
        _k3 = 0.1;
        k4 = 0.1;
    end
    """

    copasi_file = os.path.join(working_directory, 'example_model.cps')

    ## build model
    mod = model.loada(antimony_string, copasi_file)

    assert isinstance(mod, model.Model)

    fname = os.path.join(working_directory, 'experiment_data.txt')
    data = mod.simulate(0, 20, 1, report_name=fname)
    ## write data to file
    data.to_csv(fname)

And now we configure a parameter estimation like normal but set `prefix` to `'_'`.

.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, fname, context='s', parameters='a') as context:
        context.set('separator', ',')
        context.set('run_mode', True)
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 100)
        context.set('lower_bound', 1e-1)
        context.set('upper_bound', 1e1)
        context.set('prefix', '_')
        config = context.get_config()

    pe = tasks.ParameterEstimation(config)

    data = viz.Parse(pe).data
    print(data)















