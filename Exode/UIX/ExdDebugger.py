from kivy.uix.gridlayout  import GridLayout
from kivy.lang            import Builder
from kivy.uix.scrollview  import ScrollView
from kivy.properties      import BooleanProperty, StringProperty
from kivy.uix.textinput   import TextInput
from kivy.clock           import Clock
from functools import partial

import threading

from ..Core import LOG_PATH, logPy

class ExdDebugger(GridLayout):
    text = StringProperty('')

    time = BooleanProperty(True)
    core = BooleanProperty(True)
    obj  = BooleanProperty(True)
    py   = BooleanProperty(True)

    def __init__(self, app, **kwargs):

        self.stream= open(LOG_PATH, "r", encoding="utf-8")
        self.app= app

        super(ExdDebugger, self).__init__(**kwargs)

        Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        lines= self.stream.readlines()
        for line in lines:
            self.add(line)

        stk= self.text.split("\n")[-25:]
        self.text= "\n".join(stk)

    def setup(self):
        self.text= ""
        self.stream.seek(0)
        for line in self.stream.readlines():
            self.add(line)

    def getStyleCode(self, line):
        data= line.split('|',4)

        if(data[2]=="CORE" and self.core == False):
            return ""

        if(data[2]=="OBJC" and self.obj == False):
            return ""

        if(data[2]=="PYTH" and self.py == False):
            return ""

        colorSrc= "ffffff"
        if data[2] == "CORE": colorSrc= "e24141"
        if data[2] == "OBJC": colorSrc= "3aaf42"
        if data[2] == "PYTH": colorSrc= "ffbf49"

        ## Time
        if(self.time):
            t= data[0].split(' ')[1]
            time = "[color=a3a3a3]"+t+"[/color] "
        else:
            time = ""

        src  = "[color="+colorSrc+"]"+data[2]+"[/color]  "
        msg  = "[color=e2e2e2]"+data[3].split("\n")[0]+"[/color]\n"

        return time+src+msg

    def add(self, line):
        self.text += self.getStyleCode(line)

    def input(self, str):

        self.ids.codeInput.text = ""
        def foo():
            logPy(str)
            self.app.compile(str,"<string>")

        threading.Thread(target=foo).start()

Builder.load_string("""
<ExdDebugger>:
    rows: 2

    ExdTextarea:
        id: textarea
        text: root.text
        do_scroll_y: True
        scroll_y: 0

        canvas.before:
            Color:
                rgb: 0.10, 0.13, 0.15, 1
            Rectangle:
                size: self.size
                pos:  self.pos

    StackLayout:

        id: config
        size_hint: 1, None
        height:25

        UiButton:
            id: time
            text: "time"

            size_hint: None, 1
            width: 60

            normal_color: 0.31, 0.31, 0.31, 1

            on_press: root.time= (not root.time); root.setup()

        UiButton:
            id: python
            text: "python"

            size_hint: None, 1
            width: 60

            normal_color: 1.0, 0.75, 0.29, 1
            on_press: root.py= (not root.py); root.setup()

        UiButton:
            id: object
            text: "object"

            size_hint: None, 1
            width: 60

            normal_color: 0.23, 0.69, 0.26, 1
            on_press: root.obj= (not root.obj); root.setup()

        UiButton:
            id: core
            text: "core"

            size_hint: None, 1
            width: 60

            normal_color:  0.89, 0.26, 0.26, 1
            on_press: root.core = (not root.core); root.setup()

        TextInput:
            id: codeInput

            size_hint: None, 1
            width: root.width - 4*60
            height: 25

            background_color: 0.14, 0.16, 0.19, 1
            foreground_color: 0.89, 0.89, 0.89, 1

            font_size: 13
            padding_x: 20
            padding_y: 2
            multiline:False

            on_text_validate: root.input(self.text)

""")
