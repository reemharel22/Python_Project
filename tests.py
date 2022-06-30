import unittest
import equation
import diffusion_1d


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

