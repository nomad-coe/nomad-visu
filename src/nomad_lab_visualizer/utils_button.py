import ipywidgets as widgets

from .config_widgets import ConfigWidgets


class UtilsButton(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Button(
            description="For a high-quality print of the plot, click to access the plot appearance utils",
            layout=widgets.Layout(width="600px"),
        )

    def observe_changes(self, Figure, visualizer_utils_widgets, visualizer_viewers_widgets):
        def button_clicked(button):
            """
            shows the plot utils box
            """

            if Figure.path_to_structures:
                if visualizer_utils_widgets.widg_box.layout.visibility == "visible":
                    visualizer_utils_widgets.widg_box.layout.visibility = "hidden"
                    for i in range(340, -1, -1):
                        visualizer_viewers_widgets.widg_box.layout.top = str(i) + "px"
                    visualizer_utils_widgets.widg_box.layout.bottom = "0px"
                else:
                    for i in range(341):
                        visualizer_viewers_widgets.widg_box.layout.top = str(i) + "px"
                    visualizer_utils_widgets.widg_box.layout.bottom = "460px"
                    visualizer_utils_widgets.widg_box.layout.visibility = "visible"
            else:
                if visualizer_utils_widgets.widg_box.layout.visibility == "visible":
                    visualizer_utils_widgets.widg_box.layout.visibility = "hidden"
                else:
                    visualizer_utils_widgets.widg_box.layout.visibility = "visible"

        self.widget.on_click(button_clicked)
