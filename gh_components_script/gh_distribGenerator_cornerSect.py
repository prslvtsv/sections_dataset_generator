# -*- coding: utf-8 -*-
"""
@author: prslvtsv
"""
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import gblock.gh_context.gh_context as context
import copy

reload(context)

###############################################################################
# CONTEXT CREATOR BELOW | ADDS DEV METODS TO COMPONENT
# SEE GH_CONTEXT\CONTEXT_GENERAL.TXT FOR DETAILS
###############################################################################
exec(compile("".join(context.init()), "init", "exec"), locals())
###############################################################################
def replace_attr(attr_list, key, val):
    for i, at in enumerate(attr_list):
        if key in at:
            attr_list[i] = "{}:{}".format(key, val)
    return copy.copy(attr_list)


class TileMatrix:
    pass


master_distr = TileMatrix()
master_distr.data = copy.copy(left_length_tiles[0].data)
right_section = right_length_tiles[0].data[-(len(right_length_tiles)) :]
right_s = copy.copy(right_length_tiles[0].data[-(len(right_length_tiles)) :])
a = []

for i, rt in enumerate(right_section):
    for j, crv in enumerate(right_section[i]):

        newpl = []
        for inx, pt in enumerate(right_section[i][j][0].ghGeo.ToPolyline()):
            newpl.append(rg.Point3d(pt.X + move_v.X, pt.Y + move_v.Y, 0))

        t = core.Tile(
            ghGeo=rg.PolylineCurve(newpl),
            state=copy.copy(right_section[i][j][0].state),
            app=right_section[i][j][0].appNumber,
        )
        right_s[i][j][0] = t
        a.append(right_s[i][j][0].ghGeo)
    #    print rt[0][0].ghGeo.Translate(rg.Vector3d(0,0,0))
    master_distr.data.append(right_s[i])

# print master_distr.data

step_range = [range(len(left_length_tiles)), range(len(right_length_tiles) + 1)]
# print step_range

attrs = []
dr = []
att = copy.copy(attributes.splitlines())

for i in step_range[0]:
    for j in step_range[1]:
        if j == 0:
            st = master_distr.data[i:]
        else:
            st = master_distr.data[i:-j]
        if len(st) > max_length:
            continue

        w = TileMatrix()
        w.data = st
        dr.append(w)
        at = replace_attr(att, "length", len(w.data))
        attrs.append(replace_attr(at, "distribution", "{}/{}".format(i, j)))


distribution_range = dr
attributes_generated = attrs
