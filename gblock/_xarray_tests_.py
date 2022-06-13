# -*- coding: utf-8 -*-
"""
Created on Sun May 29 11:06:02 2022

@author: GUEST
"""

import numpy as np
import pandas as pd
import xarray as xr
import attrcnfg as atc


def get_shape_from_dict(attr):
    return [len(a) for a in attr.values()]


attributes = {
    "sectionType": ["90NL", "90NR", "90SL", "90SR", "LLG", "LLT"],
    "tailType": ["closeClose", "closeOpen", "openOpen"],
    "distribution": [0],
    "length": [0, 1, 2, 3, 4, 5],
}
emptyShape = get_shape_from_dict(attributes)

emptyData = np.zeros(emptyShape, dtype=object)


nandata = np.empty(emptyShape, dtype=object)
print(nandata)

for st, stv in enumerate(attributes["sectionType"]):
    for tt, ttv in enumerate(attributes["tailType"]):
        emptyData[st, tt, 0, 0] = "{}.{}.0.0".format(stv, ttv)
# print(emptyData[:, 0, 0, 0])


ep_xr = xr.DataArray(data=emptyData, dims=attributes.keys(), coords=attributes)


section_coord = {
    "sectionType": ["90NL"],
    "tailType": ["closeClose"],
    "distribution": [1],
    "length": [0],
}
section_shape = [len(a) for a in section_coord.values()]
section_data = np.zeros(section_shape, dtype=object)
section_data[0, 0, 0, 0] = "d_insetr"

section_xr = xr.DataArray(
    data=section_data, dims=attributes.keys(), coords=section_coord
)

combined = xr.concat([ep_xr, section_xr], dim="distribution")

print(combined)
