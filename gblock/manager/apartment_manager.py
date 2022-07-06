# -*- coding: utf-8 -*-
"""
Created on 03 Jul 2022

@author: prslvtsv
"""
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)

from gblock.elements.apartment import Apartment, ApartmentTemplate, ApartmentDump
from gblock.elements.apartment import apart_dump_debug_info, matrix_from_dump
from gblock.elements.tile import tile_debug_info
import gblock.elements.apartment_base_shapes as baseShape
from collections import OrderedDict
import pickle


def read_apt_dump(filename):
    dir = os.path.dirname(__file__)
    p = os.path.join(dir, os.pardir, os.pardir, "_dumps\\", filename)
    path = os.path.abspath(p)
    data = None
    with open(path, "rb") as file:
        data = pickle.load(file)
    return data


def group_apt_dump_by_shape(shapes, aparts):
    apt_groups = OrderedDict()
    for shape in shapes:
        apt_groups[shape.name] = []

    for apt in aparts:
        for shape in shapes:
            if shape.has_same_shape(matrix_from_dump(apt)):
                apt_groups[shape.name].append(apt)
    return apt_groups


if __name__ == "__main__":
    # test functionality

    apt_dumps = read_apt_dump("all_read_20220623.apt")
    apt_shapes = baseShape.UP_TO_3

    apartments = [Apartment().from_dump(ad) for ad in apt_dumps]
    apt_groups = group_apt_dump_by_shape(apt_shapes, apt_dumps)

    for n in apt_groups.keys():
        print(n, len(apt_groups[n]))

    # print(apart_dump_debug_info(apt_dumps[100], True, True, True, True))
