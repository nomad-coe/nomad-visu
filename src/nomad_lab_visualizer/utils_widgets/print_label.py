import ipywidgets as widgets

from nomad_lab_visualizer.config_widgets import ConfigWidgets


class PrintLabel(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Label(
            value="Click 'Print' to export the plot in the desired format and resolution.",
            layout=widgets.Layout(left="50px", width="640px"),
        )
