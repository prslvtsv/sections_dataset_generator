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
from gblock.utils.utils import f2s, f2f, printeach, printlines
from gblock.utils.xyz import XYZ
import gblock.elements.__testdata as td

# reload(td)
# reload(tile)
# reload(apartment)
# reload(appriser)


class FloorLayout(AssemblyBlock):
    def __init__(self, mtx=None, apt=None, parent=None):
        AssemblyBlock.__init__(self, parent)
        self.typename = "FloorLayout"
        self.matrix = mtx
        # floor spacial divisions as apartment objects
        self.spacediv = {}
        # list of xyz
        self.origin = XYZ()
        self.metrics = appriser.LayoutAppriser(self)

    def from_matrix_tiling(self, mtx_in, group_in, origin):
        # grass point3d to coord tuple)
        try:
            self.origin = XYZ(origin.X, origin.Y, origin.Z)
        except:
            self.origin = XYZ(xyz=origin)
        self.matrix = SpacialMatrix().empty(mtx_in.shape())
        # assumed matrix contains at cell.data -> (polyline, state)
        llu_gr = group_in[-1]
        corr_gr = group_in[-2]
        aparts_gr = group_in[:-2]
        # print("group_in ", group_in)
        flaten_idx = sum(group_in, [])

        # space_group -- list of matrix indexes utility - true if belongs to non residential space groups
        def space_from_group(space_group, mtx_in, sptype, utility=False):
            space = apartment.Apartment(parent=self, spaceType=sptype).from_indexes(
                space_group
            )
            space.util = utility
            space.bedrooms = -1
            for gr in space.active_cells():
                i, j = gr.index(glob=True)

                orig = mtx_in.cells[i][j]
                tileCell = tile.Tile(pos=gr.index(), instance=orig, parent=space)

                tileCell.spaceType = sptype

                tileCell.outline = [XYZ(pt.X, pt.Y, pt.Z) for pt in orig.data[0]]
                tileCell.attrib["state"] = orig.data[1]

                # change later, just sample
                space.bedrooms += 1
                ii, jj = gr.index()

                # change later, just sample
                if ii == 0 and jj == 0 and not utility:
                    tileCell.utils["wc"] = True
                else:
                    tileCell.utils["wc"] = False
                # finally assign new tile cell to space cells
                space.cells[ii][jj] = tileCell
            return space

        self.spacediv["llu"] = []
        llu = space_from_group(llu_gr, mtx_in, "llu", True)
        self.spacediv["llu"].append(llu)

        self.spacediv["corridor"] = []
        corr = space_from_group(corr_gr, mtx_in, "corridor", True)
        self.spacediv["corridor"].append(corr)

        self.spacediv["apartment"] = []
        for apt_gr in aparts_gr:
            apt = space_from_group(apt_gr, mtx_in, "residential", False)
            self.spacediv["apartment"].append(apt)
        # update floor layout matrix with new appartment tiles

        for k, v in self.spacediv.items():
            for a, apart in enumerate(self.spacediv[k]):
                for tl in self.spacediv[k][a].active_cells():
                    i, j = tl.index()
                    gi, gj = tl.index(glob=True)
                    self.matrix.cells[gi][gj] = self.spacediv[k][a].cells[i][j]
        # evaluate apartments ratio
        self.metrics.apprise()
        return self

    def relocate_to(self, location):
        t = XYZ()
        try:
            t = XYZ(location.X, location.Y, location.Z)
        except:
            if len(location) == 3:
                t = XYZ(xyz=location)
            elif len(location) == 2:
                t = XYZ(location[0], location[1])
        for spdiv in self.spacediv:
            for apt in self.spacediv[spdiv]:
                for i, iv in enumerate(apt.cells):
                    for j, jv in enumerate(apt.cells[i]):
                        if apt.cells[i][j].active:
                            for c, cv in enumerate(apt.cells[i][j].outline):
                                o = self.origin
                                l = apt.cells[i][j].outline[c]
                                apt.cells[i][j].outline[c] = XYZ.translate(l, t, o)
        return self

    def get_apartments(self):
        return self.spacediv["apartment"]

    def get_corridor(self):
        return self.spacediv["corridor"]

    def get_llu(self):
        return self.spacediv["llu"]

    def get_space_div(self):
        return sum(self.spacediv.values(), [])

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
        # print bnd_x, bnd_y
        return (bnd_x, bnd_y)

    # def _debug_clor_print(self):
    #     si, sj = self.matrix.shape()
    #     for j in sorted(range(sj), reverse=True):
    #         for i in range(si):
    #             cell = self.matrix.cells[i][j]
    #             apt = cell.parent.count_active()
    #
    #             if cell.active:
    #                 # print(cell.parent.spaceType)
    #                 if cell.parent.spaceType in "llu":
    #                     print("🟩", end="")
    #                 elif cell.parent.spaceType in "corridor":
    #                     print("⬛", end="")
    #                 else:
    #                     print(cell.get_color(apt), end="")
    #             else:
    #                 print(cell.get_color(apt), end="")
    #         print(" ", end="")
    #         for i in range(si):
    #             cell = self.matrix.cells[i][j]
    #             apt = cell.parent.count_active()
    #             print("".join([str(apt).rjust(2, " "), "|"]), end="")
    #         print(" ", end="")
    #         for i in range(si):
    #             cell = self.matrix.cells[i][j]
    #             apt = cell.parent.count_active()
    #             print("".join(["{}:{}".format(i, j), "|",]), end="")
    #             # {}:{}".format(cell.index()[0], cell.index()[1]),
    #         print(" ", end="")
    #         for i in range(si):
    #             cell = self.matrix.cells[i][j]
    #             apt = cell.parent.typename
    #             print(cell.parent.typename[:2], end=" ")
    #         print("\n", end="")

    def color_matrix_lines(self):
        si, sj = self.matrix.shape()
        lines = []
        for j in sorted(range(sj), reverse=True):
            line = []
            line.append(str(j) + " ")
            for i in range(si):
                cell = self.matrix.cells[i][j]
                apt = cell.parent.count_active()

                pointer = cell.get_color(apt)
                if cell.active and cell.parent.spaceType in "llu":
                    pointer = "🟩"
                if cell.active and cell.parent.spaceType in "corridor":
                    pointer = "⬛"
                line.append(pointer)
            line = "".join(line) + "  "
            lines.append(line)
            # "‥.‥"
        # lines.append("   " + " ".join([str(r) for r in range(si)]))
        # lines = "\n".join(lines)
        return lines

    def color_wc_lines(self):
        si, sj = self.matrix.shape()
        lines = []
        for j in sorted(range(sj), reverse=True):
            line = []
            # line.append(str(j) + " ")
            for i in range(si):
                cell = self.matrix.cells[i][j]
                # apt = cell.parent.count_active()
                # wc = cell.has_wc()
                pointer = "⬜"
                if cell.active and cell.has_wc():
                    pointer = "🟦"
                elif cell.active:
                    pointer = "⬛"
                line.append(pointer)
            line = "".join(line) + "  "
            lines.append(line)
            # "‥.‥"
        # lines.append("   " + " ".join([str(r) for r in range(si)]))
        # lines = "\n".join(lines)
        return lines

    def print_info_color(self):
        rlen = 80
        rows = []
        matrix = [
            "".join(l) for l in zip(self.color_matrix_lines(), self.color_wc_lines())
        ]
        rows.append("▔".ljust(rlen, "▔"))
        rows.extend(matrix)
        # rows.extend(self.color_matrix_lines())
        rows.append("▁".ljust(rlen, "▁"))

        appr = self.metrics.aprt(mode=".0000").splitlines()
        spacer = "".join([" " for i in range(len(appr[0]))])
        for i, l in enumerate(rows):
            if i == 0 or i == len(rows) - 1:
                continue
            idx = [ii for ii, jj in enumerate(appr)]
            if i - 1 in idx:
                rows[i] += appr[i - 1]
                rows[i] += "  "
            else:
                rows[i] += spacer
                rows[i] += "  "
        # #
        appr = self.metrics.aprt(mode="bednum").splitlines()
        spacer = "".join([" " for i in range(len(appr[0]))])
        for i, l in enumerate(rows):
            if i == 0 or i == len(rows) - 1:
                continue
            idx = [ii for ii, jj in enumerate(appr)]
            if i - 1 in idx:
                rows[i] += appr[i - 1]
                rows[i] += "  "
            else:
                rows[i] += spacer
                rows[i] += "  "
        # # print(len(appr))
        pr = "\n".join(rows)
        print(pr)


