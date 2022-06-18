# -*- coding: utf-8 -*-
"""New structure of classes

this file just representation of classes which will be used in updated operational
logic

Currently implemending.
Implemented classes commented out here

this is not finctional module. use only for ref

Created on 15 Jun 2022
@author: prslvtsv
"""


# class NestedObject:
#     def __init__(self, parent):
#         self.parent = parent
#         self.child = None


# class MatrixCell(NestedObject):
#     def __init__(self, ij, parent=None):
#         NestedObject.__init__(self, parent)
#         self.data = None
#         pass


# class SpacialMatrix:
#     def __init__(self, shape=(3, 3)):
#         self.shape = shape
#         self.cells = SpacialMatrix.create_empty(shape)
#         self.disabled = []
#
#     @staticmethod
#     def create_empty(shape, alive=True):
#         # generate 2d array of MatrixCell
#         # enable all MatrixCell, fill indexes
#         # use None for MC data attr
#         pass
#
#     def disable_cells(self, dis=[]):
#         # check if dis cells within indexes
#         # check if cell live
#         # apply disabled to cells, assign disabled to s.dis
#         pass
#
#     def count_alive(self):
#         pass


# class MatrixSlice(SpacialMatrix, NestedObject):
#     def __init__(self, parent, shape=(3, 3), span=[(0, 3), (0, 3)]):
#         SpacialMatrix.__init__(self, shape)
#         NestedObject.__init__(self, parent)
#         self.span = span
#         # read cells data from parent
#         # self.cells = parent cells at domain


# class AddressAttribute:
#     def __init__(self):
#         self.attr = {}


class Appriser:
    def __init__(self):
        pass
        # aptRatio
        # areaTotal
        # areaValuable


class DynamicRange:
    # val
    pass


# class FunctionalElement(AttribAddress, NestedObject):
#     def __init__(self, parent):
#         AttribAddress.__init__(self)
#         NestedObject.__init__(self, parent)
#         pass
#         # size = DynamicRange
#         # shape = DynamicRange
#         # metrics = Appriser


class LivingGroup:
    def __init__(self):
        # sample
        self.buildings = [Building(self), Building(self)]
        pass

    # residential
    # commercial


class Building(FunctionalElement):
    def __init__(self, parent=None):
        FunctionalElement.__init__(self, parent)
        self.sections = [Section(parent)]
        pass

    # footprint
    # sections
    # metrics
    # evaluation


class Section(FunctionalElement):
    def __init__(self, parent=None):
        FunctionalElement.__init__(self, parent)
        pass

    # neighbors
    # verticalAssembly
    # constrains
    # size
    # untRange
    # evalDomain


class VerticalAssembly(NestedObject):
    def __init__(self, parent=None):
        NestedObject.__init__(self, parent)
        pass

    # assemblyMethod
    # levels
    # facadeMatrix
    # evaluation


class Floor(FunctionalElement):
    def __init__(self, parent=None):
        FunctionalElement.__init__(self, parent)
        pass


class Layout(NestedObject):
    def __init__(self, parent=None):
        NestedObject.__init__(self, parent)
        pass


class Apartment(MatrixSlice):
    def __init__(self, parent):
        MatrixSlice.__init__(self)
        pass


# CommercialSpace(MatrixSlice)
# PublicSpace(MatrixSlice)
# EvacuationFacility(MatrixSlice)
# VerticalLink(MatrixSlice)


class Tile(MatrixCell, NestedObject):
    pass


class Side:
    pass


class LifeCycle:
    pass
