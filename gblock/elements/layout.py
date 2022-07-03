# -*- coding: utf-8 -*-
"""
Created on 15 Jun 2022

@author: prslvtsv
"""
import os
import sys
import copy
import math

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
sys.path.append(PROJECT_ROOT)

from gblock.elements.gtypes import NestedObject, AssemblyBlock
from gblock.elements.matrix import SpacialMatrix
from gblock.elements import tile, apartment, appriser
from gblock.utils.utils import f2s, f2f

reload(tile)
reload(apartment)
reload(appriser)


class FloorLayout(AssemblyBlock):
    def __init__(self, mtx=None, apt=None, parent=None):
        AssemblyBlock.__init__(self, parent)
        self.typename = "FloorLayout"
        self.matrix = mtx
        # floor spacial divisions as apartment objects
        self.spacediv = {}
        # list of xyz
        self.origin = None
        self.metrics = appriser.LayoutAppriser(self)

    def from_matrix_tiling(self, mtx_in, group_in, origin):
        # grass point3d to coord tuple)
        self.origin = list(origin)
        self.matrix = SpacialMatrix().empty(mtx_in.shape())
        # assumed matrix contains at cell.data -> (polyline, state)
        llu_gr = group_in[-1]
        corr_gr = group_in[-2]
        aparts_gr = group_in[:-2]
        flaten_idx = sum(group_in, [])

        # space_group -- list of matrix indexes utility - true if belongs to non residential space groups
        def space_from_group(space_group, mtx_in, sptype, utility=False):
            space = apartment.Apartment(parent=self).from_indexes(space_group)
            space.util = utility
            space.bedrooms = -1
            for gr in space.active_cells():
                i, j = gr.index(glob=True)
                orig = mtx_in.cells[i][j]
                tileCell = tile.Tile(pos=gr.index(), instance=orig, parent=space)
                # tileCell.parent = space
                # tileCell.pos = gr.pos
                tileCell.spaceType = sptype
                # grass point3d list to coordinates
                tileCell.outline = [[pt.X, pt.Y, pt.Z] for pt in orig.data[0]]
                tileCell.attrib["state"] = orig.data[1]

                # if tileCell.attrib["state"] not in ("llu", "corridor"):
                space.bedrooms += 1
                ii, jj = gr.index()
                if ii == 0 and jj == 1:
                    tileCell.wc = True
                else:
                    tileCell.wc = False
                space.cells[ii][jj] = tileCell

            return space

        llu = space_from_group(llu_gr, mtx_in, "llu", True)
        self.spacediv["llu"] = [llu]

        corr = space_from_group(corr_gr, mtx_in, "corridor", True)
        self.spacediv["corridor"] = [corr]

        self.spacediv["apartment"] = []
        for apt_gr in aparts_gr:
            apt = space_from_group(apt_gr, mtx_in, "residential")
            self.spacediv["apartment"].append(apt)

        # update floor layout matrix with new appartment tiles

        for k, v in self.spacediv.items():
            for a, apart in enumerate(self.spacediv[k]):
                for tl in self.spacediv[k][a].active_cells():
                    i, j = tl.index()
                    gi, gj = tl.index(glob=True)
                    self.matrix.cells[gi][gj] = self.spacediv[k][a].cells[i][j]

        # evaluate apartments ratio
        self.metrics.eval_apart_ratio()
        return self

    def relocate_to(self, location):
        # translate vector, relative to origin point
        t = (
            location[0] - self.origin[0],
            location[1] - self.origin[1],
            location[2] - self.origin[2],
        )

        self.origin[0] += t[0]
        self.origin[1] += t[1]
        self.origin[2] += t[2]

        for spdiv in self.spacediv:
            for apt in self.spacediv[spdiv]:
                for i, iv in enumerate(apt.cells):
                    for j, jv in enumerate(apt.cells[i]):
                        if apt.cells[i][j].active:
                            for c, cv in enumerate(apt.cells[i][j].outline):
                                apt.cells[i][j].outline[c][0] += t[0]
                                apt.cells[i][j].outline[c][1] += t[1]
                                apt.cells[i][j].outline[c][2] += t[2]
        return self

    def get_apartments(self):
        return self.spacediv["apartment"]

    def get_corridor(self):
        return self.spacediv["corridor"]

    def get_llu(self):
        return self.spacediv["llu"]

    def get_wc_tiles(self):
        apt = self.get_apartments()
        crv = [c.outline for c in apt.active_cells() if c.wc]
        return crv

    def get_xy_size(self):
        tl = [cell.outline_xyz(as_str=True) for cell in self.matrix.active_cells()]
        str_coords = set(sum(tl, []))
        crd_x = [float(x) for (x, y, z) in str_coords]
        crd_y = [float(y) for (x, y, z) in str_coords]
        bnd_x = abs(max(crd_x) - min(crd_x))
        bnd_y = abs(max(crd_y) - min(crd_y))
        print bnd_x, bnd_y
        return (bnd_x, bnd_y)

    # def space_divisions(self):
    #     # print self.spacediv.values()
    #     return sum(self.spacediv.values(), [])
