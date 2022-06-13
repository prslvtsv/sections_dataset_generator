# -*- coding: utf-8 -*-
"""
Created on 15 May

@author: prslvtsv
"""

import attributes as att
import core as core

import numpy as np
import pandas as pd
import xarray as xr

reload(att)
reload(core)


def test_creation():
    x = xr.DataArray(np.random.randn(2, 3), coords={"x": ["a", "b"]}, dims=("x", "y"))
    print x


def shape_array():
    pass
