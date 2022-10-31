import ipywidgets as widgets

from ..configWidgets import ConfigWidgets
from .bgColor import BgColor
from .bgColorUpdate import BgColorUpdate
from .bgToggle import BgToggle
from .colorHull import ColorHull
from .colorLine import ColorLine
from .colorPalette import ColorPalette
from .crossSize import CrossSize
from .dashHull import DashHull
from .dashLine import DashLine
from .fontColor import FontColor
from .fontFamily import FontFamily
from .fontSize import FontSize
from .markersSize import MarkersSize
from .markersSymbol import MarkersSymbol
from .plotFormat import PlotFormat
from .plotName import PlotName
from .plotResolution import PlotResolution
from .print import Print
from .printLabel import PrintLabel
from .printOutuput import PrintOutput
from .resetButton import ResetButton
from .traceSymbol import TraceSymbol
from .widthHull import WidthHull
from .widthLine import WidthLine
from .windowLabel import WindowLabel

class UtilsWidgets(ConfigWidgets):

    def __init__(self):

        self.BgColor = BgColor()
        self.BgColorUpdate = BgColorUpdate()
        self.BgToggle = BgToggle()
        self.ColorHull = ColorHull()
        self.ColorLine = ColorLine ()
        self.ColorPalette = ColorPalette()
        self.CrossSize = CrossSize()
        self.DashHull = DashHull()
        self.DashLine = DashLine()
        self.FontColor = FontColor()
        self.FontFamily = FontFamily()
        self.FontSize = FontSize()
        self.MarkersSize = MarkersSize()
        self.MarkersSymbol = MarkersSymbol()
        self.PlotFormat = PlotFormat()
        self.PlotName = PlotName()
        self.PlotResolution = PlotResolution()
        self.Print = Print()
        self.PrintLabel = PrintLabel()
        self.PrintOutput = PrintOutput()
        self.ResetButton = ResetButton()
        self.TraceSymbol = TraceSymbol()
        self.WidthHull = WidthHull()
        self.WidthLine = WidthLine()
        self.WindowLabel = WindowLabel()

        self.ColorHull.widget.disabled = True
        self.WidthHull.widget.disabled = True
        self.DashHull.widget.disabled = True

        self.ColorLine.widget.disabled = True
        self.WidthLine.widget.disabled = True
        self.DashLine.widget.disabled = True

        self.widg_box = widgets.VBox(
            [
                widgets.HBox(
                        [
                        self.MarkersSize.widget,
                        self.CrossSize.widget,
                        self.ColorPalette.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.FontSize.widget,
                        self.FontFamily.widget,
                        self.FontColor.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.TraceSymbol.widget,
                        self.MarkersSymbol.widget,
                        self.ResetButton.widget,
                        ]
                ),
                widgets.HBox(
                        [
                        self.ColorHull.widget,
                        self.WidthHull.widget,
                        self.DashHull.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.ColorLine.widget,
                        self.WidthLine.widget,
                        self.DashLine.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.BgToggle.widget,
                        self.BgColor.widget,
                        self.BgColorUpdate.widget,
                        ]
                ),
                self.PrintLabel.widget,
                widgets.HBox(
                        [
                        self.PlotName.widget,
                        self.PlotFormat.widget,
                        self.PlotResolution.widget,
                        ]
                ),
                self.Print.widget,
                self.PrintOutput.widget,
            ]
        )




    def observe_changes(self, Figure):

        self.BgColorUpdate.observe_change(Figure, self.BgColor)
        self.BgToggle.observe_change(Figure)
        self.ColorHull.observe_change(Figure)
        self.ColorLine.observe_change(Figure)
        self.ColorPalette.observe_change(Figure)
        self.CrossSize.observe_change(Figure)
        self.DashHull.observe_change(Figure)
        self.DashLine.observe_change(Figure)
        self.FontColor.observe_change(Figure)
        self.FontFamily.observe_change(Figure)
        self.FontSize.observe_change(Figure)
        self.MarkersSize.observe_change(Figure)
        self.MarkersSymbol.observe_change(Figure, self.TraceSymbol)
        self.Print.observe_change(Figure, self.PrintOutput, self.PlotName, self.PlotFormat, self.PlotResolution)
        self.ResetButton.observe_change(Figure)
        self.TraceSymbol.observe_change(Figure)
        self.WidthHull.observe_change(Figure)
        self.WidthLine.observe_change(Figure)

