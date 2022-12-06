import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class FeatColorType(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.RadioButtons(
            options=["Gradient", "Discrete"],
            value="Gradient",
            layout=widgets.Layout(width="140px", left="90px"),
            disabled=True,
        )

    def observe_change(self, visualizer_figure, feat_color_list_widget):
        def handle_change(change):
            """
            changes the type of markers coloring
            """

            ConfigWidgets.featcolor_type = change.new

            if change.new == "Gradient":
                feat_color_list_widget.options = self.continuous_gradient_colors
                ConfigWidgets.featcolor_list = "viridis"
                feat_color_list_widget.value = "viridis"
            if change.new == "Discrete":
                feat_color_list_widget.options = self.discrete_palette_colors
                ConfigWidgets.featcolor_list = "Plotly"
                feat_color_list_widget.value = "Plotly"

            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
