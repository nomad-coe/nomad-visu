import ipywidgets as widgets

from ..config_widgets import ConfigWidgets

class FeatMarkerMaxLabel (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Label(
            value="Max value: ",
            layout=widgets.Layout(left="94px", width="70px")
        )