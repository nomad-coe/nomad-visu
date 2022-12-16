import ipywidgets as widgets


class PlotName(object):
    def __init__(self):

        self.widget = widgets.Text(
            placeholder="plot",
            value="plot",
            description="Name",
            layout=widgets.Layout(width="300px"),
        )
