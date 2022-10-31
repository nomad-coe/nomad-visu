import ipywidgets as widgets

class PlotResolution (object):

    def __init__ (self):

        self.widget = widgets.Text(
            placeholder="1",
            value="1",
            description="Resolution",
            layout=widgets.Layout(width="150px"),
        )