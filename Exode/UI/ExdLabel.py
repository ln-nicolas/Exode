from kivy.lang      import Builder
from kivy.uix.label import Label
from kivy.properties  import ListProperty

Builder.load_string('''
<ExdLabel@Label>:
    text_size: self.width, self.height
    padding_x: 5
    padding_y: 5
    bgcolor: 0, 0, 0, 1

    canvas.before:
        Color:
            rgb: self.bgcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')

class ExdLabel(Label):
    bgcolor= ListProperty([0,0,0,1])
    pass
