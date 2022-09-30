from .configWidgets import ConfigWidgets
import ipywidgets as widgets
from IPython.display import display, Markdown, FileLink


class UtilsWidgets(ConfigWidgets):

    from .include.utilsWidgets._instantiate_widgets import instantiate_widgets
    from .include.utilsWidgets._observe_widgets import observe_widgets

    def __init__(self, Figure):
        
        self.instantiate_widgets(Figure)         
        self.observe_widgets(Figure)
        
        self.widg_box = widgets.VBox(
            [
                widgets.HBox(
                    [self.widg_markers_size, self.widg_cross_size, self.widg_color_palette]
                ),
                widgets.HBox(
                    [self.widg_font_size, self.widg_font_family, self.widg_font_color]
                ),
                widgets.HBox(
                    [
                        self.widg_trace_symbol,
                        self.widg_markers_symbol,
                        self.widg_reset_button,
                    ]
                ),
                widgets.HBox(
                    [self.widg_color_hull, self.widg_width_hull, self.widg_dash_hull]
                ),
                widgets.HBox(
                    [self.widg_color_line, self.widg_width_line, self.widg_dash_line]
                ),
                widgets.HBox(
                    [
                        self.widg_bgtoggle_button,
                        self.widg_bgcolor,
                        self.widg_bgcolor_update_button,
                    ]
                ),
                self.widg_print_description,
                widgets.HBox(
                    [self.widg_plot_name, self.widg_plot_format, self.widg_resolution]
                ),
                self.widg_print_button,
                self.widg_print_out,
            ]
        )
   
    def container(self):

        return self.widg_box

