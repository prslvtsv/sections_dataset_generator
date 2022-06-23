# -*- coding: utf-8 -*-
"""
Created on 22 Jun 2022

@author: prslvtsv
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from elements.matrix import SpacialMatrix, rotate_and_reflect
from collections import OrderedDict


class Apartment(SpacialMatrix):
    def __init__(self, padding=(0, 0)):
        SpacialMatrix.__init__(self, padding)
        self.attrib = OrderedDict()

    @property
    def tiles(self):
        return self.cells

    # def layout_pos(self):
    #     return self.indexes(glob=True)


class ApartmentTempate(Apartment):
    def __init__(self):
        Apartment.__init__(self)


if __name__ == "__main__":
    exactCoverResult = [
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 3), (1, 3), (2, 3), (2, 2)],
        [(1, 0), (1, 1)],
        [(2, 0), (2, 1)],
    ]

    # [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    # [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

    # [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    # [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]

    # [(0, 0), (0, 1)]
    # [(1, 0), (1, 1)]

    # [(0, 0), (0, 1)]
    # [(2, 0), (2, 1)]

    aparts = []

    for res in exactCoverResult:
        apt = Apartment().from_indexes(res)
        aparts.append(apt)
        print(apt.indexes(glob=True))
        print(apt.tiles)
        print("_____________")
        print()
    ap = aparts[0]
    bp = aparts[1]

    # print(Apartment.compare(ap, bp, mode="formation"))
