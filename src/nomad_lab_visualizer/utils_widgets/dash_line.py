import ipywidgets as widgets

from nomad_lab_visualizer.config_widgets import ConfigWidgets


class DashLine(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.line_dashs,
            description="Line dash",
            value=self.line_dash,
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def handle_change(change):
            """
            change line dash
            """
            ConfigWidgets.line_dash = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
