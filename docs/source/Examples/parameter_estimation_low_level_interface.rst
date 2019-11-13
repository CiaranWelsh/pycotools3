Parameter Estimation with the Low Level Interface
=================================================

Parameter estimation configuration in PyCoTools revolves around the :py:class:`ParameterEstimation.Config` object,
 which is merely a nested data storage class. When you use the :py:class:`ParameterEstimation.Context` object,
 you are using a high level interface to create a :py:class:`ParameterEstimation.Config` object. However, it is
 also possible to build it manually. It should be stressed however, that the Context method should be preferred
 when possible. The low level interface can be tedious but gives you more flexibility for more fine tuned
 parameter estimation configurations.

The :py:class:`ParameterEstimation.Config` Object

has four main sections:
    * models
    * datasets
    * items
    * settings

        Examples:
            >>> ## create a model
            >>> antimony_string = '''
            ...             model TestModel1()
            ...                 R1: A => B; k1*A;
            ...                 R2: B => A; k2*B
            ...                 A = 1
            ...                 B = 0
            ...                 k1 = 4;
            ...                 k2 = 9;
            ...             end
            ...             '''
            >>> copasi_filename = os.path.join(os.path.dirname(__file__), 'example_model.cps')
            >>> mod = moddel.loada(antimony_string, copasi_filename)
            >>> ## Simulate some data from the model and write to file
            >>> fname = os.path.join(os.path.dirname(__file__), 'timeseries.txt')
            >>> data = self.model.simulate(0, 10, 11)
            >>> data.to_csv(fname)
            >>>
            >>> ## create nested dict containing all the relevant arguments for your configuration
            >>> config_dict = dict(
            ...        models=dict(
            ...             ## model name is the users choice here
            ...            example1=dict(
            ...                copasi_file=copasi_filename
            ...            )
            ...        ),
            ...        datasets=dict(
            ...            experiments=dict(
            ...                 ## experiment names are the users choice
            ...                report1=dict(
            ...                    filename=self.TC1.report_name,
            ...                ),
            ...            ),
            ...            ## our validations entry is empty here
            ...            ## but if you have validation data this should
            ...            ## be the same as the experiments section
            ...            validations=dict(),
            ...        ),
            ...        items=dict(
            ...            fit_items=dict(
            ...                A=dict(
            ...                    affected_experiments='report1'
            ...                ),
            ...                B=dict(
            ...                    affected_validation_experiments=['report2']
            ...                ),
            ...            k1={},
            ...            k2={},
            ...            ),
            ...            constraint_items=dict(
            ...                k1=dict(
            ...                    lower_bound=1e-2,
            ...                    upper_bound=10
            ...                )
            ...            )
            ...        ),
            ...        settings=dict(
            ...            method='genetic_algorithm_sr',
            ...            population_size=2,
            ...            number_of_generations=2,
            ...            working_directory=os.path.dirname(__file__),
            ...            copy_number=4,
            ...            pe_number=2,
            ...            weight_method='value_scaling',
            ...            validation_weight=2.5,
            ...            validation_threshold=9,
            ...            randomize_start_values=True,
            ...            calculate_statistics=False,
            ...            create_parameter_sets=False
            ...        )
            ...    )
            >>> config = ParameterEstimation.Config(**config_dict)
        """