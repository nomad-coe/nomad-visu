import ipywidgets as widgets

class WindowLabel (object):

    def __init__(self):

        self.widget = widgets.Label(
            value="Tick the box next to the cross symbols in order to choose which windows visualizes the next "
            "structure selected in the map above."
            )