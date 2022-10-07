import ipywidgets as widgets

from ...configWidgets import ConfigWidgets

class WidthLine (ConfigWidgets):

    def __init__ (self):

        self.widget = widgets.BoundedIntText(
            description="Line width",
            value=self.line_width,
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizerFigure):

        def handle_change( change ):
            """
            change line width
            """
            ConfigWidgets.line_width = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change)