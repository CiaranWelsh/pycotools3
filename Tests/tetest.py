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
# mod.conservedMoietyAnalysis = False
# mod.steadyState()
#
# ss = dict(zip(
#     [i.replace('[', '').replace(']', '') for i in mod.steadyStateSelections],
#     mod.getSteadyStateValues(),
#     )
# )
# print(ss)



# mod.conservedMoietyAnalysis = True
# mod.steadyState()
#
# ss = dict(zip(
#     [i.replace('[', '').replace(']', '') for i in mod.steadyStateSelections],
#     mod.getSteadyStateValues(),
#     )
# )
# print(ss)


import sys
print(sys.platform)
print(sys.version)
print(te.__version__)

