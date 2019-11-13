Profile Likelihoods
===================

Since a profile likelihood is just a parameter scan of parameter estimations, all we need to do to configure a profile likelihood analysis is to setup an appropriate :py:class:`ParameterEstimation.Config` object and feed it into the :py:class:`ParameterEstimation` class. This would be tedious to do manually but is easy with :py:class:`ParameterEstimation.Context`


.. highlight:: python

    import os, glob
    import pandas, numpy
    import matplotlib.pyplot as plt
    import seaborn
    from pycotools3 import model, tasks, viz

    working_directory = os.path.abspath('')

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

    ## simulate some data, returns a pandas.DataFrame
    data = mod.simulate(0, 20, 1)

    ## write data to file
    experiment_filename = os.path.join(working_directory, 'experiment_data.txt')
    data.to_csv(experiment_filename)

The profile likelihood is calculated around the current parameter set in the model. If you want to change the current parameter set, maybe to the best fitting parameter set from a parameter estimation you can use the :py:class:`InsertParameters` class. For now, we'll assume the best parameter set is already in the model.

.. code-block:: python

   with ParameterEstimation.Context(
       mod, experiment_filename,
       context='pl', parameters='gm'
   ) as context:
       context.set('method', 'hooke_jeeves')
       context.set('pl_lower_bound', 1000)
       context.set('pl_upper_bound', 1000)
       context.set('pe_number', 25) # number of steps in each profile likelihood
       context.set('run_mode', True)
       config = context.get_config()

We set the method to hooke and jeeves, a local optimiser which does well with profile likelihoods. We also set the `pl_lower_bound` and `pl_upper_bound` arguments to 1000 (which are defaults anyway). These are multipliers, not boundaries, of the profile likelihood. For instance, if the best estimated parameter for `A` was 1, then the profile likelihood would stretch from 1-e3 to 1e3.

Now, like with other parameter estimations we can simply do

.. code-block:: python

   ParameterEstimation(config)

Because the `context=pl` was used, pycotools knows to copy the model for each parameter, remove the parameter of interest from the parameter estimation task and create a scan of the parameter of interest.









