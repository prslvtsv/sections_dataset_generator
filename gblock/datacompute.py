# -*- coding: utf-8 -*-
"""
Cartesian product function by Stackoverflow user, pv.

"""

import numpy as np


def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:, 0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m, 1:])
        for j in range(1, arrays[0].size):
            out[j * m : (j + 1) * m, 1:] = out[0:m, 1:]
    return out


# Python program for cartesian
# product of N-sets

# function to find cartesian product of two sets
def cartesianProduct(set_a, set_b):
    result = []
    for i in range(0, len(set_a)):
        for j in range(0, len(set_b)):

            # for handling case having cartesian
            # product first time of two sets
            if type(set_a[i]) != list:
                set_a[i] = [set_a[i]]

            # coping all the members
            # of set_a to temp
            temp = [num for num in set_a[i]]

            # add member of set_b to
            # temp to have cartesian product
            temp.append(set_b[j])
            result.append(temp)

    return result


# Function to do a cartesian
# product of N sets
def cartesian_py(list_a, n):

    # result of cartesian product
    # of all the sets taken two at a time
    temp = list_a[0]

    # do product of N sets
    for i in range(1, n):
        temp = cartesianProduct(temp, list_a[i])

    # print(temp)
    return temp
