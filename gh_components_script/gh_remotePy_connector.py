import inspect
import logging
from os import path
import sys
from time import sleep
import System

import scriptcontext
import Grasshopper.Kernel as kernel
import ghpythonremote
from ghpythonremote.connectors import GrasshopperToPythonRemote

location_adpt = None

try:
    remote_python_status
except:
    pass

for loc in location:
    if not location_adpt:
        if path.isfile(loc):
            location_adpt = loc

    # location_adpt

local_log_level = getattr(logging, log_level, logging.WARNING)
logger = logging.getLogger("ghpythonremote")
logger.setLevel(local_log_level)
ch = logging.StreamHandler()
ch.setLevel(local_log_level)
formatter = logging.Formatter("%(levelname)s: %(name)s:\n%(message)s")
ch.setFormatter(formatter)
logger.handlers = []
logger.addHandler(ch)
logger = logging.getLogger("ghpythonremote.GH_to_python")

ROOT = path.abspath(path.dirname(inspect.getfile(ghpythonremote)))
rpyc_server_py = path.join(ROOT, "pythonservice.py")

# Set connection to CLOSED if this is the first run
# and initialize set of linked modules
try:
    remote_python_status
except NameError:
    remote_python_status = "CLOSED"
    scriptcontext.sticky["remotepy"] = False
    lkd_modules = set()

# Wait for connection to connect or terminate
timer = 0
while remote_python_status == "CONNECTING" or remote_python_status == "CLOSING":
    sleep(1)
    timer += 1
    scriptcontext.sticky["remotepy"] = False
    if timer == 10:
        try:
            gh2py_manager.__exit__(*sys.exc_info())
        except Exception:
            pass
        remote_python_status = "CLOSED"
        scriptcontext.sticky["remotepy"] = False
        lkd_modules = set()
        raise RuntimeError(
            "Connection left in an inconsistent state and not returning. Reset "
            "everything."
        )


if run and location_adpt:
    if not remote_python_status == "OPEN":
        remote_python_status = "CONNECTING"
        gh2py_manager = GrasshopperToPythonRemote(
            rpyc_server_py,
            location=location_adpt,
            timeout=10,
            port=None,
            log_level=log_level,
            working_dir=path.abspath(path.dirname(scriptcontext.doc.Path)),
        )
        gh2py = gh2py_manager.__enter__()
        remote_python_status = "OPEN"

    # Stuff that we can reach
    rpymod = gh2py.py_remote_modules  # A getter function for a named python module
    rpy = gh2py.connection  # Represents the remote instance root object
    scriptcontext.sticky["rpy"] = rpy
    scriptcontext.sticky["remotepy"] = True
    # Add modules
    for mod in modules:
        try:
            scriptcontext.sticky[mod] = rpymod(mod)
            lkd_modules.add(mod)
        except ImportError:
            gh2py_manager.__exit__(*sys.exc_info())
            raise

elif not remote_python_status == "CLOSED":
    remote_python_status = "CLOSING"
    scriptcontext.sticky["remotepy"] = False
    # Remove linked modules
    for mod in lkd_modules:
        del scriptcontext.sticky[mod]
    del scriptcontext.sticky["rpy"]
    gh2py_manager.__exit__(*sys.exc_info())
    lkd_modules = set()
    remote_python_status = "CLOSED"
    scriptcontext.sticky["remotepy"] = False

# Change variable name because ghpython resets outputs to None before each run
linked_modules = lkd_modules

logger.info("GH to python connection is {}".format(remote_python_status))

if not location_adpt:
    ghenv.Component.AddRuntimeMessage(
        kernel.GH_RuntimeMessageLevel.Error, "Invalid python location"
    )
    print "ERROR: Проверьте путь к правильной версии Python"

if not remote_python_status == "OPEN":
    # ghenv.Component.AddRuntimeMessage(kernel.GH_RuntimeMessageLevel.Warning, 'Connection is not open')
    ghenv.Component.Params.Output[0].Recipients[
        0
    ].Properties.Colour = System.Drawing.Color.Red
    if run:
        print "ERROR: Connection failed, check log"
    else:
        print "WARNING: Component is not running -> click button"
elif remote_python_status == "OPEN":
    ghenv.Component.Params.Output[0].Recipients[
        0
    ].Properties.Colour = System.Drawing.Color.LawnGreen
