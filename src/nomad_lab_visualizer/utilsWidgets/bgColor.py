import ipywidgets as widgets

from ..configWidgets import ConfigWidgets

class BgColor (ConfigWidgets):

    def __init__ (self):

        self.widget = widgets.Text(
            placeholder=str("Default"),
            description="Color",
            value=str("Default"),
            layout=widgets.Layout(left="30px", width="200px"),
        )