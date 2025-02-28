
#Sets up colours
ColourLibrary = {
    "BLACK"        : (0 ,0, 0),
    "WHITE"        : (255, 255, 255),
    "SEA"          : (48, 84, 117),
    "WATER"        : (72, 154, 199),
    "SAND"         : (186, 170, 132),
    "BACKGROUND"   : (167, 198, 217),
    "OOZE"         : (106, 189, 85),
    "OIL"          : (26, 21, 21),
    "GOOP"         : (104, 32, 145),
    "STONE"        : (110,110,110),
    "BRICK"        : (173, 95, 81),
    "BLOOD"        : (120, 7, 7),
    "DIRT"         : (135, 98, 80),
    "MUD"          : (56, 31, 25),
    "LIME"         : (232, 230, 183),
    "MARBLE"       : (235, 234, 230),
    "ERASE"        : (255, 255, 255),
    "BUTTONUP"     : (227, 216, 220),
    "FUNCTIONUP"   : (177, 204, 161),
    "FUNCTIONFONT" : (131, 150, 119),
    "MENUCOLOUR"   : (161, 177, 204),
    "MENUACCENT"   : (123, 136, 158),
    "BUTTONFONT"   : (145, 134, 139),
    "GRASS"        : (97, 171, 87),
    "ROT"          : (93, 110, 50),
    "WIRE"         : (138, 119, 92),
    "SPARK"        : (236, 245, 76),
    "SALT"         : (145, 145, 145),
    "SEED"         : (186, 186, 147),
    "SEEDED"       : (130, 102, 64),
    "VOID"         : (0, 0, 0),
    "SPONGE"       : (207, 202, 72),
    "LAVA"         : (209, 77, 6),
    "GLASS"        : (96, 225, 240),
    "MAGMA"        : (209, 77, 6),
    "BASALT"       : (48, 47, 44)
    }

#Sets up pixel identities
#A pixel value holds the following information: [Priority, Particle Class, Colour, Particle Name, indication of equilateral momentum]
PixelLibrary = {
    "ERASE" : [99, 0, ColourLibrary["ERASE"], "ERASE",0],
    "OIL"   : [8,  3, ColourLibrary["OIL"], "OIL", 0],
    "WATER" : [10, 3, ColourLibrary["WATER"], "WATER", 0],
    "STONE" : [30, 2, ColourLibrary["STONE"], "STONE", 0],
    "SAND"  : [20, 2, ColourLibrary["SAND"], "SAND", 0],
    "BRICK" : [90, 0, ColourLibrary["BRICK"], "BRICK", 0],
    "SEA"   : [12, 3, ColourLibrary["SEA"], "SEA", 0],
    "GOOP"  : [20, 3, ColourLibrary["GOOP"], "GOOP", 0],
    "OOZE"  : [20, 3, ColourLibrary["OOZE"], "OOZE", 0],
    "BLOOD" : [10, 3, ColourLibrary["BLOOD"], "BLOOD", 0],
    "VOID"  : [90, 0, ColourLibrary["VOID"], "VOID", 0],
    "DIRT"  : [15, 2, ColourLibrary["DIRT"], "DIRT", 0],
    "MUD"   : [10, 3, ColourLibrary["MUD"], "MUD", 0],
    "LIME"  : [18, 2, ColourLibrary["LIME"], "LIME", 0],
    "MARBLE": [32, 0, ColourLibrary["MARBLE"], "MARBLE", 0],
    "GRASS" : [90, 1, ColourLibrary["GRASS"], "GRASS", 0],
    "ROT"   : [90, 0, ColourLibrary["ROT"], "ROT", 0],
    "WIRE"  : [90, 0, ColourLibrary["WIRE"], "WIRE", 0],
    "SPARK" : [90, 0, ColourLibrary["SPARK"], "SPARK", 0],
    "SALT"  : [15, 2, ColourLibrary["SALT"], "SALT", 0],
    "SEED"  : [5,  2, ColourLibrary["SEED"], "SEED", 0],
    "SEEDED": [99, 1, ColourLibrary["SEEDED"], "SEEDED", 0],
    "SPONGE": [90, 0, ColourLibrary["SPONGE"], "SPONGE", 0],
    "LAVA"  : [25, 3, ColourLibrary["LAVA"], "LAVA", 0],
    "MAGMA" : [25, 3, ColourLibrary["MAGMA"], "MAGMA", 0],
    "GLASS" : [90, 0, ColourLibrary["GLASS"], "GLASS", 0],
    "BASALT": [40, 1, ColourLibrary["BASALT"], "BASALT", 0]
    }

