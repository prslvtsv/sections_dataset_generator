# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 09:38:10 2022

@author: prslvtsv
"""

# .translate(None, "aeiouyAEIOUY")

# TODO
# simplify attribute class
# rethink option holding

"""
conda create --name py27 -c conda-forge python=2.7 numpy scipy xarray dask netCDF4 bottleneck matplotlib spyder=3.3 qtawesome=0.7 seaborn cyordereddict rpyc
"""

import attrcnfg as aconf

reload(aconf)

glAttrFloorDataSetup = aconf.attrFloorGeneral
glAttrFloorUserSetup = aconf.attrFloorUser


class AttrBase:
    def __init__(self, name=None, nameRU=None):
        self.name = name
        self.nameRU = nameRU
        self.valid = False

    @staticmethod
    def devowel(val):
        return val.translate(None, "aeiouyAEIOUY")

    def shorten(self, val, method="devowel"):
        if isinstance(val, str) and method in "dewovel":
            return AttrBase.devowel(val)
        return val

    @property
    def valid(self):
        return self._valid

    @valid.setter
    def valid(self, v):
        self._valid = v

    def __repr__(self):
        return "attr: {} {}".format(self.name, self.value)


class AttrString(AttrBase):
    def __init__(self, name=None, nameRU=None, value=None, valueRU=None):
        AttrBase.__init__(self, name, nameRU, value, valueRU)

        if self.value and isinstance(self.value, str):
            self._valid = True

    @property
    def get_value(self):
        return self.shorten(self.value)

    def get_name(self, lang="en", short=False):
        res = None

        if lang in "en":
            res = self.name
        elif lang in "ru":
            res = self.nameRU

        if short:
            try:
                return self.shorten(res)
            except:
                return res

        return res


class AttrNum(AttrBase):
    pass
    # interface for sliders


class AttrRange(AttrBase):
    pass
    # interface for ranged sliders

    # __repr__


# Obsolete needs to removerd from logic
class CurrentAttribute(object):
    def __init__(self):
        self.value = None
        self.valueRU = None
        self.valueCode = None
        self.pos = None

    def create_from_option(self, opt):
        self.value = opt["value"]
        self.valueCode = opt["valueCode"]

        # self.pos = opt["pos"]

        if "valueRU" in opt:
            self.valueRU = opt["valueRU"]
        else:
            self.valueRU = " "

        return self

    def set_current(self, currattr):
        self.value = currattr.value
        self.valueRU = currattr.valueRU
        self.valueCode = currattr.valueCode
        # self.pos = currattr.pos

        return self

    def __str__(self):
        pad = 32
        if self.value is None:
            return "None"

        return "|{}|{}|{}|{}|".format(
            self.value, self.valueRU, self.valueCode, self.currentOption
        )


# Obsolete needs to removerd from logic
class Attribute(object):
    def __init__(self):
        self.name = None
        self.nameRU = None
        self.nameCode = None
        self.options = None
        self.valuenow = None

        self.now = CurrentAttribute()

        self.bValid = False

    def assign(self, obj):
        self.name = obj.name
        self.nameRU = obj.nameRU
        self.nameCode = obj.nameCode
        self.options = obj.options
        self.valuenow = obj.valuenow
        self.bValid = obj.bValid

        return self

    def set_current_option(self, optnum):
        if len(self.options) == 0:
            print "[Attribute] set_attr_option - no option {} avaliable in>> {} ".format(
                self.name, optnum
            )
            return self

        if optnum >= self.count_options():
            print "[Attribute] set_attr_option - out of range"
            return self

        self.now.set_current(self.options[optnum]).currentOption = optnum

        return self

    def create_from_dict(self, attrdict):
        self.name = attrdict["name"]
        self.nameCode = attrdict["nameCode"]

        if "nameRU" in attrdict:
            self.nameRU = attrdict["nameRU"]
        else:
            self.nameRU = "*"

        self.options = []
        for opt in attrdict["options"]:
            self.options.append(CurrentAttribute().create_from_option(opt))

        self.set_current_option(0)

        self.bValid = True

        return self

    def count_options(self):
        try:
            return len(self.options)
        except:
            return 0

    def get_options_list(self):
        l = []
        l.append(opt.value for opt in self.options)
        return ()

    def __str__(self):
        return "attr: {}({}) = {} || {}".format(
            self.name, self.nameRU, self.valuenow, self.count_options()
        )


def parse_attr2list(aatr):
    pass
