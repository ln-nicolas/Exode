from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from ..Core   import *
from ..Object import *
from ..UIX    import *

class ExodeApp(App):
    def __init__(self):
        App.__init__(self)
        self.STACK= ExdStack()

    #compile python code inside the App
    def compile(self, str, type):
        globals()["APP"]= self
        if type=="<string>":
            exec(str,globals())
        if type=="<file>":
            f= open(str, "r+")
            exec(f.read(),globals())

    def build(self):
        app = GridLayout(rows=2)
        debugger= ExdDebugger(app=self, size_hint_y= 0.3)
        app.add_widget(self.STACK)
        app.add_widget(debugger)
        return app
