# -*- coding: utf-8 -*-
"""
@author: prslvtsv
"""
import scriptcontext as sc
import Grasshopper.Kernel.GH_RuntimeMessageLevel as runtimeMessage
import Grasshopper.Kernel as kernel


def updateComponent(msec):
    def callBack(e):
        ghenv.Component.ExpireSolution(False)

    ghDoc = ghenv.Component.OnPingDocument()
    ghDoc.ScheduleSolution(msec, gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))


try:
    sc.sticky["remotepy"]
    isConnected = sc.sticky["remotepy"]
except:
    isConnected = False

if not isConnected:
    updateComponent(1000)
    raise Exception("no connection")

try:
    exec (sc.sticky["module_import_string"])
except:
    ghenv.Component.AddRuntimeMessage(runtimeMessage.Error, "failed to load modules")

################################################################################
################################################################################


core.StateContainer.init_attributes()


def get_attr_names():
    #    al = []
    #    for attr in attr_glob:
    #        al.append(attr.name)

    return [a for a in attr_glob]


def get_attr_names_ru(cyrylic=False):
    al = []
    for attr in attr_glob:
        if cyrylic:
            al.append(attr.nameRU)
        else:
            al.append("ru__" + attr.name)
    return al


def registerOutputs(inattr):
    if ghenv.Component.Params.Output.Count >= inattr.Count:
        print "already initialized"
        return False

    for attr in inattr:
        param = kernel.Parameters.Param_GenericObject()
        param.NickName = attr
        param.Name = attr
        param.Access = kernel.GH_ParamAccess.list
        ghenv.Component.Params.RegisterOutputParam(param)
        ghenv.Component.Params.OnParametersChanged()

    return True


def unregisterOutputs():
    ghenv.Component.ExpireSolution(True)
    while ghenv.Component.Params.Output.Count > 1:

        ghenv.Component.Params.UnregisterOutputParameter(
            ghenv.Component.Params.Output[ghenv.Component.Params.Output.Count - 1]
        )


def get_attr_options(attr):
    opt = []
    for o in attr.options:
        opt.append(o.value)
    return opt


def get_attr_options_ru(attr):
    opt = []
    for o in attr.options:
        opt.append(o.valueRU)
    return opt


#        print ghenv.Component.Params.Output[i+1].Name, ' ' , attr.name

#        ghenv.Component.Params.Output[i+1].AddVolatileDataList(path,opt)
#            ghenv.Component.Params.Output[i+1].VolatileData.Append(kernel.Types.GH_String(o.value), path)
#        ghenv.Component.Params.Output[i+1].VolatileData.RemoveData(ghenv.Component.Params.Output[i+1].VolatileData[0])
#        print ghenv.Component.Params.Output[i+1].VolatileData.AllData(False)
#        ghenv.Component.Params.Output[i+1].Simplify = True


#        print attr.get_options_list()


if rebuild_outputs:
    unregisterOutputs()
    if output_ru:
        registerOutputs(
            ["-------"]
            + ["names_en", "names_ru"]
            + ["-------"]
            + get_attr_names()
            + ["-------"]
            + get_attr_names_ru()
        )

    else:
        registerOutputs(["-------"] + ["names_en"] + ["-------"] + get_attr_names())
    ghenv.Component.ExpireSolution(True)


for a in sc.sticky["attrib_obj"]:
    exec ("%s = %s" % (a.name, get_attr_options(a)))
    if output_ru:
        runame = "ru__" + a.name
        exec ("%s = %s" % (runame, get_attr_options_ru(a)))

    # print get_attr_options_ru(a)[0]

    if output_ru:
        names_ru = get_attr_names_ru(True)
    names_en = get_attr_names()
#
#    for nru in get_attr_names_ru():
#        names_ru.append(nru.split('__')[-1])
