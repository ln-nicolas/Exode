from ..Core import logObj
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

    def setupEvent(self, eventList):
        self._event= [CallBack() for event in eventList]

    def attachEvent(self, event, callback, *args):
        self._event[event].setCallBack(callback, *args)
        self.log(".attachEvent("+event+", "+str(callback)+", "+str(args))

    def event(self, event):
        return self._event[event]

    def detachEvent(self, event):
        self._event[event].reset()
        self.log(".detachEvent("+event+")")
