import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class FeatColor(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            description="Color",
            options=["Default color"] + self.hover_features,
            value="Default color",
            layout=widgets.Layout(width="250px"),
        )

    def observe_change(
        self, visualizer_figure, feat_color_type_widget, feat_color_list_widget
    ):
        def handle_change(change):
            """
            changes markers color according to a specific feature
            """

            ConfigWidgets.featcolor = change.new

            if change.new == "Default color":
                feat_color_type_widget.disabled = True
                feat_color_list_widget.disabled = True
                # self.widg_color_palette.disabled = False
            else:
                feat_color_type_widget.disabled = False
                feat_color_list_widget.disabled = False
                # self.widg_color_palette.disabled = True
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
