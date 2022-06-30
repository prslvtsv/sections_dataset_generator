# -*- coding: utf-8 -*-
"""
Created on 22 Jun 2022

@author: prslvtsv
"""
import os
import sys
import copy

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
sys.path.append(PROJECT_ROOT)

from gblock.elements.matrix import SpacialMatrix, rotate_and_reflect
from collections import OrderedDict


class Apartment(SpacialMatrix):
    def __init__(self, padding=(0, 0), parent=None):
        SpacialMatrix.__init__(self, padding)
        self.util = False
        self.parent = parent
        self.attrib = OrderedDict()

    @property
    def tiles(self):
        return self.cells

    def from_tiles(self, tiles):
        indexes = [t.index(glob=True) for t in tiles]
        data = []
        # print(indexes)
        self.from_indexes(indexes, data)
        # print(self.raw())
        tileMatrix = copy.deepcopy(self.raw())
        # print(tileMatrix)
        self.cells = tileMatrix
        self.clear_cell_data()
        return self

    # @tiles.setter
    # def tiles(self, tile):
    #     self.
    # def layout_pos(self):
    #     return self.indexes(glob=True)


class ApartmentTemplate(Apartment):
    def __init__(self):
        Apartment.__init__(self)


class ApartmentDump:
    def __init__(self):
        self.attrib = {}
        self.tiles = None


################################################
################################################
if __name__ == "__main__":
    exactCoverResult = [
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 3), (1, 3), (2, 3), (2, 2)],
        [(1, 0), (1, 1)],
        [(2, 0), (2, 1)],
    ]

    # testTiles = [elements.tile.Tile(), elements.tile.Tile()]
    # [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    # [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

    # [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    # [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]

    # [(0, 0), (0, 1)]
    # [(1, 0), (1, 1)]

    # [(0, 0), (0, 1)]
    # [(2, 0), (2, 1)]

    aparts = []

    import sys
    import pickle

    set_name = "all_read_20220623.apt"
    path = (
        "C:\\Users\\GUEST\\Documents\\CODE\\aective\\sectiondev\\sections_dataset_generator\\_dumps\\"
        + set_name
    )

    with open(path, "rb") as file:
        data = pickle.load(file)

    def print_tile_dump(tile):
        pass

    def print_apt_dump(apt):
        idx = [t.pos for t in apt.tiles]
        # sizes = [(t.size[0] / 1000, t.size[1] / 1000) for t in d.tiles]
        sizes = [t.size for t in apt.tiles]
        # attributes = [t.attrib for t in d.tiles]
        ref = [a.ref for a in apt.tiles]
        apartment = Apartment().from_indexes(idx, sizes)
        print(apartment)
        print(apartment.indexes())
        print()
        # print(apt.raw())
        for k, v in apt.attrib.items():
            print(k, "=", ", ".join(v))
        print(apt.tiles[0].attrib)

        print(ref)

        print()
        print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
        print()
        pass

    for d in data:
        print_apt_dump(d)
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
#%%
