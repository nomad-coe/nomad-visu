import ipywidgets as widgets

from ...configWidgets import ConfigWidgets

class FeatMarkerMax (ConfigWidgets):

    def __init__(self):   
   
        self.widget = widgets.BoundedFloatText(
            min=self.min_value_markerfeat,
            step=1,
            value=self.max_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px"),
            disabled=True,
        )

    def observe_change (self, visualizerFigure, featMarkerMinWidget):

        def handle_change(change):
            """
            changes the max value of the markers size
            """

            ConfigWidgets.max_value_markerfeat = change.new
            featMarkerMinWidget.max = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")