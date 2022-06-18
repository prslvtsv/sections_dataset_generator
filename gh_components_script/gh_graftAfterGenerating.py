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

import ghpythonlib.treehelpers as th
import Rhino


class TileSlot:
    def add(self, data):
        self.data = data
        return self


print [p.Indices for p in ghenv.Component.Params.Input[1].VolatileData.Paths]

tiles_out = []
bb = []
lst = th.tree_to_list(tileMatrix, None)
print lst
for j, p in enumerate(ghenv.Component.Params.Input[1].VolatileData.Paths):
    nested = []
    for i, v in enumerate(lst[j]):
        column = []
        for tileSlot in v.data:
            column.append([TileSlot().add(tt) for tt in tileSlot])
        nested.append(column)
    bb.append(nested)

tiles_out = th.list_to_tree(bb, True, [branch_indx])


attrib_out = th.list_to_tree(
    [[a for a in at] for at in attributes_read], True, [branch_indx, 0]
)
matrix_out = th.list_to_tree([[ls] for ls in lst[0]], True, [branch_indx, 0])
