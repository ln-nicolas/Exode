from kivy.uix.gridlayout  import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.lang            import Builder
from kivy.properties      import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.widget      import Widget
from kivy.uix.textinput   import TextInput
from kivy.uix.slider      import Slider
from kivy.uix.switch      import Switch
from kivy.uix.checkbox    import CheckBox

from .ExdLabel import ExdLabel
from ..Core.callback import CallBack

#
#   ExdBox
#
#   A box with 3parts:
#   two top and bottom little label, and a bigger
#   central part to containt any kind of
#   widget
#
#   Text could be show throught topleft, .. , bottomRight
#   textarea
#
class ExdBox(GridLayout):
    value = StringProperty("")
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    topLeft = StringProperty("")
    topRight= StringProperty("")
    bottomLeft= StringProperty("")
    bottomRight= StringProperty("")

    def __init__(self, dim="sm", **kwargs):
        self.dim= dim

        GridLayout.__init__(self, rows=3, size_hint=(None, None), **kwargs)

        #self.top  = self.ids.top
        self.main = self.ids.main
        #self.bottom= self.ids.bottom

        self.bind(on_size=self.updateSize)

    def updateSize(self):
        self.size_hint = (None, None)
        dim= self.dim

        if type(dim) is str:
            if dim == "sm": self.size= (130, 130)
            elif dim == "md": self.size= (260, 260)
            elif dim == "lg": self.size_hint = (.5,.5)
            elif dim == "xl": self.size_hint = (1,1)
        else:
            self.size_hint= dim


Builder.load_string('''
<ExdBox>:
    rows: 3

    GridLayout:
        id: top
        cols: 2
        size_hint: 1, None
        height: 20

        ExdLabel:
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: root.topLeft
            valign: "top"
            size_hint: 0.5, 1

        ExdLabel:
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: root.topRight
            valign: "top"
            halign: "right"
            size_hint: 0.5, 1


    GridLayout:
        id: main
        cols: 1
        size_hint: 1, 0.8

    GridLayout:
        id: bottom
        cols: 2
        size_hint: 1, None
        height: 20

        ExdLabel:
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: root.bottomLeft
            valign: "top"
            height: 20, 50

        ExdLabel:
            bgcolor: root.bgcolor
            font_size: 11
            markup: True
            text: root.bottomRight
            valign: "top"
            halign: "right"
            size_hint: 0.5, 1
''')

#
#   ExdController is design to represent and
#   control AbstractObj and mainly BoardObj, values
#   generating could also be send to a CallBack function
#
class ExdController():
    bgcolor = ListProperty([0.06, 0.25, 0.49, 1])

    def __init__(self, target, value=None, **kwargs):
        self.valueName= value
        self._value= 0

        if hasattr(target, '__call__'):
            self.cb= CallBack(target)
        else:
            self.obj= target
            target.attachView(self)
            self.cb = CallBack(target.setValue)
            try:
                self.bgcolor= target.color
            except:
                pass

        if 'color' in kwargs:
            self.bgcolor= kwargs.get('color')

    def update(self):
        self._value= self.obj.getValue(self.valueName)

    def on_value_(self, value):
        if value != self._value:
            self._value= value
            self.update_target()

    def update_target(self):
        self.cb.call(self._value, self.valueName)

#
#   ExdControllerBox
#
class ExdControllerBox(ExdController, ExdBox):

    def __init__(self, target, size, value=None, **kwargs):
        ExdController.__init__(self, target, value, **kwargs)
        ExdBox.__init__(self, size, **kwargs)

        if hasattr(target, '__init__'):
            self.topLeft = target.name
            self.topRight= target.type

            if hasattr(target, 'board'):
                self.bottomLeft= str(target.board)
            if hasattr(target, 'pins'):
                self.bottomRight= str(target.pins)

#
#   ExdViewer, show the AbstractObj's UIXView
#
class ExdViewer(ExdController, ExdLabel):

    def __init__(self, target, value=None, **kwargs):
        ExdLabel.__init__(self, markup=True,
                                valign="middle",
                                halign="center",
                                font_size=15)
        ExdController.__init__(self, target, value, **kwargs)


        self.text= self._value

    def update(self):
        self._value= self.obj.getUIXView()
        self.text  = self._value

#
#   ExdTextInput
#
class ExdTextInput(ExdController, TextInput):

    def __init__(self, target, value=None, isfloat=False, **kwargs):
        ExdController.__init__(self, target, value, **kwargs)
        TextInput.__init__(self)

        self.isfloat = isfloat

    def on_value_(self, value):

        if not self.isfloat:
            try:
                f= float(value)
                i= int(value)
                if f==i:
                    self._value= f
                else:
                    self._value= i
            except:
                return
        else:
            self._value = value

        self.text= str(self._value)
        self.update_target()

    def update(self):
        self._value= self.obj.getValue(self.value)
        self.text= str(self._value)

Builder.load_string('''
<ExdTextInput@TextInput>:
    line_height: self.height

    background_color: self.bgcolor
    foreground_color: 1, 1, 1, 1

    background_normal: ""
    background_disabled_normal:""
    background_active: ""

    font_size: 13
    multiline: False

    text: str(self._value)
    on_text_validate: self.on_value_(self.text)
''')

