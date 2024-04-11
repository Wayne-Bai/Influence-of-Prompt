from scipy import stats

def p_value(l1, l2):
    return stats.ttest_ind(l1, l2)[1]

import itertools as it

from bisect import bisect_left
from typing import List

import numpy as np
import pandas as pd
import scipy.stats as ss

from pandas import Categorical


def VD_A(l1, l2):

    m = len(l1)
    n = len(l2)

    if m != n:
        raise ValueError("Data d and f must have the same length")

    r = ss.rankdata(l1 + l2)
    r1 = sum(r[0:m])

    # Compute the measure
    # A = (r1/m - (m+1)/2)/n # formula (14) in Vargha and Delaney, 2000
    A = (2 * r1 - m * (m + 1)) / (2 * n * m)  # equivalent formula to avoid accuracy errors

    levels = [0.147, 0.33, 0.474]  # effect sizes from Hess and Kromrey, 2004
    magnitude = ["negligible", "small", "medium", "large"]
    scaled_A = (A - 0.5) * 2

    magnitude = magnitude[bisect_left(levels, abs(scaled_A))]
    estimate = A

    return estimate, magnitude

if __name__ == "__main__":
    C = [0.9108333333333334, 0.8755555555555556, 0.900277777777778, 0.9274999999999999, 0.8777777777777779]
    E = [0.8663888888888888, 0.8802777777777777, 0.7816666666666667, 0.8377777777777776, 0.9305555555555556]
    print(VD_A(C, E))

    # Large
    D = [0.7202777777777778, 0.77, 0.8544444444444445, 0.7947222222222222, 0.7577777777777778]
    print(VD_A(C, D))