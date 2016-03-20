import numpy as np
from scipy.special import binom

def Bernstein(n, k):
    """ Bernstein polynomial.
        Adapted from: https://gist.github.com/Juanlu001/7284462
    """
    coeff = binom(n, k)

    def _bpoly(x):
        return coeff * x ** k * (1 - x) ** (n - k)

    return _bpoly


def bezier(points, num=512):
    """ Build Bezier curve from points.
        Adapted from: https://gist.github.com/Juanlu001/7284462
    """
    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for ii in range(N):
        curve += np.outer(Bernstein(N - 1, ii)(t), points[ii])
    return [ c[0] for c in list(curve) ]

