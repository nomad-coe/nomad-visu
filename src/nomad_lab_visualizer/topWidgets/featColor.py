import ipywidgets as widgets

from ..configWidgets import ConfigWidgets

class FeatColor (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Dropdown(
            description="Color",
            options=["Default color"] + self.hover_features,
            value="Default color",
            layout=widgets.Layout(width="250px"),
        )

    def observe_change (self, visualizerFigure, featColorTypeWidget, featColorListWidget):

        def handle_change(change):
            """
            changes markers color according to a specific feature
            """

            ConfigWidgets.featcolor = change.new

            if change.new == "Default color":
                featColorTypeWidget.disabled = True
                featColorListWidget.disabled = True
                # self.widg_color_palette.disabled = False
            else:
                featColorTypeWidget.disabled = False
                featColorListWidget.disabled = False
                # self.widg_color_palette.disabled = True
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")
