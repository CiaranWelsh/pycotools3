Parameter Estimation with Independent Variables
===============================================

The concept of independent variables is important for
parameter fitting because it enables us to simultaneously
fit multiple datasets to a single model. The is achieved
by iterating over all the datasets in your objective function
and changing variables (such as initial concentration parameters)
to what ever they should be for that dataset. These
variables are independent variables and they basically
define the initial conditions for fitting the dataset.

Independent variables are handled in PyCoTools by appending
the string `'_indep'` after a variable in the data file itself.
PyCoTools will then recognize the variable and set it as independent
rather than dependent.

Here's an example:

.. highlight:: python

    import os, glob
    import pandas, numpy
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

    # build model
    mod = model.loada(antimony_string, copasi_file)
    assert isinstance(mod, model.Model)

    # simulate some data, returns a pandas.DataFrame
    data = mod.simulate(0, 20, 1)

    # creates a new column in the dataset called A_indep
    data['A_indep'] = 50
    # the initial abundance of A will now be set to 50 prior to estimation

    # write data to file
    experiment_filename = os.path.join(working_directory, 'experiment_data.txt')
    data.to_csv(experiment_filename)


We now configure a parameter estimation like normal.

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
