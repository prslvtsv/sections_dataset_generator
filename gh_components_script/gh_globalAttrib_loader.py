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
import collections

core.StateContainer.init_attributes()

attr_list = core.StateContainer.get_all_attr(setName).values()

names = np.array([a.name for a in attr_list])
dims = []


def map_addresses(attributes):
    mapping = collections.OrderedDict()
    for n, obj in enumerate(attributes):
        # print n

        name = obj.name
        mapping[name] = {}
        mapping[name]["pos"] = n

        for o, opt in enumerate(obj.options):
            mapping[name]["range"] = slice(None)
            mapping[name][opt.value] = o
    sc.sticky["attributes_mapping"] = mapping
    return mapping


for n in attr_list:

    n.valuenow = 0
    if n in "distribution" or n in "length":
        dims.append(1)
    else:
        dims.append(n.count_options())

###  sorting
dims = np.array(dims)
indx = (-dims).argsort()
# indx = [int(a) for a in range(len(dims))]


################
# manuallty push distr & length to end
dis = 3
dp = 8
len = 8
lp = 10
indx[lp] = 10
indx[dp] = 9
indx[11] = len
indx[12] = dis
indx[0] = 10
indx[10] = 11
print indx

dims = dims[indx]
names = names[indx]

attrib_names = [n for n in names.tolist()]
attrib_dims = [n for n in dims.tolist()]
attrib_obj = [n for n in np.array(attr_list)[indx]]


mapping_dict = [map_addresses(attrib_obj)]

sc.sticky["attrib_names"] = attrib_names
sc.sticky["attrib_dims"] = attrib_dims
sc.sticky["attrib_obj"] = attr_list

# print names
# print dims
# print indx
