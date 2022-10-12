import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

from .include.viewersWidgets.crossImageL import CrossImageL
from .include.viewersWidgets.crossImageR import CrossImageR
from .include.viewersWidgets.displayButtonL import DisplayButtonL
from .include.viewersWidgets.displayButtonR import DisplayButtonR
from .include.viewersWidgets.structureNameL import StructureNameL
from .include.viewersWidgets.structureNameR import StructureNameR
from .include.viewersWidgets.viewerL import ViewerL
from .include.viewersWidgets.viewerR import ViewerR
from .include.viewersWidgets.windowsCheckboxL import WindowsCheckboxL
from .include.viewersWidgets.windowsCheckboxR import WindowsCheckboxR
from .include.viewersWidgets.windowsLabel import WindowsLabel
from .include.viewersWidgets.windowsOutputL import WindowsOutputL
from .include.viewersWidgets.windowsOutputR import WindowsOutputR


class ViewersWidgets( ConfigWidgets ):
        

    def __init__(self, Figure):

        def handle_point_clicked( trace, points, selector ):
            """
            visualizes structure of clicked point and changes its marker symbol to a cross
            """

            if not points.point_inds:
                return

            trace = points.trace_index
            formula = Figure.FigureWidget.data[trace].text[points.point_inds[0]]
            structure = Figure.df.iloc[points.point_inds[0]]["Structure"]

            if self.windowsCheckboxL.widget.value:
                self.structureNameL.widget.value = formula
                self.viewerL.view_structure (formula, Figure, self.windowsOutputL)
            if self.windowsCheckboxR.widget.value:
                self.structureNameL.widget.value = formula
                self.viewerR.view_structure (formula, Figure, self.windowsOutputR)

            Figure.batch_update(self)

        self.crossImageL = CrossImageL()
        self.crossImageR = CrossImageR()
        self.displayButtonL = DisplayButtonL()
        self.displayButtonR = DisplayButtonR()
        self.structureNameL = StructureNameL()
        self.structureNameR = StructureNameR()
        self.viewerL = ViewerL()
        self.viewerR = ViewerR()
        self.windowsCheckboxL = WindowsCheckboxL()
        self.windowsCheckboxR = WindowsCheckboxR()
        self.windowsLabel = WindowsLabel()
        self.windowsOutputL = WindowsOutputL(self.viewerL)
        self.windowsOutputR = WindowsOutputR(self.viewerR)

        self.displayButtonL.observe_change(Figure, self.viewerL, self.structureNameL, self.windowsOutputL)
        self.displayButtonR.observe_change(Figure, self.viewerR, self.structureNameR, self.windowsOutputR)
        self.windowsCheckboxL.observe_change(self.windowsCheckboxR)
        self.windowsCheckboxR.observe_change(self.windowsCheckboxL)
        

            

        # if Figure.path_to_structures:
        for name_trace in Figure.name_traces:
            Figure.trace[str(name_trace)].on_click(
                handle_point_clicked
            )  # actions performed after clicking points on the map

        self.widg_box = widgets.VBox(
            [
                self.windowsLabel.widget,
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                widgets.HBox(
                                    [
                                        self.structureNameL.widget,
                                        self.displayButtonL.widget,
                                        self.crossImageL.widget,
                                        self.windowsCheckboxL.widget,
                                    ]
                                ),
                                self.windowsOutputL.widget,
                            ]
                        ),
                        widgets.VBox(
                            [
                                widgets.HBox(
                                    [
                                        self.structureNameR.widget,
                                        self.displayButtonR.widget,
                                        self.crossImageR.widget,
                                        self.windowsCheckboxR.widget,
                                    ]
                                ),
                                self.windowsOutputR.widget,
                            ]
                        ),
                    ]
                ),
            ]
        )
        

    def container (self):

        return self.widg_box
