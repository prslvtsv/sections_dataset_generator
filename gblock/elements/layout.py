# -*- coding: utf-8 -*-
"""
Created on 15 Jun 2022

@author: prslvtsv
"""
from .gtypes import NestedObject, AssemblyBlock


class FloorLayout(AssemblyBlock):
    def __init__(self, mtx=None, apt=None):
        AssemblyBlock.__init__(self)
        self.matrix = mtx
        self.aptGroups = apt
        self.dispPadding = (0, 0)

    def apt_indexes(self):
        return self.aptGroups

    def display_coords(self):
        return [
            [(x + self.dispPadding[0], y + self.dispPadding[1]) for (x, y) in apt]
            for apt in self.aptGroups
        ]
