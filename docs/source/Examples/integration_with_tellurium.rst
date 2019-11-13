Integration with Tellurium
==========================

`Tellurium <https://tellurium.readthedocs.io/en/latest/>`_ is a Python package built on top of
 `libRoadRunner <https://sys-bio.github.io/roadrunner/python_docs/index.html>`_, a
 C++ package for simulation and analysis of models in
 systems biology. `Antimony <http://antimony.sourceforge.net/>`_ is a
 model definition language for SBML models that was written
 by the authors of `Tellurium` and `libRoadRunner`.

Since PyCoTools has adopted `Antimony`, the same model can
be simulated and analysed with both COPASI and tellurium.

Here's a short example of how using the tellurium back end.

.. code-block:: python

    import tellurium as te

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

    mod = te.loada(antimony_string)

    # simulate a time series with 11 time points between 0 and 10
    timeseries_data = mod.simulate(0, 10, 11)

    # compute the steady state
    mod.conservedMoietyAnalysis = True
    mod.setSteadyStateSolver('nleq')
    mod.steadyState()
    mod.steadyStateSelections = ['A', 'B', 'C']
    print(dict(zip(*mod.steadyStateSelections,
                    mod.getSteadyStateValues()))
