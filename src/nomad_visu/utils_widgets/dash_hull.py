import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class DashHull(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.hull_dashs,
            description="Hull dash",
            value=self.hull_dash,
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def handle_change(change):
            """
            cange hull dash
            """
            ConfigWidgets.hull_dash = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
