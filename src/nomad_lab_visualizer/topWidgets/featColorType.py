import ipywidgets as widgets

from ..configWidgets import ConfigWidgets

class FeatColorType (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.RadioButtons(
            options=["Gradient", "Discrete"],
            value="Gradient",
            layout=widgets.Layout(width="140px", left="90px"),
            disabled=True,
        )

    def observe_change (self, visualizerFigure, featColorListWidget):

        def handle_change(change):
            """
            changes the type of markers coloring
            """

            ConfigWidgets.featcolor_type = change.new

            if change.new == "Gradient":
                featColorListWidget.options = self.continuous_gradient_colors
                ConfigWidgets.featcolor_list = "viridis"
                featColorListWidget.value = "viridis"
            if change.new == "Discrete":
                featColorListWidget.options = self.discrete_palette_colors
                ConfigWidgets.featcolor_list = "Plotly"
                featColorListWidget.value = "Plotly"

            visualizerFigure.batch_update(self)


        self.widget.observe(
            handle_change, names="value"
        )
