import unittest
from pycotools3.lhs import lhs

class LHSTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_classic_dim(self):
        s = lhs(2, 10)
        expected = [10, 2]
        self.assertListEqual(expected, list(s.shape))

    def test_classic_boundary_between_0_and_1(self):
        s = lhs(2, 10)
        actual = True
        for i in s:
            for j in i:
                if j < 0 or j > 1:
                    actual = False
        self.assertTrue(actual)

    def test_classic_boundary_between_0_01_and_100(self):
        s = lhs(2, 10, lower_bound=0.01, upper_bound=100)
        actual = True
        for i in s:
            for j in i:
                if j < 0.01 or j > 100:
                    actual = False
        self.assertTrue(actual)

    def test_centered_boundary_between_0_and_1(self):
        s = lhs(2, 10, 'c')
        actual = True
        for i in s:
            for j in i:
                if j < 0 or j > 1:
                    actual = False
        self.assertTrue(actual)

    def test_centered_boundary_between_0_01_and_100(self):
        s = lhs(2, 10, 'c', lower_bound=0.01, upper_bound=100)
        actual = True
        for i in s:
            for j in i:
                if j < 0.01 or j > 100:
                    actual = False
        self.assertTrue(actual)


    def test_maxmin_boundary_between_0_and_1(self):
        s = lhs(2, 10, 'm')
        actual = True
        for i in s:
            for j in i:
                if j < 0 or j > 1:
                    actual = False
        self.assertTrue(actual)

    def test_maxmin_boundary_between_0_01_and_100(self):
        s = lhs(2, 10, 'm', lower_bound=0.01, upper_bound=100)
        actual = True
        for i in s:
            for j in i:
                if j < 0.01 or j > 100:
                    actual = False
        self.assertTrue(actual)
        
    def test_correlate_boundary_between_0_and_1(self):
        s = lhs(2, 10, 'c')
        actual = True
        for i in s:
            for j in i:
                if j < 0 or j > 1:
                    actual = False
        self.assertTrue(actual)

    def test_correlate_boundary_between_0_01_and_100(self):
        s = lhs(2, 10, 'c', lower_bound=0.01, upper_bound=100)
        actual = True
        for i in s:
            for j in i:
                if j < 0.01 or j > 100:
                    actual = False
        self.assertTrue(actual)





if __name__ == '__main__':
    unittest.main()



























