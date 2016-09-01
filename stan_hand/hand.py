
MAX_IN = 0
MAX_MA = 0
MAX_AN_= 0
MAX_AU = 0

class Hand(BoardObj):

    def __init__(self, echo, trig, **kwargs):

        self._servoIndex = Servo()



        BoardObj.__init__(self, 'STAN\'s hand', pins=[])
