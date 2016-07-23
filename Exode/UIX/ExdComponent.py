from kivy.uix.gridlayout  import GridLayout
from kivy.lang            import Builder
from kivy.properties      import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.textinput   import TextInput

from ..Core.callback import CallBack
from ..Object.obj import AbstractObj

class ExdViewer(GridLayout):
    value = StringProperty("-")
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    def __init__(self, obj, **kwargs):

        self.obj= obj
        self.bgcolor= kwargs.get('color', obj.color)
        obj.attachView(self)

        super(ExdViewer, self).__init__(**kwargs)

    def update(self):
        self.value= self.obj.getUIXView()

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

    def __init__(self, minv, maxv,
                       target,
                       name,
                       valueName=None,
                       **kwargs):

        self.name = name
        self.min= minv
        self.max= maxv
        self.value= kwargs.get('value', int((maxv-minv)/2))

        self.valueName= valueName

        if not hasattr(target, '__call__'):
            self.obj= target
            target.attachView(self)
            self.cb = CallBack(self.obj.setValue)
            self.bgcolor= target.color
        else:
            self.cb = CallBack(target)

        if 'color' in kwargs:
            self.bgcolor= kwargs.get('color')

        super(ExdSlider, self).__init__(**kwargs)

    def update(self):
        value= self.obj.getValue(self.valueName)
        if value >= self.min and value <= self.max and value != self.value:
            self.value= value
            self.ids.slider.value= value

    def on_value(self, value):
        if value != self.value:
            self.value= value
            self.ids.slider.value= value
            self.cb.call(value, self.valueName)

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



class ExdRadio(GridLayout):
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    def __init__(self, target, name, valueName=None, **kwargs):

        self.name = name
        self.value= kwargs.get('value', False)

        self.valueName= valueName

        super(ExdRadio, self).__init__(**kwargs)

        if not hasattr(target, '__call__'):
            self.obj= target
            target.attachView(self)
            self.cb = CallBack(self.obj.setValue)
            self.bgcolor= target.color
        else:
            self.cb = CallBack(target)

        if 'color' in kwargs:
            self.bgcolor= kwargs.get('color')


    def update(self):
        value= self.obj.getValue(self.valueName)
        if value == 1: value= True
        else: value= False

        if self.value != value:
            self.value= value
            self.ids.checkbox.active= value

    def on_value(self):
        self.value= not self.value
        self.cb.call(self.value, self.valueName)


Builder.load_string('''
<ExdRadio>:
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

    CheckBox:
        id: checkbox
        active: root.value
        bgcolor: 0.25, 0.56, 0.72, 0.8

        on_active: root.on_value()
        size_hint: 1, 0.6

        canvas.before:
            Color:
                rgb: 0.10, 0.13, 0.15, 1
            Rectangle:
                size: self.size
                pos: self.pos

    ExdLabel:
        id: value

        size_hint: 1, 0.2
        line_height: root.height*0.2

        background_color: root.bgcolor
        foreground_color: 1, 1, 1, 1

        background_normal: ""
        background_disabled_normal:""
        background_active: ""


        font_size: 13
        multiline:False

        text: str(int(checkbox.active))
''')

from kivy.uix.button import Button

class ExdPushButton(GridLayout):
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    def __init__(self, callback, name, **kwargs):

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
