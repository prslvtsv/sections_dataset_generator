# -*- coding: utf-8 -*-
"""
Created on 06 Jul 2022

@author: prslvtsv
"""
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)
from collections import OrderedDict
from gblock.elements.matrix import SpacialMatrix

A = "⬛⬛"
B = "⬛⬛⬛"
C = "⬛⬛⬛⬛"
D = "⬜⬛⬜\n⬛⬛⬛"
E = "⬜⬜⬛\n⬛⬛⬛"
F = "⬛⬜⬛\n⬛⬛⬛"
G = "⬜⬛⬛\n⬛⬛⬛"
H = "⬛⬛⬛\n⬛⬛⬛"
I = "⬜⬜⬛\n⬜⬜⬛\n⬛⬛⬛"
J = "⬜⬜⬛\n⬜⬛⬛\n⬛⬛⬛"
K = "⬜⬛⬛\n⬜⬛⬛\n⬛⬛⬛"
L = "⬜⬛⬛\n⬛⬛⬛\n⬛⬛⬛"
M = "⬛⬛\n⬛⬛"

_all = [A, B, C, D, E, F, G, H, I, J, K, L, M]
_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]


class ApartmentShape:
    def __init__(self, name, strshape):
        self.name = name
        self.strshape = strshape
        self.indexes = self.to_index()
        self.matrix = SpacialMatrix().from_indexes(self.indexes)
        # self.bedrooms = len(self.indexes) - 1

    def to_index(self):
        sh = self.strshape.splitlines()
        idx = []
        for j, jv in enumerate(sh):
            for i, iv in enumerate(jv):
                if iv in "⬛":
                    idx.append((i, j))
        return idx

    def info(self):
        return "name: {}\n{}\n{}".format(self.name, self.strshape, str(self.indexes))

    def has_same_shape(self, other):
        return SpacialMatrix.compare(self.matrix, other, mode="formation")


ALL = [ApartmentShape(n, v) for n, v in list(zip(_names, _all))]
UP_TO_1 = [ApartmentShape(n, v) for n, v in list(zip(_names[:1], _all[:1]))]
UP_TO_2 = [ApartmentShape(n, v) for n, v in list(zip(_names[:2], _all[:2]))]
UP_TO_3 = [ApartmentShape(n, v) for n, v in list(zip(_names[:5], _all[:5]))]


def print_up_to_2():
    shapes = [v.info() for v in ALL]
    return "\n\n".join(shapes)


def print_up_to_3():
    shapes = [v.info() for v in UP_TO_3]
    return "\n\n".join(shapes)


def print_all():
    shapes = [v.info() for v in ALL]
    return "\n\n".join(shapes)
