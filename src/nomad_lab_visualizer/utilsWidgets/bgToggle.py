import ipywidgets as widgets

from ..configWidgets import ConfigWidgets

class BgToggle (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Button(
            description="Toggle on/off background",
            layout=widgets.Layout(left="50px", width="200px"),
        )

    def observe_change(self, visualizerFigure):

        def button_clicked( button):
            """
            switch color of the background
            """
            if self.bg_toggle:
                self.bg_toggle = False
            else:
                self.bg_toggle = True
            visualizerFigure.batch_update(self)

        self.widget.on_click(button_clicked)
