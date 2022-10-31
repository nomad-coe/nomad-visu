import ipywidgets as widgets

from ..configWidgets import ConfigWidgets
from .featx import Featx
from .featy import Featy
from .fractSlider import FractSlider
from .labelFract import LabelFract
from .featColor import FeatColor
from .featColorList import FeatColorList
from .featColorType import FeatColorType
from .featMarker import FeatMarker
from .featMarkerMax import FeatMarkerMax
from .featMarkerMaxLabel import FeatMarkerMaxLabel
from .featMarkerMin import FeatMarkerMin
from .featMarkerMinLabel import FeatMarkerMinLabel

class TopWidgets(ConfigWidgets):

    def __init__(self):

        self.Featx = Featx()
        self.Featy = Featy()
        self.FractSlider = FractSlider()
        self.LabelFract = LabelFract()
        self.FeatColor = FeatColor()
        self.FeatColorType = FeatColorType()
        self.FeatColorList = FeatColorList()
        self.FeatMarker = FeatMarker()
        self.FeatMarkerMin = FeatMarkerMin()
        self.FeatMarkerMinLabel = FeatMarkerMinLabel()
        self.FeatMarkerMax = FeatMarkerMax()
        self.FeatMarkerMaxLabel = FeatMarkerMaxLabel()

        self.widg_box = widgets.VBox(
            [
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                self.Featx.widget,
                                self.Featy.widget,
                                widgets.HBox(
                                    [
                                        self.LabelFract.widget,
                                        self.FractSlider.widget]
                                ),
                            ]
                        ),
                        widgets.VBox(
                            [
                                self.FeatColor.widget,
                                widgets.HBox(
                                    [
                                        self.FeatColorType.widget,
                                        self.FeatColorList.widget],
                                        layout=widgets.Layout(top="10px"),
                                ),
                            ]
                        ),
                        widgets.VBox(
                            [
                                self.FeatMarker.widget,
                                widgets.VBox(
                                    [
                                        widgets.HBox(
                                            [
                                                self.FeatMarkerMinLabel.widget,
                                                self.FeatMarkerMin.widget,
                                            ],
                                        ),
                                        widgets.HBox(
                                            [
                                                self.FeatMarkerMaxLabel.widget,
                                                self.FeatMarkerMax.widget,
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

    def observe_changes (self, Figure, visualizerUtilsWidgets):

        self.Featx.observe_change(
            Figure,
            self.FractSlider.widget,
            visualizerUtilsWidgets.ColorLine.widget,
            visualizerUtilsWidgets.WidthLine.widget,
            visualizerUtilsWidgets.DashLine.widget
            )
        self.Featy.observe_change(
            Figure,
            self.FractSlider.widget,
            visualizerUtilsWidgets.ColorLine.widget,
            visualizerUtilsWidgets.WidthLine.widget,
            visualizerUtilsWidgets.DashLine.widget
            )
        self.FractSlider.observe_change(Figure)
        self.FeatColor.observe_change(Figure, self.FeatColorType.widget, self.FeatColorList.widget)
        self.FeatColorType.observe_change(Figure, self.FeatColorList.widget)
        self.FeatColorList.observe_change(Figure)
        self.FeatMarker.observe_change(Figure, self.FeatMarkerMin.widget, self.FeatMarkerMax.widget)
        self.FeatMarkerMin.observe_change(Figure, self.FeatMarkerMax.widget)
        self.FeatMarkerMax.observe_change(Figure, self.FeatMarkerMin.widget)
