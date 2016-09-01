from .gardenGraph import Graph, MeshLinePlot
from .polarGraph  import PolarGraph
from kivy.uix.gridlayout  import GridLayout
from kivy.lang      import Builder

from .ExdComponent import ExdBox

class ExdTimeGraph(ExdBox):

    def __init__(self, delta=5000, size="md",
                       name  = "[b]graph[/b]",
                       xlabel='time (s)', ylabel="y",
                       ymin=0, ymax=1, **kwargs):
        ExdBox.__init__(self, size)
        self.topLeft= name
        self.topRight= str(delta)+" ms"

        self.delta= delta

        self.graph= Graph( xlabel= xlabel, ylabel= ylabel,
                           ymin=ymin, ymax=ymax,
                           y_ticks_major=(ymax-ymin)/5,
                           x_ticks_minor=delta/1000-0.1,
                           y_grid_label=True, x_grid_label=True,
                           x_grid= False, y_grid= True,
                           background_color=  [0.10, 0.13, 0.15, 1],
                           **kwargs)
        self.main.add_widget(self.graph)

    def update_graph(self, *largs):
        graph= self.graph
        for p in graph.plots:
            if p.points == []:
                return

        _xmax = max([ t[0] for plot in graph.plots for t in plot.points ])

        graph.xmax= _xmax+ (self.delta*0.05)/1000
        graph.xmin= _xmax- (self.delta*0.95)/1000

    def add_plot(self, plot):
        self.graph.add_plot(plot)
        plot.bind(on_clear_plot=self.update_graph)

class ExdPolarGraph(ExdBox):

    def __init__(self, size="md",
                       name="[b]graph[/b]",
                       radial_tick= 4,
                       linear_tick= 10,
                       scale=10,
                       **kwargs):

        ExdBox.__init__(self, size)
        self.topLeft= name
        self.graph= PolarGraph(radial_tick=radial_tick, linear_tick=linear_tick,
                               scale=scale)
        self.main.add_widget(self.graph)

    def add_plot(self, plot):
        self.graph.add_plot(plot)
