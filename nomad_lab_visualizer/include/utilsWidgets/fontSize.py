import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class FontSize (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.BoundedIntText(
            placeholder=str(self.font_size),
            description="Font size",
            value=str(self.font_size),
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizerFigure):

        def handle_change( change):
            """
            changes font size
            """
            ConfigWidgets.font_size = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")
