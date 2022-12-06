import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class FeatMarker(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            description="Marker",
            options=["Default size"] + self.hover_features,
            value="Default size",
            layout=widgets.Layout(width="250px"),
        )

    def observe_change(
        self,
        visualizer_figure,
        feat_marker_min_value_widget,
        feat_marker_max_value_widget,
    ):
        def handle_change(change):
            """
            change markers size according to a specific feature
            """

            if change.new == "Default size":
                feat_marker_max_value_widget.disabled = True
                feat_marker_min_value_widget.disabled = True
                # self.widg_markers_size.disabled = False
                # self.widg_cross_size.disabled = False
            else:
                feat_marker_max_value_widget.disabled = False
                feat_marker_min_value_widget.disabled = False
                # self.widg_markers_size.disabled = True
            # self.widg_cross_size.disabled = True

            ConfigWidgets.featmarker = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
