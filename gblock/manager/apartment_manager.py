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
import copy
import pickle

APT_DUMP = "all_read_20220623.apt"
ETALON_TEST_DUMP = "apart_test_etalon_20220711.apt"


def read_apt_dump(filename):
    dir = os.path.dirname(__file__)
    p = os.path.join(dir, os.pardir, os.pardir, "_dumps\\", filename)
    path = os.path.abspath(p)
    data = None
    with open(path, "rb") as file:
        data = pickle.load(file)
    return data


def group_apartments_by_shape(shapes, aparts):
    apt_groups = OrderedDict()
    # for shape in shapes:
    #     apt_groups[shape.name] = []

    for apt in aparts:
        for shape in shapes:
            if shape.has_same_shape(apt):
                if shape.name not in apt_groups.keys():
                    apt_groups[shape.name] = []
                apt.shapeType = " ".join([shape.name, str(len(apt_groups[shape.name]))])
                apt_groups[shape.name].append(copy.deepcopy(apt))
    return apt_groups


def print_catalogue_info(groups, short=False, lim=-1, length=False):
    if length:
        res = []
        for n in groups.keys():
            res.append(" ".join([n, str(len(groups[n]))]))
        print("\n".join(res))
        return True
    for k, v in groups.items():
        l = len(v) if lim == -1 else lim
        for i in range(l):
            if i >= len(v):
                continue
            print(k, i)
            if short:
                print(v[i].info(info=False, short=True))
            else:
                print(v[i].info(info=True, attr=True, tile=True))


def apartment_catalogue_from_file(filename, mm2m=False):
    apt_dumps = read_apt_dump(filename)
    apt_shapes = baseShape.ALL

    apartments = [Apartment().from_dump(ad, mm2m=mm2m) for ad in apt_dumps]
    return group_apartments_by_shape(apt_shapes, apartments)


#
# def apartment_catalogue_from_data(data, tometers=True):
#     apt_dumps = data
#     apt_shapes = baseShape.UP_TO_3
#
#     apartments = [Apartment().from_dump(ad, mm2m=tometers) for ad in apt_dumps]
#     return group_apartments_by_shape(apt_shapes, apartments)


if __name__ == "__main__":
    # test functionality

    aptcat = apartment_catalogue_from_file(ETALON_TEST_DUMP)
    print_catalogue_info(aptcat, short=True, lim=1)
    # print_catalogue_info(aptcat, short=False)
    # print(v[i].info(info=False, matrix=True, attr=False, tile=False))
    # print(apart_dump_debug_info(apt_dumps[100], True, True, True, True))
