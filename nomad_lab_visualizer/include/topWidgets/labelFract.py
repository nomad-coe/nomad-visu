import ipywidgets as widgets

from ...configWidgets import ConfigWidgets

class LabelFract (ConfigWidgets):

    def __init__ (self):

        self.widget = widgets.Label(
            value="Fraction: ", 
            layout=widgets.Layout(left="95px")
        )