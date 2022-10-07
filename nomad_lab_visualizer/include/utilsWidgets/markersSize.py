import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class MarkersSize (ConfigWidgets):

    def __init__ (self):
        self.widget = widgets.BoundedIntText(
            placeholder=str(self.marker_size),
            description="Marker size",
            value=str(self.marker_size),
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizerFigure):

        def handle_change(change):
            """
            change markers size
            """

            ConfigWidgets.marker_size = int(change.new)
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")