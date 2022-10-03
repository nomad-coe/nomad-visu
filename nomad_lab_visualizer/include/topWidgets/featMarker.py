import ipywidgets as widgets

from ...configWidgets import ConfigWidgets

class FeatMarker (ConfigWidgets):

    def __init__(self):
    
        self.widget = widgets.Dropdown(
            description="Marker",
            options=["Default size"] + self.hover_features,
            value="Default size",
            layout=widgets.Layout(width="250px"),
        )

    def observe_change(self, visualizerFigure, featMarkerMinValueWidget, featMarkerMaxValueWidget):

        def handle_change(change):
            """
            change markers size according to a specific feature
            """

            if change.new == "Default size":
                featMarkerMaxValueWidget.disabled = True
                featMarkerMinValueWidget.disabled = True
                # self.widg_markers_size.disabled = False
                # self.widg_cross_size.disabled = False
            else:
                featMarkerMaxValueWidget.disabled = False
                featMarkerMinValueWidget.disabled = False
                # self.widg_markers_size.disabled = True
            # self.widg_cross_size.disabled = True

            ConfigWidgets.featmarker = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")
