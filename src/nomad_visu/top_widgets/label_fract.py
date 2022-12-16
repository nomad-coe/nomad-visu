import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class LabelFract(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Label(
            value="Fraction: ", layout=widgets.Layout(left="95px")
        )
