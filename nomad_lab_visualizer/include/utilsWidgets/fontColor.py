import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class FontColor (ConfigWidgets):

    def __init__(self):    

        self.widget = widgets.Dropdown(
            options=self.font_colors,
            description="Font color",
            value="Black",
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change (self, visualizerFigure):

        def handle_change( change):
            """
            changes font color
            """
            ConfigWidgets.font_color = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")
