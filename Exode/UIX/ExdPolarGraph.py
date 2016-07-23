from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import *
from kivy.graphics.texture import Texture
from kivy.properties import ListProperty
from .gardenGraph import Plot
from .ExdLabel import *

import math

class PolarGraph(Widget):

    def __init__(self, **kwargs):
        self.bind(pos=self.draw,
                  size=self.draw)

        self.tick_color= [0.51, 0.51, 0.51, 1]
        self.plots= []

        super(PolarGraph, self).__init__(**kwargs)

        self.ratio= 1
        if self.size_hint[0] != None:
            self.ratio= self.size_hint[0]


    def draw(self, *args):
        self.canvas.clear()
        self.update_ticks(*args)
        self.update_plots(*args)

    def update_ticks(self, *args):

        self.nb_radial_tick= 4
        self.radial_ticks = {}

        self.nb_linear_tick= 10
        self.linear_tick = {}

        with self.canvas:
            Color(*self.tick_color)
            for i in range(1,self.nb_radial_tick+1):
                self.radial_ticks[i]= Line(circle=(self.center_x,
                                                   self.center_y,
                                                   self.ratio*i*(self.height/self.nb_radial_tick)/2))

            for i in range(0,self.nb_linear_tick):
                self.linear_tick[i]=  Line(points=[self.center_x, self.center_y,
                                                   self.center_x+self.ratio*self.width*math.cos(i*(6.28/self.nb_linear_tick))*.5,
                                                   self.center_y+self.ratio*self.width*math.sin(i*(6.28/self.nb_linear_tick))*.5],
                                                   width=1)

    def add_plot(self, plot):
        if plot in self.plots:
            return
        plot.bind(on_clear_plot=self.draw)
        self.update_plots()
        self.plots.append(plot)

    def update_plots(self, *args):
        for plot in self.plots:
            self.scale= 100

            with self.canvas:
                Color(0,1,0)

                for pt in plot.points:
                    a= math.radians(pt[0])
                    m= pt[1]

                    x= self.center_x + math.cos(a)*min(1,m/self.scale)*(self.width*self.ratio)*.5
                    y= self.center_y + math.sin(a)*min(1,m/self.scale)*(self.width*self.ratio)*.5

                    Rectangle(pos=(x,y), size=(2,2))


class polarPlot(Plot):
    pass

class ExdPolarGraph(GridLayout):

    def __init__(self, name, color=[0.06, 0.25, 0.49, 1], **kwargs):

        GridLayout.__init__(self, size_hint=(None, None),
                              width=260, height=260,
                              rows=3,
                              padding= (0,0),
                              **kwargs)

        self.title= ExdLabel(size_hint=(1,0.1), bgcolor=color,
                             text="[b]"+name+"[/b]",
                             markup=True,
                             halign="center")

        self.graph= PolarGraph(size_hint=(0.8,0.8))

        self.data= ExdLabel(size_hint=(1,0.1), bgcolor=[0.10, 0.13, 0.15, 1],
                             markup=True,
                             halign="center")

        self.add_widget(self.title)
        self.add_widget(self.graph)
        self.add_widget(self.data)

    def add_plot(self, plot):
        self.graph.add_plot(plot)



Builder.load_string('''
<ExdPolarGraph>:
    canvas.before:
        Color:
            rgb: 0.10, 0.13, 0.15, 1
        Rectangle:
            size: self.size
            pos: self.pos
''')
