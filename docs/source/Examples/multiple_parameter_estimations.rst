Multiple Parameter Estimations
==============================
Configuring multiple parameter estimations is easy with COPASI because you can configure a parameter estimation task, configure a scan repeat item with the `subtask` set to `parameter estimation` and hit run. This is what pycotools does under the hood to configure a parameter estimation, even if the desired number of parameter estimations is 1.

Moreover, pycotools additionally supports the running of multiple copies of your copasi file in separate processes, or on a cluster.

.. highlight:: python

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

     copasi_file = os.path.join(working_directory, 'negative_fb.cps')
     mod = model.loada(antimony_string, copasi_file )

     data_fname = os.path.join(working_directory, 'timecourse.txt')
     mod.simulate(0, 10, 1, report_name=data_fname)

     assert os.path.isfile(data_fname)

Increasing Parameter Estimation Throughput
--------------------------------------------
The `pe_number` argument specifies the number that gets entered into the copasi scan repeat item while the `copy_number` argument specifies the number of identical model copies to make.

.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, data_fname, context='s', parameters='g') as context:
        context.set('copy_number', 2)
        context.set('pe_number', 2)
        context.set('randomize_start_values', True)
        context.set('run_mode', True)
        config = context.get_config()

    pe = tasks.ParameterEstimation(config)
    data = viz.Parse(pe)


.. note::

   The `copy_number` argument here doesn't really do anything useful because `run_mode=True`. This tells pycotools to run the parameter estimations in series (i.e. back to back) and therefore the `copy_number` argument here does nothing.


However, it is also possible to give `run_mode='parallel'` and in this case, each of the model copies will be run simultaneously.

.. code-block:: python

    with tasks.ParameterEstimation.Context(mod, data_fname, context='s', parameters='g') as context:
        context.set('copy_number', 2)
        context.set('pe_number', 2)
        context.set('randomize_start_values', True)
        context.set('run_mode', 'parallel)
        config = context.get_config()

    pe = tasks.ParameterEstimation(config)
    data = viz.Parse(pe)

.. warning::

   Users should not use `run_mode='parallel'` in combination with a high `copy_number` as it will slow your system.

Your system has a limited amount of resources and can only handle a number of parameter estimations being run at once. For this reason, be careful when choosing the `copy_number`. For reference, my computer can run approximately 8 parameter estimations in different processes before slowing.

If you have access to a cluster running either SunGrid Engine or Slurm then each of the `copy_number` models will be submitted as separate jobs. To do this set `run_mode='slurm` or `run_mode='sge'` (see :py:class:`tasks.Run`).

.. warning::

   The cluster functions are fully operational on the Newcastle University clusters but untested on other clusters. If you run into trouble, contact me for help.

It is easy to support other cluster systems by adding a method to :py:class:`tasks.Run` using :py:meth:`tasks.Run.run_sge` and :py:meth:`tasks.Run.run_slurm` as examples.













