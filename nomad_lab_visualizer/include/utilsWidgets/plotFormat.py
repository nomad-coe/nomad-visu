import ipywidgets as widgets

class PlotFormat(object):

    def __init__(self):

        self.widget = widgets.Text(
            placeholder="png",
            value="png",
            description="Format",
            layout=widgets.Layout(width="150px"),
        )