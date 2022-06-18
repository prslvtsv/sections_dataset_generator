# -*- coding: utf-8 -*-
"""Old core classes used in current scripts itteration

All are OBSOLETE, moving to new class structure (see gblock.elemets for additiinal info)

Created on Tue Apr 18 09:38:10 2022
@author: prslvtsv
"""

import attributes as att
import copy
import collections
import vec as vc

reload(att)


class SmartInterval:
    def __init__(self, min=0, max=1, now=0):
        self.min = min
        self.max = max
        self.now = now

    def contain(self, val):
        return (val >= self.min) and (val <= self.max)

    def get_span(self):
        return abs(self.max - self.min)

    def get_bounds(self):
        return (self.min, self.max)

    def __str__(self):
        return "{}.{}.{}".format(self.min, self.max, self.now)


# ''' length object to handle both logical (tiles) and metric (m) length of the section/floor together with limits'''
# class LengthLM():
#     def __init__(self, logMin = 0, logMax = 0, metMin = 0, metMax = 1):
#         self.logical = Interval(logMin, logMax)
#         self.metric  = Interval(metMin, metMax)
#         self.nowL = 0
#         self.nonM = 0


class Length:
    def __init__(self, lmin=0, lmax=0, lnow=0, mmin=0, mmax=0, mnow=0):
        self.logical = SmartInterval(lmin, lmax, lnow)
        self.metric = SmartInterval(mmin, mmax, mnow)

    def __str__(self):
        return "{}.{}.{}.{}.{}.{}".format(
            self.logical.min,
            self.logical.max,
            self.logical.min,
            self.metric.min,
            self.metric.max,
            self.metric.now,
        )


# TODO
# • class is obsolete by now
# • cleaner attr nandler to feed values into both gh and np\xarray
class StateContainer(object):
    """representation of current conditions set of attributes"""

    _bInit = False
    _floorAttrAll = collections.OrderedDict()
    _floorAttrUser = collections.OrderedDict()

    def __init__(self):
        self.attributes = {}
        self.floorAttr = None
        self.floorAttrUser = None

    def create_attributes(self):
        if not StateContainer._bInit:
            print "attrubutes not initilized"
            return self

        self.floorAttr = collections.OrderedDict(StateContainer._floorAttrAll)
        self.floorAttrUser = copy.deepcopy(StateContainer._floorAttrUser)

        # for fa in StateContainer._floorAttrAll:

        # for fa in StateContainer._floorAttrAll:

    def pull_attrib_line(self):
        at = []

        for attr in self.floorAttrUser.values:
            print attr
            at.append(attr.now.value)

        return "|".join(at)

    @staticmethod
    def init_attributes():

        if StateContainer._bInit:
            return True

        ordered_floorData = collections.OrderedDict(
            sorted(att.glAttrFloorDataSetup.items())
        )
        ordered_floorDataUser = collections.OrderedDict(
            sorted(att.glAttrFloorUserSetup.items())
        )

        for name in ordered_floorData:

            attr = att.Attribute().create_from_dict(ordered_floorData[name])
            StateContainer._floorAttrAll[name] = attr
            # print attr

        for name in ordered_floorDataUser:

            attr = att.Attribute().create_from_dict(ordered_floorDataUser[name])
            StateContainer._floorAttrUser[name] = attr
            # print attr

        # print "[StateContainer] init complete | global - {} | user - {}".format(
        #     len(StateContainer._floorAttrAll), len(StateContainer._floorAttrUser)
        # )

        StateContainer._bInit = True
        return True

    @staticmethod
    def get_all_attr(name="floor_user"):

        # print type(name)

        if not StateContainer._bInit:
            print "[StateContainer] not init"
            return None

        if name.endswith("floor"):
            return StateContainer._floorAttrAll

        if name.endswith("floor_user"):
            return StateContainer._floorAttrUser

        return None

    def __str__(self):
        return "state: {} user: {}".format(self.floorAttr, self.floorAttrUser)


class Tile(object):
    def __init__(
        self,
        points=[vc.Vec3(0, 0, 0), vc.Vec3(0, 1, 0), vc.Vec3(0, 2, 0)],
        ghGeo=None,
        state=None,
        app=1,
        matPos=[0, 0],
    ):

        # base geometry of the tile
        self.outline = points
        self.state = state
        self.ghGeo = ghGeo
        self.appNumber = app
        self._matPos = matPos

    @property
    def matPos(self):
        return self._matPos

    @matPos.setter
    def matPos(self, v):
        self._matPos = v
        return self

    def expl_matPos(self, v):
        self._matPos = v
        return self

    def __str__(self):
        return "<T:{}:{}:{}>".format(self.state[:3], self._matPos[0], self._matPos[1])

    def __repr__(self):
        return "<T:{}:{}:{}>".format(self.state[:3], self._matPos[0], self._matPos[1])


class Floor(object):
    def __init__(self):
        self.attrState = StateContainer()
        self.attrState.create_attributes()
        self.attrList = None

        self.geo = {
            "tiles": [],
            "outline": [],
            "front": [],
            "spine": [],
            "origin": vc.Vec3(),
        }

        return self

    def add_tile(self, tile):
        if not isinstance(tile, Tile):
            raise ValueError("expected tile got {}".format(type(tile)))

        self.geo["tiles"].append(tile)
        # print 'tile added ', self.geo['tiles'][-1]
        return self

    def set_geo(self, geoname, l):
        self.geo[geoname] = l
        return self

    def get_geo(self):
        return self.geo

    def get_tiles(self):
        return self.geo["tiles"]

    def move_to(self, pt):
        move = pt

        for inx, tile in enumerate(self.geo["tiles"]):
            for i, point in enumerate(self.geo["tiles"][inx].outline):
                self.geo["tiles"][inx].outline[i] = point - move

        for i, point in enumerate(self.geo["outline"]):
            self.geo["outline"][i] = point - move

        for i, point in enumerate(self.geo["front"]):

            self.geo["front"][i] = point - move

        self.geo["origin"] = self.geo["origin"] - move

        return self

    # def __repr__(self):
    #     return "[FLOOR]: {} origin: {} tiles: {}".format(
    #         self.attrState, self.geo["origin"], len(self.geo["tiles"])
    #     )

    def __repr__(self):
        return "FL"

    def __unicode__(self):
        return "FL"


class Section:
    pass
