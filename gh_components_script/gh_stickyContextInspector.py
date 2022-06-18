import scriptcontext as sc
import Grasshopper.Kernel.GH_RuntimeMessageLevel as runtimeMessage
import ghpythonremote
import Rhino
import Grasshopper as gh


def updateWithTimer(ghEnv, msec):
    def callBack(e):
        ghEnv.Component.ExpireSolution(False)

    ghDoc = ghEnv.Component.OnPingDocument()
    ghDoc.ScheduleSolution(msec, gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))


try:
    sc.sticky["remotepy"]
    isConnected = sc.sticky["remotepy"]
    print "remote_py:   ", isConnected
except:
    print "remote_py:   ", isConnected
    isConnected = False

try:
    exec (sc.sticky["module_import_string"])
    print "modules:     YES"
except:
    print "modules:     NO"
#    ghenv.Component.AddRuntimeMessage(runtimeMessage.Error, 'failed to load modules')

sticky_content = []
events = []
event_obj = []

try:
    sc.sticky["events"]
    print "events:     ", len(sc.sticky["events"])
    for e in sc.sticky["events"]:
        events.append(e)
except:
    print "events:     NO"
    events = None

try:
    sc.sticky["component_event_obj"]
    #    print 'events:     ', len(sc.sticky['events'])
    for e in sc.sticky["component_event_obj"]:
        event_obj.append(e)
except:
    events_obj = None

if not show_global_out:
    for key in sc.sticky.keys():
        if key == "printglobal":
            continue

        if apply_filter:
            for f in show:
                if f in key:
                    if key not in ignore:
                        skey = key
                        sval = sc.sticky[key]
                        if "show_keys" not in display_opt:
                            skey = "*"
                        if "show_vals" not in display_opt:
                            sval = "*"
                        sticky_content.append("{}:{}".format(skey, sval))
        else:
            skey = key
            sval = sc.sticky[key]
            if "show_keys" not in display_opt:
                skey = "*"
            if "show_vals" not in display_opt:
                sval = "*"
            sticky_content.append("{}:{}".format(skey, sval))
else:
    try:
        sc.sticky["printglobal"]
        for line in sc.sticky["printglobal"]:
            sticky_content.append(line)
    except:
        sticky_content.append("no global output initilized")


if enable_live:
    updateWithTimer(ghenv, 1000)
