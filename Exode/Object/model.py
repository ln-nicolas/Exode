from ..Core import *
from ..Core.boardManager import *
from ..Core.callback import *

class obj:

    def __init__(self, signature, autoLoad=True):
        self.signature= signature
        if autoLoad:
            BOARD.autoAddObj(self)

    def __repr__(self):
        return str(self.board)+"."+self.signature

    def log(self, msg):
        logObj(str(self)+msg)

    def on(self, board):
        if self.board == None:
            self.setup(board)
        return self

    def setupEvent(self, eventList):
        self._event= {event:CallBack() for event in eventList}

    def attachEvent(self, event, callback, *args):
        self.log(".attachEvent("+event+", "+str(callback)+", "+str(args))
        if not event in self._event:
            logCore(event+" is not defined on "+str(self))
        self._event[event].setCallback(callback, *args)

    def event(self, event):
        return self._event[event]

    def detachEvent(self, event):
        if not event in self._event:
            logCore(event+" is not defined on "+str(self))
        self._event[event].reset()
        self.log(".detachEvent("+event+")")
