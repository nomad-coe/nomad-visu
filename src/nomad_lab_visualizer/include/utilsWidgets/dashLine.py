import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class DashLine (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.line_dashs,
            description="Line dash",
            value=self.line_dash,
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizerFigure):

        def handle_change( change):
            """
            change line dash
            """
            ConfigWidgets.line_dash = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")