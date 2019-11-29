Running Time Series
====================

First generate a model

.. code-block:: python
    :linenos:

    import os
    from pycotools3 import model, tasks


    model_string = """
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

        A = 0;
        B = 0;
        C = 0;
        APlusB := A + B;
    end
    """

    # when running from a script you can use the special __file__ variable
    if os.path.isfile(__file__):
        copasi_file = os.path.join(os.path.dirname(__file__), 'copasi_file.cps')
    else:
        copasi_file = os.path.join(os.path.abspath(''), 'copasi_file.cps')

    # create a copasi model
    mod = model.loada(model_string, copasi_file)
    assert isinstance(mod, model.Model)

To run a time course simulation use:

>>> # from 0 to 100 by step size of 0.1
>>> mod.simulate(0, 100, 0.1, variables='m')
         A         B         C
Time
0     0.000000  0.000000  0.000000
1     0.095163  0.004837  0.000159
2     0.181269  0.018730  0.001208
3     0.259182  0.040810  0.003882
4     0.329680  0.070277  0.008766
5     0.393469  0.106377  0.016316
6     0.451188  0.148384  0.026874
7     0.503415  0.195577  0.040682
8     0.550671  0.247230  0.057889
9     0.593430  0.302596  0.078559
10    0.632121  0.360899  0.102679

The output is a `:py:class:`pandas.DataFrame` <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_.

.. note::

    The `variables` argument is `'m'` by default.

This gives you the time series of all the metabolites. If you also
want global quantities (or even local parameters - though they are constants anyway)
you can use `'g'` or `'l'`.

For instance:

Return time series for global variables

>>> mod.simulate(0, 100, 0.1, variables='g')
        APlusB  S   k1   k2   k3   k4   k5   k6
Time
0     0.000000  1  0.1  0.1  0.1  0.1  0.1  0.1
1     0.100000  1  0.1  0.1  0.1  0.1  0.1  0.1
2     0.199999  1  0.1  0.1  0.1  0.1  0.1  0.1
3     0.299992  1  0.1  0.1  0.1  0.1  0.1  0.1
4     0.399957  1  0.1  0.1  0.1  0.1  0.1  0.1
5     0.499847  1  0.1  0.1  0.1  0.1  0.1  0.1
6     0.599572  1  0.1  0.1  0.1  0.1  0.1  0.1
7     0.698992  1  0.1  0.1  0.1  0.1  0.1  0.1
8     0.797901  1  0.1  0.1  0.1  0.1  0.1  0.1
9     0.896026  1  0.1  0.1  0.1  0.1  0.1  0.1
10    0.993020  1  0.1  0.1  0.1  0.1  0.1  0.1


Return time series for metabolites and global variables

>>> mod.simulate(0, 100, 0.1, variables='mg')


             A    APlusB         B         C  S ...    k2   k3   k4   k5   k6
Time                                            ...
0     0.000000  0.000000  0.000000  0.000000  1 ...   0.1  0.1  0.1  0.1  0.1
1     0.095163  0.100000  0.004837  0.000159  1 ...   0.1  0.1  0.1  0.1  0.1
2     0.181269  0.199999  0.018730  0.001208  1 ...   0.1  0.1  0.1  0.1  0.1
3     0.259182  0.299992  0.040810  0.003882  1 ...   0.1  0.1  0.1  0.1  0.1
4     0.329680  0.399957  0.070277  0.008766  1 ...   0.1  0.1  0.1  0.1  0.1
5     0.393469  0.499847  0.106377  0.016316  1 ...   0.1  0.1  0.1  0.1  0.1
6     0.451188  0.599572  0.148384  0.026874  1 ...   0.1  0.1  0.1  0.1  0.1
7     0.503415  0.698992  0.195577  0.040682  1 ...   0.1  0.1  0.1  0.1  0.1
8     0.550671  0.797901  0.247230  0.057889  1 ...   0.1  0.1  0.1  0.1  0.1
9     0.593430  0.896026  0.302596  0.078559  1 ...   0.1  0.1  0.1  0.1  0.1
10    0.632121  0.993020  0.360899  0.102679  1 ...   0.1  0.1  0.1  0.1  0.1

Return time series for metabolites, global variables
and local parameters (though remember there are none in this current topology)

>>> mod.simulate(0, 100, 0.1, variables='mgl')
         A         B        C
Time
0     1.000000  1.000000  1.00000
1     0.082146  0.072788  2.81673
2     0.069317  0.062367  2.83276
3     0.068980  0.062080  2.82647
4     0.068817  0.061934  2.81989
5     0.068657  0.061789  2.81332
6     0.068497  0.061645  2.80677
7     0.068337  0.061502  2.80023
8     0.068178  0.061358  2.79371
9     0.068019  0.061215  2.78720
10    0.067861  0.061073  2.78071


Alternative simulation methods
------------------------------

Copasi supports several model simulation algorithms. PyCoTools
supports most of these, including:

    * deterministic (the default)
    * direct
    * gibson_bruck
    * tau_leap
    * adaptive_tau_leap
    * hybrid_runge_kutta
    * hybrid_lsoda
    * hybrid_rk45

To use one of these alternative methods, ensure your model
is adequate for the simulation you are performing (i.e. no reversible
reactions and low enough copy numbers for stochastic simulation)
and use the `method` argument to :py:meth:`pycotools3.model.Model.simulate`

.. note::

    The example model above is not suitable to stochastic simulation

.. code-block::

    >>> mod.simulate(0, 100, 0.1, variables='m', method='direct')


Plotting
========

If you have used :py:meth:`pycotools3.model.Model.simulate()` then you will
have a :py:class:`pandas.DataFrame`. In this case, you might as well use
either `pandas` plotting facilities or `matplotlib` with `seaborn`. You could also
use `plotly`, `plotly` with `dash` or `bokeh`.

There are also some inherent plotting facilities in pycotools.

With PyCoTools
--------------

Visualisation in pycotools works by passing a plotter class an instance of a task.
In this case we need a handle to the TimeCourse task.

>>> from pycotools3 import tasks, viz
>>> tc = tasks.TimeCourse(model=mod, start=0, end=10, step_size=1)
>>> viz.PlotTimeCourse(tc, savefig=True, show=True)

Since the inherent plotting module is basically just a wrapper around
matplotlib and seaborn, it might be a good idea to use these tools instead.

Here's an example.

With matplotlib
---------------

Here's a very simple example using `matplotlib <https://matplotlib.org/3.1.1/users/index.html>`_.

.. code-block::
    :linenos:

    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_context('talk')

    df = mod.simulate(0, 100, 0.1, variables='m')

    for i in df:
        if i != 'Time:
            fig = plt.plot(df['Time'], df[i], label=i)
            seaborn.despine(fig=fig, top=True, right=True)
            plt.legend()
            plt.xlabel('Time')
            plt.ylabel('concentration')


































