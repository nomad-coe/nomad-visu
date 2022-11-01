import ipywidgets as widgets

from ..config_widgets import ConfigWidgets
from .bg_color import BgColor
from .bg_color_update import BgColorUpdate
from .bg_toggle import BgToggle
from .color_hull import ColorHull
from .color_line import ColorLine
from .color_palette import ColorPalette
from .cross_size import CrossSize
from .dash_hull import DashHull
from .dash_line import DashLine
from .font_color import FontColor
from .font_family import FontFamily
from .font_size import FontSize
from .markers_size import MarkersSize
from .markers_symbol import MarkersSymbol
from .plot_format import PlotFormat
from .plot_name import PlotName
from .plot_resolution import PlotResolution
from .print_button import Print
from .print_label import PrintLabel
from .print_output import PrintOutput
from .reset_button import ResetButton
from .trace_symbol import TraceSymbol
from .width_hull import WidthHull
from .width_line import WidthLine
from .window_label import WindowLabel

class UtilsWidgets(ConfigWidgets):

    def __init__(self):

        self.bg_color = BgColor()
        self.bg_color_update = BgColorUpdate()
        self.bg_toggle = BgToggle()
        self.color_hull = ColorHull()
        self.color_line = ColorLine ()
        self.color_palette = ColorPalette()
        self.cross_size = CrossSize()
        self.dash_hull = DashHull()
        self.dash_line = DashLine()
        self.font_color = FontColor()
        self.font_family = FontFamily()
        self.font_size = FontSize()
        self.markers_size = MarkersSize()
        self.markers_symbol = MarkersSymbol()
        self.plot_format = PlotFormat()
        self.plot_name = PlotName()
        self.plot_resolution = PlotResolution()
        self.print = Print()
        self.print_label = PrintLabel()
        self.print_output = PrintOutput()
        self.reset_button = ResetButton()
        self.trace_symbol = TraceSymbol()
        self.width_hull = WidthHull()
        self.width_line = WidthLine()
        self.window_label = WindowLabel()

        self.color_hull.widget.disabled = True
        self.width_hull.widget.disabled = True
        self.dash_hull.widget.disabled = True

        self.color_line.widget.disabled = True
        self.width_line.widget.disabled = True
        self.dash_line.widget.disabled = True

        self.widg_box = widgets.VBox(
            [
                widgets.HBox(
                        [
                        self.markers_size.widget,
                        self.cross_size.widget,
                        self.color_palette.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.font_size.widget,
                        self.font_family.widget,
                        self.font_color.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.trace_symbol.widget,
                        self.markers_symbol.widget,
                        self.reset_button.widget,
                        ]
                ),
                widgets.HBox(
                        [
                        self.color_hull.widget,
                        self.width_hull.widget,
                        self.dash_hull.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.color_line.widget,
                        self.width_line.widget,
                        self.dash_line.widget
                        ]
                ),
                widgets.HBox(
                        [
                        self.bg_toggle.widget,
                        self.bg_color.widget,
                        self.bg_color_update.widget,
                        ]
                ),
                self.print_label.widget,
                widgets.HBox(
                        [
                        self.plot_name.widget,
                        self.plot_format.widget,
                        self.plot_resolution.widget,
                        ]
                ),
                self.print.widget,
                self.print_output.widget,
            ]
        )




    def observe_changes(self, Figure):

        self.bg_color_update.observe_change(Figure, self.bg_color)
        self.bg_toggle.observe_change(Figure)
        self.color_hull.observe_change(Figure)
        self.color_line.observe_change(Figure)
        self.color_palette.observe_change(Figure)
        self.cross_size.observe_change(Figure)
        self.dash_hull.observe_change(Figure)
        self.dash_line.observe_change(Figure)
        self.font_color.observe_change(Figure)
        self.font_family.observe_change(Figure)
        self.font_size.observe_change(Figure)
        self.markers_size.observe_change(Figure)
        self.markers_symbol.observe_change(Figure, self.trace_symbol)
        self.print.observe_change(Figure, self.print_output, self.plot_name, self.plot_format, self.plot_resolution)
        self.reset_button.observe_change(Figure)
        self.trace_symbol.observe_change(Figure)
        self.width_hull.observe_change(Figure)
        self.width_line.observe_change(Figure)

