# -*- coding: utf-8 -*-
"""
Created on 15 Jun 2022

@author: prslvtsv
"""
import os
import sys
import copy

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
sys.path.append(PROJECT_ROOT)

from gblock.elements.gtypes import NestedObject, AssemblyBlock
from gblock.elements.matrix import SpacialMatrix
from gblock.elements import tile, apartment

reload(tile)
reload(apartment)
# reload(gblock.elements.tile)
# from gblock.elements.tile import Tile

# reload(Tile)
# reload(SpacialMatrix)
# reload(Apartment)


class FloorLayout(AssemblyBlock):
    def __init__(self, mtx=None, apt=None):
        AssemblyBlock.__init__(self)
        self.matrix = mtx
        self.aptGroups = apt
        self.dispPadding = (0, 0)
        self.spacediv = {}
        self.origin = None

    def from_matrix_tiling(self, matrix, group, origin):
        # grass point3d to coord tuple)
        self.origin = list(origin)
        # assumed matrix contains at cell.data -> (polyline, state)
        llu_gr = group[-1]
        corr_gr = group[-2]
        aparts = group[:-2]
        flaten_idx = sum(group, [])
        # print(llu_gr)
        self.matrix = SpacialMatrix().empty(matrix.shape())

        llu = apartment.Apartment(parent=self).from_indexes(llu_gr)
        llu.util = True
        # print llu.active_indexes()
        for gr in llu.active_cells():
            i, j = gr.index(glob=True)
            # print "glob llu", i, j
            orig = matrix.cells[i][j]
            tileCell = tile.Tile(instance=orig)
            tileCell.parent = llu
            # grass point3d list to coordinates
            tileCell.outline = [[pt.X, pt.Y, pt.Z] for pt in orig.data[0]]
            tileCell.attrib["state"] = orig.data[1]
            ii, jj = gr.index()
            llu.cells[ii][jj] = tileCell
        self.spacediv["llu"] = [llu]

        corr = apartment.Apartment(parent=self).from_indexes(corr_gr)
        corr.util = True
        for gr in corr.active_cells():
            i, j = gr.index(glob=True)
            orig = matrix.cells[i][j]
            tileCell = tile.Tile(instance=orig)
            tileCell.parent = corr
            # grass point3d list to coordinates
            tileCell.outline = [[pt.X, pt.Y, pt.Z] for pt in orig.data[0]]
            tileCell.attrib["state"] = orig.data[1]
            ii, jj = gr.index()
            corr.cells[ii][jj] = tileCell
        self.spacediv["corridor"] = [corr]

        self.spacediv["apartment"] = []
        for agr in aparts:
            apt = apartment.Apartment(parent=self).from_indexes(agr)
            for gr in apt.active_cells():
                i, j = gr.index(glob=True)
                orig = matrix.cells[i][j]
                tileCell = tile.Tile(instance=orig)
                tileCell.parent = apt
                # grass point3d list to coordinates
                tileCell.outline = [[pt.X, pt.Y, pt.Z] for pt in orig.data[0]]
                tileCell.attrib["state"] = orig.data[1]
                ii, jj = gr.index()
                apt.cells[ii][jj] = tileCell
            self.spacediv["apartment"].append(apt)
        return self

    def apt_indexes(self):
        return self.aptGroups

    def display_coords(self):
        return [
            [(x + self.dispPadding[0], y + self.dispPadding[1]) for (x, y) in apt]
            for apt in self.aptGroups
        ]

    def relocate_to(self, location):
        t = (
            location[0] - self.origin[0],
            location[1] - self.origin[1],
            location[2] - self.origin[2],
        )

        for spdiv in self.spacediv:
            for apt in self.spacediv[spdiv]:
                for i, iv in enumerate(apt.cells):
                    for j, jv in enumerate(apt.cells[i]):
                        if apt.cells[i][j].active:
                            for c, cv in enumerate(apt.cells[i][j].outline):
                                # print "bef", apt.cells[i][j].outline[c][0]
                                apt.cells[i][j].outline[c][0] += t[0]
                                # print "aft", apt.cells[i][j].outline[c][0]
                                apt.cells[i][j].outline[c][1] += t[1]
                                apt.cells[i][j].outline[c][2] += t[2]
                        # for i, v in enumerate(apt.cells[r][c].outline):
                        #     print type(apt.cells[r][c].outline[i])
                        #     apt.cells[r][c].outline[i].X += t[0]
                        # apt.cells[r][c].outline[i] = (
                        #     v[0] + t[0],
                        #     v[1] + t[1],
                        #     v[2] + t[2],
                        # )
        return self

    def space_divisions(self):
        # print self.spacediv.values()
        return sum(self.spacediv.values(), [])
