# -*- coding: utf-8 -*-
"""Inner code from ghPython component sorting generated floors and growing trees along axis
Creates tree structures to represent generated floors geometry

Inputs:
    attributes_existing([str, ...]): <ListAccess>, flat list of existing floors attributes
    dimensions_along([str, ...]): <ListAccess>, names of attibutes to sort along

Outputs:
    filter_dict: mapping filter
    filter_indexes(gh_tree): branch per attribute, tree indexes correspongin to attr values
    key_tree
    none_tree
    zero_tree

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

import ghpythonlib.treehelpers as th
from collections import OrderedDict as oddict
from operator import itemgetter

shape = []
val_shape = oddict()
dimensionValues = oddict()

for dim in dimensions_along:
    dimensionValues[dim] = []

for att in attributes_existing:
    at = dict([a.split(":") for a in att.splitlines()])
    for dim in dimensions_along:
        dimensionValues[dim].append(at[dim])

for k, v in dimensionValues.items():
    if k in "length":
        dim_keys = dict([[a, int(a)] for a in v])
    #    elif k in 'distribution':
    #        dim_keys = dict([a.split('/') for a in v])
    else:
        dim_keys = dict([[a, a] for a in v])

    dim_keys = oddict(sorted(dim_keys.items(), key=itemgetter(1)))
    print dim_keys
    #    if k in 'length':
    #        dim_keys = oddict(reversed(list(dim_keys.items())))
    dim_shape = oddict()
    for dk in dim_keys.keys():
        dim_shape[dk] = v.count(dk)
    val_shape[k] = dim_shape

shape = [len(v.values()) for v in val_shape.values()]
print shape

# for k, v in val_shape.items():
#    val_shape[k] = oddict(sorted(v.items(), key=itemgetter(1)))
# print val_shape

# magic happens here
# recursive nesting
def nest_down(lst, lvl, empty):
    #    print lst[lvl]
    if lvl + 1 >= len(lst):
        if not empty:
            return [[k for vv in range(v)] for k, v in lst[lvl].items()]
        else:
            return [[None for vv in range(v)] for k, v in lst[lvl].items()]
    return [nest_down(lst, lvl + 1, empty) for l in range(len(lst[lvl]))]


def nest_down_zeros(lst, lvl, empty):
    #    print lst[lvl]
    if lvl + 1 >= len(lst):
        return [[0 for vv in range(v)] for k, v in lst[lvl].items()]
    return [nest_down_zeros(lst, lvl + 1, empty) for l in range(len(lst[lvl]))]


# print val_shape.values()
nestedKey = nest_down(val_shape.values(), 0, False)
nestedNone = nest_down(val_shape.values(), 0, True)
nestedZeros = nest_down_zeros(val_shape.values(), 0, True)
# print nestedZeros
# print np.array(nestedNone).shape
# print val_shape

mapping = []
mapping_dict = oddict()
for vs in val_shape.values():
    mapping.append(["{}:{}".format(k, i) for i, k in enumerate(vs.keys())])
    for i, k in enumerate(vs.keys()):
        mapping_dict[k] = i

# def p(a):
#    print a
# [p(vsk)for vsk, vsv in val_shape.items()]
key_tree = th.list_to_tree(nestedKey, True)
none_tree = th.list_to_tree(nestedNone, True)
zero_tree = th.list_to_tree(nestedZeros, True)

filter_indexes = th.list_to_tree(mapping, True)
filter_dict = [mapping_dict]
