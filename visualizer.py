from staticVisualizer import StaticVisualizer
from widgetsInteractionsMixin import WidgetsInteractionsMixin
from IPython.display import display, Markdown, FileLink, clear_output
import ipywidgets as widgets
import numpy as np

class Visualizer(StaticVisualizer, WidgetsInteractionsMixin):
    def __init__(self, df, embedding_features, hover_features, target, sisso=None, path_to_structures=None):
        super().__init__(df, embedding_features, hover_features, target, sisso, path_to_structures)
        from include._instantiate_widgets import instantiate_widgets
        from include._view_structure import view_structure_r, view_structure_l
        from include._colors import make_colors
        from include._updates import update_hover_variables, update_df_on_map, update_layout_figure, update_markers_size


        for cl in np.arange(self.n_classes):
            self.trace['Class ' + str(self.classes[cl])].on_click(self.handle_point_clicked)  # actions are performed after clicking points on the map

        self.widg_featx.observe(self.handle_xfeat_change, names='value')
        self.widg_featy.observe(self.handle_yfeat_change, names='value')
        self.widg_featmarker.observe(self.handle_markerfeat_change, names='value')
        self.widg_featcolor.observe(self.handle_colorfeat_change, names='value')
        self.widg_gradient.observe(self.handle_gradient_change, names='value')
        self.widg_colorpalette.observe(self.handle_colorpalette_change, names='value')
        self.widg_plotutils_button.on_click(self.plotappearance_button_clicked)
        self.widg_frac_slider.observe(self.handle_frac_change, names='value')
        self.widg_display_button_l.on_click(self.display_button_l_clicked)
        self.widg_display_button_r.on_click(self.display_button_r_clicked)
        self.widg_checkbox_l.observe(self.handle_checkbox_l, names='value')
        self.widg_checkbox_r.observe(self.handle_checkbox_r, names='value')
        # self.widg_reset_button.on_click(self.reset_button_clicked)
        self.widg_bgcolor_update_button.on_click(self.bgcolor_update_button_clicked)
        self.widg_print_button.on_click(self.print_button_clicked)
        self.widg_bgtoggle_button.on_click(self.bgtoggle_button_clicked)
        self.widg_width_hull.observe(self.handle_hullslinewidth_change, names='value')
        self.widg_style_hull.observe(self.handle_hullslinestyle_change, names='value')
        self.widg_color_hull.observe(self.handle_hullslinecolor_change, names='value')
        self.widg_classes_symbol.observe(self.handle_classes_symbol_change, names='value')
        self.widg_symbols.observe(self.handle_symbols_change, names='value')
        # self.scatter_cls0.on_click(self.update_point_cls0)
        # self.scatter_cls1.on_click(self.update_point_cls1)
        self.widg_markersize.observe(self.handle_markersize_change, names='value')
        self.widg_crosssize.observe(self.handle_crossize_change, names='value')
        self.widg_fontfamily.observe(self.handle_fontfamily_change, names='value')
        self.widg_fontsize.observe(self.handle_fontsize_change, names='value')


        self.output_l.layout = widgets.Layout(width="400px", height='350px')
        self.output_r.layout = widgets.Layout(width="400px", height='350px')


