import unittest
import numpy as np


from . import resistance2temperature, temperature2resistance, t2r, r2t


# Testdata from table A.1 in IEC60751
TESTDATA = np.array(
    [
        [604.0, 314.99],
        [432.0, 258.06],
        [172.0, 165.51],
        [-200.0, 18.53],
        [805.0, 377.19],
        [822.0, 382.24],
        [361.0, 233.56],
        [409.0, 250.19],
        [455.0, 265.87],
        [203.0, 176.96],
        [100.0, 138.51],
        [718.0, 350.84],
        [-135.0, 45.94],
        [0.0, 100.00],
        [330.0, 222.68],
        [493.0, 278.64],
        [-156.0, 37.22],
        [380.0, 240.18],
        [850.0, 390.48],
        [449.0, 263.84],
        [-15.0, 94.12],
        [658.0, 332.16],
        [-11.0, 95.69],
    ]
)


class TestConversion(unittest.TestCase):
    def setUp(self):
        self.t = TESTDATA[:, 0]
        self.R = TESTDATA[:, 1]

    def test_resistance2temperature(self):
        t = resistance2temperature(self.R)
        np.testing.assert_allclose(t, self.t, rtol=1e-4, atol=1e-2)

    def test_temperature2resistance(self):
        R = temperature2resistance(self.t)
        np.testing.assert_allclose(R, self.R, rtol=1e-4, atol=1e-2)

    def test_t2r(self):
        R = t2r(self.t)
        np.testing.assert_allclose(R, self.R, rtol=1e-4, atol=1e-2)

    def test_r2t(self):
        t = r2t(self.R)
        np.testing.assert_allclose(t, self.t, rtol=1e-4, atol=1e-2)


if __name__ == "__main__":
    unittest.main()
