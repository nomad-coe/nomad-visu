from .configWidgets import ConfigWidgets
import ipywidgets as widgets

class UtilsButton( ConfigWidgets ):

    def __init__( self, Figure, visualizerUtilsWidgets, visualizerViewersWidgets ):

        self.widg_utils_button = widgets.Button(
            description="For a high-quality print of the plot, click to access the plot appearance utils",
            layout=widgets.Layout(width="600px"),
        )
        def utils_button_clicked( button):
            """
            shows the plot utils box
            """

            if Figure.path_to_structures:
                if visualizerUtilsWidgets.widg_box.layout.visibility == "visible":
                    visualizerUtilsWidgets.widg_box.layout.visibility = "hidden"
                    for i in range(340, -1, -1):
                        visualizerViewersWidgets.widg_box.layout.top = str(i) + "px"
                    visualizerUtilsWidgets.widg_box.layout.bottom = "0px"
                else:
                    for i in range(341):
                        visualizerViewersWidgets.widg_box.layout.top = str(i) + "px"
                    visualizerUtilsWidgets.widg_box.layout.bottom = "400px"
                    visualizerUtilsWidgets.widg_box.layout.visibility = "visible"
            else:
                if visualizerUtilsWidgets.widg_box.layout.visibility == "visible":
                    visualizerUtilsWidgets.widg_box.layout.visibility = "hidden"
                else:
                    visualizerUtilsWidgets.widg_box.layout.visibility = "visible"

        self.widg_utils_button.on_click(utils_button_clicked)

    def container (self):

        return self.widg_utils_button