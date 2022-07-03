# -*- coding: utf-8 -*-
"""
Created on 01 Jul 2022

@author: prslvtsv
"""

import os
import sys

# import math
# import decimal as dec

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
sys.path.append(PROJECT_ROOT)


from gblock.utils.utils import f2s, f2f, f2d
from collections import OrderedDict
import time


class AppriserBase:
    def __init__(self, target):
        self.target = target


class LayoutAppriser(AppriserBase):
    def __init__(self, target):
        AppriserBase.__init__(self, target)
        self.eval_prec = 6
        self.disp_prec = 4
        self.aptratio = ApartmentRatio(prec=self.eval_prec)
        self.size = None

    def eval_apart_ratio(self):
        aparts = self.target.get_apartments()
        bedrooms = [apt.bedrooms for apt in aparts]
        self.aptratio.evaluate(bedrooms)

    def aprt(self, mode="obj"):
        if mode.startswith("."):
            if len(mode) < 2:
                prec = self.disp_prec
            else:
                prec = len(mode) - 1
            return self.aptratio.print_ratio(prec=prec)
        elif mode in "%":
            return self.aptratio.print_percent()
        elif mode in "obj":
            return self.aptratio

    def match_ratio_tollerance(self, vals, toll):
        return self.aptratio.match_tollerance(vals, toll)

    # call after floorLayout fully created
    def apprise(self):
        self.eval_apart_ratio()
        return self


####################################################################
# Evaluation modules below
####################################################################
class EvalBase:
    def __init__(self, bands, name="b", precision=4):
        self.evname = name
        # evaluation band names
        self._bands = bands
        # keeped as float
        self._values = OrderedDict()
        # used for float round ups
        self._prec = precision

    @property
    def pr(self):
        return self._prec

    @property
    def val(self):
        return [f2f(v, self.pr) for v in self._values.values()]

    def valstr(self, prec=None, altval=None):
        if not altval:
            altval = self.val
        if not prec:
            prec = self.pr
        return [f2s(v, prec) for v in altval]

    def setval(self, name, val):
        self._values[name] = val
        return self

    def setvals(self, vals):
        # print(isinstance(vals, dict) or isinstance(vals, OrderedDict))
        if isinstance(vals, dict) or isinstance(vals, OrderedDict):
            # print("working with dict")
            for k, v in vals.items():
                self.setval(k, v)
        else:
            for i, v in enumerate(self._values.keys()):
                k = list(self._values.keys())[i]
                self.setval(k, vals[i])
        return self

    def reset(self, chaincall=None):
        # print(self.evname, "reset")
        self._values = OrderedDict()
        for k, v in self._bands.items():
            self._values[k] = f2f(0.0, self.pr)
        if chaincall is not None:
            chaincall(self)
        return self

    def for_print(self, altval=None, nonzero=True, prec=None):
        if prec is None:
            prec = self.pr
        if not altval:
            altval = self.valstr(altval=altval, prec=prec)
        bands = self._bands.keys()
        longest = max([len(k) for k in bands])
        # pad band names with spaces
        bands = [b.ljust(longest - len(b), " ") for b in bands]
        vals = zip(bands, altval)

        if nonzero:
            vals = [v for v in vals if f2s(v[1], self.pr) != f2s(0, self.pr)]
        return "\n".join([": ".join([n, f2s(v, prec)]) for n, v in vals])

    def __repr__(self):
        vals = self.valstr(2)
        if not sum([int(v[0]) for v in vals]):
            vals = [v[1:] for v in vals]
        return "".join(["|", self.evname, "|", " ".join(vals), "| "])

    # def __str__(self):
    #     vals = zip(self._bands.keys(), self.values_str)
    #     return "\n".join([": ".join([n, v]) for n, v in vals])


class LayoutSize(EvalBase):
    def __init__(self, prec=2):
        if prec <= 1:
            prec = 2
        b = ["x", "y", "midlen", "loglen", "faclen", "wid"]
        bands = OrderedDict(zip(b, range(len(b))))
        EvalBase.__init__(self, bands, "sz", prec)
        self.reset()


