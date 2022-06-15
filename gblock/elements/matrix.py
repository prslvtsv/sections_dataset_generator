# -*- coding: utf-8 -*-
"""
Created on 15 Jun 2022

@author: prslvtsv
"""

from gtypes import NestedObject, AssemblyBlock


class MatrixCell(NestedObject):
    def __init__(self, pos, parent=None, enable=False):
        NestedObject.__init__(self, parent)
        self.pos = pos
        self.data = None
        self.active = enable

    def index_glob(self):
        if self.parent is None:
            return self.index()
        elif not isinstance(self.parent, SpacialMatrix):
            return self.index()
        return (
            self.index()[0] + self.parent.padding[0],
            self.index()[1] + self.parent.padding[1],
        )

    def index(self):
        return self.pos


class SpacialMatrix(AssemblyBlock):
    def __init__(self, padding=(0, 0)):
        AssemblyBlock.__init__(self)
        # self.shape = shape
        self.cells = []
        self.padding = padding

    def enable_cells_by_indexes(self, indxs):
        # print(self.data)
        for i, j in indxs:
            self.cells[i][j].active = True
        return self

    def fill_by_indexes(self, indxs, data):
        for pos in range(len(indxs)):
            i, j = indxs[pos]
            if data is None:
                self.cells[i][j].data = None
            elif (isinstance(data, list) or isinstance(data, set)) and len(data) == len(
                indxs
            ):
                self.cells[i][j].data = data[pos]
            else:
                self.cells[i][j].data = data
        return self

    def _active(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j].active:
                    yield self.cells[i][j]

    def active_cells(self):
        return [a for a in self._active()]

    def active_indexes(self):
        return [a.pos for a in self._active()]

    def _rows(self):
        for i in range(len(self.cells)):
            yield self.cells[i]

    def raw(self):
        return [[c.data for c in a] for a in self._rows()]

    @staticmethod
    def create_empty(shape, padding=(0, 0)):
        mtx = SpacialMatrix(padding)
        si, sj = shape
        mtx.cells = []

        for i in range(0, si):
            mtx.cells.append([])

            for j in range(0, sj):
                mtx.cells[i].append(MatrixCell((i, j), mtx))
        return mtx

    @staticmethod
    def create_from_indexes(indxs, data=None):
        bnd = SpacialMatrix.bound_indexes(indxs)
        shp = SpacialMatrix.shape_from_bound(bnd)
        pdn = SpacialMatrix.padding_from_bound(bnd)

        return (
            SpacialMatrix.create_empty(shp, pdn)
            .enable_cells_by_indexes(indxs)
            .fill_by_indexes(indxs, data)
        )

    @staticmethod
    def bound_indexes(indx):
        if len(indx) == 0:
            return ((0, 0), (0, 0))
        elif len(indx[0]) == 0:
            return ((0, 0), (0, 0))
        ri = [a[0] for a in indx]
        rj = [a[1] for a in indx]

        return ((min(ri), max(ri)), (min(rj), max(rj)))

    @staticmethod
    def shape_from_bound(bound):
        if bound[0][0] + bound[0][1] + bound[1][0] + bound[1][1] == 0:
            return (0, 0)
        return ((bound[0][1] - bound[0][0]) + 1, (bound[1][1] - bound[1][0]) + 1)

    @staticmethod
    def padding_from_bound(bound):
        if bound[0][0] + bound[0][1] + bound[1][0] + bound[1][1] == 0:
            return (0, 0)
        return (bound[0][0], bound[1][0])

    @staticmethod
    def parse_indexes(indx):
        return [
            (int(r.split(",")[0]), int(r.split(",")[1]))
            for r in indx.strip().split(":")
        ]


if __name__ == "__main__":

    indexes = SpacialMatrix.parse_indexes(
        "0,0:1,0:2,0:0,1:1,1:2,1:3,1:4,1:0,2:2,2:3,2:4,2:0,3:2,3:3,3:4,3:0,4:2,4:3,4:4,4:0,5:2,5:3,5:4,5:0,6:1,6:2,6:3,6:4,6:0,7:1,7:2,7:3,7:4,7:0,8:1,8:2,8:3,8:4,8:0,9:1,9:3,9:4,9:0,10:1,10"
    )

    spmtx = SpacialMatrix.create_from_indexes(indexes, 1)
    print(len(spmtx.cells), len(spmtx.cells[0]))
    print(spmtx.raw())
    active_cell_obj = spmtx.active_cells()
    active_indx = spmtx.active_indexes()
    print(active_indx)
