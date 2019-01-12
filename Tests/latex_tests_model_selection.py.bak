from pycotools import utils, tasks, viz, model
import os
from multiprocessing import Process
import unittest

raise NotImplemented

class LatexTests(unittest.TestCase):
    def setUp(self):
        ## create model selection directory

        self.dire = os.path.join(os.path.dirname(__file__), 'model_selection')
        if not os.path.isdir(self.dire):
            os.makedirs(self.dire)

        self.copasi_file1 = os.path.join(self.dire, 'negative_feedback.cps')
        self.copasi_file2 = os.path.join(self.dire, 'positive_feedback.cps')
        self.copasi_file3 = os.path.join(self.dire, 'feedforward.cps')

        with model.BuildAntimony(self.copasi_file1) as loader:
            self.mod1 = loader.load(
                """
                model model1
                    compartment cell = 1.0
                    var A in cell
                    var B in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kBProd = 0.3
                    kBDeg = 0.4
                    A = 0
                    B = 0

                    AProd: => A; cell*vAProd
                    ADeg: A =>; cell*kADeg*A*B
                    BProd: => B; cell*kBProd*A
                    BDeg: B => ; cell*kBDeg*B
                end
                """
            )

        with model.BuildAntimony(self.copasi_file2) as loader:
            self.mod2 = loader.load(
                """
                model model2
                    compartment cell = 1.0
                    var A in cell
                    var B in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kBProd = 0.3
                    kBDeg = 0.4
                    vBasalAProd = 0.001
                    A = 0
                    B = 0

                    AProd: => A; cell*vAProd*B+vBasalAProd
                    ADeg: A =>; cell*kADeg*A
                    BProd: => B; cell*kBProd*A
                    BDeg: B => ; cell*kBDeg*B
                end
                """
            )

        with model.BuildAntimony(self.copasi_file3) as loader:
            self.mod3 = loader.load(
                """
                model model3
                    compartment cell = 1.0
                    var A in cell
                    var B in cell
                    var C in cell

                    vAProd = 0.1
                    kADeg = 0.2
                    kBProd = 0.3
                    kBDeg = 0.4
                    kCDeg = 0.5
                    kCProd = 0.6
                    A = 0
                    B = 0
                    C = 0

                    AProd: => A; cell*vAProd
                    ADeg: A =>; cell*kADeg*A
                    BProd: => B; cell*kBProd*A
                    BDeg: B => ; cell*kBDeg*B
                    CProd: => C; cell*kCProd*A*B
                    CDeg: C => ; cell*kCDeg*C
                end
                """
            )

        self.TC = self.simulate_data()

        self.MMF = self.configure_model_selection()
        
        self.plot_data()

        self.filename = os.path.join(self.dire, 'latex_test.pdf')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.MMF.project_dir)
        
    def simulate_data(self):
        """
        simulate some data from model1
        :return:
        """
        TC = tasks.TimeCourse(self.mod1, end=100, steps=10, intervals=10)
        utils.format_timecourse_data(TC.report_name)
        return TC

    def configure_model_selection(self):
        MMF = tasks.MultiModelFit(self.dire,
                                  method='genetic_algorithm',
                                  population_size=5,
                                  number_of_generations=20,
                                  copy_number=1,
                                  pe_number=1,
                                  run_mode=True,
                                  overwrite_config_file=True,
                                  lower_bound=1e-2,
                                  upper_bound=1e2)
        MMF.write_config_file()
        MMF.setup()
        MMF.run()
        return MMF

    def plot_data(self):
        print('plotting data')
        P = Process(target=viz.ModelSelection, args=(self.MMF,),
                    kwargs={'savefig': True})
        P.start()
        P.join()
        for MPE in self.MMF:
            for j in [viz.Boxplots, viz.LikelihoodRanks]:
                P = Process(target=j, args=(MPE,),
                            kwargs={'savefig': True})
                P.start()
                P.join()

    def test(self):
        L = utils.Latex(self.filename)
        model_selection_graph_dire = os.path.join(self.dire, 'ModelSelectionGraphs')
        assert os.path.isdir(model_selection_graph_dire)
        L.prepare_document(self.dire, subdirs=True)
        self.assertTrue(os.path.isfile(self.filename))











if __name__ == '__main__':
    unittest.main()
















