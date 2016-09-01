#   global.py
#
#   This file contained the global variables use
#   by the Exode library
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

# board's functions
_FUNCTIONS = {

    "pinMode":0,
    "digitalWrite":1,
    "digitalRead":2,
    "digitalSwitch":3,

    "analogWrite":4,
    "analogRead":5,

    "addServo":6,
    "removeServo":7,
    "writeServo":8,

    "pulse":9,
    "pulseIn":10,

    "executeThread":11,
    "initThread":12,
    "deleteThread":13,

    "checkExode":14
    }
    
_INV_FUNCTIONS = {v: k for k, v in _FUNCTIONS.items()}
def ID(name):
    return _FUNCTIONS[name]

_VARIABLES = {
    0:0,
    1:1,
    'OUTPUT':1,
    'INPUT':0,
    'HIGH':1,
    'LOW': 0,
    'ON':1,
    'OFF':0
}
