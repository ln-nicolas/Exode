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

    def __init__(self, radial_tick=4, linear_tick=10, scale=10, **kwargs):
        self.bind(pos=self.draw,
                  size=self.draw)

        self.tick_color= [0.51, 0.51, 0.51, 1]
        self.plots= []

        self.nb_radial_tick= radial_tick
        self.nb_linear_tick= linear_tick

        self.scale= scale

        super(PolarGraph, self).__init__(**kwargs)
        self.ratio= 1

        if self.size_hint[0] != None:
            self.ratio= self.size_hint[0]


    def draw(self, *args):
        self.canvas.clear()

        if hasattr(self, "parent"):
            self.ratio= min(self.parent.size_hint_x, self.parent.size_hint_y)
        self.dim= min(self.width, self.height)

        self.update_ticks(*args)
        self.update_plots(*args)

    def update_ticks(self, *args):

        with self.canvas:
            Color(*self.tick_color)
            for i in range(1,self.nb_radial_tick+1):
                Line(circle=(self.center_x,
                             self.center_y,
                             self.ratio*i*(self.height/self.nb_radial_tick)/2))

            for i in range(1,self.nb_linear_tick+1):
                tick_len = self.dim*self.ratio*.5
                Line(points=[self.center_x-tick_len*math.cos(i*(3.14/self.nb_linear_tick)),
                             self.center_y-tick_len*math.sin(i*(3.14/self.nb_linear_tick)),
                             self.center_x+tick_len*math.cos(i*(3.14/self.nb_linear_tick)),
                             self.center_y+tick_len*math.sin(i*(3.14/self.nb_linear_tick))],
                             width=1)

    def add_plot(self, plot):
        if plot in self.plots:
            return
        plot.bind(on_clear_plot=self.draw)
        self.update_plots()
        self.plots.append(plot)

    def update_plots(self, *args):
        for plot in self.plots:
            with self.canvas:
                Color(plot.color)

                for pt in plot.points:
                    t= pt[0]
                    a= math.radians(pt[1][0])
                    m= pt[1][1]

                    x= self.center_x + math.cos(a)*min(1,m/self.scale)*(self.dim*self.ratio)*.5
                    y= self.center_y + math.sin(a)*min(1,m/self.scale)*(self.dim*self.ratio)*.5

                    Rectangle(pos=(x,y), size=(2,2))


class polarPlot(Plot):
    pass
