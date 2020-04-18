from unittest import TestCase
from distribution import PiecewiseFunction

class TestPiecewiseFunction(TestCase):
    def test_call(self):
        f = PiecewiseFunction([0,1,2], [lambda x: 0, lambda x: x**2])
        with self.assertRaises(Exception) as context:
            f(-1)
        with self.assertRaises(Exception) as context:
            f(2.1)

        self.assertEqual(f(0.5), 0.0)
        self.assertEqual(f(1.5), 1.5**2)