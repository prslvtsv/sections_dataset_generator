# -*- coding: utf-8 -*-
"""
Created on 05 June 2022
for Aective Team
@author: prslvtsv
"""


def load_modules(component_locals, method_locals):
    if "sc" not in component_locals.keys():
        import scriptcontext as sc

        component_locals["sc"] = sc
        method_locals["sc"] = sc
        #
    if "gh" not in component_locals.keys():
        import Grasshopper as gh

        component_locals["gh"] = gh
        method_locals["gh"] = gh
        #
    if "runtimeMessage" not in component_locals.keys():
        import Grasshopper.Kernel.GH_RuntimeMessageLevel as runtimeMessage

        component_locals["runtimeMessage"] = runtimeMessage
        method_locals["runtimeMessage"] = runtimeMessage
        #
    if "kernel" not in component_locals.keys():
        import Grasshopper.Kernel as kernel

        component_locals["kernel"] = kernel
        method_locals["kernel"] = kernel

    from collections import OrderedDict as ordDict

    component_locals["ordDict"] = ordDict
    method_locals["ordDict"] = ordDict
