import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class FeatMarkerMin(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.BoundedFloatText(
            min=0,
            max=self.max_value_markerfeat,
            step=1,
            value=self.min_value_markerfeat,
            disabled=True,
            layout=widgets.Layout(left="91px", width="60px", height="10px"),
        )

    def observe_change(self, visualizer_figure, feat_marker_max_widget):
        def handle_change(change):
            """
            changes the min value of the markers size
            """

            ConfigWidgets.min_value_markerfeat = change.new
            feat_marker_max_widget.min = change.new
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
