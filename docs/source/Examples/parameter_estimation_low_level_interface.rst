Parameter Estimation with the Low Level Interface
=================================================

Parameter estimation configuration in PyCoTools revolves around the :py:class:`ParameterEstimation.Config` object,
 which is merely a nested data storage class. When you use the :py:class:`ParameterEstimation.Context` object,
 you are using a high level interface to create a :py:class:`ParameterEstimation.Config` object. However, it is
 also possible to build it manually. It should be stressed however, that the Context method should be preferred
 when possible. The low level interface can be tedious but gives you more flexibility for more fine tuned
 parameter estimation configurations. While there is not getting around the fact that
 building the :py:class:`ParameterEstimation.Config` object can take time, I have built
 in a 'default system' whereby if a (non-compulsory) section is left blank, then
 PyCoTools tries to use the default values.

The :py:class:`ParameterEstimation.Config` Object is a bit like a Struct from other
 languages. You can access attributes using either dot notation or dictionary like
 access.

There are four main sections to the Config object:

    * models
    * datasets
    * items
    * settings

Each of these are described in detail below.

models
------
This is a nested structure containing an arbitrary
number of models for simultaneous configuration. It is the users
responsibility that it makes sense to configure multiple models
for parameter estimation in the same way.

    * models
        * model1_name (leaf): full string to model 1 copasi file
        * model2_name (leaf): full string to model 2 copasi file
        * ...

.. highlight::

    models = dict(
        model1=dict(copasi_file='</full/path/to/copasi_file1.cps'),
        model2=dict(copasi_file='</full/path/to/copasi_file2.cps')
    )

.. note::

    The nested structure of the models section remains a deprecated
    version of PyCoTools. Since it does not need to be nested, this will
    be changing to non-nested in the near future.


datasets
--------

This is where we tell PyCoTools about the data were using for
 parameter estimation. The datasets attribute is itself nested with the following
 structure:

    * datasets
        * experiments
        * validations

Both `experiments` and `validations` are nested structures and they are pretty much identical.
 The difference is that those configured via the `experiments` section are used for calibrating/training
 the model while those in the validation section are only used for validation (or testing). For simplicity,
 the structure of both is described in one section.

    * experiments (or validation)
        * experiment_name. An arbitrary string representing the name of the experiment.
            * filename (leaf). The full path to the dataset
            * affected_models. Analogous to affected_experiments or affected_validation_experiments, you can have an experiment target only one (or more) model. This feature is a superser of COPASI. Defaults to the string 'all' which is translated to all models.
            * mappings. Another nested structure for mapping arguments. If left blank, PyCoTools will assume 1:1 mappings between experimental data file headers and model variables. Independent variables are assumed to contain a trailing `_indep`, i.e. `PI3K_indep`. This should have as many elements as there are columns in the data file.
                * Experimental variable name (or time). These should be the same as used for data column headers.
                    * model_object (leaf node). The object that corresponds to the experimental variable name.
                    * role (leaf node). Either `time`, `ignored` (default), `dependent` or `independent`
            * separator (leaf). Overrides the separator in the settings section, for when they are different. However, good practice is to always use the same separator and set the separator in the settings section.
            * normalize_weights_per_experiment (leaf): boolean, default=True.

Here's an example of the datasets section.

.. highlight::

    datasets=dict(
        experiments= dict(
            report1 = dict(
                filename='full/path/to_datafile1.csv',
                affected_models='all',
                mappings=dict(
                    Time=dict(
                        model_object='Time',
                        role='time'
                    ),
                    A=dict(
                        model_object='A'),
                        role='dependent'),
                    ),
                )
            ),
            # note the absence of the mappings field. This tells
            # PyCoTools that you have used the suggested convention
            # of matching model variables with data file headers and using
            # '_indep' suffix for independent variables.
            report2=dict(
                filename='full/path/to_datafile2.csv',
                separator='\t'  #overrides separator from main settings menu
            )
        ),
        # This data will not be used for parameter estimation. Only validation.
        validations=dict(
            report3=dict(
                filename='full/path/to_datafile3.csv',
                affected_models='model1',  # this validation experiment only affects model1
                # were excepting default mapping convention
            ),
        )
    )

items
-----

This is where we configure the parameters to be estimated, their boundaries, start values
 and affected experiments. The `items` structure is composed of `fit_items` and `constraint_items`.

    * items
        * fit_items
        * constraint_items

Similarly to the experiment section, fit_items and constraint_items are nearly identical. The
 difference is that whilst fit items are used to define the parameter space constraints are
 used to restrict the parameter space to a subset of the full parameter space. An estimation
 with constraints can explore beyond the restrictions imposed by the constraints but solutions
 that violate the constraints will not be excepts. In contrast, the solution cannot go beyond the
 boundaries of the boundaries set by the fit_items.

.. highlight::

    items = dict(
        fit_items=dict(
            A=dict(
                affected_experiments=['report1'],
                affected_models=['model1'],
                affected_validation_experiments=['report3'],
                lower_bound=15,
                start_value=0.1,
                upper_bound=35
            ),
            B=dict(
                affected_experiments=['report1', 'report2'],
                affected_models=['model1'],
                affected_validation_experiments=['report3'],
                lower_bound=0.05,
                start_value=1.05,
                upper_bound=36
            ),
            C=dict(
                affected_experiments=['report1', 'report2'],
                affected_models=['model1'],
                affected_validation_experiments=['report3'],
                lower_bound=0.05,
                start_value=1.0,
                upper_bound=36
            )
        ),
        constraint_items=dict(
            C=dict(
                affected_experiments=['report1', 'report2'],
                affected_models=['model1'],
                affected_validation_experiments=['report3'],
                lower_bound=16,
                start_value=1.05,
                upper_bound=26
                )
        )
    )

