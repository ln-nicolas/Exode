from .gardenGraph import Graph, MeshLinePlot
from kivy.uix.gridlayout  import GridLayout
from kivy.lang      import Builder

from .ExdLabel import ExdLabel

class ExdRealTimeGraph(GridLayout):

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

        self.graph= Graph(x_ticks_minor=5,
        x_ticks_major=500, y_ticks_major=500, ylabel='y',
        y_grid_label=True, x_grid_label=False, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=0, ymax=1000,
        size_hint=(0.8, 0.8))

        self.data= ExdLabel(size_hint=(1,0.1), bgcolor=[0.10, 0.13, 0.15, 1],
                             markup=True,
                             halign="center")

        self.add_widget(self.title)
        self.add_widget(self.graph)
        self.add_widget(self.data)

    def _update_graph(self, *largs):

        graph= self.graph
        for p in graph.plots:
            if p.points == []:
                return

        _xmax = max([ t[0] for plot in graph.plots for t in plot.points ])

        _ymin = min([ t[1] for plot in graph.plots for t in plot.points if t[0]>(_xmax-5000)])
        _ymax = max([ t[1] for plot in graph.plots for t in plot.points if t[0]>(_xmax-5000)])

        graph.xmax=_xmax+200
        graph.xmin=_xmax-5000
        graph.y_ticks_major = round((graph.ymax - graph.ymin)/10,0)


    def add_plot(self, plot):
        self.graph.add_plot(plot)
        plot.bind(on_clear_plot=self._update_graph)

Builder.load_string('''
<ExdRealTimeGraph>:
    canvas.before:
        Color:
            rgb: 0.10, 0.13, 0.15, 1
        Rectangle:
            size: self.size
            pos: self.pos
''')
