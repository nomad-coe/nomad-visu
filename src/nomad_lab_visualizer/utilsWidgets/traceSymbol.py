import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class TraceSymbol (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Dropdown(
                options=[' '],
                description="Classes",
                value=' ',
                layout=widgets.Layout(left="30px", width="200px"),
            )

    def observe_change (self, visualizerFigure):    

        self.widget.options = visualizerFigure.name_traces
        self.widget.value = visualizerFigure.name_traces[0]