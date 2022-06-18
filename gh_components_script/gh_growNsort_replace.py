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
exec(compile("".join(context.init()), "init", "exec"), locals())
###############################################################################

import ghpythonlib.treehelpers as th
from collections import OrderedDict as oddict
from operator import itemgetter

attr = th.tree_to_list(attributes_in, None)
data = th.tree_to_list(data_in, None)
path_mapper = mapping_filter

path = []
mask = []
for i, at in enumerate(attr):
    if at != None:
        for j, v in enumerate(at):
            path_dict = dict(
                [[d.split(":")[0], d.split(":")[1]] for d in v[0].splitlines()]
            )
            map = [path_mapper[path_dict[gr]] for gr in group_by]
            pp = gh.Kernel.Data.GH_Path()
            for m in map:
                pp = pp.AppendElement(int(m))
            path.append(pp)
            ms = "{" + "{};{}".format(i, j) + "}"
            mask.append(ms)
#    else:
#        path.append(None)
replace_mask = mask
generated_path = path
