import oct2py
import numpy as np


def get_coefs(points, coef_count):

    # call octave to calculate the coefficients
    oc = oct2py.Oct2Py()
    coefs = np.zeros([2, coef_count], dtype=float)
    [[coefs[0][0], coefs[1][0]]] = oc.get_coef(points, 0)
    for i in range ((coef_count - 1) // 2):
        [[coefs[0][2 * i + 1], coefs[1][2 * i + 1]]] = oc.get_coef(points, i + 1)
        [[coefs[0][2 * i + 2], coefs[1][2 * i + 2]]] = oc.get_coef(points, -i - 1)
    return coefs