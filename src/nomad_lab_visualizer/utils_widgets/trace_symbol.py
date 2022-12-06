import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class TraceSymbol(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            options=[" "],
            description="Classes",
            value=" ",
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure):

        self.widget.options = visualizer_figure.name_traces
        self.widget.value = visualizer_figure.name_traces[0]
