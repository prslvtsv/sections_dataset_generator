# -*- coding: utf-8 -*-
"""
Created on 03 Jul 2022

@author: prslvtsv
"""
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)

from gblock.utils.utils import f2s, f2f


def _csub(a, b):
    return a - b


def _csum(a, b):
    return a + b


class XYZ:
    # float precision
    FP = 4

    def __init__(self, xx=0, yy=0, zz=0, xyz=None):
        if xyz is None:
            crd = [f2f(xx, XYZ.FP), f2f(yy, XYZ.FP), f2f(zz, XYZ.FP)]
        else:
            crd = [f2f(xyz[0], XYZ.FP), f2f(xyz[1], XYZ.FP), f2f(xyz[2], XYZ.FP)]
        self._xyz = crd

    @property
    def x(self):
        return self._xyz[0]

    @x.setter
    def x(self, val):
        self._xyz[0] = f2f(val, XYZ.FP)

    @property
    def y(self):
        return self._xyz[1]

    @x.setter
    def y(self, val):
        self._xyz[1] = f2f(val, XYZ.FP)

    @property
    def z(self):
        return self._xyz[2]

    @x.setter
    def z(self, val):
        self._xyz[2] = f2f(val, XYZ.FP)

    @property
    def X(self):
        return self._xyz[0]

    @x.setter
    def X(self, val):
        self._xyz[0] = f2f(val, XYZ.FP)

    @property
    def Y(self):
        return self._xyz[1]

    @x.setter
    def Y(self, val):
        self._xyz[1] = f2f(val, XYZ.FP)

    @property
    def Z(self):
        return self._xyz[2]

    @x.setter
    def Z(self, val):
        self._xyz[2] = f2f(val, XYZ.FP)

    @property
    def xyz(self):
        return self._xyz

    @xyz.setter
    def xyz(self, val):
        self._xyz[0] = f2f(val[0], XYZ.FP)
        self._xyz[1] = f2f(val[1], XYZ.FP)
        self._xyz[2] = f2f(val[2], XYZ.FP)

    def __repr__(self):
        return "".join(["(", ", ".join([f2s(c, 2) for c in self.xyz]), ") "])

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def translate(f, t, origin=None):
        if origin is None:
            origin = XYZ(0, 0, 0)
        transform = XYZ(xyz=list(map(_csub, t.xyz, origin.xyz)))
        return XYZ(xyz=list(map(_csum, f.xyz, transform.xyz)))


if __name__ == "__main__":
    point = XYZ(10, 20, 1)
    origin = XYZ(5, 5, 0)
    target = XYZ(0, 0, 0)
    point = XYZ.translate(point, target, origin)
    print(point)
    point.x = 6
    print(point.X, point.x)
