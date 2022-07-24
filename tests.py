import unittest
import equation
import diffusion_1d
import schrodinger_1d
import wave_1d

class Test_schrodinger_1d(unittest.TestCase):
    def __init__(self):
        self.schrodinger_test = schrodinger_1d.schrodinger1D(20, 400, 5, 400,
                                                             'Gaussian',10, 1, -5, 'Gaussian potential')
        self.test_normalization()

    def test_normalization(self):
        pass

class Test_wave_1d(unittest.TestCase):
    def __init__(self):
        self.wave_test = wave_1d.Wave1D(10, 100, 30, 500, 0.006, 'Sinc wave',
                                     10, 1, -5)

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

