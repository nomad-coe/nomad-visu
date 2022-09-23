from .configWidgets import ConfigWidgets
from .include._batch_update import batch_update
from .include._updates import marker_style_updates, fract_change_updates
import ipywidgets as widgets
import os
import py3Dmol
from .utilsWidgets import UtilsWidgets
from .viewersWidgets import ViewersWidgets

class UtilsButton( ConfigWidgets ):
    def __init__( self, Figure, UtilsWidgets, ViewersWidgets ):

        self.widg_utils_button = widgets.Button(
            description="For a high-quality print of the plot, click to access the plot appearance utils",
            layout=widgets.Layout(width="600px"),
        )
        def utils_button_clicked( button):
            """
            shows the plot utils box
            """

            if Figure.path_to_structures:
                if UtilsWidgets.widg_box_utils.layout.visibility == "visible":
                    UtilsWidgets.widg_box_utils.layout.visibility = "hidden"
                    for i in range(340, -1, -1):
                        ViewersWidgets.widg_box_viewers.layout.top = str(i) + "px"
                    UtilsWidgets.widg_box_utils.layout.bottom = "0px"
                else:
                    for i in range(341):
                        ViewersWidgets.widg_box_viewers.layout.top = str(i) + "px"
                    UtilsWidgets.widg_box_utils.layout.bottom = "400px"
                    UtilsWidgets.widg_box_utils.layout.visibility = "visible"
            else:
                if UtilsWidgets.widg_box_utils.layout.visibility == "visible":
                    UtilsWidgets.widg_box_utils.layout.visibility = "hidden"
                else:
                    UtilsWidgets.widg_box_utils.layout.visibility = "visible"

        self.widg_utils_button.on_click(utils_button_clicked)

    def container (self):
        return self.widg_utils_button