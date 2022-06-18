# -*- coding: utf-8 -*-
"""New Context initilizer (see gh_context module for old version)

Currently WIP

Created on 04 June 2022
for Aective Team
@author: prslvtsv
"""


def create_pins(loc, dir, pinNames, access="item", prefix="", optional=True):
    access = get_access_type(loc, access)
    guids = []
    for name in pinNames:
        name = _prefix_name(name, prefix)

        if dir in "in":
            if prefix:
                name = "ai_{}".format(name)

            i = loc["ghenv"].Component.Params.IndexOfInputParam(name)
            if i == -1:
                guids.append(_register_pinin(loc, name, access, optional))
            else:
                guids.append(loc["ghenv"].Component.Params.Input[i].InstanceGuid)

        if dir in "out":
            i = loc["ghenv"].Component.Params.IndexOfOutputParam(name)
            if i == -1:
                guids.append(_register_pinout(loc, name, access))
            else:
                guids.append(loc["ghenv"].Component.Params.Output[i].InstanceGuid)
    return guids


def delete_pins(loc, dir, pinGuids=[]):
    for guid in pinGuids:
        if dir in "in":
            _uregister_pinin(loc, guid)
            # loc["ghenv"].Component.ExpireSolution(True)
        else:
            _uregister_pinout(loc, guid)
            # loc["ghenv"].Component.ExpireSolution(True)


def exist(loc, name, prefix=""):
    name = _prefix_name(name, prefix)
    iin = loc["ghenv"].Component.Params.IndexOfInputParam(name)
    iout = loc["ghenv"].Component.Params.IndexOfOutputParam(name)
    return iin != -1 or iout != -1


def _prefix_name(name, prefix):
    return "{}{}".format(prefix, name)


def get_access_type(loc, access):
    if access in "list":
        return loc["kernel"].GH_ParamAccess.list
    elif access in "three":
        return loc["kernel"].GH_ParamAccess.tree
    else:
        return loc["kernel"].GH_ParamAccess.item


def _register_pinout(loc, name, access):
    param = loc["kernel"].Parameters.Param_GenericObject()
    param.NickName = name
    param.Name = name
    param.Access = access
    loc["ghenv"].Component.Params.RegisterOutputParam(param)
    loc["ghenv"].Component.Params.OnParametersChanged()
    # loc["ghenv"].Component.Params.OnParametersChanged()
    return param.InstanceGuid


def _register_pinin(loc, name, access, optional=True):
    param = loc["kernel"].Parameters.Param_GenericObject()
    param.NickName = name
    param.Name = name
    param.Access = access
    param.Optional = optional
    loc["ghenv"].Component.Params.RegisterInputParam(param)
    loc["ghenv"].Component.Params.OnParametersChanged()
    # loc["ghenv"].Component.Params.OnParametersChanged()
    return param.InstanceGuid


def _uregister_pinout(loc, guid):
    pidx = loc["ghenv"].Component.Params.IndexOfOutputParam(guid)
    if pidx != -1:
        pin = loc["ghenv"].Component.Params.Output[pidx]
        loc["ghenv"].Component.Params.UnregisterOutputParameter(pin)
        loc["ghenv"].Component.Params.OnParametersChanged()


def _uregister_pinin(loc, guid):
    pidx = loc["ghenv"].Component.Params.IndexOfInputParam(guid)
    if pidx != -1:
        pin = loc["ghenv"].Component.Params.Input[pidx]
        loc["ghenv"].Component.Params.UnregisterInputParameter(pin)
        loc["ghenv"].Component.Params.OnParametersChanged()
