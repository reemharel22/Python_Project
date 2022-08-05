import unittest
import equation
import diffusion_1d
import schrodinger_1d
import wave_1d
import numpy as np
from gui import Gui
from main import controller

class TestSchrodinger1d(unittest.TestCase):
    def setUp(self) -> None:
        self.schrodinger_test = schrodinger_1d.schrodinger1D(Gui.default_Schrodinger_dict['x_max'],
                                                             Gui.default_Schrodinger_dict['nx'],
                                                             Gui.default_Schrodinger_dict['t_max'],
                                                             Gui.default_Schrodinger_dict['nt'],
                                                             Gui.Initial_func[0],
                                                             Gui.default_init_condition['amplitude'],
                                                             Gui.default_init_condition['phase/sigma'],
                                                             Gui.default_init_condition['wave_vector/mu'],
                                                             Gui.potential_type_list[1])
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
        mechanical condition) by using the trapezoidal rule. Notice that we integrate over the vector x limits.
        The trapz method of numpy has some error, it means that the result is only an approximation (a good
        approximation) so the condition of identity up to 3 decimal places probably makes sense.
        """
        self.schrodinger_test.solve()
        first = np.trapz(y=self.schrodinger_test.solutions[-1], x=self.schrodinger_test.x)
        second = 1
        places = 3
        msg = 'Schrodinger is not normalized!'
        self.assertAlmostEqual(first, second, places, msg, delta=None)

    def test_solution(self):
        """
        This test checks that the solution is reasonable.
        """
        self.schrodinger_test.solve()
        self.assertTrue((self.schrodinger_test.solutions[0] == np.zeros([Gui.default_Schrodinger_dict['nt'] + 1,
                                                                         Gui.default_Schrodinger_dict['nx'] + 1]))
                        .all())
        self.assertTrue((self.schrodinger_test.solutions[-1] != np.zeros([Gui.default_Schrodinger_dict['nt'] + 1,
                                                                         Gui.default_Schrodinger_dict['nx'] + 1]))
                        .all())

class TestWave1d(unittest.TestCase):
    def setUp(self) -> None:
        self.wave_test = wave_1d.Wave1D(Gui.default_wave_dict['x_max'], Gui.default_wave_dict['nx'],
                                        Gui.default_wave_dict['t_max'], Gui.default_wave_dict['nt'],
                                        Gui.default_wave_dict['velocity'], Gui.Initial_func[1],
                                        Gui.default_init_condition['amplitude'],
                                        Gui.default_init_condition['phase/sigma'],
                                        Gui.default_init_condition['wave_vector/mu'])
        self.test_initialize()

    def test_initialize(self):
        """
        This test checks that the initialization is correct.
        """
        self.assertTrue((self.wave_test.solutions[0] == np.zeros([500 + 1, 100 + 1])).all())
        self.assertTrue((self.wave_test.x == np.linspace(-10, 10, 100 + 1)).all())
        self.assertTrue((self.wave_test.t == np.linspace(0, 30, 500 + 1)).all())

    def test_solution(self):
        """
        This test checks that the solution is reasonable.
        """
        self.wave_test.solve()
        self.assertTrue((self.wave_test.solutions[0] == np.zeros([Gui.default_wave_dict['nt'] + 1,
                                                                  Gui.default_wave_dict['nx'] + 1])).all())
        self.assertTrue((self.wave_test.solutions[-1] != np.zeros([Gui.default_wave_dict['nt'] + 1,
                                                                   Gui.default_wave_dict['nx'] + 1])).all())

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


