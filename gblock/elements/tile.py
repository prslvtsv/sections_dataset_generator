# -*- coding: utf-8 -*-
"""
Created on 22 Jun 2022

@author: prslvtsv
"""
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)

from gblock.elements.matrix import MatrixCell
from gblock.utils.utils import f2s, f2f


class Tile(MatrixCell):
    def __init__(self, pos=None, parent=None, enable=False, instance=None):
        if instance is None:
            MatrixCell.__init__(self, pos, parent, enable)
        else:
            self._init_from_instance(pos, instance, parent)
        self.typename = "Tile"
        self.attrib = {}
        self.outline = None
        self.size = (3.3, 6.4)
        self.window = None
        self.door = None

    def _init_from_instance(self, pos, obj, apt):
        MatrixCell.__init__(self, pos, apt, obj.active)

    def outline_xyz(self, as_str=False, closed=False):
        res = None
        if as_str:
            res = [(f2s(x), f2s(y), f2s(z)) for (x, y, z) in self.outline]
        else:
            res = [(f2f(x), f2f(y), f2f(z)) for (x, y, z) in self.outline]

        return res if closed else res[:-1]


class TileDump:
    def __init__(self):
        self.pos = None
        self.attrib = {}
        self.utils = {}
        self.outline = []
        self.size = []
        self.ref = {}


################################################
################################################
if __name__ == "__main__":
    tile = Tile()
    tile.clear_data()
