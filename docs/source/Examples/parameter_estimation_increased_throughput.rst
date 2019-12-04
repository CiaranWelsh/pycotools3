Simple Parameter Estimation
===========================
This is an example of how to configure a simple parameter estimation using pycotools. We first create a toy model for demonstration, then simulate some experimental data from it and fit it back to the model, using pycotools for configuration.

Configuring a model for parameter estimation
--------------------------------------------

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

Serial Execution
----------------

As shown in other examples, you can run a single parameter estimation using PyCoTools as a
controller by setting `run_mode=True`.

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

Parallel Execution
------------------

PyCoTools also enables you to increase parameter estimation throughput by automating
the parallel execution of multiple model copies. To do this, we simply set `run_mode='parallel'`.
With `'parallel'` mode, there are a few additional settings that you need
to know about.

    * `copy_number` is the number of model copies that you want to run
    * `pe_number` is the number of parameter estimations each of `copy_number` models will run in serial
    * `nproc` is the number of processes to use for getting through all `copy_number` models.

The configuration below will run 20 parameter estimations using a pool of 6 processes.

.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, experiment_filename, context='s', parameters='g') as context:
        context.set('separator', ',')
        context.set('run_mode', 'parallel')
        context.set('copy_number', 20)
        context.set('pe_number', 1)
        context.set('max_active', 6)
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 100)
        context.set('lower_bound', 1e-1)
        context.set('upper_bound', 1e1)
        config = context.get_config()
    pe = tasks.ParameterEstimation(config)

.. warning::::

    If you set `max_active` to a number larger than the number of
    cores in your machine, although you will be running more models
    at once, you will be running each model more slowly. Running at full
    capacity, a single COPASI instance takes about 12% CPU.
    If you set `max_active` to 12 on an 8 core machine, each instance will
    run at about 4% CPU.

On a Computer Cluster
---------------------


If you have access to a computer cluster, then PyCoTools already supports
`Slurm` and `SunGridEngine` sheduling systems. If you are using `slurm`, set
`run_mode='slurm'` and PyCoTools will submit `copy_number` jobs using `sbatch`.
If you are using `SunGridEngine` then set `run_mode='sge'`.

.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, experiment_filename, context='s', parameters='g') as context:
        context.set('separator', ',')
        context.set('run_mode', 'slurm') # or sge
        context.set('copy_number', 300)
        context.set('pe_number', 1)
        context.set('max_active', 6)
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 100)
        context.set('lower_bound', 1e-1)
        context.set('upper_bound', 1e1)
        config = context.get_config()
    pe = tasks.ParameterEstimation(config)


.. note::

    PyCoTools will expect Copasi to already be available
    in the environment so that the command `CopasiSE` will produce
    Copasi's help message and not an error.

If you are using a scheduling system different to `SGE` or `Slurm`
then you'll have to write your own wrapper, analogous to
:py:meth:`pycotools3.tasks.Run.submit_copasi_job_SGE` and
:py:meth:`pycotools3.tasks.Run.submit_copasi_job_slurm`. This shouldn't
be too difficult. If you run into trouble please submit an issue
on `GitHub <https://github.com/CiaranWelsh/pycotools3/issues>`_.


