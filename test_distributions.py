from unittest import TestCase
from distribution import PiecewiseFunction, PiecewiseUniform, expected_value
import numpy as np


class TestExpected_value(TestCase):
    def test_expected_value_simple(self):
        d = PiecewiseUniform([0,1], [1.0])
        f = PiecewiseFunction([-np.inf, np.inf], [lambda x: x])
        self.assertAlmostEqual(expected_value(d, f), 0.5, delta=1e-3)

    def test_expected_value_symetric(self):
        d = PiecewiseUniform([-10,10], [1.0])
        f = PiecewiseFunction([-np.inf, np.inf], [lambda x: x])
        self.assertAlmostEqual(expected_value(d, f), 0.0, delta=1e-3)

    def test_ev_gaussian(self):
        d = PiecewiseUniform([-100,100], [1.0])
        f = lambda x: np.exp(-(x**2) / 0.1)
        self.assertAlmostEqual(expected_value(d, f, resolution=0.1), 0.0, delta=1e-1)

    def test_piecewise_function(self):
        d = PiecewiseUniform([-100, 100], [1.0])
        f = PiecewiseFunction([-np.inf, 0, np.inf], [lambda x: 1, lambda x: 10])
        self.assertAlmostEqual(expected_value(d, f, resolution=0.1), 11/2, delta=1e-1)

    def test_piecewise_distribution(self):
        d = PiecewiseUniform([-100, 0, 100], [1.0, 10.0])
        f = lambda x: 1.0
        self.assertAlmostEqual(expected_value(d, f, resolution=0.1), 1.0, delta=1e-1)

    def test_piecewise_function_and_distribution(self):
        d = PiecewiseUniform([-10, 0, 10], [1.0, 9.0])
        f = PiecewiseFunction([-np.inf, 0, np.inf], [lambda x: 1, lambda x: 10])
        self.assertAlmostEqual(expected_value(d, f), (.9 * 10 + .1), delta=1e-3)