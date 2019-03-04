import unittest
import os

class TestCopasiPresent(unittest.TestCase):
    """
    Tests that COPASI can be downloaded from my repo.



    """
    def setUp(self):
        pass

    def test(self):
        import pycotools3
        copasi_directory = os.path.join(
            os.path.dirname(pycotools3.__file__), 'COPASI'
        )
        self.assertTrue(os.path.isdir(copasi_directory))
        print(copasi_directory)













if __name__ == '__main__':
    unittest.main()