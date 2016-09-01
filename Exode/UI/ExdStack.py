from kivy.uix.stacklayout  import StackLayout
from kivy.lang            import Builder


Builder.load_string('''
<ExdStack>:
    padding: 5, 5, 5, 5
    spacing: 5, 5

    canvas.before:
        Color:
            rgb: 0.19, 0.22, 0.25, 1
        Rectangle:
            size: self.size
            pos: self.pos

''')

from ..Core   import *
from ..Object import *


class ExdStack(StackLayout):

    def __init__(self, **kwargs):
        super(ExdStack, self).__init__(**kwargs)

    def add_widget(self, widget, index=0):
        StackLayout.add_widget(self, widget, index=0)

        if hasattr(widget, 'updateSize'):
            widget.updateSize()
