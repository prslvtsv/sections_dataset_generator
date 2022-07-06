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
