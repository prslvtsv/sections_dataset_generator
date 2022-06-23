# -*- coding: utf-8 -*-
"""Helper functions to utilize Grashopper SDK & RhinoCommon SDK methods

UPD 17.06.2022: Needs cleaning & documenting

Created on 05.05.2022
@author: prslvtsv
"""


from Rhino.Geometry import Point3d, Point, Curve, Polyline, PolylineCurve
import rhinoscript.view as v
from vec import Vec3
import Rhino

import core

reload(core)

# works with Point3d
def xy2ij(points):
    xx, yy = [p.X for p in points], [p.Y for p in points]
    unique_x = sorted(list(set([round(x) for x in xx])))
    unique_y = sorted(list(set([round(y) for y in yy])))
    i = [unique_x.index(round(xp)) for xp in xx]
    j = [unique_y.index(round(yp)) for yp in yy]
    return list(zip(i, j))


class Convert:
    @staticmethod
    def point2vec(p3d):
        return Vec3(p3d.X, p3d.Y, p3d.Z) if isinstance(p3d, Point3d) else None

    @staticmethod
    def point2coord(p3d):
        return (p3d.X, p3d.Y, p3d.Z)

    @staticmethod
    def polyline2coord(poly):
        return [Convert.point2coord(p) for p in poly.ToArray()]


class Helper:
    @staticmethod
    def get_by_id_geo(guid):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(guid)
        return obj.Geometry

    @staticmethod
    def get_by_id_obj(guid):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(guid)
        return obj

    @staticmethod
    def get_obj_by_region(guid):

        regid = Rhino.RhinoDoc.ActiveDoc.Objects.Find(guid)
        viewport = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.MainViewport
        fltr = Rhino.DocObjects.ObjectType.AnyObject

        objects = None
        objects = Rhino.RhinoDoc.ActiveDoc.Objects.FindByWindowRegion(
            viewport, regid.Geometry.ToPolyline(), True, fltr
        )

        if objects:
            rhinoGeo = []
            layer = []
            for rhobj in objects:

                if rhobj.Id == guid:
                    continue

                rhinoGeo.append(rhobj.Id)
                layer.append(
                    Rhino.RhinoDoc.ActiveDoc.Layers[
                        rhobj.Attributes.LayerIndex
                    ].FullPath
                )

            return rhinoGeo, layer

        return None

    @staticmethod
    def point3d_to_vec3(p3d):
        if isinstance(p3d, Point3d):
            return Vec3(p3d.X, p3d.Y, p3d.Z)

        print ("[ERROR] point3d_to_vec3 expected Point3D as argument got ", type(p3d))
        return None

    @staticmethod
    def vec3_to_point3d(v3):
        if isinstance(v3, Vec3):
            return Point3d(v3.x, v3.y, v3.z)

        print ("[ERROR] vec3_to_point3d expected vec3 as argument got ", type(v3))
        return None

    @staticmethod
    def convert_pv_list(lst):

        if len(lst) == 0:
            return None

        res = []

        if isinstance(lst[0], Point3d):
            for i in lst:
                res.append(Helper.point3d_to_vec3(i))
            return res

        elif isinstance(lst[0], Vec3):
            for i in lst:
                res.append(Helper.vec3_to_point3d(i))
            return res

        print "[ERROR] convert_pv_list failed to convert, types mismatch"
        return None

    @staticmethod
    def read_floor_from_frame(gid):
        # geo, layer = None, None
        geo, layer = Helper.get_obj_by_region(gid)
        # try:
        #
        #     print geo
        # except:
        #     return None

        newfloor = core.Floor()

        # if len(geo) < 10:
        #     print len(geo)

        for i in range(len(geo)):
            path = layer[i].split("::")

            # check if tile is polyline and adds vec3 list of points to tile + state name
            if path[1] in "tiles":

                pln = Helper.get_by_id_geo(geo[i])

                if not isinstance(pln, PolylineCurve):
                    # raise ValueError('not all tiles are polylines - check rhino set!')
                    print pln, " skipped as not polyline"
                    continue

                newfloor.add_tile(
                    core.Tile(Helper.convert_pv_list(pln.ToPolyline()), path[-1])
                )

            # reads all refgeo layers and objects/ typecheck for polyline / point3d
            elif path[1] in "refgeo":
                g = Helper.get_by_id_geo(geo[i])

                if isinstance(g, PolylineCurve):
                    newfloor.geo[path[-1]] = Helper.convert_pv_list(g.ToPolyline())
                elif isinstance(g, Point):
                    newfloor.geo[path[-1]] = Helper.point3d_to_vec3(g.Location)
                else:
                    print "something is wrong with types of ref geo ", type(g)

            # reads text attributes and sets corresponding attr values
            elif path[1] in "attrib_txt":
                attrtxt = Helper.get_by_id_geo(geo[i])
                lines = attrtxt.PlainText.splitlines()

                for lin in lines:
                    name = lin.split(":")[0]
                    code = lin.split(":")[1]
                    # if name in "length" or name in "distribution":
                    #     continue
                    if code == "in":
                        code = "inside"

                    newfloor.attrState.floorAttrUser[str(name)].now.value = code
                    newfloor.attrState.floorAttrUser[str(name)].now.valueCode = code
                    # print

            else:
                print "undefined path {}".format(path[1])

        newfloor.move_to(newfloor.geo["origin"])
        return newfloor

        # TODO
        # sort tiles in correct order
        # detect logical length
        # detect missing attributes
