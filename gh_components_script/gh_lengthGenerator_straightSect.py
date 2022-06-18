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


lt = range(min_length, max_length)
lt.reverse()
# length_range_tiles.append(copy.copy(tile_matrix_max))

working = copy.copy(tile_matrix_max)
range_tiles.append(working)
att = copy.copy(attributes_read.splitlines())

attrs.append(replace_attr(att, "length", len(working.data)))

for size in lt:
    if size % 2 == 0:
        w = TileMatrix()
        w.data = working.data[:-1]
        working = w
        range_tiles.append(w)
        attrs.append(replace_attr(att, "length", len(w.data)))
        print len(w.data)

    else:
        w = TileMatrix()
        w.data = working.data[1:]
        working = w
        range_tiles.append(w)
        attrs.append(replace_attr(att, "length", len(w.data)))
        print len(w.data)

attributes_generated = attrs
length_range_tiles = range_tiles
