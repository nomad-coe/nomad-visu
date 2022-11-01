import ipywidgets as widgets

from nomad_lab_visualizer.config_widgets import ConfigWidgets

from .cross_image_l import CrossImageL
from .cross_image_r import CrossImageR
from .display_button_l import DisplayButtonL
from .display_button_r import DisplayButtonR
from .structure_name_l import StructureNameL
from .structure_name_r import StructureNameR
from .viewer_l import ViewerL
from .viewer_r import ViewerR
from .windows_checkbox_l import WindowsCheckboxL
from .windows_checkbox_r import WindowsCheckboxR
from .windows_label import WindowsLabel
from .windows_output_l import WindowsOutputL
from .windows_output_r import WindowsOutputR


class ViewersWidgets(ConfigWidgets):
    def __init__(self):

        self.cross_image_l = CrossImageL()
        self.cross_image_r = CrossImageR()
        self.display_button_l = DisplayButtonL()
        self.display_button_r = DisplayButtonR()
        self.structure_name_l = StructureNameL()
        self.structure_name_r = StructureNameR()
        self.viewer_l = ViewerL()
        self.viewer_r = ViewerR()
        self.windows_checkbox_l = WindowsCheckboxL()
        self.windows_checkbox_r = WindowsCheckboxR()
        self.windows_label = WindowsLabel()
        self.windows_output_l = WindowsOutputL()
        self.windows_output_r = WindowsOutputR()

        self.widg_box = widgets.VBox(
            [
                self.windows_label.widget,
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                widgets.HBox(
                                    [
                                        self.structure_name_l.widget,
                                        self.display_button_l.widget,
                                        self.cross_image_l.widget,
                                        self.windows_checkbox_l.widget,
                                    ]
                                ),
                                self.windows_output_l.widget,
                            ]
                        ),
                        widgets.VBox(
                            [
                                widgets.HBox(
                                    [
                                        self.structure_name_r.widget,
                                        self.display_button_r.widget,
                                        self.cross_image_r.widget,
                                        self.windows_checkbox_r.widget,
                                    ]
                                ),
                                self.windows_output_r.widget,
                            ]
                        ),
                    ]
                ),
            ]
        )

    def observe_changes(self, Figure):

        self.display_button_l.observe_change(
            Figure, self.viewer_l, self.structure_name_l, self.windows_output_l
        )
        self.display_button_r.observe_change(
            Figure, self.viewer_r, self.structure_name_r, self.windows_output_r
        )
        self.windows_checkbox_l.observe_change(self.windows_checkbox_r)
        self.windows_checkbox_r.observe_change(self.windows_checkbox_l)

        def handle_point_clicked(trace, points, selector):
            """
            visualizes structure of clicked point and changes its marker symbol to a cross
            """

            if not points.point_inds:
                return

            trace = points.trace_index
            formula = Figure.FigureWidget.data[trace].text[points.point_inds[0]]
            structure = Figure.df.iloc[points.point_inds[0]]["Structure"]

            if self.windows_checkbox_l.widget.value:
                self.structure_name_l.widget.value = formula
                self.viewer_l.view_structure(formula, Figure, self.windows_output_l)
            if self.windows_checkbox_r.widget.value:
                self.structure_name_l.widget.value = formula
                self.viewer_r.view_structure(formula, Figure, self.windows_output_r)

            Figure.batch_update(self)

        if Figure.path_to_structures:
            for name_trace in Figure.name_traces:
                Figure.trace[str(name_trace)].on_click(
                    handle_point_clicked  # actions performed after clicking points on the map
                )