################################################
################################################
if __name__ == "__main__":
    mtx_data = list(zip(td.mtx_tile_crv, td.mtx_state))
    mtx = SpacialMatrix().from_indexes(td.mtx_idx, data=mtx_data)
    # print("td tiling ", td.tiling_a)
    flt_a = FloorLayout().from_matrix_tiling(mtx, td.tiling_b, td.mtx_origin)
    flt_b = FloorLayout().from_matrix_tiling(mtx, td.tiling_a, td.mtx_origin)
    flt_a.relocate_to((0, 0, 0))
    # print(mtx)
    # print(" ")
    for i in range(100):
        flt_a.print_info_color()
        flt_b.print_info_color()
    # print(len(flt_a.get_llu()), len(flt_a.get_corridor()), len(flt_a.get_apartments()))
    # ll = sum([a.count_active() for a in flt_a.get_llu()])
    # lc = sum([a.count_active() for a in flt_a.get_corridor()])
    # la = sum([a.count_active() for a in flt_a.get_apartments()])
    # print(sum([ll, lc, la]), flt_a.matrix.count_active())
    # printlines(flt_a.spacediv.values())
    # space = sum(flt_a.spacediv.values(), [])
    # printlines([repr(a) for a in space])
    # def space_divisions(self):
    #     # print self.spacediv.values()
    #     return sum(self.spacediv.values(), [])
