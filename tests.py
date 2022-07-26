import unittest
import equation
import diffusion_1d
import schrodinger_1d
import wave_1d
import numpy as np

class TestSchrodinger1d(unittest.TestCase):
    def setUp(self) -> None:
        self.schrodinger_test = schrodinger_1d.schrodinger1D(20, 400, 5, 400,
                                                             'Gaussian',10, 1, -5, 'Gaussian potential')
        self.test_initialize()
        self.test_normalization()

    def test_initialize(self):
        """
        This test checks that the initialization is correct.
        """
        self.assertTrue((self.schrodinger_test.solutions[0] == np.zeros([400 + 1, 400 + 1])).all())
        self.assertTrue((self.schrodinger_test.x == np.linspace(-20, 20, 400 + 1)).all())
        self.assertTrue((self.schrodinger_test.t == np.linspace(0, 5, 400 + 1)).all())

    def test_normalization(self):
        """
        This test checks if the probability amplitude is normalized at the end of the process (a critical Quantum
        mechanical condition) by using the trapezoidal rule. Notice that we integrate over the vector x. This means
        that the result is only an approximation (a good approximation). Also, the trapz method of numpy has some error
        so the condition of identity up to 3 decimal places probably makes sense.
        """
        self.schrodinger_test.solve()
        first = np.trapz(y=self.schrodinger_test.solutions[-1], x=self.schrodinger_test.x)
        second = 1
        places = 3
        msg = 'Schrodinger is normalized!'
        self.assertAlmostEqual(first, second, places, msg, delta=None)

class Test_wave_1d(unittest.TestCase):
    def setUp(self) -> None:
        self.wave_test = wave_1d.Wave1D(10, 100, 30, 500, 0.006, 'Sinc wave',
                                     10, 1, -5)
        self.test_initialize()

    def test_initialize(self):
        """
        This test checks that the initialization is correct.
        """
        self.assertTrue((self.wave_test.solutions[0] == np.zeros([500 + 1, 100 + 1])).all())
        self.assertTrue((self.wave_test.x == np.linspace(-10, 10, 100 + 1)).all())
        self.assertTrue((self.wave_test.t == np.linspace(0, 30, 500 + 1)).all())

class TestDiffusion(unittest.TestCase):
    def __init__(self):
        self.eq1 = diffusion_1d.Diffusion1D(1.5, 50, 3, 100, 0.01, 100.0, 0.01)
        self.test_initialize()

    def test_initialize(self):
        self.assertIsNotNone(self.eq1.solutions)
        self.assertIsNotNone(self.eq1.x)
        self.assertIsNotNone(self.eq1.t)
        print("Success!")

    def test_solution(self):
        self.eq1.solve()

class TestGui(unittest.TestCase):
    def setUp(self) -> None:
        self.test_show_special_entries_and_save_choice()
        self.test_click_solve_equation()
        self.test_get_from_initial_func_drop_down_list()

    def test_show_special_entries_and_save_choice(self):
        pass

    def test_click_solve_equation(self):
        pass

    def test_get_from_initial_func_drop_down_list(self):
        pass


