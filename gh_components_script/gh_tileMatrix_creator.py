# -*- coding: utf-8 -*-
""" OBSOLETE, moved to new matrix logic
@author: prslvtsv
"""
import scriptcontext as sc
import gblock.gh_context.gh_context as context

reload(context)

###############################################################################
# CONTEXT CREATOR BELOW | ADDS DEV METODS TO COMPONENT
# SEE GH_CONTEXT\CONTEXT_GENERAL.TXT FOR DETAILS
###############################################################################
exec(compile("".join(context.init()), "init", "exec"), locals())
###############################################################################

from collections import Counter


class TileMatrix:
    pass


tileMatrixOrdered = []
tileMatrixOrderedBool = []
tileMatrixOrderedShape = []

for i in range(0, 3):
    tileMatrixOrdered.append([])
    tileMatrixOrderedBool.append([])
    tileMatrixOrderedShape.append([])
    for j in range(0, len(tiles_core)):
        tileMatrixOrdered[i].append(None)
        tileMatrixOrderedBool[i].append(0)
        tileMatrixOrderedShape[i].append(0)


out_row = [[] for c in tiles_core]
core_row = [[c.expl_matPos([1, i])] for i, c in enumerate(tiles_core)]
inner_row = [[] for c in tiles_core]

for i, to in enumerate(tiles_out):
    #    print to.UserDictionary.GetString('state')
    to.matPos = [0, map_out[i]]
    out_row[map_out[i]].append(to)

for i, ti in enumerate(tiles_in):
    ti.matPos = [2, map_in[i]]
    inner_row[map_in[i]].append(ti)

matrix = [out_row, core_row, inner_row]

for i, r in enumerate(tileMatrixOrdered[0]):
    if len(out_row[i]) == 0:
        tileMatrixOrdered[0][i] = [None]
    else:
        tileMatrixOrdered[0][i] = out_row[i]
    if len(core_row[i]) == 0:
        tileMatrixOrdered[1][i] = [None]
    else:
        tileMatrixOrdered[1][i] = core_row[i]

    if len(inner_row[i]) == 0:
        tileMatrixOrdered[2][i] = [None]
    else:
        tileMatrixOrdered[2][i] = inner_row[i]

for i, r in enumerate(tileMatrixOrdered):
    for j, rj in enumerate(tileMatrixOrdered[i]):
        tileMatrixOrderedShape[i][j] = len(tileMatrixOrdered[i][j])
        #        for rjk in rj:
        #            print rjk.matPos
        if len(tileMatrixOrdered[i][j]) > 0:
            tileMatrixOrderedBool[i][j] = True
        else:
            tileMatrixOrderedBool[i][j] = False

tmo = TileMatrix()
tmo.data = tileMatrixOrdered

tmos = TileMatrix()
tmos.data = tileMatrixOrderedShape

tmob = TileMatrix()
tmob.data = tileMatrixOrderedBool


flipped_matrix = []

for i, iv in enumerate(tileMatrixOrdered[1]):
    column = [tileMatrixOrdered[0][i], tileMatrixOrdered[1][i], tileMatrixOrdered[2][i]]
    flipped_matrix.append(column)


corner_collapse_tile_idx = None
if Counter(map_out).most_common(1)[0][1] > 1:
    corner_collapse_tile_idx = Counter(map_out).most_common(1)[0][0]

# mid = Counter(map_in).most_common(1)[0][0]


com = TileMatrix()
com.data = flipped_matrix
column_oriented_matrix = com

tiles_ordered_matrix = tmo
tiles_ordered_matrix_shape = tmos
tiles_ordered_matrix_bool = tmob

distribution_anchor_tile_idx = corner_collapse_tile_idx
