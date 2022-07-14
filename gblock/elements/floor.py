# -*- coding: utf-8 -*-
"""
Created on 10 Jul 2022

@author: prslvtsv
"""
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)

from gblock.elements.layout import FloorLayout
from gblock.elements.matrix import SpacialMatrix
from gblock.elements.gtypes import AssemblyBlock
from gblock.elements.appriser import FloorAppriser
from gblock.utils.xyz import XYZ
from collections import OrderedDict


class FloorObject(AssemblyBlock):
    def __init__(self, parent=None):
        AssemblyBlock.__init__(self, parent)
        self.typename = "FloorObject"
        self.assemblyDiagram = None
        self.level = None
        self.height = 3.3
        self._layouts = None
        self.layout = None

        self.attrib = None
        self.metrics = FloorAppriser(self)
        self.origin = XYZ()
        self.outline = None

    def from_assembly_diagram(self, indexes, crv, state, origin):
        try:
            self.origin = XYZ(origin.X, origin.Y, origin.Z)
        except:
            self.origin = XYZ(xyz=origin)

        tile = list(zip(crv, state))
        print(len(matrix.active_indexes()))
        self.assemblyDiagram = SpacialMatrix.from_indexes(
            matrix.active_indexes(), data=tile
        )
