# -*- coding: utf-8 -*-
"""
Created on 28 May 2022

@author: prslvtsv
"""
import sys


def init(path="", remote=True, modules=True, autoupdate=True, misc=True):
    # current version does't handl partial init
    path += sys.path[0]
    path += "\\gblock\\gh_context\\"
    path += "context_general.txt"
    file = open(path, "rt")
    blocks = file.read().split("%block_spliter")
    file.close()

    return blocks


###############################################################################
# CONTEXT CREATOR BELOW | ADDS DEV METODS TO COMPONENT
# SEE GH_CONTEXT\CONTEXT_GENERAL.TXT FOR DETAILS
###############################################################################

# exec(compile("".join(context.init()),"init","exec"),locals())

###############################################################################
