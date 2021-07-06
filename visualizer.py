from staticVisualizer import StaticVisualizer
from widgetsInteractionsMixin import WidgetsInteractionsMixin
from IPython.display import display, Markdown, FileLink, clear_output
import ipywidgets as widgets


class Visualizer(StaticVisualizer, WidgetsInteractionsMixin):
    def __init__(self, df, embedding_features, hover_features, target, sisso=None, path_to_structures=None):
        super().__init__(df, embedding_features, hover_features, target, sisso, path_to_structures)
        from include._instantiate_widgets import instantiate_widgets
        from include._view_structure import view_structure_r, view_structure_l
        from include._colors import make_colors
        from include._updates import update_hover_variables, update_df_on_map, update_layout_figure, update_markers_size

        for name in self.name_trace:
            self.trace[name].on_click(self.handle_point_clicked)  # actions are performed after clicking points on the map

        self.widg_featx.observe(self.handle_xfeat_change, names='value')
        self.widg_featy.observe(self.handle_yfeat_change, names='value')
        self.widg_featmarker.observe(self.handle_markerfeat_change, names='value')
        self.widg_featcolor.observe(self.handle_colorfeat_change, names='value')
        self.widg_gradient.observe(self.handle_gradient_change, names='value')
        self.widg_plotutils_button.on_click(self.plotappearance_button_clicked)
        self.widg_frac_slider.observe(self.handle_frac_change, names='value')
        self.widg_display_button_l.on_click(self.display_button_l_clicked)
        self.widg_display_button_r.on_click(self.display_button_r_clicked)

        self.output_l.layout = widgets.Layout(width="400px", height='350px')
        self.output_r.layout = widgets.Layout(width="400px", height='350px')


