import unittest
import numpy as np


from . import resistance2temperature, temperature2resistance, t2r, r2t


# Testdata from table A.1 in IEC60751
TESTDATA = np.array([
    [ 604.  ,  314.99],
    [ 432.  ,  258.06],
    [ 172.  ,  165.51],
    [-200.  ,   18.52],
    [ 805.  ,  377.19],
    [ 822.  ,  382.24],
    [ 361.  ,  233.56],
    [ 409.  ,  250.19],
    [ 455.  ,  265.87],
    [ 203.  ,  176.96],
    [ 100.  ,  138.51],
    [ 718.  ,  350.84],
    [-135.  ,   45.94],
    [   0.  ,  100.00],
    [ 330.  ,  222.68],
    [ 493.  ,  278.64],
    [-156.  ,   37.22],
    [ 380.  ,  240.18],
    [ 850.  ,  390.48],
    [ 449.  ,  263.84],
    [ -15.  ,   94.12],
    [ 658.  ,  332.16],
    [ -11.  ,   95.69]
    ])


class TestConversion(unittest.TestCase):
    def setUp(self):
        self.t = TESTDATA[:, 0]
        self.R = TESTDATA[:, 1]

    def test_resistance2temperature(self):
        t = np.round(resistance2temperature(self.R), 2)
        np.testing.assert_array_equal(t, self.t)
    
    def test_temperature2resistance(self):
        R = np.round(temperature2resistance(self.t), 2)
        np.testing.assert_array_equal(R, self.R)


if __name__ == "__main__":
    unittest.main()