# -*- coding: utf-8 -*-
"""
Created on 22 Jun 2022

@author: prslvtsv
"""
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)

from gblock.elements.matrix import MatrixCell
from gblock.utils.utils import f2s, f2f
import copy


class Tile(MatrixCell):
    def __init__(self, pos=None, parent=None, enable=False, instance=None):
        if instance is None:
            MatrixCell.__init__(self, pos, parent, enable)
        else:
            self._init_from_instance(pos, instance, parent)
        self.typename = "Tile"
        # roomTypes aptName
        self.attrib = {}
        # wc balcony logia terrace
        # DO NOT access directly pls, use methods provided
        self.utils = {}

        self.outline = None
        self.size = (3.3, 6.4)
        self.window = None
        self.door = None

    def _init_from_instance(self, pos, obj, apt):
        # print("inscance creation ", pos)
        MatrixCell.__init__(self, pos, apt, obj.active)

    def outline_xyz(self, as_str=False, closed=False):
        res = None
        if as_str:
            res = [(f2s(x), f2s(y), f2s(z)) for (x, y, z) in self.outline]
        else:
            res = [(f2f(x), f2f(y), f2f(z)) for (x, y, z) in self.outline]

        return res if closed else res[:-1]

    def from_dump(self, tiledump, mm2m=True):
        td = tiledump

        def to_m(mm):
            return f2f(mm * 0.01, 4) if mm2m else f2f(mm, 4)

        # print(td.attrib.keys())
        # print(td.utils.keys())
        self.pos = copy.deepcopy(td.pos)
        self.attrib["roomTypes"] = td.attrib["roomsTypes"]
        self.utils["wc"] = td.utils["wetZone"]
        self.utils["balcony"] = td.utils["balcony"]
        self.utils["logia"] = td.utils["logia"]
        self.utils["terrace"] = td.utils["terrace"]

        self.outline = [tuple([to_m(x), to_m(y), to_m(z)]) for x, y, z in td.outline]
        self.size = tuple([to_m(v) for v in td.size])
        if td.ref["windowPoint"] is not None:
            self.window = tuple([to_m(v) for v in td.ref["windowPoint"]])
        if td.ref["doorPoint"] is not None:
            self.door = tuple([to_m(v) for v in td.ref["doorPoint"]])

        return self

    def has_wc(self):
        return self.utils["wc"]

    def has_balcony(self):
        return self.utils["balcony"]

    def has_logia(self):
        return self.utils["logia"]

    def has_terrace(self):
        return self.utils["terrace"]


class TileDump:
    def __init__(self):
        self.pos = None
        self.attrib = {}
        self.utils = {}
        self.outline = []
        self.size = []
        self.ref = {}


def tile_debug_info(tile):
    pos = "{}:\n        [{}:{}]".format("index", tile.pos[0], tile.pos[1])
    attributes = "\n".join(
        ["      • " + ": ".join([str(k), str(v)]) for k, v in tile.attrib.items()]
    )
    attributes = "attributes: \n" + attributes
    utility = "\n".join(
        ["      • " + ": ".join([str(k), str(v)]) for k, v in tile.utils.items()]
    )
    utility = "utility: \n" + utility
    references = "\n".join(
        ["      • " + ": ".join([str(k), str(v)]) for k, v in tile.ref.items()]
    )
    references = "references: \n" + references
    size = "{}:\n        {},{}".format("size", tile.size[0], tile.size[1])
    outline = [", ".join([f2s(x, 2), f2s(y, 2), f2s(y, 2)]) for x, y, z in tile.outline]
    outline = "outline: \n" + "\n".join(["        ({})".format(o) for o in outline])

    return "\n    ".join(
        [
            "-------------------------------",
            "TILE {} INFO:".format(tile.pos),
            pos,
            attributes,
            utility,
            references,
            size,
            outline,
        ]
    )


################################################
################################################
if __name__ == "__main__":
    tile = Tile()
    tile.clear_data()
