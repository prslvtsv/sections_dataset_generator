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

from gblock.manager.apartment_manager import (
    apartment_catalogue_from_file,
    print_catalogue_info,
)

from gblock.elements.apartment_base_shapes import print_all

"""
- read apartments to apartment library
- group apartments by matrix representation
- read assembly diagrams to assembly diagram library
- solve layout tiling for given flats & assembly diagrams
- validate tiling solutions
- store tiling solutions
- link existing flats to tiling solutions -> generate layouts with apartment outline optins
- generate outline dimensions sets
- rebuild geometry for outlines
- calculate all metrics

- vertical assembly manager
- generate sections

"""

APT_DUMP = "all_read_20220623.apt"
ETALON_TEST_DUMP = "apart_test_etalon_20220711.apt"

if __name__ == "__main__":

    aptcat = apartment_catalogue_from_file(APT_DUMP)
    print_catalogue_info(aptcat, short=False, lim=10)
    print_catalogue_info(aptcat, length=True)

    # print(print_all())
