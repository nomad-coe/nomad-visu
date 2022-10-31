import ipywidgets as widgets

from ...configWidgets import ConfigWidgets

class FractSlider (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.BoundedFloatText(
            min=0,
            max=1,
            step=0.01,
            value=self.fract,
            layout=widgets.Layout(left="98px", width="60px"),
        )

    def observe_change (self, visualizerFigure):
        
        def handle_change(change):
            """
            changes the fraction visualized
            """

            ConfigWidgets.fract = change.new
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names='value')

