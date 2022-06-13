# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import xarray as xr
import attrcnfg as acfg
import datacompute as dc


def parse_params(param):
    dimNames = np.array([att["name"] for att in param.values()])
    dimDepth = np.array([len(att["options"]) for att in param.values()])

    crd = []
    for att in param.values():

        for o in att["options"]:
            print(att["name"] + " " + o["value"] + " " + str(len(att["options"])))
        print()
        crd.append([opt["value"] for opt in att["options"]])
    coord = np.array(crd, dtype="object")
    indx = (-dimDepth).argsort()
    # print(dimDepth)
    # print(coord[indx].tolist())

    return dimNames[indx], dimDepth[indx], coord[indx]


axis, dim, crd = parse_params(acfg.attrFloorUser)
# print(axis, dim, crd)

emptyDataStruct = np.zeros(dim, dtype=np.object)
cartesianProduct = np.array(dc.cartesian_py(crd.tolist(), len(crd)))
# print(axis)
# coordDict = {}
# for c in crd:
#     coordDict[]
#     print(crd)

# {dict(zip(axis.tolist(), crd.tolist()))}
# print(coordDict)
# print (dim)

b = emptyDataStruct[slice, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(b)
# xbase = xr.DataArray(data=emptyDataStruct, coords=coordDict, dims=axis)
