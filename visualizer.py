from staticVisualizer import StaticVisualizer
from widgetsInteractionsMixin import WidgetsInteractionsMixin
import ipywidgets as widgets


class Visualizer(StaticVisualizer, WidgetsInteractionsMixin):
    def __init__(self, df, embedding_features, hover_features, target, smart_fract=False, convex_hull=False, regr_line_coefs=None, path_to_structures=None):
        super().__init__(df, embedding_features, hover_features, target, smart_fract, convex_hull, regr_line_coefs, path_to_structures)


        if self.path_to_structures:
            for name_trace in self.trace_name:
                self.trace[name_trace].on_click(self.handle_point_clicked)  # actions are performed after clicking points on the map

        self.widg_featx.observe(self.handle_xfeat_change, names='value')
        self.widg_featy.observe(self.handle_yfeat_change, names='value')
        self.widg_featmarker.observe(self.handle_markerfeat_change, names='value')
        self.widg_featcolor.observe(self.handle_colorfeat_change, names='value')
        self.widg_featcolor_list.observe(self.handle_featcolor_list_change, names='value')
        self.widg_featcolor_type.observe(self.handle_featcolor_type_change, names='value')
        self.widg_featmarker_maxvalue.observe(self.handle_featmarker_maxvalue_change, names='value')
        self.widg_featmarker_minvalue.observe(self.handle_featmarker_minvalue_change, names='value')
        self.widg_color_palette.observe(self.handle_colorpalette_change, names='value')
        self.widg_utils_button.on_click(self.utils_button_clicked)
        self.widg_fract_slider.observe(self.handle_fract_change, names='value')
        self.widg_display_button_l.on_click(self.display_button_l_clicked)
        self.widg_display_button_r.on_click(self.display_button_r_clicked)
        self.widg_checkbox_l.observe(self.handle_checkbox_l, names='value')
        self.widg_checkbox_r.observe(self.handle_checkbox_r, names='value')
        self.widg_reset_button.on_click(self.reset_button_clicked)
        self.widg_bgcolor_update_button.on_click(self.bgcolor_update_button_clicked)
        self.widg_print_button.on_click(self.print_button_clicked)
        self.widg_bgtoggle_button.on_click(self.bgtoggle_button_clicked)
        self.widg_width_hull.observe(self.handle_width_hull_change, names='value')
        self.widg_style_hull.observe(self.handle_style_hull_change, names='value')
        self.widg_color_hull.observe(self.handle_color_hull_change, names='value')
        self.widg_width_line.observe(self.handle_width_line_change, names='value')
        self.widg_style_line.observe(self.handle_style_line_change, names='value')
        self.widg_color_line.observe(self.handle_color_line_change, names='value')
        self.widg_trace_symbol.observe(self.handle_trace_symbol_change, names='value')
        self.widg_markers_symbol.observe(self.handle_markers_symbol_change, names='value')
        self.widg_markers_size.observe(self.handle_markers_size_change, names='value')
        self.widg_cross_size.observe(self.handle_cross_size_change, names='value')
        self.widg_font_family.observe(self.handle_font_family_change, names='value')
        self.widg_font_size.observe(self.handle_font_size_change, names='value')
        self.widg_font_color.observe(self.handle_font_color_change , names='value')
        self.output_l.layout = widgets.Layout(width="400px", height='350px')
        self.output_r.layout = widgets.Layout(width="400px", height='350px')


