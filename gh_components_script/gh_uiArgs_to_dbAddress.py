# OBSOLETE

import Grasshopper.Kernel as kernel
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

print attr_glob


def get_attr_names():
    #    al = []
    #    for attr in attr_glob:
    #        al.append(attr.name)

    return [a for a in attr_glob]


def registerInputs(inattr):
    if ghenv.Component.Params.Input.Count >= inattr.Count:
        print "already initialized"
        return False

    for attr in inattr:
        param = kernel.Parameters.Param_String()
        param.NickName = attr
        param.Name = attr
        param.Access = kernel.GH_ParamAccess.item
        param.Optional = True

        ghenv.Component.Params.RegisterInputParam(param)
        ghenv.Component.Params.OnParametersChanged()

    return True


def unregisterInputs():

    while ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.UnregisterInputParameter(
            ghenv.Component.Params.Input[ghenv.Component.Params.Input.Count - 1]
        )


def map_address():
    names = get_attr_names()
    address = np.zeros((len(names))).tolist()

    for name in names:
        idx = ghenv.Component.Params.IndexOfInputParam(name)
        data = ghenv.Component.Params.Input[idx].VolatileData
        if not data.IsEmpty:
            data = data.Branches[0][0].Value
        else:
            data = "range"
        if data == "na" or data == "n/a":
            data = "range"

        i = sc.sticky["attributes_mapping"][name]["pos"]
        address[i] = sc.sticky["attributes_mapping"][name][data]

    print address
    return address


if rebuild_inputs:
    unregisterInputs()
    registerInputs(get_attr_names())
    ghenv.Component.ExpireSolution(True)

# conctr = coctrncentrateInputs()
# attrs, idx = concentrateInputs()
# attrs_joined = ' | '.join(attrs)
# idx_joined = ' |  '. join([str(i) for i in idx])
address_sliced = map_address()
# print "⚫⚪⬛⬜"
