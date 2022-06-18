# -*- coding: utf-8 -*-
"""
@author: prslvtsv
"""
import scriptcontext as sc
import gblock.gh_context.gh_context as context

reload(context)

###############################################################################
# CONTEXT CREATOR BELOW | ADDS DEV METODS TO COMPONENT
# SEE GH_CONTEXT\CONTEXT_GENERAL.TXT FOR DETAILS
###############################################################################
exec (compile("".join(context.init()), "init", "exec"), locals())
###############################################################################

from collections import OrderedDict


def parse_params(param):
    # print param
    dimNames = np.array([att.name for att in param])
    dimDepth = np.array([len(att.options) for att in param])
    # print dimNames
    # print dimDepth

    crd = []
    for att in param:
        #
        #        for o in att.options:
        #            print (att.name + " " + o.value + " " + str(len(att.options)))
        #        print ()
        crd.append([opt.value for opt in att.options])
    coord = np.array(crd, dtype="object")
    indx = (-dimDepth).argsort()
    # print(dimDepth)
    # print(coord[indx].tolist())

    return dimNames, dimDepth, coord, indx
    # return dimNames[indx], dimDepth[indx], coord[indx], indx


axis, dim, crd, sortidx = parse_params(attr_glob)
attrs = [str(a) for a in axis]


def make_selector_at(i):
    return dict(OrderedDict(zip(attrs, [str(c[i]) for c in crd])))


emptyDataStruct = np.zeros(dim, dtype=np.object)


database = emptyDataStruct
shape = [int(dim) for dim in emptyDataStruct.shape]

coordinates = OrderedDict(zip(attrs, [[str(c) for c in cc] for cc in crd]))
print coordinates
xrDataBase = xr.DataArray(data=emptyDataStruct, coords=dict(coordinates), dims=attrs)
# print type(make_selector_at(0)['corridorWidth'])
# print xrDataBase[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# xrDataBase.loc[make_selector_at(0)] = 'jsdfskljdn'
# print xrDataBase.loc[make_selector_at(0)]

database = xrDataBase
