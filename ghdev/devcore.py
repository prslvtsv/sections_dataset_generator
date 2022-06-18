# -*- coding: utf-8 -*-
"""New Context initilizer (see gh_context module for old version)

Currently WIP

Created on 04 June 2022
for Aective Team
@author: prslvtsv
"""


class DataContainer:
    def __init__(self):
        pass

    def content(self):
        return self.__dict__

    def has(self, key):
        return key in self.__dict__

    def __repr__(self):
        return "".join(["<", " | ".join(self.content().keys()), ">"])


# wraper to use print with generators
def gprint(toprint):
    print toprint


# print separate lines as one line with \n
def printlines(lst):
    print "\n".join(lst)


# print list line by line
def printeach(lst):
    [gprint(i) for i in lst]


# expire component every % miliseconds
def recompute_solution_timed(_loc, msec):
    def callBack(e):
        _loc["ghenv"].Component.ExpireSolution(False)

    ghDoc = loc["ghenv"].Component.OnPingDocument()
    ghDoc.ScheduleSolution(
        msec, _loc["gh"].Kernel.GH_Document.GH_ScheduleDelegate(callBack)
    )
