from ..Core import *
from ..Core.boardManager import *
from ..Core.callback import *

def uix_updater(func):
    def wrapper(self, *args):
        val = func(self, *args)

        for view in self.ui_view:
            view.update()

        return val
    return wrapper

class obj:

    def __init__(self, name, autoLoad=True, pins=[], type="obj"):

        self.name= name
        self.pins= pins
        self.type= type

        self.ui_view= []

        if autoLoad:
            BOARD.autoAddObj(self)

    def __repr__(self):
        return str(self.board)+"."+self.name

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

    @uix_updater
    def attachView(self, view):
        self.ui_view.append(view)

    def setPlot(self, plot):
        self._plot= plot

    def event(self, event):
        return self._event[event]

    def detachEvent(self, event):
        if not event in self._event:
            logCore(event+" is not defined on "+str(self))
        self._event[event].reset()
        self.log(".detachEvent("+event+")")
