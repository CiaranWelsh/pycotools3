import site
site.addsitedir('/home/b3053674/Documents/pycotools')
from pycotools import model, viz, tasks, Models
import glob, os

print(Models)

zi_model_dire = r'/home/b3053674/Documents/Models/2018/01_Jan/ZiModel'

zi_path = os.path.join(zi_model_dire, 'ZiModelRemade.cps')

if os.path.isfile(zi_path):
    os.remove(zi_path)

##some parameters
v_T1R = 0.0103
v_T2R = 0.02869
ki_EE = 0.33
kr_EE = 0.033
ki_cave = 0.33
kr_cave = 0.03742
kcd = 0.005
k_LRC = 2197
klid = 0.02609
kdeg_T1R_EE = 0.005
kdeg_T2R_EE = 0.025
kimp_Smad3c = 0.16
kexp_Smad3n = 1
kimp_Smad4c = 0.08
kexp_Smad4n = 0.5
k_smads_complex_c = 6.85e-05
kimp_smads_complex_c = 0.16
kdiss_smads_complex_n = 0.1174
vol_cyt = 0.0035
vol_nuc = 0.00105

with model.Build(zi_path) as m:
    ## set model name and units
    m.name = 'Zi2011'
#     m.time_unit = 's'
#     m.quantity_unit = 'nmol'
#     m.volume_unit = 'l'

    ## add compartments
    m.add('compartment', name='Medium', initial_value=1)
    m.add('compartment', name='Cytoplasm', initial_value=vol_cyt)
    m.add('compartment', name='Nucleus', initial_value=vol_nuc)

    ## add metabolites
    m.add('metabolite', name='Smad3c', concentration=492.61, compartment='Cytoplasm')
    m.add('metabolite', name='Smad3n', concentration=236.45, compartment='Nucleus')
    m.add('metabolite', name='Smad4c', concentration=1149.4, compartment='Cytoplasm')
    m.add('metabolite', name='Smad4n', concentration=551.72, compartment='Nucleus')
    #
    m.add('metabolite', name='T1R_Surf', concentration=0.237, compartment='Cytoplasm')
    m.add('metabolite', name='T1R_Cave', concentration=2.092, compartment='Cytoplasm')
    m.add('metabolite', name='T1R_EE', concentration=2.06, compartment='Cytoplasm')

    m.add('metabolite', name='T2R_Surf', concentration=0.202, compartment='Cytoplasm')
    m.add('metabolite', name='T2R_Cave', concentration=1.778, compartment='Cytoplasm')
    m.add('metabolite', name='T2R_EE', concentration=1.148, compartment='Cytoplasm')

    m.add('metabolite', name='LRC_Surf', concentration=0, compartment='Cytoplasm')
    m.add('metabolite', name='LRC_Cave', concentration=0, compartment='Cytoplasm')
    m.add('metabolite', name='LRC_EE', concentration=0, compartment='Cytoplasm')

    m.add('metabolite', name='Smads_Complex_c', concentration=0, compartment='Cytoplasm')
    m.add('metabolite', name='Smads_Complex_n', concentration=0, compartment='Nucleus')
    m.add('metabolite', name='TGF_beta', concentration=0.08, compartment='Medium')

    #add reactions
    m.add('reaction', name='R1_Smad2_import', expression='Smad3c -> Smad3n', rate_law='k*Smad3c',
          parameter_values={'k': kimp_Smad3c*vol_cyt})

    m.add('reaction', name='R2_Smad2_export', expression='Smad3n -> Smad3c', rate_law='k*Smad3n',
          parameter_values={'k': kexp_Smad3n*vol_nuc})

    m.add('reaction', name='R3_Smad4_import', expression='Smad4c -> Smad4n', rate_law='k*Smad4c',
          parameter_values={'k': kimp_Smad4c*vol_cyt})

    m.add('reaction', name='R4_Smad4_export', expression='Smad4n -> Smad4c', rate_law='k*Smad4n',
          parameter_values={'k': kexp_Smad4n*vol_nuc})

    m.add('reaction', name='R5_T1R_production', expression=' -> T1R_Surf', rate_law='v',
          parameter_values={'v': v_T1R})

    m.add('reaction', name='R6_T1R_Cave_formation', expression='T1R_Surf -> T1R_Cave', rate_law='k*T1R_Surf',
          parameter_values={'k': ki_cave})

    m.add('reaction', name='R7_T1R_Cave_recycling', expression='T1R_Cave -> T1R_Surf', rate_law='k*T1R_Cave',
          parameter_values={'k': kr_cave})

    m.add('reaction', name='R8_T1R_EE_formation', expression='T1R_Surf -> T1R_EE', rate_law='k*T1R_Surf',
          parameter_values={'k': ki_EE})

    m.add('reaction', name='R9_T1R_EE_recycling', expression='T1R_EE -> T1R_Surf', rate_law='k*T1R_EE',
          parameter_values={'k': kr_EE})

    m.add('reaction', name='R10_T1R_EE_degradation', expression='T1R_EE -> ', rate_law='k*T1R_EE',
          parameter_values={'k': kdeg_T1R_EE})

    m.add('reaction', name='R11_T2R_production', expression=' -> T2R_Surf', rate_law='1*v',
          parameter_values={'v': v_T2R})

    m.add('reaction', name='R12_T2R_Cave_formation', expression='T2R_Surf -> T2R_Cave', rate_law='k*T2R_Surf',
          parameter_values={'k': ki_cave})

    m.add('reaction', name='R13_T2R_Cave_recycling', expression='T2R_Cave -> T2R_Surf', rate_law='k*T2R_Cave',
          parameter_values={'k': kr_cave})

    m.add('reaction', name='R14_T2R_EE_formation', expression='T2R_Surf -> T2R_EE', rate_law='k*T2R_Surf',
          parameter_values={'k': ki_EE})

    m.add('reaction', name='R15_T2R_EE_recycling', expression='T2R_EE -> T2R_Surf + TGF_beta', rate_law='k*T2R_EE',
          parameter_values={'k': kr_EE*vol_cyt})

    m.add('reaction', name='R16_T2R_EE_degradation', expression='T2R_EE -> ', rate_law='k*T2R_EE',
          parameter_values={'k': kdeg_T2R_EE})

    m.add('reaction', name='R17_LRC_formation', expression='TGF_beta + T2R_Surf + T1R_Surf -> LRC_Surf',
          rate_law='k*TGF_beta*T2R_Surf*T1R_Surf',
          parameter_values={'k': k_LRC*vol_cyt})

    m.add('reaction', name='R18_LRC_Cave_formation', expression='LRC_Surf -> LRC_Cave', rate_law='k*LRC_Surf',
          parameter_values={'k': ki_cave})

    m.add('reaction', name='R19_LRC_Cave_recycling', expression='LRC_Cave -> T1R_Surf + TGF_beta + T2R_Surf',
          rate_law='k*LRC_Cave',
          parameter_values={'k': kr_cave*vol_cyt})

    m.add('reaction', name='R20_LRC_EE_formation', expression='LRC_Surf -> LRC_EE', rate_law='k*LRC_Surf',
          parameter_values={'k': ki_EE})

    m.add('reaction', name='R21_LRC_EE_recycling', expression='LRC_EE -> T1R_Surf + T2R_Surf + TGF_beta',
          rate_law='k*LRC_EE',
          parameter_values={'k': kr_EE*vol_cyt})

    m.add('reaction', name='R22_LRC_EE_degradation', expression='LRC_EE -> ', rate_law='k*LRC_EE',
          parameter_values={'k': kcd})

    m.add('reaction', name='R23_Smads_Complex_formation', expression='Smad3c + Smad4c -> Smads_Complex_c;  LRC_EE',
          rate_law='k*Smad3c*Smad4c',
          parameter_values={'k': k_smads_complex_c})

    m.add('reaction', name='R24_Smads_Complex_import', expression='Smads_Complex_c -> Smads_Complex_n',
          rate_law='k*Smads_Complex_c',
          parameter_values={'k': kimp_smads_complex_c*vol_cyt})

    m.add('reaction', name='R25_Smads_Complex_Dissociation', expression='Smads_Complex_n -> Smad4n + Smad3n',
          rate_law='k*Smads_Complex_n',
          parameter_values={'k': kdiss_smads_complex_n})

    m.add('reaction', name='R26_LRC_Cave_degradation', expression='LRC_Cave -> ;  Smads_Complex_n',
          rate_law='k*LRC_Cave*Smads_Complex_n',
          parameter_values={'k': klid})

m = model.Model(zi_path)
m.open()

