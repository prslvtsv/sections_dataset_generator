# -*- coding: utf-8 -*-
"""
Created on 16 May 2022

@author: prslvtsv
"""

# TODO
# • use list instead
# • remove name codes
# • provide options just with value, remove rest

attrFloorUser = {
    "residentialClass": {
        "name": "residentialClass",
        "nameRU": "класс жилья",
        "nameCode": "RESCL",
        "options": [
            {"value": "base", "valueRU": "базовый", "valueCode": "BS", "pos": 0},
        ],
    },
    "region": {
        "name": "region",
        "nameRU": "регион",
        "nameCode": "REG",
        "options": [
            {
                "value": "moscow",
                "valueRU": "Московская обл",
                "valueCode": "MSC",
                "pos": 0,
            },
        ],
    },
    "buildingTech": {
        "name": "buildingTech",
        "nameRU": "технология строительства",
        "nameCode": "BLDTCH",
        "options": [
            {"value": "monolyth", "valueRU": "монолит", "valueCode": "MON", "pos": 0},
        ],
    },
    "fireClass": {
        "name": "fireClass",
        "nameRU": "класс пожарной безопасности",
        "nameCode": "FRCL",
        "options": [{"value": "c0", "valueRU": "c0", "valueCode": "c0", "pos": 0},],
    },
    "sectionType": {
        "name": "sectionType",
        "nameRU": "тип секции",
        "nameCode": "SCTP",
        "options": [
            {"value": "LLT", "valueRU": "широтная", "valueCode": "LLT", "pos": 0},
            {"value": "LLG", "valueRU": "меридианная", "valueCode": "LLG", "pos": 1},
            {"value": "90SL", "valueRU": "угловая ЮЛ", "valueCode": "90SL", "pos": 2},
            {"value": "90NL", "valueRU": "угловая СЛ", "valueCode": "90NL", "pos": 3},
            {"value": "90SR", "valueRU": "угловая ЮП", "valueCode": "90SR", "pos": 4},
            {"value": "90NR", "valueRU": "угловая СП", "valueCode": "90NR", "pos": 5},
        ],
    },
    "tailType": {
        "name": "tailType",
        "nameCode": "TT",
        "nameRU": "положение в блоке",
        "options": [
            {
                "value": "openOpen",
                "valueRU": "отдельно стоящая",
                "valueCode": "OO",
                "pos": 0,
            },
            {
                "value": "openClose",
                "valueRU": "торец в конце",
                "valueCode": "OC",
                "pos": 1,
            },
            {
                "value": "closeOpen",
                "valueRU": "торец в начале",
                "valueCode": "CO",
                "pos": 2,
            },
            {
                "value": "closeClose",
                "valueRU": "внутри блока",
                "valueCode": "CC",
                "pos": 3,
            },
        ],
    },
    "firstFloor": {
        "name": "firstFloor",
        "nameCode": "FFT",
        "nameRU": "тип первого этажа",
        "options": [
            {
                "value": "regularLiving",
                "valueRU": "типовой этаж",
                "valueCode": "RL",
                "pos": 0,
            },
            {
                "value": "groundLiving",
                "valueRU": "первый жилой",
                "valueCode": "GL",
                "pos": 1,
            },
            {
                "value": "groundCommerce",
                "valueRU": "первый внп",
                "valueCode": "GC",
                "pos": 2,
            },
            {
                "value": "groundMixed",
                "valueRU": "первый смешанный",
                "valueCode": "GM",
                "pos": 3,
            },
        ],
    },
    "heightLimit": {
        "name": "heightLimit",
        "nameRU": "пожарная высота",
        "nameCode": "HLM",
        "options": [
            # какой тут код писать
            {"value": "28", "valueRU": "28", "valueCode": "HL28", "pos": 0},
            {"value": "50", "valueRU": "50", "valueCode": "HL50", "pos": 1},
            {"value": "75", "valueRU": "75", "valueCode": "HL75", "pos": 2},
        ],
    },
    "corridorWidth": {
        "name": "corridorWidth",
        "nameRU": "ширина коридора",
        "nameCode": "CWDTH",
        "options": [
            # какой тут код писать
            {"value": "1700", "valueRU": "1700", "valueCode": "CW17", "pos": 0},
            {"value": "2200", "valueRU": "2200", "valueCode": "CW22", "pos": 1},
        ],
    },
    "groundFloorAccess": {
        "name": "groundFloorAccess",
        "nameRU": "кол-во входов",
        "nameCode": "GFACC",
        "options": [
            {
                "value": "single",
                "valueRU": "1 входная группа",
                "valueCode": "SIN",
                "pos": 0,
            },
            {
                "value": "pathTrough",
                "valueRU": "проходной",
                "valueCode": "PTH",
                "pos": 1,
            },
            {
                "value": "undefined",
                "valueRU": "неопределен",
                "valueCode": "UNDF",
                "pos": 2,
            },
            # {"value": "na", "valueRU": "na", "valueCode": "NA"},
        ],
    },
    "LLUplacement": {
        "name": "LLUplacement",
        "nameRU": "расположение ЛЛУ",
        "nameCode": "LLUPL",
        "options": [
            {"value": "out", "valueRU": "наружний", "valueCode": "OUT", "pos": 0},
            {"value": "in", "valueRU": "внутренний", "valueCode": "INS", "pos": 1},
        ],
    },
    "distribution": {
        "name": "distribution",
        "nameRU": "распределение",
        "nameCode": "distrib",
        "uiIgnore": "yes",
        "force_pos": -2,
        "type": "flexrange",
        "options": [
            {"value": "0", "valueRU": "0", "valueCode": "0", "pos": 0},
            # {"value": "80", "valueRU": "80", "valueCode": "100", "pos": 0},
            # {"value": "60", "valueRU": "60", "valueCode": "100", "pos": 0},
            # {"value": "40", "valueRU": "40", "valueCode": "100", "pos": 0},
            # {"value": "20", "valueRU": "20", "valueCode": "100", "pos": 0},
            # {"value": "0", "valueRU": "0", "valueCode": "0", "pos": 1},
        ],
    },
    "length": {
        "name": "length",
        "nameRU": "логическая длина",
        "nameCode": "logleng",
        "uiIgnore": "yes",
        "force_pos": -1,
        "type": "flexrange",
        "options": [
            {"value": "0", "valueRU": "0", "valueCode": "0", "pos": 0},
            # {"value": "1", "valueRU": "макс", "valueCode": "1", "pos": 1},
            # {"value": "2", "valueRU": "макс", "valueCode": "2", "pos": 2},
            # {"value": "3", "valueRU": "макс", "valueCode": "3", "pos": 3},
            # {"value": "4", "valueRU": "макс", "valueCode": "4", "pos": 4},
            # {"value": "max", "valueRU": "макс", "valueCode": "max", "pos": 5},
        ],
    },
    # 'LLUshift': {
    #     'name':'LLUshift',
    #     'nameRU':'сдвиг ЛЛУ',
    #     'nameCode':'LLUSHFT',
    #     #слайдер
    #     'options':[
    #         {'value':'_slider_', 'valueRU':'_slider_', 'valueCode':'_sliderLLUSHFT_'},
    #         ]
    #     },
    # слайдеры по ширине и длине блока
    # 'sectionLen1': {
    #     'name':'sectionLen1',
    #     'nameRU':'Длина 1',
    #     'nameCode':'L1',
    #     'options':[
    #         {'value':'_slider_', 'valueRU':'_slider_', 'valueCode':'_sliderL1_'},
    #         ]
    #     },
    # 'sectionLen2': {
    #     'name':'sectionLen2',
    #     'nameRU':'Длина 2',
    #     'nameCode':'L2',
    #     'options':[
    #         {'value':'_slider_', 'valueRU':'_slider_', 'valueCode':'_sliderL2_'},
    #         ]
    #     },
    # 'sectionWid1': {
    #     'name':'sectionWid1',
    #     'nameRU':'Ширина 1',
    #     'nameCode':'W1',
    #     'options':[
    #         {'value':'_slider_', 'valueRU':'_slider_', 'valueCode':'_sliderW1_'},
    #         ]
    #     },
    # 'sectionWid2': {
    #     'name':'sectionWid2',
    #     'nameRU':'Ширина 2',
    #     'nameCode':'W2',
    #     'options':[
    #         {'value':'_slider_', 'valueRU':'_slider_', 'valueCode':'_sliderW2_'},
    #         ]
    #     },
}


