Simple Parameter Estimation
===========================
This is an example of how to configure a simple parameter estimation using pycotools. We first create a toy model for demonstration, then simulate some experimental data from it and fit it back to the model, using pycotools for configuration.

.. doctest:: python

    import os, glob
    import pandas, numpy
    import matplotlib.pyplot as plt
    import seaborn
    from pycotools3 import model, tasks, viz
    seaborn.set_context(context='talk')		# set seaborn context for formatting output of plots

    ## Choose a directory for our model and analysis. Note this can be anywhere. 
    working_directory = os.path.dirname(__file__)

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


Parameter estimation configuration in pycotools3 revolves around the :py:class:`tasks.ParameterEstimation.Config` object which is the input to the parameter estimation task. The object necessarily takes a lot of manual configuration to ensure it is flexible enough for any parameter estimation configuration. However, the :py:class:`ParameterEstimation.Context` class is a tool for simplifying the construction of a Config object.

.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, experiment_filename, context='s', parameters='g') as context:
        context.set('separator', ',')
        context.set('run_mode', True)
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 100)
        context.set('lower_bound', 1e-1)
        context.set('upper_bound', 1e1)

        config = context.get_config()

    pe = tasks.ParameterEstimation(config)

    data = viz.Parse(pe).data
    print(data)
