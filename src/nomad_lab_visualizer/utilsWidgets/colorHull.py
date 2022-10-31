import ipywidgets as widgets

from ..configWidgets import ConfigWidgets

class ColorHull (ConfigWidgets):

    def __init__ (self):

        self.widget = widgets.Dropdown(
            options=self.color_hull,
            description="Hull color",
            value=self.hull_color,
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizerFigure):

        def handle_change( change ):
            """
            change hull color
            """
            ConfigWidgets.hull_color = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names='value')