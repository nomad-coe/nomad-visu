import ipywidgets as widgets

from .configWidgets import ConfigWidgets
from .include.topWidgets.featx import Featx
from .include.topWidgets.featy import Featy
from .include.topWidgets.fractSlider import FractSlider
from .include.topWidgets.labelFract import LabelFract
from .include.topWidgets.featColor import FeatColor
from .include.topWidgets.featColorList import FeatColorList
from .include.topWidgets.featColorType import FeatColorType
from .include.topWidgets.featMarker import FeatMarker
from .include.topWidgets.featMarkerMax import FeatMarkerMax
from .include.topWidgets.featMarkerMaxLabel import FeatMarkerMaxLabel
from .include.topWidgets.featMarkerMin import FeatMarkerMin
from .include.topWidgets.featMarkerMinLabel import FeatMarkerMinLabel

class TopWidgets(ConfigWidgets):

    def __init__(self, Figure):

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

        self.Featx.observe_change(Figure, self.FractSlider.widget)        
        self.Featy.observe_change(Figure, self.FractSlider.widget)
        self.FractSlider.observe_change(Figure)
        self.FeatColor.observe_change(Figure, self.FeatColorType.widget, self.FeatColorList.widget)
        self.FeatColorType.observe_change(Figure, self.FeatColorList.widget)
        self.FeatColorList.observe_change(Figure)
        self.FeatMarker.observe_change(Figure, self.FeatMarkerMin.widget, self.FeatMarkerMax.widget)
        self.FeatMarkerMin.observe_change(Figure, self.FeatMarkerMax.widget)
        self.FeatMarkerMax.observe_change(Figure, self.FeatMarkerMin.widget) 
        
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
    
    def container(self):

        return self.widg_box