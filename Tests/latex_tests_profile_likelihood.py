import site

site.addsitedir('/home/b3053674/Documents/pycotools')
from pycotools import utils, tasks, viz, model
import os
from multiprocessing import Process
import unittest


class LatexTests(unittest.TestCase):
    def setUp(self):
        ## create model selection directory

        self.dire = os.path.join(os.path.dirname(__file__), 'profile_likelihood_latex_tests')
        if not os.path.isdir(self.dire):
            os.makedirs(self.dire)

        self.copasi_file = os.path.join(self.dire, 'negative_feedback.cps')

        with model.BuildAntimony(self.copasi_file) as loader:
            self.mod = loader.load(
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


        self.TC = self.simulate_data()

        self.MPE = self.do_parameter_estimation()

        self.pl = self.do_profile_likelihood()

        self.filename = os.path.join(self.dire, 'latex_test.pdf')

    def tearDown(self):
        import shutil
        # shutil.rmtree(self.dire)

    def simulate_data(self):
        """
        simulate some data from model1
        :return:
        """
        TC = tasks.TimeCourse(self.mod, end=100, steps=10, intervals=10)
        utils.format_timecourse_data(TC.report_name)
        return TC

    def do_parameter_estimation(self):
        MPE = tasks.MultiParameterEstimation(
            self.mod, self.TC.report_name, lower_bound=0.01, upper_bound=1,
            run_mode=True, pe_number=2, method='genetic_algorithm',
            number_of_generations=10, population_size=10
        )
        MPE.write_config_file()
        MPE.setup()
        MPE.run()
        return MPE

    def do_profile_likelihood(self):
        data = viz.Parse(self.MPE).data
        pl = tasks.ProfileLikelihood(model=self.mod, df=data, index=0, run=True,
                                     tolerance=1e1, iteration_limit=5)
        viz.PlotProfileLikelihood(pl, savefig=True, y=['RSS', 'kADeg'])
        return pl

    def test(self):
        """
        There is not a good test condition to see
        whether the latex file is without mistakes.
        To check this, comment out the tearDown
        method, manually check the file and then
        uncomment out again.
        :return:
        """
        L = utils.Latex(self.filename)
        L.profile_likelihood(self.pl.results_directory)
        # L.prepare_document(self.dire, subdirs=True)
        # self.assertTrue(os.path.isfile(self.filename))


if __name__ == '__main__':
    unittest.main()
















