# -*- coding: utf-8 -*-
"""Matrix objects to utilize tiles & attr data management

representation of 2d array as spacialMatrix data container
helps for fast matrix creation with cell indexes or
cell central points

helps to maintain nested data structure assisting fast getting\setting
of stored data

SpacialMatrix contain 2d nested lists with MatrixCell container
MatrixCell might be active\disabled representing existing\missing tiles
in matrix structure

Use this as a module for further development logic
Runs pure IronPython \ Cpython 2.7+, no additional dependencies required

Created on 15 Jun 2022
@author: prslvtsv
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from elements.gtypes import NestedObject, AssemblyBlock


class MatrixCell(NestedObject):
    """Smalest data container unit, stores any type of info in .data property"""

    def __init__(self, pos, parent=None, enable=False):
        NestedObject.__init__(self, parent)
        self.pos = pos
        self.data = None
        self.active = enable
        if not self.parent is None:
            self.pp = self.parent.padding

    def _glob(self):
        if not self.parent is None:
            # print(self.pos, self.pp)
            return (self.pos[0] + self.pp[0], self.pos[1] + self.pp[1])
        return self.index()

    def index(self, glob=False):
        return self._glob() if glob else self.pos

    def __repr__(self):
        # return "⚫" if self.active else "⚪"
        return "⬛" if self.active else "⬜"


class SpacialMatrix(AssemblyBlock):
    """data container in form of 2d nested lists handling aseembly & assesment logic"""

    def __init__(self, padding=(0, 0)):
        AssemblyBlock.__init__(self)
        # self.shape = shape
        self.cells = []
        self.padding = padding

    def enable_cells_by_indexes(self, indxs):
        for i, j in indxs:
            self.cells[i][j].active = True
        return self

    def fill_by_indexes(self, indxs, data):
        for pos, v in enumerate(indxs):
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

    def _every_cell(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                yield self.cells[i][j]

    def indexes(self, glob=False):
        return [a.index(glob) for a in self._every_cell()]

    def active_cells(self):
        return [a for a in self._every_cell() if a.active]

    def active_indexes(self, glob=False):
        return [a.index(glob) for a in self._every_cell() if a.active]

    def count_active(self):
        return len(self.active_cells())

    def _rows(self):
        for i in range(len(self.cells)):
            yield self.cells[i]

    def raw(self):
        return [[c.data for c in a] for a in self._rows()]

    def indexes_as_matrix(self, glob=False):
        return [[c.index(glob) for c in a] for a in self._rows()]

    def shape(self):
        return (len(self.cells), len(self.cells[0]))

    def __repr__(self):
        rp = [[c.__repr__() for c in a] for a in self._rows()]
        # print(rp)
        col = []
        for i in range(len(rp[0])):
            col.append([])
        for i in range(len(col)):
            col[i] = "".join([r[i] for r in rp])
        col.reverse()
        return "\n".join(col)

    def __str__(self):
        return self.__repr__()

    def empty(self, shape, padding=(0, 0)):
        self.padding = padding
        si, sj = shape
        self.cells = []
        for i in range(0, si):
            self.cells.append([])
            for j in range(0, sj):
                self.cells[i].append(MatrixCell((i, j), self))
        return self

    def from_indexes(self, indxs, data=None):
        iv, jv = [a[0] for a in indxs], [a[1] for a in indxs]
        pnd = (min(iv), min(jv))
        loc_idx = [(i - pnd[0], j - pnd[1]) for (i, j) in indxs]
        bnd = SpacialMatrix.bound_indexes(loc_idx)
        shp = SpacialMatrix.shape_from_bound(bnd)
        self.empty(shp, pnd)
        self.enable_cells_by_indexes(loc_idx)
        self.fill_by_indexes(loc_idx, data)
        return self

    # # OBSOLETE remove later
    # @staticmethod
    # def create_empty(shape, padding=(0, 0)):
    #     mtx = SpacialMatrix(padding)
    #     si, sj = shape
    #     mtx.cells = []
    #     for i in range(0, si):
    #         mtx.cells.append([])
    #         for j in range(0, sj):
    #             mtx.cells[i].append(MatrixCell((i, j), mtx))
    #     return mtx

    # # OBSOLETE remove later
    # @staticmethod
    # def create_from_indexes(indxs, data=None):
    #     iv, jv = [a[0] for a in indxs], [a[1] for a in indxs]
    #     pnd = (min(iv), min(jv))
    #     loc_idx = [(i - pnd[0], j - pnd[1]) for (i, j) in indxs]
    #     bnd = SpacialMatrix.bound_indexes(loc_idx)
    #     shp = SpacialMatrix.shape_from_bound(bnd)
    #     mtx = SpacialMatrix.create_empty(shp, pnd)
    #     mtx.enable_cells_by_indexes(loc_idx).fill_by_indexes(loc_idx, data)

    #     return mtx

    @staticmethod
    def bound_indexes(indx):
        """computes matrix actual index ranges from list of (i, j) indexes"""
        if len(indx) == 0:
            return ((0, 0), (0, 0))
        elif len(indx[0]) == 0:
            return ((0, 0), (0, 0))
        ri, rj = [a[0] for a in indx], [a[1] for a in indx]
        return ((min(ri), max(ri)), (min(rj), max(rj)))

    @staticmethod
    def shape_from_bound(bound):
        return ((bound[0][1] - bound[0][0]) + 1, (bound[1][1] - bound[1][0]) + 1)

    @staticmethod
    def padding_from_bound(bound):
        if bound[0][0] + bound[0][1] + bound[1][0] + bound[1][1] == 0:
            return (0, 0)
        return (bound[0][0], bound[1][0])

    @staticmethod
    def parse_indexes(indx):
        """converts string representation to [(i, j), ...], formated as - "i,j:i,j:i,j" """
        return [
            (int(r.split(",")[0]), int(r.split(",")[1]))
            for r in indx.strip().split(":")
        ]

    @staticmethod
    def compare(a, b, mode="exact"):
        def xor_sets(a, b):
            xr = set(a) ^ set(b)
            return xr

        def shape(a, b):
            return not xor_sets(a.shape(), b.shape())

        def overlay_exact(a, b):
            return not xor_sets(a, b)

        def overlay_rotational(a, b):
            rotated = list(rotate_and_reflect(a.active_indexes()))
            return any([overlay_exact(r, b.active_indexes()) for r in rotated])

        if mode in "shape":
            return shape(a, b)
        # test if
        if mode in "exact":
            return overlay_exact(a.active_indexes(), b.active_indexes())
        # test if matrix formation same despite spacial orientation
        if mode in "formation":
            return overlay_rotational(a, b)


#############################################################################
# from polyomino lib
def rotations(tile, and_reflections=True):
    if and_reflections:
        return rotate_and_reflect(tile)
    else:
        return rotate(tile)


ROTATIONS = [[[1, 0], [0, 1]], [[0, -1], [1, 0]], [[-1, 0], [0, -1]], [[0, 1], [-1, 0]]]


ROTATIONS_AND_REFLECTIONS = [
    [[1, 0], [0, 1]],
    [[0, -1], [1, 0]],
    [[-1, 0], [0, -1]],
    [[0, 1], [-1, 0]],
    [[-1, 0], [0, 1]],
    [[0, -1], [-1, 0]],
    [[1, 0], [0, -1]],
    [[0, 1], [1, 0]],
]


def rotate_and_reflect(tile):
    return unique_after_transform(tile, ROTATIONS_AND_REFLECTIONS)


def rotate(tile):
    return unique_after_transform(tile, ROTATIONS)


def unique_after_transform(tile, transforms):
    s = set()
    for m in transforms:
        rotated = [
            (m[0][0] * t[0] + m[0][1] * t[1], m[1][0] * t[0] + m[1][1] * t[1])
            for t in tile
        ]
        mx = min(s[0] for s in rotated)
        my = min(s[1] for s in rotated)
        shifted = [(t[0] - mx, t[1] - my) for t in rotated]
        key = tuple(sorted(shifted))
        if key not in s:
            yield shifted
            s.add(key)


#############################################################################


if __name__ == "__main__":
    # used just for development test purpose

    indexes = SpacialMatrix.parse_indexes(
        "0,0:1,0:2,0:0,1:1,1:2,1:3,1:4,1:0,2:2,2:3,2:4,2:0,3:2,3:3,3:4,3:0,4:2,4:3,4:4,4:0,5:2,5:3,5:4,5:0,6:1,6:2,6:3,6:4,6:0,7:1,7:2,7:3,7:4,7:0,8:1,8:2,8:3,8:4,8:0,9:1,9:3,9:4,9:0,10:1,10"
    )

    m = SpacialMatrix().from_indexes(indexes)
    print(m.__repr__())
    # print(len(spmtx.cells), len(spmtx.cells[0]))
    # print(spmtx.raw())
    # active_cell_obj = spmtx.active_cells()
    # active_indx = spmtx.active_indexes()
    # print(active_indx)
    # print(active_indx)
