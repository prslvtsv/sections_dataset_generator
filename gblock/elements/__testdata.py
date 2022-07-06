# -*- coding: utf-8 -*-
"""
Created on 3 Jul 2022

@author: prslvtsv
"""
import os
import sys
import copy
import math

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)
from gblock.utils.utils import f2s, f2f, f2d

mtx_idx = [
    (4, 4),
    (3, 4),
    (1, 3),
    (0, 4),
    (0, 5),
    (0, 3),
    (1, 2),
    (0, 2),
    (1, 1),
    (0, 1),
    (1, 0),
    (0, 0),
    (4, 3),
    (3, 3),
    (2, 3),
    (1, 4),
    (2, 4),
    (4, 2),
    (3, 2),
    (2, 2),
    (2, 0),
    (2, 1),
]
mtx_state = [
    "fixed",
    "fixed",
    "corridor",
    "fixed",
    "fixed",
    "fixed",
    "corridor",
    "free",
    "corridor",
    "free",
    "corridor",
    "free",
    "corridor",
    "corridor",
    "corridor",
    "llu",
    "llu",
    "fixed",
    "custom",
    "custom",
    "custom",
    "custom",
]
tile_crv = [
    [
        ("-683.0641", "242.7886", "0.0000"),
        ("-679.7641", "242.7886", "0.0000"),
        ("-679.7641", "236.1886", "0.0000"),
        ("-683.0641", "236.1886", "0.0000"),
        ("-683.0641", "242.7886", "0.0000"),
    ],
    [
        ("-686.3641", "242.7886", "0.0000"),
        ("-683.0641", "242.7886", "0.0000"),
        ("-683.0641", "236.1886", "0.0000"),
        ("-686.3641", "236.1886", "0.0000"),
        ("-686.3641", "242.7886", "0.0000"),
    ],
    [
        ("-692.9641", "232.8886", "0.0000"),
        ("-690.0141", "232.8886", "0.0000"),
        ("-690.0141", "236.1886", "0.0000"),
        ("-692.9641", "236.1886", "0.0000"),
        ("-692.9641", "232.8886", "0.0000"),
    ],
    [
        ("-692.9641", "236.1886", "0.0000"),
        ("-692.9641", "239.4886", "0.0000"),
        ("-699.5641", "239.4886", "0.0000"),
        ("-699.5641", "236.1886", "0.0000"),
        ("-692.9641", "236.1886", "0.0000"),
    ],
    [
        ("-692.9641", "239.4886", "0.0000"),
        ("-692.9641", "242.7886", "0.0000"),
        ("-699.5641", "242.7886", "0.0000"),
        ("-699.5641", "239.4886", "0.0000"),
        ("-692.9641", "239.4886", "0.0000"),
    ],
    [
        ("-692.9641", "232.8886", "0.0000"),
        ("-692.9641", "236.1886", "0.0000"),
        ("-699.5641", "236.1886", "0.0000"),
        ("-699.5641", "232.8886", "0.0000"),
        ("-692.9641", "232.8886", "0.0000"),
    ],
    [
        ("-692.9641", "228.6886", "0.0000"),
        ("-690.0141", "228.6886", "0.0000"),
        ("-690.0141", "232.8886", "0.0000"),
        ("-692.9641", "232.8886", "0.0000"),
        ("-692.9641", "228.6886", "0.0000"),
    ],
    [
        ("-692.9641", "228.6886", "0.0000"),
        ("-692.9641", "232.8886", "0.0000"),
        ("-699.5641", "232.8886", "0.0000"),
        ("-699.5641", "228.6886", "0.0000"),
        ("-692.9641", "228.6886", "0.0000"),
    ],
    [
        ("-692.9641", "225.3886", "0.0000"),
        ("-690.0141", "225.3886", "0.0000"),
        ("-690.0141", "228.6886", "0.0000"),
        ("-692.9641", "228.6886", "0.0000"),
        ("-692.9641", "225.3886", "0.0000"),
    ],
    [
        ("-692.9641", "225.3886", "0.0000"),
        ("-692.9641", "228.6886", "0.0000"),
        ("-699.5641", "228.6886", "0.0000"),
        ("-699.5641", "225.3886", "0.0000"),
        ("-692.9641", "225.3886", "0.0000"),
    ],
    [
        ("-692.9641", "222.0886", "0.0000"),
        ("-690.0141", "222.0886", "0.0000"),
        ("-690.0141", "225.3886", "0.0000"),
        ("-692.9641", "225.3886", "0.0000"),
        ("-692.9641", "222.0886", "0.0000"),
    ],
    [
        ("-692.9641", "222.0886", "0.0000"),
        ("-692.9641", "225.3886", "0.0000"),
        ("-699.5641", "225.3886", "0.0000"),
        ("-699.5641", "222.0886", "0.0000"),
        ("-692.9641", "222.0886", "0.0000"),
    ],
    [
        ("-683.0641", "232.8886", "0.0000"),
        ("-679.7641", "232.8886", "0.0000"),
        ("-679.7641", "236.1886", "0.0000"),
        ("-683.0641", "236.1886", "0.0000"),
        ("-683.0641", "232.8886", "0.0000"),
    ],
    [
        ("-686.3641", "232.8886", "0.0000"),
        ("-683.0641", "232.8886", "0.0000"),
        ("-683.0641", "236.1886", "0.0000"),
        ("-686.3641", "236.1886", "0.0000"),
        ("-686.3641", "232.8886", "0.0000"),
    ],
    [
        ("-690.0141", "232.8886", "0.0000"),
        ("-686.3641", "232.8886", "0.0000"),
        ("-686.3641", "236.1886", "0.0000"),
        ("-690.0141", "236.1886", "0.0000"),
        ("-690.0141", "232.8886", "0.0000"),
    ],
    [
        ("-692.9641", "242.7886", "0.0000"),
        ("-690.0141", "242.7886", "0.0000"),
        ("-690.0141", "236.1886", "0.0000"),
        ("-692.9641", "236.1886", "0.0000"),
        ("-692.9641", "242.7886", "0.0000"),
    ],
    [
        ("-690.0141", "242.7886", "0.0000"),
        ("-686.3641", "242.7886", "0.0000"),
        ("-686.3641", "236.1886", "0.0000"),
        ("-690.0141", "236.1886", "0.0000"),
        ("-690.0141", "242.7886", "0.0000"),
    ],
    [
        ("-683.0641", "232.8886", "0.0000"),
        ("-679.7641", "232.8886", "0.0000"),
        ("-679.7641", "228.6886", "0.0000"),
        ("-683.0641", "228.6886", "0.0000"),
        ("-683.0641", "232.8886", "0.0000"),
    ],
    [
        ("-686.3641", "228.6886", "0.0000"),
        ("-686.3641", "232.8886", "0.0000"),
        ("-683.0641", "232.8886", "0.0000"),
        ("-683.0641", "228.6886", "0.0000"),
        ("-686.3641", "228.6886", "0.0000"),
    ],
    [
        ("-690.0141", "228.6886", "0.0000"),
        ("-690.0141", "232.8886", "0.0000"),
        ("-686.3641", "232.8886", "0.0000"),
        ("-686.3641", "228.6886", "0.0000"),
        ("-690.0141", "228.6886", "0.0000"),
    ],
    [
        ("-690.0141", "222.0886", "0.0000"),
        ("-690.0141", "225.3886", "0.0000"),
        ("-686.3641", "225.3886", "0.0000"),
        ("-686.3641", "222.0886", "0.0000"),
        ("-690.0141", "222.0886", "0.0000"),
    ],
    [
        ("-690.0141", "225.3886", "0.0000"),
        ("-690.0141", "228.6886", "0.0000"),
        ("-686.3641", "228.6886", "0.0000"),
        ("-686.3641", "225.3886", "0.0000"),
        ("-690.0141", "225.3886", "0.0000"),
    ],
]


class pgp3d:
    def __init__(self, crd):
        x, y, z = crd
        self.X = f2f(float(x), 4)
        self.Y = f2f(float(y), 4)
        self.Z = f2f(float(z), 4)


mtx_tile_crv = [[pgp3d(p) for p in crv] for crv in tile_crv]

mtx_origin = (-699.56412817743194, 242.78855629713451, 0.0)
tiling_a = [
    [(2, 2), (3, 2), (4, 2), (4, 3)],
    [(0, 3), (0, 4), (0, 5)],
    [(0, 1), (0, 2)],
    [(1, 0), (0, 0)],
    [(2, 0), (2, 1)],
    [(4, 4), (3, 4)],
    [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)],
    [(1, 4), (2, 4)],
]
tiling_b = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(4, 2), (4, 3), (4, 4), (3, 4)],
    [(0, 1), (0, 2), (0, 3)],
    [(0, 4), (0, 5)],
    [(3, 2), (2, 2)],
    [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)],
    [(1, 4), (2, 4)],
]
