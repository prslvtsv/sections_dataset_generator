# -*- coding: utf-8 -*-
"""Module to enable even callbacks inside GH using Rhino Events

This module uses ghPython component uinique runtime ID to create per component
event handler and expire quie in global Rhino context.
Aslo uses component locals() to pass object references around (arg:"loc" in methods)


UPD 17.06.2022: Mainly used now for automatic component recompute
    helping with Rhino script context sticky variables usage.
    resolves issue when context updates do not propagate to the component,
    unless it's manualy updated.

    It becomes ridiculously painful to click and re-run every compoennt one by one,
    when having several of them utilizing Rhino sctipt context (SC)

Created on 23.05.2022
@author: prslvtsv
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Grasshopper.Kernel as kernel
import Rhino

key_events = "events"
key_comp_expire = "component_expire"
key_comp_event_obj = "component_event_obj"

# try:
#     locals()['sc']
#
class ExpireEvent(object):

    envInitilized = False

    def __init__(self, component):
        self.id = component.InstanceGuid.ToString()
        self.component = component

        ExpireEvent.envInitilized = ExpireEvent.init_events()
        sc.sticky[key_comp_expire][self.id] = False

    @staticmethod
    def init_events():
        if ExpireEvent.envInitilized:
            return True

        # ensure all context dictionaries created
        if key_events not in sc.sticky:
            sc.sticky[key_events] = {}
        if key_comp_expire not in sc.sticky:
            sc.sticky[key_comp_expire] = {}
        if key_comp_event_obj not in sc.sticky:
            sc.sticky[key_comp_event_obj] = {}

        return True

    def trigger_expire(self):
        sc.sticky[key_comp_expire][self.id] = True

    def track(self, event, func, key):
        self.key_id = "{}:{}".format(key, self.id)
        firstRun = False
        # register event type
        if self.key_id not in sc.sticky[key_events]:
            sc.sticky[key_events][self.key_id] = event
            firstRun = True

        # register callback
        if self.key_id not in sc.sticky:
            sc.sticky[self.key_id] = func
            event += sc.sticky[self.key_id]
            firstRun = True

        # register exire event flag
        if self.id not in sc.sticky[key_comp_expire]:
            sc.sticky[key_comp_expire][self.id] = False
            firstRun = True

        # register event object to allow unregistration
        if self.id not in sc.sticky[key_comp_event_obj]:
            sc.sticky[key_comp_event_obj][self.id] = self
            firstRun = True

        return firstRun

    @staticmethod
    def untrack_component(guid):
        if guid in sc.sticky[key_comp_event_obj].keys():
            if sc.sticky[key_comp_event_obj][guid].untrack():
                sc.sticky[key_comp_event_obj].pop(guid, None)

    def untrack(self):
        if self.key_id in sc.sticky[key_events].keys():
            if self.key_id in sc.sticky.keys():
                sc.sticky[key_events][self.key_id] -= sc.sticky[self.key_id]
                sc.sticky[key_events].pop(self.key_id)
                sc.sticky.Remove(self.key_id)

        sc.sticky[key_comp_expire].pop(self.id, None)

        return True

    # @staticmethod
    # def untrack_all():
    #     for key in sc.sticky[key_events]:
    #         if key in sc.sticky:
    #             sc.sticky[key_events][key] -= sc.sticky[key]
    #             sc.sticky.Remove(key)
    #     sc.sticky[key_events] = {}
    #
    #     for key in sc.sticky[key_comp_expire]:
    #         sc.sticky[key_comp_expire].clear()
    #     # sc.sticky["component_expire"] = {}

    def expire_event(self, sender, e):
        if sc.sticky[key_comp_expire][self.id] == True:
            # rs.MessageBox(
            #     "solution expired for {}".format(self.id),
            #     buttons=0,
            #     title="Component Expire",
            # )

            self.component.ExpireSolution(True)
            sc.sticky[key_comp_expire][self.id] = False


def is_tracking_updates(loc):
    try:
        # print loc["ghenv"].Component.InstanceGuid.ToString()
        # print loc["sc"].sticky[key_comp_event_obj]
        return (
            loc["ghenv"].Component.InstanceGuid.ToString()
            in loc["sc"].sticky[key_comp_event_obj]
        )
    except:
        print "check tracking except"
        return False


def register_component_updates(loc):
    ExpireEvent.init_events()
    exp_event = ExpireEvent(loc["ghenv"].Component)
    exp_event.track(Rhino.RhinoApp.Idle, exp_event.expire_event, "Rhino_Idle")
    # ghenv[0].Component.ExpireSolution(True)


def unregister_component_updates(loc):
    try:
        ExpireEvent.untrack_component(loc["ghenv"].Component.InstanceGuid.ToString())
    except:
        print "no auto update registered"


def unregister_updates_all(ids):
    for id in ids:
        try:
            ExpireEvent.untrack_component(id)
        except:
            print "no auto update registered"
