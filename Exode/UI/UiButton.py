from kivy.lang       import Builder
from kivy.uix.button import Button

class UiButton(Button):

    def switch(self):
        self.pressed = (not self.pressed)
        if (self.pressed): self.background_color = self.pressed_color
        else: self.background_color = self.normal_color


Builder.load_string('''
<UiButton>:
    normal_color: 0.31, 0.01, 0.31, 0.31, 1
    pressed_color: 0.13, 0.15, 0.2, 1
    pressed: False

    background_color: self.normal_color
    background_normal: ''

    font_size: 12

    on_press: self.switch()
''')
