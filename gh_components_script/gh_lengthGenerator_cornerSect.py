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
import copy

range_tiles = []
attrs = []


def replace_attr(attr_list, key, val):
    for i, at in enumerate(attr_list):
        if key in at:
            attr_list[i] = "{}:{}".format(key, val)
    return copy.copy(attr_list)


class TileMatrix:
    pass


len_max = len(tile_matrix_max.data)
len_max_left = anchor_max_idx - 1
len_max_right = len_max - (anchor_max_idx + 1)
print len_max_left, " ", len_max_right

len_min = len(tile_matrix_min.data)
len_min_left = anchor_min_idx - 1
len_min_right = len_min - (anchor_min_idx + 1)
print len_min_left, " ", len_min_right

if len_max_left - len_min_left > 0 and len_max_right - len_min_right == 0:
    reduction_steps = range(len_max_left - len_min_left + 1)
elif len_max_left - len_min_left > 0 and len_max_right - len_min_right > 0:
    reduction_steps = [
        range(len_max_left - len_min_left + 1),
        range(-(len_max_right - len_min_right), 0),
    ]

print reduction_steps
att = copy.copy(attributes_read.splitlines())

for step in reduction_steps:
    st = tile_matrix_max.data[step:]
    w = TileMatrix()
    w.data = st
    range_tiles.append(w)
    attrs.append(replace_attr(att, "length", len(w.data)))
    print step
    print st
    print attrs[-1]

attributes_generated = attrs
length_range_tiles = range_tiles
