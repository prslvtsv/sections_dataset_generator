# -*- coding: utf-8 -*-
"""
Created on 22 Jun 2022

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

from gblock.elements.matrix import SpacialMatrix, rotate_and_reflect
from gblock.elements.tile import Tile, tile_debug_info
from gblock.utils.utils import f2s, f2f
from collections import OrderedDict


class Apartment(SpacialMatrix):
    def __init__(self, padding=(0, 0), parent=None, spaceType=""):
        SpacialMatrix.__init__(self, padding)
        self.typename = "Apartment"
        self.encoding = None
        # true if this apartment represents unitily space (llu, corridor, etc)
        self.util = False
        self.parent = parent
        self.attrib = OrderedDict()
        self.spaceType = spaceType
        self.bedrooms = 0

    @property
    def tiles(self):
        return self.cells

    def tiles_outline(self):
        return [cell.outline for cell in self.active_cells()]

    def from_dump(self, dump, mm2m=True):
        ad = dump.attrib
        indexes = [a.pos for a in dump.tiles]
        self.from_indexes(indexes)

        def to_m(mm):
            return f2f(mm * 0.01, 4) if mm2m else f2f(mm, 4)

        self.typename = "Catalogue_Apartment"
        self.spaceType = "residential"
        self.encoding = ad["Name"][0]
        self.attrib["unitLocation"] = copy.deepcopy(ad["UnitLocation"])
        self.attrib["kitchenType"] = copy.deepcopy(ad["KitchenType"])
        self.attrib["bathroomType"] = copy.deepcopy(ad["BathroomType"])
        self.attrib["blockingType"] = copy.deepcopy(ad["BlockingType"])
        self.attrib["mirrorWidth"] = ad["MirroredByWidthAxis"][0] not in "n"
        self.attrib["mirrorDepth"] = ad["MirroredByDepthAxis"][0] not in "n"
        rnumb = 0
        try:
            rnumb = int(ad["RoomsNumber"][0])
        except:
            pass
        # print("room numb", )
        self.bedrooms = rnumb

        for td in dump.tiles:
            tile = Tile(pos=td.pos, parent=self, enable=True).from_dump(td)
            self.cells[tile.index()[0]][tile.index()[1]] = tile

        return self

    @property
    def depth(self):
        return max(set([c.size[1] in self.active_cells()]))

    # @property
    # def width(self):
    #     return sum([c.size[0] in self.active_cells()])

    def tiles_sizes(self):
        cells = self.active_cells()
        return list(zip([c.size in cells], [c.index() in cells]))

    def generate_outline(self):
        def sh_str(fl):
            n = str(math.trunc(round(fl * 100)))
            if n not in "0":
                n = ".".join([n[:-2], n[-2:]])
            return n

        tl = [
            [(sh_str(x), sh_str(y), sh_str(z)) for (x, y, z) in cl.outline]
            for cl in self.active_cells()
        ]
        # print tl
        str_coords = set(sum(tl, []))
        # print str_coords
        coords = [((float(x), float(y), float(z))) for (x, y, z) in str_coords]
        display_mtx = SpacialMatrix().from_coordinates(coords)
        # print display_mtx.shape()
        b_out, b_in = display_mtx.get_matrix_boundary_indeces()
        # print [c.data for c in display_mtx.cells_at(b_out)]
        return [c.data for c in display_mtx.cells_at(b_out)]


class ApartmentTemplate(Apartment):
    def __init__(self):
        Apartment.__init__(self)
        self.typename = "ApartmentTemplate"


class ApartmentDump:
    def __init__(self):
        self.attrib = {}
        self.tiles = None


def matrix_from_dump(dump):
    return SpacialMatrix().from_indexes([d.pos for d in dump.tiles])


def apart_dump_debug_info(apt, info=True, matrix=True, attr=False, tile=False):
    res = []
    res.append("▔".ljust(100, "▔"))

    label = "APT DUMP INFO:\n    {}".format(apt.attrib["Name"][0])
    mtx = SpacialMatrix().from_indexes([a.pos for a in apt.tiles])
    mtx = "\n".join(["    " + l for l in repr(mtx).splitlines()])
    indexes = ", ".join(["{}:{}".format(a.pos[0], a.pos[1]) for a in apt.tiles])
    indexes = "    indexes: \n        " + indexes
    attributes = "\n".join(
        ["      • " + ": ".join([str(k), str(v)]) for k, v in apt.attrib.items()]
    )
    attributes = "    apt attributes: \n" + attributes
    tiles = [tile_debug_info(t) for t in apt.tiles]
    if info:
        res.append(label + "\n")
        res.append(indexes + "\n")
    if matrix:
        res.append(mtx + "\n")
    if attr:
        res.append(attributes)
    if tile:
        res.extend(tiles)
    res.append("▁".ljust(100, "▁"))
    return "\n".join(res)


################################################
################################################
if __name__ == "__main__":

    # exactCoverResult = [
    #     [(0, 0), (0, 1), (0, 2), (1, 2)],
    #     [(0, 3), (1, 3), (2, 3), (2, 2)],
    #     [(1, 0), (1, 1)],
    #     [(2, 0), (2, 1)],
    # ]
    #
    # # testTiles = [elements.tile.Tile(), elements.tile.Tile()]
    # # [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    # # [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    #
    # # [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    # # [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]
    #
    # # [(0, 0), (0, 1)]
    # # [(1, 0), (1, 1)]
    #
    # # [(0, 0), (0, 1)]
    # # [(2, 0), (2, 1)]
    #
    # aparts = []
    #
    # import sys
    # import pickle
    #
    # set_name = "all_read_20220623.apt"
    # path = (
    #     "C:\\Users\\GUEST\\Documents\\CODE\\aective\\sectiondev\\sections_dataset_generator\\_dumps\\"
    #     + set_name
    # )
    #
    # with open(path, "rb") as file:
    #     data = pickle.load(file)
    #
    # def print_tile_dump(tile):
    #     pass
    #
    # def print_apt_dump(apt):
    #     idx = [t.pos for t in apt.tiles]
    #     # sizes = [(t.size[0] / 1000, t.size[1] / 1000) for t in d.tiles]
    #     sizes = [t.size for t in apt.tiles]
    #     # attributes = [t.attrib for t in d.tiles]
    #     ref = [a.ref for a in apt.tiles]
    #     apartment = Apartment().from_indexes(idx, sizes)
    #     print(apartment)
    #     print(apartment.indexes())
    #     print()
    #     # print(apt.raw())
    #     for k, v in apt.attrib.items():
    #         print(k, "=", ", ".join(v))
    #     print(apt.tiles[0].attrib)
    #
    #     print(ref)
    #
    #     print()
    #     print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
    #     print()
    #     pass
    #
    # for d in data:
    #     print_apt_dump(d)
    # for res in exactCoverResult:

    # apt = Apartment().from_indexes(res)
    # aparts.append(apt)
    # testTiles.append(apt.cells)
    # print(apt.active_cells())
    # print(apt.cells)
    # aptTempl = ApartmentTemplate().from_tiles(apt.cells_list())
    # print(aptTempl)
    #     print(apt.indexes(glob=True))
    #     print(apt.tiles)
    #     print("_____________")
    #     print()
    # ap = aparts[0]
    # bp = aparts[1]
    # print(Apartment.compare(ap, bp, mode="formation"))

    # print(testTiles)
    pass
