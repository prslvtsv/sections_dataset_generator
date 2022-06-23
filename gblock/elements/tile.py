# -*- coding: utf-8 -*-
"""
Created on 22 Jun 2022

@author: prslvtsv
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from elements.matrix import MatrixCell


class Tile(MatrixCell):
    def __init__(self, pos, parent, enable=False):
        MatrixCell.__init__(self, pos, parent, enable)
        self.attrib = {}
        self.outline = None
        self.size = (3.3, 6.4)
        self.window = None
        self.door = None

    # def set_attributes(self, attrib):
    #     self.attrib = atrib


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
