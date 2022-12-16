import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class BgToggle(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Button(
            description="Toggle on/off background",
            layout=widgets.Layout(left="50px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def button_clicked(button):
            """
            switch color of the background
            """
            if self.bg_toggle:
                self.bg_toggle = False
            else:
                self.bg_toggle = True
            visualizer_figure.batch_update(self)

        self.widget.on_click(button_clicked)
