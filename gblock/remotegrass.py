# -*- coding: utf-8 -*-
"""

🔸 intended for use with gh-python-remote CPython 2.7 🔸

Created on 18 May 2022

@author: prslvtsv
"""
import numpy as np
import pandas as pd
import xarray as xr
import attrcnfg as acfg


def test_method():
    return "string from py"


def parse_params(param):
    dimNames = np.array([att["name"] for att in param.values()])
    dimDepth = np.array([len(att["options"]) for att in param.values()])

    crd = []
    for att in param.values():

        for o in att["options"]:
            print (att["name"] + " " + o["value"] + " " + str(len(att["options"])))
        print ()
        crd.append([opt["value"] for opt in att["options"]])
    coord = np.array(crd, dtype="object")
    indx = (-dimDepth).argsort()
    # print(dimDepth)
    # print(coord[indx].tolist())

    return dimNames[indx], dimDepth[indx], coord[indx]


def concentrateInputs():
    unset = "•"
    value = unset
    res = []
    for i in range(2, ghenv.Component.Params.Input.Count):
        print i
        name = attr_list[i].nameCode
        data = ghenv.Component.Params.Input[i].VolatileData

        if data.IsEmpty():
            value = unset
            print "unset"
    #        else:
    #            for idx, opt in enumerate(attr_list[i-2].options):
    #                print opt
    #                if opt.value == data.Branches[0][0].Value:
    #                    value = '{}||{}'.format(idx, opt.value)
    #                    print value

    print res
    return res


def cartesianProduct(set_a, set_b):
    result = []
    for i in range(0, len(set_a)):
        for j in range(0, len(set_b)):

            # for handling case having cartesian
            # product first time of two sets
            if type(set_a[i]) != list:
                set_a[i] = [set_a[i]]

            # coping all the members
            # of set_a to temp
            temp = [num for num in set_a[i]]

            # add member of set_b to
            # temp to have cartesian product
            temp.append(set_b[j])
            result.append(temp)

    return result


def cartesian_py(list_a, n):
    # result of cartesian product
    # of all the sets taken two at a time
    temp = list_a[0]

    # do product of N sets
    for i in range(1, n):
        temp = cartesianProduct(temp, list_a[i])

    # print(temp)
    return temp
