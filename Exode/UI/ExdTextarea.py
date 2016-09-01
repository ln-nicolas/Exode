from kivy.lang      import Builder
from kivy.uix.label import Label
from kivy.uix.scrollview  import ScrollView


Builder.load_string('''
<ExdTextarea@ScrollView>:
    text: ""

    Label:
        padding_x: 5
        padding_y: 5

        valign: "top"
        text:root.text
        markup: True

        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
''')

class ExdTextarea(ScrollView):
    pass
