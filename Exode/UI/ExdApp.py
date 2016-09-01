from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from ..Core   import *
from ..Object import *
from ..UI     import *

class ExodeApp(App):
    def __init__(self):
        App.__init__(self)
        self.STACK= ExdStack()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.keyEvents = {}

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        for key in self.keyEvents.keys():
            if key == keycode[1]:
                self.keyEvents[keycode[1]].call()
        return True

    def addKeyEvent(self, keycode, callback_function):
        self.keyEvents[keycode]= CallBack(callback_function)

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
