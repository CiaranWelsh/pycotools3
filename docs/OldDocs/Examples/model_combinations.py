import tellurium as te
from itertools import combinations
import os


def antimony_string(new_reactions):
    return """
        model *New_Model()
        
          // Compartments and Species:
          compartment nuc, cyt;
          species A in nuc, B in nuc, C in nuc;
        
          // Assignment Rules:
          ThisIsAssignment := A2B + B2C;
        
          // Reactions:
          A2B_0: A => B; nuc*A2B*A;
          B2C_0: B -> C; nuc*(B2C*B - B2C_0_k2*C);
          {}
          
          // Species initializations:
          A = 1
          B = 1
          C = 1
        
          // Compartment initializations:
          nuc = 1;
          cyt = 3;
        
          // Variable initializations:
          A2B = 4;
          B2C = 9;
          B2C_0_k2 = 0.1;
          C2A_k1 = 0.1;
          ADeg_k1 = 0.1;
        
          // Other declarations:
          var ThisIsAssignment;
          const nuc, cyt, A2B, B2C;
        
          // Unit definitions:
          unit volume = 1e-3 litre;
          unit substance = 1e-3 mole;

        end""".format(new_reactions)


def new_reaction1():
    return """
    C2A: C => A; nuc*C2A_k1*C;
    """.strip()

def new_reaction2():
    return """
    ADeg: A => ; nuc*ADeg_k1*A;
    """.strip()


def create_combinations(*args):
    n = len(args)
    comb_list = []
    for i in reversed(range(n+1)):
        comb_list += [j for j in combinations(range(n), i)]

    return enumerate(comb_list)

# sbml = te.antimonyToSBML(antimony_string())
# print(sbml)


if __name__ == '__main__':
    working_directory = os.path.dirname(__file__)

    model_combinations = create_combinations(new_reaction1(), new_reaction2())

    reactions_map = {
        0: new_reaction1(),
        1: new_reaction2()
    }

    fnames = []
    for model_id, topology in model_combinations:
        reactions_string = ''
        for reaction in topology:
            reactions_string += reactions_map[reaction] + '\n'

        model_string = antimony_string(reactions_string)
        sbml = te.antimonyToSBML(model_string)
        fname = os.path.join(working_directory, 'topology{}.sbml'.format(model_id))
        with open(fname, 'w') as f:
            f.write(sbml)
        print('file written to "{}"'.format(fname))
        fnames.append(fname)


    for f in fnames:
        assert os.path.isfile(f)



# Here's a simple example with a fake model I use for testing'