.. note::

    `affected_experiments`, `affected_models`, and `affected_validation_experiments` all
    accept the special string `all` which resolves to all of your data files. This is default
    behaviour for both `affected_experiments` and `affected_models` whereas the default behaviour for
    `affected_validation_experiments` is None.

Settings
--------

settings = dict(
    calculate_statistics=False,     # Corresponds to the `calculate_statistics` flag in copasi
    config_filename=config.yml      # Filename for saving config to file
    context=s,                      # Alters the behaviour of the configuration. See :py:class:`ParameterEstimation.Context`.
    cooling_factor=0.85             # Parameter estimation algorithm setting
    copy_number=1,                  # How many times to copy the copasi file for simultaneous runs
    create_parameter_sets=False,    # Corresponds to the create_parameter_sets flag in copasi
    cross_validation_depth=1,       # depth of cross validation. Corresponds to COPASI, (though this feature was buggy during development)
    fit=1,                          # This is an index of parameter estimation. Increment by 1 to repeat a similar parameter estimation to test alternative configurations
    iteration_limit=50,             # Parameter estimation algorithm setting
    lower_bound=0.05                # Default lower boundary for all parameters in the estimation. Can be overwritten under the fit_items section to have different boundaries for every fit item.
    max_active=3,                   # When running
    method=genetic_algorithm_sr,    # which algorithm to use
    number_of_generations=100,      # Parameter estimation algorithm setting
    number_of_iterations=100000,    # Parameter estimation algorithm setting
    overwrite_config_file=False,    # Set to True to explicitely overwrite existing configuration file.
    pe_number=1,                    # How many parameter estimations
    pf=0.475                        # Parameter estimation algorithm settings
    pl_lower_bound=1000,            # When context is set to 'pl' for profile likelihood configurations, this defines the upper boundary of the analysis. The upper boundary is the best estimated parameter multiplied by this value.
    pl_upper_bound=1000,            # When context is set to 'pl' for profile likelihood configurations, this defines the lower boundary of the analysis. The lower boundary is the best estimated parameter divided by this value.
    population_size=38,             # Parameter estimation algorithm setting
    prefix=None,                    # Prefix used to automatically locate parameters to be estimated. For instance, you can 'tag' each parameter you want to include in the estimation with an underscore at the begining (i.e. _kAktPhosphorylation) to filter the parameters for estimation.
    problem=Problem1,               # This is the name of the folder that will be created to contain the results.
    quantity_type=concentration,    # either 'concentration' or 'particle_numbers' to switch between the two.
    random_number_generator=1,      # Parameter estimation algorithm setting.
    randomize_start_values=False,   # Corresponds to the 'randomize_start_values' flag in copasi
    report_name=PEData.txt          # The base report name for the parameter estimation output. This is automatically modified when copy_number is > 1. The results have as many rows as `pe_number`.
    results_directory=ParameterEstimationData,  # This folder stores the actual parameter estimation results, within the fit directory (which is within the Problem directory)
    rho=0.2                         # Parameter estimation algorithm setting
    run_mode=False,                 # Switch between False
    save=False,
    scale=10,                       # Parameter estimation algorithm setting
    seed=0,                         # Parameter estimation algorithm setting
    start_temperature=1,            # Parameter estimation algorithm setting
    start_value=0.1                 # Parameter estimation algorithm setting
    starting_parameter_sets=None,   # Experimental feature.
    std_deviation=1.0e-06           # Parameter estimation algorithm setting
    swarm_size=50,                  # Parameter estimation algorithm setting
    tolerance=1.0e-05               # Parameter estimation algorithm setting
    update_model=False,             # Corresponds to the update model flag in copasi
    upper_bound=36,                 # Default upper boundary for all parameters in the estimation. Can be overwritten under the fit_items section to have different boundaries for every fit item.
    use_config_start_values=False,  # If True, parameter estimation will start from the start values specified under the `fit_items` section.
    validation_threshold=8.5        # Corresponds to the validation threshold in COPASI. This is the default value that can be overwritten by giving this argument to the validation dataset section.
    validation_weight=4,            # Corresponds to the validation weight in COPASI.  This is the default value that can be overwritten by giving this argument to the validation dataset section.
    weight_method=value_scaling,    # Which weight method to use. Default='mean_squared'. Other options: mean, standard_deviation or value_scaling
    working_directory=/home/ncw135/Documents/pycotools3/Tests   # The overall directory for the whole analysis. Defaults to the same directory containing the first copasi file found for configuration.
)

Building a :py:class:`ParameterEstimation.Config` object
--------------------------------------------------------

When you have configured the relevant sections, you can simply call the :py:class:`ParameterEstimation.Config` constructor
 to create your object.

Assuming you have nested dictionaries containing the apprioriate information detailed above:

.. highlight::

    config = tasks.ParameterEstimation.Config(
                models=models,
                datasets=datasets,
                items=items,
                settings=settings
            )

The config is formatted using yaml for ease of inspection.

.. note::

    It is possible to load from yaml file on disk. Documentation to come.


Using a :py:class:`ParameterEstimation.Context` as a template
-------------------------------------------------------------

The most effective way to use the low level interface is to let the :py:class:`ParameterEstimation.Context`
 do most of the work and then retrieve the mostly configured config string and then make your
 desired ammendments.
