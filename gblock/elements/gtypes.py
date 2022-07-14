# -*- coding: utf-8 -*-
"""Base classes to enable shared sunctionality among operational blocks

Created on 15 Jun 2022
@author: prslvtsv
"""


class NestedObject(object):
    """Simple class hangling owner objects logic, assist in fast object cross ref"""

    def __init__(self, parent, child=None):
        self.typename = "NestedObject"
        self.parent = parent
        self.child = child

    # TODO:
    # extend with nested tree travel methods


class AttribAddress:
    """Base class to handle conversion from attributes to labeled address in xarray DB"""

    def __init__(self):
        self.attadr = {}

    # TODO:
    # all needed operations. currently works just as a placeholder


class AssemblyBlock(NestedObject, AttribAddress):
    """Base class for all objects used in algorithm logic as construction elements i.e. Section, Floor"""

    def __init__(self, parent=None):
        NestedObject.__init__(self, parent)
        AttribAddress.__init__(self)
        # dev test arg
        self.typename = "assembly_block"

        # TODO:
        # add property -> size = DynamicRange
        # add property -> shape = DynamicRange
        # add property -> metrics = Appriser
        # add other functional blocks


if __name__ == "__main__":
    # used only for dev tests
    pass
