from include._updates import update_hover_variables, update_df_on_map, update_layout_figure, update_markers_size
from include._colors import make_colors
from include._view_structure import view_structure_r, view_structure_l


class WidgetsInteractionsMixin:

    def handle_xfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordingly
        self.feat_x = change.new
        update_layout_figure(self)

    def handle_yfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordingly
        self.feat_y = change.new
        update_layout_figure(self)

    def plotappearance_button_clicked(self, button):
        if self.widg_box_utils.layout.visibility == 'visible':
            self.widg_box_utils.layout.visibility = 'hidden'
            for i in range(290, -1, -1):
                self.widg_box_viewers.layout.top = str(i) + 'px'
            self.widg_box_utils.layout.bottom = '0px'
        else:
            for i in range(291):
                self.widg_box_viewers.layout.top = str(i) + 'px'
            self.widg_box_utils.layout.bottom = '400px'
            self.widg_box_utils.layout.visibility = 'visible'

    def handle_markerfeat_change(self, change):
        update_markers_size(self, feature=change.new)
        update_layout_figure(self)

    def handle_frac_change(self, change):
        self.frac = change.new
        update_df_on_map(self)
        update_hover_variables(self)
        update_layout_figure(self)

    def handle_colorfeat_change(self, change):
        make_colors(self, feature=change.new, gradient=self.widg_gradient.value)
        update_layout_figure(self)

    def handle_gradient_change(self, change):
        make_colors(self, feature=self.widg_featcolor.value, gradient=change.new)
        update_layout_figure(self)

    def updatefrac_button_clicked(self, button):
        self.frac = self.widg_frac_slider.value
        # self.make_dfclusters()
        update_hover_variables(self)
        update_layout_figure(self)

    def handle_point_clicked(self, trace, points, selector):
        # changes the points labeled with a cross on the map.

        if not points.point_inds:
            return

        trace = points.trace_index
        formula = self.fig.data[trace].text[points.point_inds[0]]

        if self.widg_checkbox_l.value:
            self.trace_l = [trace, formula]
            # self.replica_l = 0
        if self.widg_checkbox_r.value:
            self.trace_r = [trace, formula]
            # self.replica_r = 0

        # self.make_dfclusters()
        # self.update_appearance_variables()
        update_layout_figure(self)

        if self.widg_checkbox_l.value:
            self.widg_compound_text_l.value = formula
            view_structure_l(self, formula)
        if self.widg_checkbox_r.value:
            self.widg_compound_text_r.value = formula
            view_structure_r(self, formula)
