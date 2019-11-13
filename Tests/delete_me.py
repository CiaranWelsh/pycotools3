from pycotools3 import tasks, model, viz, misc
import os

ant = """
model *TestModel1()
    // Compartments and Species:
    compartment nuc, cyt;
    species A in nuc, B in nuc, C in nuc;
    
    // Assignment Rules:
    ThisIsAssignment := A2B + B2C;
    
    // Reactions:
    A2B_0: A => B; nuc*A2B*A;
    B2C_0: B -> C; nuc*(B2C*B - B2C_0_k2*C);
    C2A: C => A; nuc*C2A_k1*C;
    ADeg: A => ; nuc*ADeg_k1*A;
    
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
    
    // Display Names:
    A2B_0 is "A2B";
    B2C_0 is "B2C";
end"""
copasi_file = os.path.join(os.getcwd(), 'copasi_file.cps')
mod = model.loada(ant, copasi_file=copasi_file)

TC1 = tasks.TimeCourse(mod, end=1000, step_size=100,
                       intervals=10, report_name='report1.txt')

TC2 = tasks.TimeCourse(mod, end=1000, step_size=100,
                       intervals=10, report_name='report2.txt')

TC3 = tasks.TimeCourse(mod, end=1000, step_size=100,
                       intervals=10, report_name='report3.txt')

TC4 = tasks.TimeCourse(mod, end=1000, step_size=100,
                       intervals=10, report_name='report4.txt')

TC5 = tasks.TimeCourse(mod, end=1000, step_size=100,
                       intervals=10, report_name='report5.txt')

## add some noise
data1 = misc.add_noise(TC1.report_name)
data2 = misc.add_noise(TC2.report_name)
data3 = misc.add_noise(TC3.report_name)
data4 = misc.add_noise(TC4.report_name)
data5 = misc.add_noise(TC5.report_name)

## remove the data
os.remove(TC1.report_name)
os.remove(TC2.report_name)
os.remove(TC3.report_name)
os.remove(TC4.report_name)
os.remove(TC5.report_name)

## rewrite the data with noise
data1.to_csv(TC1.report_name, sep='\t')
data2.to_csv(TC2.report_name, sep='\t')
data3.to_csv(TC3.report_name, sep='\t')
data4.to_csv(TC4.report_name, sep='\t')
data5.to_csv(TC5.report_name, sep='\t')

misc.correct_copasi_timecourse_headers(TC1.report_name)
misc.correct_copasi_timecourse_headers(TC2.report_name)
misc.correct_copasi_timecourse_headers(TC3.report_name)
misc.correct_copasi_timecourse_headers(TC4.report_name)
misc.correct_copasi_timecourse_headers(TC5.report_name)

config = tasks.ParameterEstimation.Config(
    models={
        'model1': {
            'copasi_file': copasi_file,
        },
    },
    datasets={
        'experiments': {
            'report1': {
                'filename': TC1.report_name,
                'affected_models': 'all',
                'mappings': {
                    'Time': {
                        'model_object': 'Time',
                        'role': 'time'
                    },
                    'A': {
                        'model_object': 'A',
                        'role': 'dependent',
                    },
                }
            },
            'report2': {
                'filename': TC2.report_name,
                'separator': '\t'
            }
        },
        'validations': {
            'report3': {
                'filename': TC3.report_name,
                'affected_models': 'model1',

            }
        }
    },
    items={
        'fit_items': {

            'A': {
                'lower_bound': 15,
                'upper_bound': 35,
                'affected_experiments': 'report1',
                'affected_validation_experiments': 'report3',
                'affected_models': 'all',
                'start_value': 17.5
            },
            'B': {},
            'C': {}
        },
        'constraint_items': {
            'C': {
                'upper_bound': 26,
                'lower_bound': 16
            }
        },
    },
    settings={
        'method': 'genetic_algorithm_sr',
        'population_size': 38,
        'number_of_generations': 100,
        'copy_number': 1,
        'pe_number': 1,
        'weight_method': 'value_scaling',
        'validation_weight': 4,
        'validation_threshold': 8.5,
        'working_directory': os.path.dirname(__file__),
        'run_mode': False,
        'lower_bound': 0.05,
        'upper_bound': 36
    }
)
PE = tasks.ParameterEstimation(config)

print(PE)

items = dict(
    constraint_items=dict(
        C=dict(
            affected_experiments=['report1', 'report2'],
            affected_models=['model1'],
            affected_validation_experiments=['report3'],
            lower_bound=16,
            start_value=1.05,
            upper_bound=26
            )
    ),
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
    )
)