class ApartmentRatio(EvalBase):
    bands = OrderedDict([("st", 0), ("b1", 1), ("b2", 2), ("b3", 3), ("b4", 4)])

    def __init__(self, prec=6):
        if prec <= 1:
            prec = 2
        EvalBase.__init__(self, ApartmentRatio.bands, "a%", prec)
        self.reset(chaincall=self._postreset())

    def _postreset(self):
        # print("postreset")
        self.bedsCount = OrderedDict()

    def evaluate(self, bedrooms):
        self.reset(chaincall=self._postreset())
        # print "_values", self.values
        total = len(bedrooms)
        count = OrderedDict()
        # print "unq bdrm", set(bedrooms)
        for bd in set(bedrooms):
            count[bd] = bedrooms.count(bd)
        # print "count", count
        self.bedsCount = count
        m = OrderedDict([(vv, kk) for kk, vv in self._bands.items()])
        for k, v in count.items():
            self.setval(m[k], f2f(float(v) / total))
        # print(sum(self.val))
        itr = 5
        while not self.balance_total() and itr > 0:
            # print("while runs ", abs(5 - itr))
            itr -= 1

    def from_ratios(self, st=0, b1=0, b2=0, b3=0, b4=0, balance=False, ratios=None):
        if ratios is None:
            ratios = [st, b1, b2, b3, b3]
            self.setvals(ratios)
        else:
            if (len(self._values.keys()) - len(ratios)) != 0:
                # print("len not equal")
                if isinstance(ratios, dict) or isinstance(ratios, OrderedDict):
                    self.setvals(ratios)
                else:
                    l = ratios[:]
                    for i in range(len(self._values.keys()) - len(ratios)):
                        l.append(0.0)
                    self.setvals(l)
        if balance:
            self.balance_bands()
        return self

    def balance_total(self):
        # balance total to exact 1.0
        # print("run balance")
        d = f2f(-sum(self.val) + 1.0, self.pr + 1)
        if len(str(f2f(d, self.pr + 1)).split(".")[1]) > self.pr:
            self._prec = self.pr + 1
        nonzero = [(k, v) for k, v in self._values.items() if v != 0.0]
        change_key = sorted(nonzero, key=lambda x: x[1])[0][0]
        self._values[change_key] += d
        return self.validate_total()

    def validate_total(self):
        return sum(self.val) == 1.0

    def balance_bands(self):
        total = sum(self.val)
        if total != 0:
            val = [f2f(v / total, self.pr) for v in self.val]
        self.setvals(val)
        itr = 5
        while not self.balance_total() and itr > 0:
            itr -= 1

    def print_ratio(self, prec=None):
        if prec is None:
            prec = self.pr
        return self.for_print(prec=prec)

    def print_beds(self):
        return self.for_print(altval=self.bedsCount.values(), prec=0)

    def print_percent(self, prec=2):
        if prec < 2:
            prec = 2
        val = [f2f(float(v * 100), prec) for v in self.val]
        frmt = self.for_print(altval=val, prec=prec).splitlines()
        return "\n".join(["".join([s, " %"]) for s in frmt])

    def match_ratio(self, other, tolerance=None):
        if tolerance is None:
            tolerance = f2f(0.02, 2)
        vv = [f2f(self._values[k], self.pr) for k in other.keys()]
        ov = [f2f(other[k], self.pr) for k in other.keys()]

        pairs = list(zip(vv, ov))
        delta = [abs(a - b) for (a, b) in pairs]
        print([d <= tolerance for d in delta])
        match = all([d <= tolerance for d in delta])
        return match


if __name__ == "__main__":
    # start = time.process_time_ns()
    # print(time.time())
    # bedrooms = [1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    bedrooms = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4]
    # bedrooms = [1, 1, 2, 3, 3]
    fl = OrderedDict([("b3", 0.4), ("b2", 0.23)])
    ft = [0, 0, 0.2, 0.4]
    # def eval_apart_ratio(self):
    #     aparts = self.target.get_apartments()
    #     bedrooms = [apt.bedrooms for apt in aparts]
    #     self.aptratio.evaluate(bedrooms)
    class TAPT:
        def __init__(self, b):
            self.bedrooms = b

    class TFL:
        def __init__(self):
            self.aprts = []
            bdr = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4]
            for b in bdr:
                self.aprts.append(TAPT(b))

        def get_apartments(self):
            return self.aprts

    test_layout = TFL()
    tla = LayoutAppriser(target=test_layout).apprise()
    print(tla.aprt())
    print(tla.aprt("."))

    # print(time.time())
    # print(time.process_time_ns() - start)
    # ar = ApartmentRatio(prec=4)
    # ar.evaluate(bedrooms)

    # ApartmentRatio.balance_bands(ft)
    # print(ar)
    # print(ar.print_ratio())
    # print(ar.print_percent())
    # print(ar.print_beds())
    # print(ar.match_ratio(fl, 0.1))
    # pr = ApartmentRatio().from_ratios(ratios=fl)
    # print(pr.print_ratio(2))
    # print(ApartmentRatio().from_ratios(ratios=ft).print_ratio())
    # print(ar.for_print_beds())
    # print(ar.val_beds())
