# -*- coding: utf-8 -*-
"""
Created on 03 Jul 2022

@author: prslvtsv
"""
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
)

from decimal import getcontext, Decimal, Context, ROUND_HALF_EVEN, ROUND_DOWN


def f2s(f, n=4):
    if n:
        f = round(float(f), n)
        sn = str(f).split(".")
        # print(f, sn)
        left = sn[0]
        try:
            right = sn[1].ljust(n, "0")
        except:
            d = f2d(f, n)
            sn = str(d).split(".")
            left = sn[0]
            right = sn[1].ljust(n, "0")
        return ".".join([left, right])
    else:
        return str(int(round(f)))


def f2f(f, n=4):
    # return type(f2s(f, n))
    return float(f2s(f, n))


def f2d(f, n=4):
    # if n <= 1:
    #     n = 2
    con = Context(prec=n * 2, rounding=ROUND_HALF_EVEN)
    getcontext().prec = n * 2
    # f = f2s(f, n)
    d = con.create_decimal_from_float(f)
    p = "".join([".", "".join([str(0) for i in range(n - 1)]), "1"])
    dd = con.create_decimal(p)
    return d.quantize(dd, rounding=ROUND_HALF_EVEN)


def ghpt2xyz(pt, prec=6, asstr=False):
    x, y, z = pt.X, pt.Y, pt.Z
    if asstr:
        return (f2s(x, prec), f2s(y, prec), f2s(z, prec))
    return (f2f(x, prec), f2f(y, prec), f2f(z, prec))


# to work in grass
def ghply2xyz(polyline, prec=6, asstr=False):
    points = polyline.ToArray()
    return [ghpt2xyz(pt, prec, asstr) for pt in points]


def gprint(toprint):
    print(toprint)


def printlines(lst):
    print("\n\n".join(lst))
    # print("")


# print list line by line
def printeach(lst):
    [gprint(i) for i in lst]


################################################
################################################
if __name__ == "__main__":

    # print(" ".join(["res:", f2s(20, 4)]))
    # print(" ".join(["res:", f2s(999.1, 4)]))
    # print(" ".join(["res:", f2s(0.01, 4)]))
    print(" ".join(["res:", f2s(0.001 / 3, 5)]))
    print(" ".join(["res:", f2s(0.0001, 5)]))
    print(" ".join(["res:", f2s(20.3, 0)]))
    # print(" ".join(["res:", f2s(-0.00015123123, 2)]))

    # print("res:", f2f(-20, 4))
    # print("res:", f2f(999.1, 4))
    # print("res:", f2f(0.01, 4))
    # print("res:", f2f(0.001, 4))
    # print("res:", f2f(-0.0001, 4))
    # print("res:", f2f(-0.00015123123, 2))

    # print("res:", f2d(-20, 4))
    # print("res:", f2d(1, 4))
    # print("res:", f2d(0.01, 4))
    # print("res:", f2d(0.001, 4))
    # print("res:", f2d(-0.0001, 4))
    # print("res:", f2d(-0.00015123123, 4))

    print(f2d(10 / 3))
    pass
