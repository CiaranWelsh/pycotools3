Parameter estimation with multiple models
=========================================
This is an example of how to configure a parameter estimation for multiple COPASI models using pycotools. We first create two similar but different toy models for demonstration, then simulate some experimental data from one of them and and fit it back to both models.

.. code-block:: python

    import os, glob
    import pandas, numpy
    import matplotlib.pyplot as plt
    import seaborn
    from pycotools3 import model, tasks, viz

    seaborn.set_context(context='talk')

    ## Choose a directory for our model and analysis
    working_directory = os.path.dirname(__file__)

    model1_string = """
    model model1()

        R1:   => A ; k1*S;
        R2: A =>   ; k2*A;
        R3:   => B ; k3*A;
        R4: B =>   ; k4*B*C; //feedback term
        R5:   => C ; k5*B;
        R6: C =>   ; k6*C;

        S = 1;
        k1 = 0.1;
        k2 = 0.1;
        k3 = 0.1;
        k4 = 0.1;
        k5 = 0.1;
        k6 = 0.1;
    end
    """

    model2_string = """
    model model2()
        R1:   => A ; k1*S;
        R2: A =>   ; k2*A*C; //feedback term
        R3:   => B ; k3*A;
        R4: B =>   ; k4*B;
        R5:   => C ; k5*B;
        R6: C =>   ; k6*C;

        S = 1;
        k1 = 0.1;
        k2 = 0.1;
        k3 = 0.1;
        k4 = 0.1;
        k5 = 0.1;
        k6 = 0.1;
    end
    """
    copasi_file1 = os.path.join(working_directory, 'model1.cps')
    copasi_file2 = os.path.join(working_directory, 'model2.cps')

    antimony_strings = [model1_string, model2_string]
    copasi_files = [copasi_file1, copasi_file2]

    model_list = []
    for i in range(len(copasi_files)):
        with model.BuildAntimony(copasi_files[i]) as builder:
            model_list.append(builder.load(antimony_strings[i]))

    ## simulate some data, returns a pandas.DataFrame
    data = model_list[0].simulate(0, 20, 1)

    ## write data to file
    experiment_filename = os.path.join(working_directory, 'data_from_model1.txt')
    data.to_csv(experiment_filename)

    with tasks.ParameterEstimation.Context(model_list, experiment_filename, context='s', parameters='g') as context:
        context.set('separator', ',')
        context.set('run_mode', True)
        context.set('randomize_start_values', True)
        context.set('method', 'genetic_algorithm')
        context.set('population_size', 25)
        context.set('lower_bound', 1e-1)
        context.set('upper_bound', 1e1)

        config = context.get_config()

    pe = tasks.ParameterEstimation(config)

    data = viz.Parse(pe).data

    print(data)

