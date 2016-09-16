from . import InstructionSet, byte, long, float, signedLong

exodeInstructionSet = InstructionSet(name="Exode")

instructions = [
    [0,  "pinMode",                byte*3],
    [1,  "digitalWrite",           byte*2],
    [2,  "digitalRead",            byte*2],
    [3,  "digitalSwitch",          byte],
    [4,  "analogWrite",            byte*2],
    [5,  "analogRead",             byte*2],
    [6,  "addServo",               byte*2 + long],
    [7,  "removeServo",            byte],
    [8,  "writeServo",             byte + long],
    [9,  "pulse",                  byte + long],
    [10, "pulseIn",                byte*2],
    [14, "checkExode",             []],
    [15, "addStepper",             byte*6],
    [16, "setStepperAcceleration", byte + float],
    [17, "setStepperSpeed",        byte + float],
    [18, "moveStepper",            byte + signedLong]
]

for inst in instructions:
    id = inst[0]
    name = inst[1]
    types = inst[2]
    exodeInstructionSet.setInstruction(id, name, types)
