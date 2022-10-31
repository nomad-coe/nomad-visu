import ipywidgets as widgets

from ..configWidgets import ConfigWidgets

class CrossSize (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.BoundedIntText(
            placeholder=str(self.cross_size),
            description="Cross size",
            value=str(self.cross_size),
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizerFigure):

        def handle_change(change):
            """
            change cross size
            """

            ConfigWidgets.cross_size = int(change.new)
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")