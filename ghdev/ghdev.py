# -*- coding: utf-8 -*-
"""New Context initilizer (see gh_context module for old version)

Currently WIP

Created on 04 June 2022
for Aective Team
@author: prslvtsv
"""


def init_dev_tools(loc, path="", conf=True, verbose=False):
    """ loads and defines bunch of dev tools, pushes them back to component"""
    # declare here localOnly vars
    import pins as pin

    reload(pin)
    import libloader as libs

    reload(libs)
    # reload(delete_pins)
    # reload(exist)
    pinMapIn = None
    config = []
    temp = None
    ordDict = None
    k = None
    # save var names which wont be pushed back to component
    _localOnlyKeys = None
    _localOnlyKeys = locals().keys()

    ###################################################################
    # WARNING : everything declared below pushed back to the component!
    ###################################################################

    # if component has settings input with valid congiguration - use it
    try:
        if "settings" in loc.keys():
            if len(loc["settings"]) > 0:
                config = loc["settings"]
    except:
        pass
    #
    #
    # HELPERS
    # //////////////////////////////////////////////////////////
    from devcore import (
        DataContainer,
        gprint,
        printlines,
        printeach,
        recompute_solution_timed,
    )

    # MODULES
    # //////////////////////////////////////////////////////////
    # pushin to component locals here is redundant but these libs  are used
    # in some previously designed init functions so it helps to avoid hustle

    libs.load_modules(loc, locals())
    # printeach(locals().items())
    #
    #

    # PERSISTENT STORAGE
    # //////////////////////////////////////////////////////////
    # check if exists, update assigment
    try:
        loc["sc"].sticky[_pers_id(loc)]
        vault = loc["sc"].sticky[_pers_id(loc)]
        loc["vault"] = vault
    except:
        loc["sc"].sticky[_pers_id(loc)] = DataContainer()
        vault = loc["sc"].sticky[_pers_id(loc)]
        loc["vault"] = vault

    if not vault.has("config"):
        vault.config = config
    else:
        # update on config change & keep config internalized
        if config in "default" or len(config) == 0:
            config = vault.config
        else:
            vault.config = config

    if not vault.has("firstRun"):
        vault.firstRun = True
    #
    #

    # CREATE PININs
    # //////////////////////////////////////////////////////////
    # print ordDict
    pinMapIn = ordDict()
    pinMapIn["set"] = "settings"
    if "forceUpdate" in config:
        pinMapIn["upd"] = "upd_group"
    if "autoPins" in config:
        pinMapIn["autoin"] = "pins_in"
        pinMapIn["autoout"] = "pins_out"

    if not vault.has("pins"):
        print "no pins in vault"
        vault.pins = DataContainer()
        if not vault.pins.has("input"):
            vault.pins.input = ordDict()
        if not vault.pins.has("output"):
            vault.pins.output = ordDict()
        if "strict" not in vault.pins.input.keys():
            vault.pins.input["strict"] = ordDict()
        if "strict" not in vault.pins.output.keys():
            vault.pins.output["strict"] = ordDict()
        if "weak" not in vault.pins.input.keys():
            vault.pins.input["weak"] = ordDict()
        if "weak" not in vault.pins.output.keys():
            vault.pins.output["weak"] = ordDict()

    # pins_to_remove = []
    # if loc['vault'].firstRun:
    #     loc['ghenv'].Component.Param.
    temp = pin.create_pins(loc, "in", pinMapIn.values())
    temp = ordDict(zip(pinMapIn.values(), temp))
    vault.pins.input["strict"] = temp
    temp = None

    # delete pins if config changed
    # if "autoPins" in config:
    temp = []
    print pinMapIn.values()
    for k in vault.pins.input["strict"].keys():
        if k not in pinMapIn.values():
            temp.append(vault.pins.input["strict"][k])
    pin.delete_pins(loc, "in", temp)
    temp = None

    # FORCE UPDATE
    # //////////////////////////////////////////////////////////
    if "forceUpdate":
        pass
    #
    #

    #
    #
    # REMOTE PY
    # //////////////////////////////////////////////////////////
    # checks connections, raises Exception otherwice
    if "remotePy" in config:
        print "remotepy activated"
        _wait_remotepy_connection(loc, recompute_solution_timed)
    #
    #

    # run this at the end of init code block
    # //////////////////////////////////////////////////////////
    _push_to_component_locals(loc, locals(), _localOnlyKeys)

    if "saveSettings" not in config and len(config) > 0:
        vault.config = []
        # clean_presistant_storage(loc)

    if verbose:
        print "following modules & methods initilized "
        printlines(_get_created_names(locals(), _localOnlyKeys))

    def q_expire(loc):
        loc["ghenv"].Component.ExpireSolution(True)

    def q_del_pin(loc):
        _delete_pins(loc, "in", all=True)

    # if vault.firstRun:
    #     vault.toexec = []
    #     vault.toexec.append(q_expire)

    vault.firstRun = False
    # //////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////


def clean_presistant_storage(loc):
    loc["sc"].sticky[_pers_id(loc)] = DataContainer()
    # loc["ghenv"].Component.ExpireSolution(True)


def _pers_id(loc):
    return "".join(
        ["persistent_storage_", loc["ghenv"].Component.InstanceGuid.ToString()]
    )


def _remove_key(_dict, k):
    """ wraper to use del keyword inside generators"""
    del _dict[k]


def _push_to_component_locals(local_external, local_this, saved):
    """ propagate all variables back to component & cleans argumet keys"""
    local_external.update(local_this)
    [_remove_key(local_external, k) for k in saved]


def _get_created_names(loc, saved):
    """ returns only new locals keys"""
    imported = {}
    imported.update(loc)
    [_remove_key(imported, k) for k in saved]
    return ["{} {}".format(k, type(loc[k])) for k in imported.keys()]


def _wait_remotepy_connection(loc, recompute):
    try:
        loc["sc"].sticky["remotepy"]
        connected = sc.sticky["remotepy"]
    except:
        connected = False

    if not connected:
        # recompute component every second
        recompute(loc, 1000)
        loc["ghenv"].Component.AddRuntimeMessage(
            loc["runtimeMessage"].Error,
            " component requires remotepy to work,\nlooking for connection... ",
        )

    # ghenv.Component.ExpireSolution(True)
    # while ghenv.Component.Params.Output.Count > 1:
    #
    #     ghenv.Component.Params.UnregisterOutputParameter(
    #         ghenv.Component.Params.Output[ghenv.Component.Params.Output.Count - 1]
    #     )
