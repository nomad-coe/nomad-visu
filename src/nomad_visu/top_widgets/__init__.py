import ipywidgets as widgets

from ..config_widgets import ConfigWidgets

from .feat_x import Featx
from .feat_y import Featy
from .fract_slider import FractSlider
from .label_fract import LabelFract
from .feat_color import FeatColor
from .feat_color_list import FeatColorList
from .feat_color_type import FeatColorType
from .feat_marker import FeatMarker
from .feat_marker_max import FeatMarkerMax
from .feat_marker_max_label import FeatMarkerMaxLabel
from .feat_marker_min import FeatMarkerMin
from .feat_marker_min_label import FeatMarkerMinLabel


class TopWidgets(ConfigWidgets):
    def __init__(self):

        self.featx = Featx()
        self.featy = Featy()
        self.fract_slider = FractSlider()
        self.label_fract = LabelFract()
        self.feat_color = FeatColor()
        self.feat_color_type = FeatColorType()
        self.feat_color_list = FeatColorList()
        self.feat_marker = FeatMarker()
        self.feat_marker_min = FeatMarkerMin()
        self.feat_marker_min_label = FeatMarkerMinLabel()
        self.feat_marker_max = FeatMarkerMax()
        self.feat_marker_max_label = FeatMarkerMaxLabel()

        self.widg_box = widgets.VBox(
            [
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                self.featx.widget,
                                self.featy.widget,
                                widgets.HBox(
                                    [self.label_fract.widget, self.fract_slider.widget]
                                ),
                            ]
                        ),
                        widgets.VBox(
                            [
                                self.feat_color.widget,
                                widgets.HBox(
                                    [
                                        self.feat_color_type.widget,
                                        self.feat_color_list.widget,
                                    ],
                                    layout=widgets.Layout(top="10px"),
                                ),
                            ]
                        ),
                        widgets.VBox(
                            [
                                self.feat_marker.widget,
                                widgets.VBox(
                                    [
                                        widgets.HBox(
                                            [
                                                self.feat_marker_min_label.widget,
                                                self.feat_marker_min.widget,
                                            ],
                                        ),
                                        widgets.HBox(
                                            [
                                                self.feat_marker_max_label.widget,
                                                self.feat_marker_max.widget,
                                            ],
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )

    def observe_changes(self, figure, visualizer_utils_widgets):

        self.featx.observe_change(
            figure,
            self.fract_slider.widget,
            visualizer_utils_widgets.color_line.widget,
            visualizer_utils_widgets.width_line.widget,
            visualizer_utils_widgets.dash_line.widget,
        )
        self.featy.observe_change(
            figure,
            self.fract_slider.widget,
            visualizer_utils_widgets.color_line.widget,
            visualizer_utils_widgets.width_line.widget,
            visualizer_utils_widgets.dash_line.widget,
        )
        self.fract_slider.observe_change(figure)
        self.feat_color.observe_change(
            figure, self.feat_color_type.widget, self.feat_color_list.widget
        )
        self.feat_color_type.observe_change(figure, self.feat_color_list.widget)
        self.feat_color_list.observe_change(figure)
        self.feat_marker.observe_change(
            figure, self.feat_marker_min.widget, self.feat_marker_max.widget
        )
        self.feat_marker_min.observe_change(figure, self.feat_marker_max.widget)
        self.feat_marker_max.observe_change(figure, self.feat_marker_min.widget)
