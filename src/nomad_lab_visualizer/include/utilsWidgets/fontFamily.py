import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class FontFamily (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.font_families,
            description="Font family",
            value=self.font_families[0],
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change (self, visualizerFigure):
  
        def handle_change( change):
            """
            changes font family
            """
            ConfigWidgets.font_family = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")
