# -*- coding: utf-8 -*-
"""
Created on 15 Jun 2022

@author: prslvtsv
"""


class NestedObject(object):
    def __init__(self, parent, child=None):
        self.parent = parent
        self.child = child


class AttribAddress:
    def __init__(self):
        self.attr = {}


class AssemblyBlock(NestedObject, AttribAddress):
    def __init__(self, parent=None):
        NestedObject.__init__(self, parent)
        AttribAddress.__init__(self)
        self.typename = "assembly_block"
        # TODO
        # size = DynamicRange
        # shape = DynamicRange
        # metrics = Appriser

    def devTest(self):
        print("self {} {}".format(self.typename, self))
        print("parent {} {}".format(self.parent.typename, self.parent))


class Piece(AssemblyBlock):
    def __init__(self, parent=None):
        AssemblyBlock.__init__(self, parent)
        self.typename = "piece"


if __name__ == "__main__":

    pobj = AssemblyBlock()
    chobj = Piece(pobj)
    cchobj = Piece(chobj)

    chobj.devTest()
    cchobj.devTest()
