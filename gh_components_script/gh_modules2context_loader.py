import rhinoscriptsyntax as rs
import scriptcontext as sc
import Grasshopper as gh


def updateComponent(msec):
    def callBack(e):
        ghenv.Component.ExpireSolution(False)

    ghDoc = ghenv.Component.OnPingDocument()
    ghDoc.ScheduleSolution(msec, gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))


def reload_modules():
    try:
        sc.sticky["gblock.core"]
        sc.sticky["gblock.core"] = reload(sc.sticky["gblock.core"])

        sc.sticky["gblock.ghhelp"]
        sc.sticky["gblock.ghhelp"] = reload(sc.sticky["gblock.ghhelp"])

        sc.sticky["gblock.event_handling"]
        sc.sticky["gblock.event_handling"] = reload(sc.sticky["gblock.event_handling"])

        sc.sticky["gblock_init"]
        sc.sticky["gblock_init"] = True

        print "modules reloaded"

    except:
        import gblock.core as core
        import gblock.ghhelp as ghh
        import gblock.event_handling as ev

        sc.sticky["gblock.core"] = core
        sc.sticky["gblock.ghhelp"] = ghh
        sc.sticky["gblock.event_handling"] = ev
        sc.sticky["gblock_init"] = True

        print "modules imported"

    print "remote py running: ", isConnected


################################################################
try:
    sc.sticky["remotepy"]
    isConnected = sc.sticky["remotepy"]
except:
    isConnected = False

if not isConnected:
    updateComponent(1000)
    raise Exception("no connection")


try:
    sc.sticky["gblock_init"]
    sc.sticky["module_import_string"] = ""

    if sc.sticky["gblock_init"]:
        txt = sc.sticky["module_import_string"]
        #        txt += "import scriptcontext as sc" + '\n'
        txt += "import System" + "\n"
        txt += "core = sc.sticky['gblock.core']" + "\n"
        txt += "ghh = sc.sticky['gblock.ghhelp']" + "\n"
        txt += "ev = sc.sticky['gblock.event_handling']" + "\n"
        sc.sticky["module_import_string"] = txt
    try:
        sc.sticky["remotepy"]

        if sc.sticky["remotepy"]:
            txt = sc.sticky["module_import_string"]
            txt += "pd = sc.sticky['pandas']" + "\n"
            txt += "xr = sc.sticky['xarray']" + "\n"
            txt += "np = sc.sticky['numpy']" + "\n"
            txt += "rpy = sc.sticky['rpy']" + "\n"
            sc.sticky["module_import_string"] = txt
    except:
        pass
except:
    reload_modules()

if reload_dependencies:
    reload_modules()

    # ghenv.Component.ExpireSolution(True)
