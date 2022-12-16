import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class ColorLine(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.color_line,
            description="Line color",
            value=self.line_color,
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def handle_change(change):
            """
            change line color
            """
            ConfigWidgets.line_color = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
