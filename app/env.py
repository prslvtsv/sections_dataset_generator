# -*- coding: utf-8 -*-
"""
24 Jun 2022

@author: prslvtsv

"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import apart_solver as solver
from gblock.elements.matrix import SpacialMatrix


def main():
    groups, indxs = solver.solve_possible_tiling()
    for xss in groups:
        idx = [x for xs in xss for x in xs]
        for x in xss:
            mtx = SpacialMatrix().from_indexes(x)
            # print(mtx.shape())
            print(mtx.display())
            print()

    # for c in indxs:
    #     print(c)


if __name__ == "__main__":

    main()

    # MyApp.run(title="Simple App", log="textual.log")
