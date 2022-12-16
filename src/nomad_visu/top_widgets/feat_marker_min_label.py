import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class FeatMarkerMinLabel(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Label(
            value="Min value: ", layout=widgets.Layout(left="94px", width="70px")
        )
