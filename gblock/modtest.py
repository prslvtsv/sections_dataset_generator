# -*- coding: utf-8 -*-
"""
Created on 15 May

@author: prslvtsv
"""

import database as db
reload(db)


dct = {'attr1':'one', 'attr2':'two', 'attr3':'three'}

def xarrtest():
    db.test_creation()

def v_as(val = ' ', **kwargs):
    name = kwargs.pop('name', None)
    print name


if __name__ == '__main__':
    # xarrtest()
    v_as(dct)

