# -*- coding: utf-8 -*-
"""Convert list of GH Point3d to SpacialMatrix

each point represents active(enabled) cell in matrix structure

Inputs:
    • points([Point3d, ...]),<ListAccess>: list of points located on the same plane.
        Recomended to use points organized in sqare grid, with equal distance between points in x&y directions
Output:
    • indexes([(int, int), ...]): list of tuples of i j cell indexes
    • xy([(float, float), ...]): list of tuples of xy sorted coodrinates

@author: prslvtsv
"""

from math import floor, log10


def sort_pt_xy(pt, round=False):
    if round:
        return sorted(
            [(math.floor(p.X), math.floor(p.Y)) for p in pt], key=lambda k: [k[0], k[1]]
        )
    return sorted([(p.X, p.Y) for p in pt], key=lambda k: [k[0], k[1]])


def graft_xy(coords):
    def gr(coord):
        for c in coord:
            yield [col for col in coord if col[0] == c[0]]

    return list(gr(coords))


def calc_step_xy(coords):
    xval = [c[0] for c in coords]
    yval = [c[1] for c in coords]
    dx = [
        round(abs(v - pv)) for (v, pv) in zip(xval[:-1], xval[1:]) if abs(v - pv) > 0.2
    ]
    dy = [
        round(abs(v - pv)) for (v, pv) in zip(yval[:-1], yval[1:]) if abs(v - pv) > 0.2
    ]
    if len(dx) == 0:
        dx.append(1.0)
    if len(dy) == 0:
        dy.append(1.0)
    print dx, dy
    step_x = max(set(dx), key=dx.count)
    step_y = max(set(dy), key=dy.count)
    #    print step_x, step_y
    return step_x, step_y


#    return rnd_n(step_x, 1), rnd_n(step_y, 1)


def coord_to_index(coords):
    sx, sy = calc_step_xy(coords)
    #    print sx, sy
    xmin = min([c[0] for c in coords])
    ymin = min([c[1] for c in coords])
    #    def p(d):print(d)
    #    [p(x) for (x, y) in coords]
    return [
        (int(round((x - xmin) / sx)), int(round((y - ymin) / sy))) for (x, y) in coords
    ]


#    return [(int((x-xmin)/sx), int((y-ymin)/sy)) for (x, y) in coords]


def points2matrix_xy(points):
    return sort_pt_xy(points)


def points2matrix_ij(points):
    return coord_to_index(sort_pt_xy(points))
