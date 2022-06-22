#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22 Jun 2022

@author: prslvtsv
"""

from matrix import SpacialMatrix, MatrixCell, rotate_and_reflect


class Apartment(SpacialMatrix):
    def __init__(self, padding=(0, 0)):
        SpacialMatrix.__init__(self, padding)

    def layout_pos(self):
        return self.indexes(glob=True)

    @staticmethod
    def create_empty(shape, padding=(0, 0)):
        mtx = Apartment(padding)
        si, sj = shape
        mtx.cells = []
        for i in range(0, si):
            mtx.cells.append([])
            for j in range(0, sj):
                mtx.cells[i].append(MatrixCell((i, j), mtx))
        return mtx

    @staticmethod
    def create_from_indexes(indxs, data=None):
        iv, jv = [a[0] for a in indxs], [a[1] for a in indxs]
        pnd = (min(iv), min(jv))
        loc_idx = [(i - pnd[0], j - pnd[1]) for (i, j) in indxs]
        bnd = Apartment.bound_indexes(loc_idx)
        shp = Apartment.shape_from_bound(bnd)
        return (
            Apartment.create_empty(shp, pnd)
            .enable_cells_by_indexes(loc_idx)
            .fill_by_indexes(loc_idx, data)
        )

    @staticmethod
    def compare(a, b, mode="exact"):
        def xor_sets(a, b):
            xr = set(a) ^ set(b)
            return len(xr)

        def shape(a, b):
            return True if xor_sets(a.shape(), b.shape()) == 0 else False

        def overlay_exact(a, b):
            return True if xor_sets(a, b) == 0 else False

        def overlay_rotational(a, b):
            rotated = list(rotate_and_reflect(a.active_indexes()))
            result = sum([overlay_exact(r, b.active_indexes()) for r in rotated])
            return True if result >= 1 else False

        # test if
        if mode in "exact":
            return overlay_exact(a, b)
        # test if matrix formation same despite spacial orientation
        if mode in "formation":
            return overlay_rotational(a, b)


# def apart_from_indexes(indexes):
#     return Apartment.create_from_indexes(indexes)


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
        apt = Apartment.create_from_indexes(res)
        aparts.append(apt)
        # print(apt.indexes())
        # print(apt.layout_pos())
        # print()
    ap = aparts[0]
    bp = aparts[-1]

    print(Apartment.compare(ap, bp))
