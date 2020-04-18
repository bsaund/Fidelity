from unittest import TestCase
from distribution import PiecewiseUniform


def get_distribution_sum(d):
    s = 0.0
    for l, u, p in zip(d.bounds, d.bounds[1:], d.probability_densities):
        s += (u - l) * p
    return s


class TestPiecewiseUniform(TestCase):
    def test_normalize(self):
        d = PiecewiseUniform([0,.5,1.0], [.3, .7])
        self.assertAlmostEqual(1.0, get_distribution_sum(d), delta = 1e-5)

        d = PiecewiseUniform([0,.5,1.0], [3, 7])
        self.assertAlmostEqual(1.0, get_distribution_sum(d), delta = 1e-5)

        d = PiecewiseUniform([0,13, 84, 104], [3, 7, 2])
        self.assertAlmostEqual(1.0, get_distribution_sum(d), delta = 1e-5)
