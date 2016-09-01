#   Object.obj.py
#
#   Abstract mother class of all Exode's obj
#
#   Created by Lenselle Nicolas, July, 2016.
#   lenselle.nicolas@gmail.com

from ..Core import BOARD, logCore, logObj, EXD_TIME
from ..Core.callback import CallBack


#
#   Decorator, to update viewers
#
def uix_view_update(func):
    def wrapper(self, *args):
        val = func(self, *args)
        for view in self.views:
            view.update()
        return val
    return wrapper

#
#   AbstractObj, any kind of Exd's obj
#
class AbstractObj:

    def __init__(self, name="noname"):
        self.type  = "obj"
        self.name  = name
        self.views = []
        self.events = {}

        self.color = [0.06, 0.25, 0.49, 1]

    def __repr__(self):
        return self.name

    # log system

    def log(self, msg):
        logObj(str(self)+msg)

    # UIX

    def getUIXView(self):
        # Return a string representation of itself,
        # could be styled with markdown
        return "[b]{}[/b]".format(self.name)

    def getValue(self, name):
        # getter
        return -1

    def setValue(self, value, name):
        # setter
        pass

    @uix_view_update
    def attachView(self, view):
        # Attach a viewer widget to
        # this
        self.views.append(view)

    def setColor(self, color):
        self.color= color

    # Event management

    def setupEvent(self, eventList):
        self.events= {event:CallBack() for event in eventList}

    def attachEvent(self, event, callback, *args):
        self.log(".attachEvent("+event+", "+str(callback)+", "+str(args))
        if not event in self.events:
            logCore(event+" is not defined on "+str(self))
            self.event[event]= CallBack(function=callback)
        self.event[event].setCallback(callback, *args)

    def event(self, event):
        return self.events[event]

    def detachEvent(self, event):
        if not event in self.events:
            logCore(event+" is not defined on "+str(self))
        self.events[event].reset()
        self.log(".detachEvent("+event+")")

#
# BoardObj, obj on a board
#
class BoardObj(AbstractObj):

    def __init__(self, name, pins=[], autoLoad=True):
        AbstractObj.__init__(self, name)

        self.type = "boardObj"
        self.pins = pins

        if autoLoad:
            BOARD.autoAddObj(self)

    def setup(self, board):
        pass

    def __repr__(self):
        return str(self.board)+"."+self.name

    def on(self, board):
        # Init this obj on board
        if not hasattr(self, 'board'):
            self.board= board
            self.setup(board)
        return self


#
# DataObj, obj generating data
#
class DataObj:

    def __init__(self):
        self.plot= None

    def setPlot(self, plot):
        self.plot= plot

        if hasattr(self, 'color'):
            self.plot.color= self.color

    def appendData(self, data):
        if not self.plot is None:
            self.plot.points.append((EXD_TIME(), data))
