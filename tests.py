import unittest
import diffusion_1d
import schrodinger_1d
import wave_1d
import numpy as np
from gui import Gui
import scipy.integrate as integrate
import default

class TestSchrodinger1d(unittest.TestCase):
    def setUp(self) -> None:
        self.schrodinger_test = schrodinger_1d.schrodinger1D(default.default_Schrodinger_dict['x_max'],
                                                             default.default_Schrodinger_dict['nx'],
                                                             default.default_Schrodinger_dict['t_max'],
                                                             default.default_Schrodinger_dict['nt'],
                                                             Gui.Initial_func[0],
                                                             default.default_init_condition['amplitude'],
                                                             default.default_init_condition['phase/sigma'],
                                                             default.default_init_condition['wave_vector/mu'],
                                                             Gui.potential_type_list[1])


    def test_initialize(self):
        """
        This test checks that the initialization is correct.
        """
        self.assertTrue((self.schrodinger_test.solutions[0] == np.zeros([default.default_Schrodinger_dict['nt'] + 1,
                                                                         default.default_Schrodinger_dict['nx'] + 1]))
                        .all())
        self.assertTrue((self.schrodinger_test.x == np.linspace(-default.default_Schrodinger_dict['x_max'],
                                                                default.default_Schrodinger_dict['x_max'],
                                                                default.default_Schrodinger_dict['nx'] + 1)).all())
        self.assertTrue((self.schrodinger_test.t == np.linspace(0, default.default_Schrodinger_dict['t_max'],
                                                                default.default_Schrodinger_dict['nt'] + 1)).all())
        print('Schrodinger initialization is correct!')

    def test_normalization_beginning(self):
        """
        This test checks if the probability amplitude is normalized at the beginning of the process (a critical Quantum
        mechanical condition).
        """
        self.schrodinger_test.solve()
        prob_dis = self.schrodinger_test.f0_squared
        sum_of_prob = self.schrodinger_test.A**2*integrate.quad(prob_dis, -default.default_Schrodinger_dict['x_max'],
                                                                default.default_Schrodinger_dict['x_max'])[0]
        second = 1
        places = 10
        msg = 'Schrodinger is not normalized at the beginning!'
        self.assertAlmostEqual(sum_of_prob, second, places, msg,  delta=None)
        print('Schrodinger normalization at the beginning is correct!')

    def test_normalization_end(self):
        """
        Using the trapezoidal rule, this test checks if the probability amplitude is normalized at the end of the process
        (a critical Quantum mechanical condition). Notice that we integrate over the vector x limits
        The trapz method of numpy has some error, which means that the result is only an approximation (a good
        approximation), so the condition of identity up to 1 decimal place probably makes sense.
        """
        self.schrodinger_test.solve()
        first = np.trapz(y=self.schrodinger_test.solutions[-1], x=self.schrodinger_test.x)
        second = 1
        places = 1
        msg = 'Schrodinger is not normalized!'
        self.assertAlmostEqual(first, second, places, msg, delta=None)
        print('Schrodinger normalization at the end is correct!')

    def test_solution(self):
        """
        This test checks that the solution is reasonable.
        """
        self.schrodinger_test.solve()
        self.assertTrue((self.schrodinger_test.solutions[0] == np.zeros([default.default_Schrodinger_dict['nt'] + 1,
                                                                         default.default_Schrodinger_dict['nx'] + 1]))
                        .all())
        self.assertTrue((self.schrodinger_test.solutions[-1] != np.zeros([default.default_Schrodinger_dict['nt'] + 1,
                                                                         default.default_Schrodinger_dict['nx'] + 1]))
                        .all())
        print('Schrodinger solution is reasonable!')

class TestWave1d(unittest.TestCase):
    def setUp(self) -> None:
        self.wave_test = wave_1d.Wave1D(default.default_wave_dict['x_max'], default.default_wave_dict['nx'],
                                        default.default_wave_dict['t_max'], default.default_wave_dict['nt'],
                                        default.default_wave_dict['velocity'], Gui.Initial_func[1],
                                        default.default_init_condition['amplitude'],
                                        default.default_init_condition['phase/sigma'],
                                        default.default_init_condition['wave_vector/mu'])

    def test_initialize(self):
        """
        This test checks that the initialization is correct.
        """
        self.assertTrue((self.wave_test.solutions[0] == np.zeros([default.default_wave_dict['nt'] + 1,
                                                                  default.default_wave_dict['nx'] + 1])).all())
        self.assertTrue((self.wave_test.x == np.linspace(-default.default_wave_dict['x_max'],
                                                         default.default_wave_dict['x_max'],
                                                         default.default_wave_dict['nx'] + 1)).all())
        self.assertTrue((self.wave_test.t == np.linspace(0, default.default_wave_dict['t_max'],
                                                         default.default_wave_dict['nt'] + 1)).all())
        print('Wave initialization is correct!')


    def test_solution(self):
        """
        This test checks that the solution is reasonable.
        """
        self.wave_test.solve()
        self.assertTrue((self.wave_test.solutions[0] == np.zeros([default.default_wave_dict['nt'] + 1,
                                                                  default.default_wave_dict['nx'] + 1])).all())
        self.assertTrue((self.wave_test.solutions[-1] != np.zeros([default.default_wave_dict['nt'] + 1,
                                                                   default.default_wave_dict['nx'] + 1])).all())
        print('Wave solution is reasonable!')

class TestDiffusion(unittest.TestCase):
    def setUp(self) -> None:
        self.eq1 = diffusion_1d.Diffusion1D(default.default_heat_dict['x_max'], default.default_heat_dict['nx'],
                                            default.default_heat_dict['t_max'], default.default_heat_dict['nt'],
                                            default.default_heat_dict['alpha'], default.default_heat_dict['b_val'],
                                            default.default_heat_dict['init'])

    def test_initialize(self):
        self.assertIsNotNone(self.eq1.solutions)
        self.assertIsNotNone(self.eq1.x)
        self.assertIsNotNone(self.eq1.t)
        print("Success!")

    def test_solution(self):
        self.eq1.solve()