import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class WidthLine(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.BoundedIntText(
            description="Line width",
            value=self.line_width,
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def handle_change(change):
            """
            change line width
            """
            ConfigWidgets.line_width = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
