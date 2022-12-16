import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class WidthHull(ConfigWidgets):
    def __init__(self):
        self.widget = widgets.BoundedIntText(
            description="Hull width",
            value=str(self.hull_width),
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def handle_change(change):
            """
            change width hull
            """

            ConfigWidgets.hull_width = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
