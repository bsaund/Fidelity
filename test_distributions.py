from unittest import TestCase
from distribution import PiecewiseFunction, PiecewiseUniform, numerical_expected_value, \
    PiecewiseDefiniteIntegralFunction, analytic_expected_value
import numpy as np


class TestNumericalExpectedValue(TestCase):
    def test_expected_value_simple(self):
        d = PiecewiseUniform([0,1], [1.0])
        f = PiecewiseFunction([-np.inf, np.inf], [lambda x: x])
        self.assertAlmostEqual(numerical_expected_value(d, f), 0.5, delta=1e-3)

    def test_expected_value_symetric(self):
        d = PiecewiseUniform([-10,10], [1.0])
        f = PiecewiseFunction([-np.inf, np.inf], [lambda x: x])
        self.assertAlmostEqual(numerical_expected_value(d, f), 0.0, delta=1e-3)

    def test_ev_gaussian(self):
        d = PiecewiseUniform([-100,100], [1.0])
        f = lambda x: np.exp(-(x**2) / 0.1)
        self.assertAlmostEqual(numerical_expected_value(d, f, resolution=0.1), 0.0, delta=1e-1)

    def test_piecewise_function(self):
        d = PiecewiseUniform([-100, 100], [1.0])
        f = PiecewiseFunction([-np.inf, 0, np.inf], [lambda x: 1, lambda x: 10])
        self.assertAlmostEqual(numerical_expected_value(d, f, resolution=0.1), 11 / 2, delta=1e-1)

    def test_piecewise_distribution(self):
        d = PiecewiseUniform([-100, 0, 100], [1.0, 10.0])
        f = lambda x: 1.0
        self.assertAlmostEqual(numerical_expected_value(d, f, resolution=0.1), 1.0, delta=1e-1)

    def test_piecewise_function_and_distribution(self):
        d = PiecewiseUniform([-10, 0, 10], [1.0, 9.0])
        f = PiecewiseFunction([-np.inf, 0, np.inf], [lambda x: 1, lambda x: 10])
        self.assertAlmostEqual(numerical_expected_value(d, f), (.9 * 10 + .1), delta=1e-3)


class TestAnalyticExpectedValue(TestCase):
    def test_analystic_ev_with_single_regions(self):
        d = PiecewiseUniform([0,1], [1.0])
        f = PiecewiseDefiniteIntegralFunction([0, 1], [lambda x: x])
        self.assertEqual(analytic_expected_value(d, f), 1.0)