#Specific list with VOID and ERASE filtered out for pixel interaction 
NonVoidLister = list(PixelLibrary.keys())
ListNonVoided = NonVoidLister[:NonVoidLister.index('VOID')] + NonVoidLister[NonVoidLister.index('VOID')+1:]
NonEraseLister = ListNonVoided[:ListNonVoided.index('ERASE')] + ListNonVoided[ListNonVoided.index('ERASE')+1:]


#List of possible interactions
#[0] is the pixel considered for transformation (A)
#[1] are the pixels that are considered as agents (B)
#[2] is the pixel into which A will turn when in contact with B (C)
#[3] is the internal chance a transformation will occur where the cap is 10000
#[4] are all the possible pixel locations in respect to the current pixel using PixelSenser() for which transformation can occur
#[5] indicates if the agent is removed after transformation where True = -B
PixelInteractionLibrary = [
    ["STONE", ["WATER", "SEA"],    "SAND",     9975, [1,2,3,4,5,6,7,8], False],
    ["LIME",  ["MARBLE", "STONE"], "MARBLE",   9950, [1,2,3],           False],
    ["LIME",  ["OOZE"],            "OOZE",     8000, [1,2,3,4,5,6,7,8], True],
    ["LIME",  ["WATER"],           "WATER",    9940, [1,2,3,4,5,6,7,8], True],
    ["SALT",  ["WATER"],           "SEA",      9975, [1,2,3,4,5,6,7,8], True],
    ["GOOP",  ["OOZE"],            "WATER",    9500, [1,2,3,4,5,6,7,8], True],
    ["SALT",  ["GOOP"],            "OOZE",     9995, [1,2,3,4,5,6,7,8], True],
    ["DIRT",  ["WATER", "SEA"],    "MUD",      9970, [1,2,3,4,5,6,7,8], True],
    ["BLOOD", ["OOZE", "ROT"],     "ROT",      9900, [1,2,3,4,5,6,7,8], False],
    ["GRASS", ["OOZE", "ROT"],     "ROT",      9900, [1,2,3,4,5,6,7,8], True],
    ["ROT",   ["ERASE", "OOZE"],   "OOZE",     9900, [1,2,3,4,5,6,7,8], False],
    ["SEED",  ["DIRT"],            "SEEDED",   9100, [7],               True],
    ["SEEDED",["ERASE"],           "GRASS",    9950, [1,2,3,4,5],       False],
    

    ["VOID", NonEraseLister, "VOID", 0, [1,2,3,4,5,6,7,8], True],
    ["SPONGE",["OIL", "WATER", "SEA", "GOOP", "OOZE", "BLOOD"], "SPONGE", 0, [1,2,3,4,5,6,7,8], True],
    ["STONE",["LAVA", "MAGMA"], "MAGMA", 9940, [1,2,3,4,5,6,7,8], False],
    ["LAVA",["SEA", "WATER"], "BASALT", 9900, [1,2,3,4,5,6,7,8], True],
    ["MAGMA",["SEA", "WATER"], "STONE", 9900, [1,2,3,4,5,6,7,8], True],
    ["SAND",["LAVA"], "GLASS", 9960, [1,2,3,4,5,6,7,8], False]
    
    ]



ButtonLibrary = {
    (0, 0) : "SAND",
    (0, 1) : "STONE",
    (0, 2) : "LIME",
    (0, 3) : "DIRT",
    (0, 4) : "SALT",
    (1, 0) : "WATER",
    (1, 1) : "SEA",
    (1, 2) : "GOOP",
    (1, 3) : "OOZE",
    (1, 4) : "OIL",
    (1, 5) : "MUD",
    (1, 6) : "BLOOD",
    (1, 7) : "LAVA",
    (2, 0) : "BRICK",
    (2, 1) : "MARBLE",
    (2, 2) : "GRASS",
    (2, 3) : "WIRE",
    (2, 4) : "SEED",
    (2, 5) : "SPARK",
    (2, 6) : "ROT",
    (2, 7) : "ERASE",
    (2, 8) : "GLASS",
    
    #Not end-functional buttons
    (3, 0) : "SEEDED",
    (3, 1) : "VOID",
    (3, 2) : "SPONGE",
    (3, 3) : "BASALT",
    (3, 4) : "MAGMA"
    }