attrFloorGeneral = {
    "floorType": {
        "name": "floorType",
        "nameCode": "FT",
        "options": [
            {"value": "regular", "valueCode": "reg"},
            {"value": "first", "valueCode": "frst"},
            {"value": "last", "valueCode": "lst"},
        ],
    },
    "floorUsage": {
        "name": "floorUsage",
        "nameCode": "FU",
        "options": [
            {"value": "residential", "valueCode": "rsd"},
            {"value": "commerce", "valueCode": "cmm"},
            {"value": "mixed", "valueCode": "mxt"},
        ],
    },
    "azimuthRange": {
        "name": "azimuthRange",
        "nameCode": "AR",
        "options": [
            {"value": "315-45", "valueCode": "0"},
            {"value": "45-135", "valueCode": "90"},
            {"value": "135-225", "valueCode": "180"},
            {"value": "225-315", "valueCode": "270"},
        ],
    },
    "bendDegree": {
        "name": "bendDegree",
        "nameCode": "BD",
        "options": [
            {"value": "0", "valueCode": "0"},
            {"value": "90", "valueCode": "90"},
            {"value": "135", "valueCode": "135"},
        ],
    },
    "sideJoinStart": {
        "name": "sideJoinStart",
        "nameCode": "SJS",
        "options": [
            {"value": False, "valueCode": "0"},
            {"value": True, "valueCode": "1"},
        ],
    },
    "sideJoinEnd": {
        "name": "sideJoinEnd",
        "nameCode": "SJE",
        "options": [
            {"value": False, "valueCode": "0"},
            {"value": True, "valueCode": "1"},
        ],
    },
    "heightLimit": {
        "name": "heightLimit",
        "nameCode": "HL",
        "options": [
            {"value": 28, "valueCode": "28"},
            {"value": 50, "valueCode": "50"},
            {"value": 75, "valueCode": "75"},
        ],
    },
    "corridorWidth": {
        "name": "corridorWidth",
        "nameCode": "CW",
        "options": [{"value": 1.7, "valueCode": "n"}, {"value": 2.2, "valueCode": "w"}],
    },
    # новые от Альфии
    "lengthLogicalLow": {
        "name": "lengthLogicalLow",
        "nameCode": "LLL",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lengthLogicalHigh": {
        "name": "lengthLogicalHigh",
        "nameCode": "LLH",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lengthLogicalNow": {
        "name": "lengthLogicalNow",
        "nameCode": "LLN",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lengthSpacialLow": {
        "name": "lengthSpacialLow",
        "nameCode": "LSL",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lengthSpacialHigh": {
        "name": "lengthSpacialHigh",
        "nameCode": "LSH",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lengthSpacialNow": {
        "name": "lengthSpacialNow",
        "nameCode": "LSN",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lengthTweekRange": {
        "name": "lengthTweekRange",
        "nameCode": "LTR",
        "options": [{"value": "", "valueCode": ""}],
    },
    "distributionRange": {
        "name": "distributionRange",
        "nameCode": "DR",
        "options": [{"value": "", "valueCode": ""}],
    },
    "distributionLogical": {
        "name": "distributionLogical",
        "nameCode": "DL",
        "options": [{"value": "", "valueCode": ""}],
    },
    "distributionNormalized": {
        "name": "distributionNormalized",
        "nameCode": "DN",
        "options": [{"value": "", "valueCode": ""}],
    },
    "elevatorInsideOutside": {
        "name": "elevatorInsideOutside",
        "nameCode": "EIO",
        "options": [{"value": "", "valueCode": ""}],
    },
    "elevatorPlacementRange": {
        "name": "elevatorPlacementRange",
        "nameCode": "EPA",
        "options": [{"value": "", "valueCode": ""}],
    },
    "elevatorPlacementNow": {
        "name": "elevatorPlacementNow",
        "nameCode": "EPN",
        "options": [{"value": "", "valueCode": ""}],
    },
    "apptLayoutConfiguration": {
        "name": "apptLayoutConfiguration",
        "nameCode": "ALC",
        "options": [{"value": "", "valueCode": ""}],
    },
    "tileWidthSet": {
        "name": "tileWidthSet",
        "nameCode": "TWS",
        "options": [{"value": "", "valueCode": ""}],
    },
    "depthOuterNow": {
        "name": "depthOuterNow",
        "nameCode": "DON",
        "options": [{"value": "", "valueCode": ""}],
    },
    "depthInnerNow": {
        "name": "depthInnerNow",
        "nameCode": "DIN",
        "options": [{"value": "", "valueCode": ""}],
    },
    "depthTotalNow": {
        "name": "depthTotalNow",
        "nameCode": "DTN",
        "options": [{"value": "", "valueCode": ""}],
    },
    "apptTypeDistribution": {
        "name": "apptTypeDistribution",
        "nameCode": "ATD",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lengthTweek": {
        "name": "lengthTweek",
        "nameCode": "LT",
        "options": [{"value": "", "valueCode": ""}],
    },
    "evaluationParam": {
        "name": "evaluationParam",
        "nameCode": "EP",
        "options": [{"value": "", "valueCode": ""}],
    },
    "urbanBlockposition": {
        "name": "UrbanBlockposition",
        "nameCode": "UBP",
        "options": [{"value": "", "valueCode": ""}],
    },
    "lluType": {
        "name": "LluType",
        "nameCode": "LUT",
        "options": [{"value": "", "valueCode": ""}],
    },
    "entranceType": {
        "name": "EnterGroupType",
        "nameCode": "EGT",
        "options": [{"value": "", "valueCode": ""}],
    },
}


# sectionType:
# tailType:
# firstFloor:
# groundFloorAccess:
# LLUplacement:
# length:min/max
# distribution:0/100


# sectionType:90SL
# tailType:openOpen
# firstFloor:regularLiving
# groundFloorAccess:n/a
# LLUplacement:out
# length:max
# distribution:0
