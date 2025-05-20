"""The SER algorithm for estimating the inverse correlation matrix
from _Adaptive Signal Processing_ by Widrow & Stearns."""

import numpy as np

class ser:
    def __init__(self, n, m):
        """Initialize the SER algorithm. SER computes q, a scaled
        n x n version of the inverse of the input cross correlation
        matrix. The input data are assumed to be stationary over a
        length of m samples."""

        self.q = np.identity(n, 'f') * 10.
        self.alpha = pow(2., -1. / m)
        self.k = 0

    def add(self, x):
        """Add the next input sample vector x to q."""

        x = x.astype('f')
        s = self.q.dot(x)
        g = self.alpha + x.dot(s)
        self.q = (self.q - np.outer(s, s) / g) / self.alpha
        self.k += 1

    def r(self):
        "Return the estimate of the inverse correlation matrix."

        #s = (1. - pow(self.alpha, self.k)) / (1. - self.alpha)
        s = 1 / (1 - self.alpha)    # asymptotic value
        return s * self.q
