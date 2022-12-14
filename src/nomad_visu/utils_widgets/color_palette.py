import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class ColorPalette(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.discrete_palette_colors,
            description="Color palette",
            value=self.discrete_palette_colors[0],
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def handle_change(change):
            """
            change color palette used to distinguish different traces
            """

            ConfigWidgets.color_palette = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
