from unittest import TestCase
from distribution import PiecewiseDefiniteIntegralFunction
import numpy as np

class TestPiecewiseDefiniteIntegralFunction(TestCase):
    def test_evaluate_constant_function_with_one_region(self):
        f =PiecewiseDefiniteIntegralFunction([-np.inf, np.inf], [lambda x: x])
        self.assertEqual(f.evaluate(-10, 5), 15)
        self.assertEqual(f.evaluate(14, 14), 0)
        self.assertEqual(f.evaluate(0,1), 1)

    def test_evaluate_const_function_with_two_regions(self):
        f = PiecewiseDefiniteIntegralFunction([-np.inf, 5, np.inf], [lambda x: x, lambda x: 2*x])
        self.assertEqual(f.evaluate(-10, 0), 10)
        self.assertEqual(f.evaluate(10, 15), 10)
        self.assertEqual(f.evaluate(-10, 10), 25)
        self.assertEqual(f.evaluate(10, 10), 0)
        self.assertEqual(f.evaluate(5, 5), 0)
        self.assertEqual(f.evaluate(5, 5.5), 1.0)
        self.assertEqual(f.evaluate(4.5, 5), 0.5)

    def test_evaluate_const_function_with_three_regions(self):
        f = PiecewiseDefiniteIntegralFunction([-10, 0, 5, 10], [lambda x: x, lambda x: 2*x, lambda x: x**2])
        self.assertEqual(f.evaluate(-10, 0), 10)
        self.assertEqual(f.evaluate(-10, 5), 20)
        self.assertEqual(f.evaluate(5, 10), 75)
        self.assertEqual(f.evaluate(-10, 10), 95)


    def test_evaluate_checks(self):
        f = PiecewiseDefiniteIntegralFunction([10, 15, 25], [lambda x: x, lambda x: 2 * x])
        with self.assertRaises(Exception) as context:
            f.evaluate(9,11)
        with self.assertRaises(Exception) as context:
            f.evaluate(14, 26)
        with self.assertRaises(Exception) as context:
            f.evaluate(9, 26)
        with self.assertRaises(Exception) as context:
            f.evaluate(-10, -9)
        with self.assertRaises(Exception) as context:
            f.evaluate(26, 27)
        with self.assertRaises(Exception) as context:
            f.evaluate(17, 13)
        self.assertEqual(f.evaluate(11,12), 1)