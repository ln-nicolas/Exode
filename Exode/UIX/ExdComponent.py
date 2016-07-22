from kivy.uix.gridlayout  import GridLayout
from kivy.lang            import Builder
from kivy.properties      import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.textinput   import TextInput

from ..Core.callback import CallBack

class ExdViewer(GridLayout):
    value = StringProperty("-")
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    def __init__(self, obj, color=[0.06, 0.25, 0.49, 1], **kwargs):

        self.obj= obj
        self.bgcolor= color
        obj.attachView(self)

        super(ExdViewer, self).__init__(**kwargs)

    def updateDigPin(self):
        if self.obj._period != -1:
            if self.obj._mode == 1:
                self.value = "[b] periodic switch [/b]\n"+str(self.obj._period)+" ms"

        else:
            if self.obj._lvl == 1: self.value = "[size=25][b]HIGH[/b][/size]"
            else: self.value = "[size=25][b]LOW[/b][/size]"

    def updateAnaPin(self):
        if self.obj._period == -1:
            self.value = "value \n[b]"+str(self.obj.value)+"[/b]"
        else:
            self.value = "value \n[b]" + str(self.obj.value) + "[/b]\n listen " + str(self.obj._period) + "ms"

    def update(self):

        if(self.obj.type=="DigPin"): self.updateDigPin()
        if(self.obj.type=="AnaPin"): self.updateAnaPin()

Builder.load_string('''
<ExdViewer>:
    rows: 3
    size: 130, 130
    size_hint: None, None

    GridLayout:
        id: top
        cols: 2
        size_hint: 1, 0.2

        ExdLabel:
            id: name
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: "#"+root.obj.name
            valign: "top"
            size_hint: 0.5, 1

        ExdLabel:
            id: type
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: root.obj.type
            valign: "top"
            halign: "right"
            size_hint: 0.5, 1


    GridLayout:
        id: middle
        cols: 1
        size_hint: 1, 0.8

        ExdLabel:
            id: valueLabel
            bgcolor: 0.10, 0.13, 0.15, 1
            markup: True
            text: root.value
            valign: "middle"
            halign: "center"
            font_size: 15
            height: 20, 50

            canvas.before:
                Color:
                    rgb: self.bgcolor
                Rectangle:
                    size: self.size
                    pos: self.pos

    GridLayout:
        id: bottom
        cols: 2
        size_hint: 1, 0.2

        ExdLabel:
            id: board
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: root.obj.board.name
            valign: "top"
            height: 20, 50

        ExdLabel:
            id: type
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: str(root.obj.pins)
            valign: "top"
            halign: "right"
            size_hint: 0.5, 1
''')

class ExdSlider(GridLayout):
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    def __init__(self, minv, maxv, value,
                       callback,
                       name,
                       color=[0.06, 0.25, 0.49, 1],
                       **kwargs):
        self.cb = CallBack(callback)
        self.bgcolor= color

        self.name = name
        self.min= minv
        self.max= maxv
        self.value= value

        super(ExdSlider, self).__init__(**kwargs)

    def on_value(self, value):
        if value != self.value:
            self.value= value
            self.ids.slider.value= value
            self.cb.call(value)

Builder.load_string('''
<ExdSlider>:
    rows: 3
    size: 130, 130
    size_hint: None, None

    ExdLabel:
        id: name
        bgcolor: root.bgcolor
        font_size: 13
        markup: True
        text: "#"+root.name
        valign: "top"
        halign: "left"
        size_hint: 1, 0.2

    Slider:
        id: slider
        orientation: 'horizontal'
        min: root.min
        max: root.max
        value: root.value
        bgcolor: 0.25, 0.56, 0.72, 0.8

        on_touch_up: root.on_value(int(slider.value))
        size_hint: 1, 0.6

        canvas.before:
            Color:
                rgb: 0.10, 0.13, 0.15, 1
            Rectangle:
                size: self.size
                pos: self.pos

    TextInput:
        id: valueInput

        size_hint: 1, 0.2
        line_height: root.height*0.2

        background_color: root.bgcolor
        foreground_color: 1, 1, 1, 1

        background_normal: ""
        background_disabled_normal:""
        background_active: ""


        font_size: 13
        multiline:False

        text: str(int(slider.value))
        on_text_validate: root.on_value(int(self.text))
''')

from kivy.uix.button import Button

class ExdPushButton(GridLayout):
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    def __init__(self, callback, name, color=[0.06, 0.25, 0.49, 1],**kwargs):

        self.name= name
        self.bgcolor= color

        self.cb= CallBack(callback)
        super(ExdPushButton, self).__init__(**kwargs)

    def switch(self):
        ExdButton.switch(self)
        self.cb.call()

Builder.load_string('''
<ExdPushButton>:
    rows: 3
    size: 130, 130
    size_hint: None, None

    ExdLabel:
        id: name
        bgcolor: root.bgcolor
        font_size: 13
        markup: True
        text: "#"+root.name
        valign: "top"
        halign: "left"
        size_hint: 1, 0.2

    Button:
        id: button
        size_hint: 1, 0.8

        background_color: root.bgcolor
        background_down:""

        on_press: root.cb.call()

''')
