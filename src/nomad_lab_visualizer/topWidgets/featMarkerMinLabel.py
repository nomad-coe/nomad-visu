import ipywidgets as widgets

from ..configWidgets import ConfigWidgets

class FeatMarkerMinLabel (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Label(
            value="Min value: ",
            layout=widgets.Layout(left="94px", width="70px")
        )