#
#   ExdSlider
#
class ExdSlider(ExdController, Slider):

    def __init__(self, minv, maxv, target, value=None, isfloat=False, **kwargs):
        ExdController.__init__(self, target, value, **kwargs)

        self.min= minv
        self.max= maxv
        self._value= kwargs.get('value', int((maxv-minv)/2))
        Slider.__init__(self)

        self.float= isfloat

    def on_value_(self, value):
        if not self.float:
            value= int(value)

        if value != self._value:
            self._value= value
            self.update_target()

    def update(self):
        self._value= self.obj.getValue(self.value)
        self.value = self._value

Builder.load_string('''
<ExdSlider@Slider>:
    min: self.min
    max: self.max

    value: self._value
    on_touch_up: self.on_value_(self.value)

    canvas.before:
        Color:
            rgb: self.bgcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')

#
#   ExdRadio
#
class ExdRadio(ExdController, StackLayout):

    def __init__(self, target, title, value=None,**kwargs):
        self._value= True
        self.title = title
        StackLayout.__init__(self)
        ExdController.__init__(self, target, value, **kwargs)


    def on_value_(self, value):
        if value != self._value:
            self._value= value
            self.update_target()

    def update(self):
        self._value= self.obj.getValue(self.value)
        self.ids.check.active= self._value

Builder.load_string('''
<ExdRadio>:
    canvas.before:
        Color:
            rgb: self.bgcolor
        Rectangle:
            size: self.size
            pos: self.pos

    ExdLabel:
        id: title
        bgcolor: root.bgcolor
        font_size: 14
        markup: True
        text: root.title
        valign: "middle"
        halign: "center"
        size_hint_x: .8

    CheckBox:
        id: check
        active: root._value
        on_active: root.on_value_(self.active)
        size_hint_x: .1

''')

#
#   ExdSwitch
#
class ExdSwitch(ExdController, Switch):

    def __init__(self, target, value=None, **kwargs):
        Switch.__init__(self)
        ExdController.__init__(self, target, value, **kwargs)

        self.bind(active=self.on_switch)

    # just a compatibility layer
    def on_switch(self, inst, value):
        self.on_value_(value)

    def on_value_(self, value):
        if value != self._value:
            self._value= value
            self.update_target()

    def update(self):
        self._value= self.obj.getValue(self.value)
        self.active= self._value

Builder.load_string('''
<ExdSwitch>:
    canvas.before:
        Color:
            rgb: self.bgcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')

#
#   ExdViewerBox
#
class ExdViewerBox(ExdControllerBox):

    def __init__(self, target, size="sm", value=None, **kwargs):
        ExdControllerBox.__init__(self, target, size, value, **kwargs)
        self.viewer= ExdViewer(target, value, color=[0.10, 0.13, 0.15, 1])
        self.main.add_widget(self.viewer)

        self.update= self.viewer.update
#
#   ExdTextInputBox
#
class ExdTextInputBox(ExdControllerBox):

    def __init__(self, target, size="sm", value=None, **kwargs):
        ExdControllerBox.__init__(self, target, size, value, **kwargs)
        self.textinput= ExdTextInput(target, value, color=[0.10, 0.13, 0.15, 1])
        self.main.add_widget(self.textinput)

        self.update= self.textinput.update

#
#   ExdSliderBox
#
class ExdSliderBox(ExdControllerBox):

    def __init__(self, minv, maxv, target,
                 size="sm", value=None,
                 isfloat=False, **kwargs):

        ExdControllerBox.__init__(self, target, size, value, **kwargs)

        # Slider update input, then update hiddenController
        # input update slider, then update hiddenController
        self.slider= ExdSlider(minv, maxv, self.updateInput,
                               value, isfloat,
                               color=[0.10, 0.13, 0.15, 1], **kwargs)
        self.input = ExdTextInput(self.updateSlider, value, isfloat,
                                  color=[0.10, 0.13, 0.15, 1])

        # hiddenController update target
        self.hiddenController= ExdController(target, value)

        self.main.add_widget(self.slider)
        self.main.add_widget(self.input)

        self.update= self.globalUpdate
        self.update()

    def updateInput(self, value, name):
        self.input.on_value_(value)
        self.hiddenController.on_value_(value)

    def updateSlider(self, value, name):
        self.slider.on_value_(float(value))
        self.hiddenController.on_value_(float(value))

    def globalUpdate(self):
        self.hiddenController.update()
        value= self.hiddenController._value
        self.slider.value= value
        self.input.text  = str("{:.3f}".format(value))

#
#   ExdRadioBox
#
class ExdRadioBox(ExdControllerBox):

    def __init__(self, target, title, size="sm", value=None, **kwargs):
        ExdControllerBox.__init__(self, target, size, value, **kwargs)
        self.radio= ExdRadio(target, title, value,
                             color=[0.10, 0.13, 0.15, 1], **kwargs)
        self.main.add_widget(self.radio)

        self.update= self.radio.update
#
#   ExdSwitchBox
#
class ExdSwitchBox(ExdControllerBox):

    def __init__(self, target, size="sm", value=None, **kwargs):
        ExdControllerBox.__init__(self, target, size, value, **kwargs)
        self.switch= ExdSwitch(target, value,
                               color=[0.10, 0.13, 0.15, 1], **kwargs)
        self.main.add_widget(self.switch)

        self.update= self.switch.update
