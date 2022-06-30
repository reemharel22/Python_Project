import unittest
import equation
import diffusion_1d


class TestDiffusion(unittest.TestCase):

    def test_initialize(self):
        eq1 = diffusion_1d.Diffusion1D()
        self.assertIsNotNone(eq1.solutions)
        self.assertIsNotNone(eq1.x)
        self.assertIsNotNone(eq1.t)
    
