import numpy as np


def check_bounds_order(bounds):
    for l, u in zip(bounds, bounds[1:]):
        if l >= u:
            raise Exception("Bounds must be in increasing order")

class PiecewiseFunction:
    def __init__(self, bounds, functions):
        """
        :param bounds: list of n+1 bounds
        :param functions: list of n functions. The appropriate one will be evaluated based on the bounds
        """
        self.bounds = bounds
        self.functions = functions
        if len(bounds) != len(functions) + 1:
            raise Exception("Length of bounds must be one larger than length of functions")
        check_bounds_order(bounds)


    def __call__(self, x):
        for l, u, f in zip(self.bounds, self.bounds[1:], self.functions):
            if l <= x and x < u:
                return f(x)
        raise Exception("x={} is out of range [{}, {}]".format(x, self.bounds[0], self.bounds[-1]))


class PiecewiseDefiniteIntegralFunction:
    def __init__(self, bounds, indefinite_integral_functions):
        """
        Integral of a piecewise function
        :param bounds: list of n+1 bounds for each piecewise region
        :param indefinite_integral_functions: list of n indefinite integraph functions
        """
        if len(bounds) != len(indefinite_integral_functions) + 1:
            raise Exception("Length of bounds must be one larger than length of functions")
        check_bounds_order(bounds)
        self.bounds = bounds
        self.f = indefinite_integral_functions

    def evaluate(self, x1, x2):
        """
        evaluates the definite integral from x1 to x2
        :param x1: lower range
        :param x2: upper range
        :return:
        """
        if x1 < self.bounds[0]:
            raise Exception("x1 ({}) is below lower bound ({})".format(x1, self.bounds[0]))
        if x2 > self.bounds[-1]:
            raise Exception("x2 ({}) is above upper bound ({})".format(x2, self.bounds[-1]))
        if x1 > x2:
            raise Exception("x1 ({}) is greater than x2 ({})".format(x1, x2))

        s = 0.0
        for l, u, f in zip(self.bounds, self.bounds[1:], self.f):
            if l <= x1 and x1 < u:
                s -= f(x1)
                if x2 <= u:
                    s += f(x2)
                    return s
                s += f(u)
                x1 = u
        raise Exception("Invalid execution path, this should not ever be executed")


class PiecewiseUniform:
    def __init__(self, bounds, probability_densities):
        """
        :param bounds: list of n+1 bounds. e.g. [0, 5, 7.5, 10]
        :param probability_densities: list of probability n densities. This will be normalized. e.g. [.05, .2, .2]
        """
        self.bounds = bounds
        self.probability_densities = probability_densities

        if len(bounds) != len(probability_densities) + 1:
            raise Exception("Length of bounds must be one larger than length of probability_densities")
        check_bounds_order(bounds)

        self._normalize()

    def _normalize(self):
        sum = 0
        for lower, upper, prob in zip(self.bounds, self.bounds[1:], self.probability_densities):
            if prob < 0:
                raise Exception("Probabilities cannot be negative")
            sum += (upper - lower) * prob
        if sum == 0:
            raise Exception("Probability density is 0")
        self.probability_densities = [p/sum for p in self.probability_densities]

    def __call__(self, x):
        for l, u, p in zip(self.bounds, self.bounds[1:], self.probability_densities):
            if l<=x and x<u:
                return p
        raise Exception("x={} is out of range [{}, {}]".format(x, self.bounds[0], self.bounds[-1]))


def expected_value(dist, f, resolution = 0.0001):
    """
    Approximate expected Value of f under distribution dist
    :param dist: probability distribution
    :param f: function
    :param resolution: resolution of the sample for approximation
    :return: expected value
    """
    e = 0
    for x in np.arange(dist.bounds[0], dist.bounds[-1], resolution):
        e += f(x) * dist(x) * resolution
    return e

