Cross validation
================
Validation experiments are not used in model calibration. Instead the objective function is evaluated on validation data to see if the model can predict data it has not already seen. This can then be used as stopping criteria for the algorithm as we give a threshold for the closeness of the validation fits to simulations. This idea is common practice in machine learning and is used to prevent overfitting.

Cross validation is a new feature of pycotools3 but has been supported by COPASI for some years. The idea is to rotate calibration and validation datasets until you have tried all the combinations.

Cross validation can help identify datasets which do and don't fit well together. Here we create a model, simulate 3 datasets, make a data set up and use cross validation to infer the dataset that is made up.

.. code-block:: python
    
    # imports and create our antimony model string
    from pycotools3 import model, tasks

    working_directory = os.path.abspath('')
    antimony_string =  '''
        model negative_feedback()
            // define compartments
            compartment cell = 1.0
            //define species
            var A in cell
            var B in cell
            //define some global parameter for use in reactions
            vAProd = 0.1
            kADeg  = 0.2
            kBProd = 0.3
            kBDeg  = 0.4
            //define initial conditions
            A      = 0
            B      = 0
            //define reactions
            AProd:  => A; cell*vAProd
            ADeg: A =>  ; cell*kADeg*A*B
            BProd:  => B; cell*kBProd*A
            BDeg: B =>  ; cell*kBDeg*B
        end
        '''
    
    # Create string to where we want to copasi model to go
    copasi_file = os.path.join(os.path.dirname(__file__), 'negative_fb.cps')
    mod = model.loada(antimony_string, copasi_file )  # create the pycotools model

    # create some filenames for experimental data
    tc_fname1 = os.path.join(working_directory, 'timecourse1.txt')
    tc_fname2 = os.path.join(working_directory, 'timecourse2.txt')
    ss_fname1 = os.path.join(working_directory, 'steady_state1.txt')
    ss_fname2 = os.path.join(working_directory, 'steady_state2.txt')

    # simulate/create some experimental data
    model.simulate(0, 5, 0.1, report_name=self.tc_fname1)
    model.simulate(0, 10, 0.5, report_name=self.tc_fname2)
    dct1 = {
        'A': 0.07,
        'B': 0.06,
        'C': 2.8
    }
    dct2 = {
        'A': 846,
        'B': 697,
        'C': 739
    }
    ss1 = pandas.DataFrame(dct1, index=[0])
    ss1.to_csv(self.ss_fname1, sep='\t', index=False)
    ss2 = pandas.DataFrame(dct2, index=[0])
    ss2.to_csv(self.ss_fname2, sep='\t', index=False)


Configuring a cross validation experiment is similar to running parameter estimation or profile likelihoods: the difference is that you use `context='cv'` as argument to :py:class:`ParameterEstimation.Context`.

.. code-block:: python

    with tasks.ParameterEstimation.Context(
        model, experiments, context='cv', parameters='gm'
    ) as context:
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 20)
        context.set('number_of_generations', 50)
        context.set('validation_threshold', 500)
        context.set('cross_validation_depth', 1) ## 3/4 datasets calibration; 1/4 for validation.
        context.set('copy_number', 3) #3 per model (5 models here)
        context.set('run_mode', True)
        context.set('lower_bound', 1e-3)
        context.set('upper_bound', 1e2)
        config = context.get_config()

    pe = ParameterEstimation(config)
    data = pycotools3.viz.Parse(pe).concat()

	


.. note::

   The `cross_validation_depth` argument specifies how far to go combinatorially. For instance, when `cross_validation_depth=2` and there are 4 datasets, all combinations of 2 datasets for experiments and 2 for validation will be applied.

.. warning::

   While validation experiments are correctly configured with pycotools, there seems to be some instability in the current release of Copasi regarging multiple experiments in the `validation datasets` feature. Validation experiments work well when only one validation experiment is specified, but can crash when more than one is given.

.. note::

   The `copy_number` applies per model here. So 4 datasets, `cross_validation_depth=1` means four models are configured for validation. Also configured is the model without any validation experiments for convenience.

The `validation_weight` and `validation_threshold` arguments are specific for validations. The copasi docs are vague on precisely what these mean but the higher the threshold, the more rigerous the validation.
















