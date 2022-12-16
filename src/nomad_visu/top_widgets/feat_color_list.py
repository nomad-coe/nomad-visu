import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class FeatColorList(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            disabled=True,
            options=self.continuous_gradient_colors,
            value="viridis",
            layout=widgets.Layout(width="65px", height="35px", left="40px"),
        )

    def observe_change(self, visualizer_figure):
        def handle_change(change):
            """
            changes the color that is used for markers
            """

            ConfigWidgets.featcolor_list = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
