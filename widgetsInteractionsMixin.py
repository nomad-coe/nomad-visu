from IPython.display import display, Markdown, FileLink
from include._updates import update_hover_variables, update_df_on_map, update_layout_figure, update_markers_size
from include._colors import make_colors
from include._view_structure import view_structure_r, view_structure_l
import numpy as np

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
        make_colors( self, feature=change.new )
        update_layout_figure(self)

    def handle_colorpalette_change(self, change):
        make_colors ( self )
        update_layout_figure(self)

    def handle_gradient_change(self, change):
        make_colors(self, feature=self.widg_featcolor.value)
        update_layout_figure(self)

    def updatefrac_button_clicked(self, button):
        self.frac = self.widg_frac_slider.value
        # self.make_dfclusters()
        update_hover_variables(self)
        update_layout_figure(self)

    def handle_fontfamily_change(self, change):
        self.fig.update_layout(
            font=dict(family=change.new)
        )

    def handle_fontsize_change(self, change):
        self.fig.update_layout(
            font=dict(size=change.new)
        )

    def handle_markersize_change(self, change):

        self.marker_size = int(change.new)
        update_markers_size(self)
        update_layout_figure(self)

    def handle_crossize_change(self, change):

        self.cross_size = int(change.new)
        update_markers_size(self, feature=self.widg_featmarker.value)
        update_layout_figure(self)

    def handle_hullslinewidth_change(self, change):
        
        self.hullsline_width = change.new
        with self.fig.batch_update():
            for cl in np.arange(self.n_classes):
                self.trace['Hull '+str(self.classes[cl])].line.width = change.new

    def handle_hullslinecolor_change(self, change):
        
        self.hullsline_color = change.new
        print(change.new)
        with self.fig.batch_update():
            for cl in np.arange(self.n_classes):
                self.trace['Hull '+str(self.classes[cl])].line.color = change.new

    def handle_hullslinestyle_change(self, change):

        self.hullsline_style = change.new
        with self.fig.batch_update():
            for cl in np.arange(self.n_classes):
                self.trace['Hull '+str(self.classes[cl])].line.dash = change.new


    # def handle_clslinewidth_change(self, change):

    #     self.clsline_width = change.new
    #     with self.fig.batch_update():
    #         self.scatter_clsline.line.width = change.new

    # def handle_clslinestyle_change(self, change):

    #     with self.fig.batch_update():
    #         self.scatter_clsline.line.dash = change.new

    # def handle_markersymbol_cls0_change(self, change):

    #     for i, e in enumerate(self.symbols_cls0):
    #         if e == self.marker_symbol_cls0:
    #             self.symbols_cls0[i] = change.new
    #     self.marker_symbol_cls0 = change.new
    #     self.update_markers()

    # def handle_markersymbol_cls1_change(self, change):

    #     for i, e in enumerate(self.symbols_cls1):
    #         if e == self.marker_symbol_cls1:
    #             self.symbols_cls1[i] = change.new
    #     self.marker_symbol_cls1 = change.new
    #     self.update_markers()

    def bgtoggle_button_clicked(self, button):

        if self.bg_toggle:
            self.bg_toggle = False
            self.fig.update_layout(
                plot_bgcolor='white',
                xaxis=dict(gridcolor='rgb(229,236,246)', showgrid=True, zeroline=False),
                yaxis=dict(gridcolor='rgb(229,236,246)', showgrid=True, zeroline=False),
            )
        else:
            self.bg_toggle = True
            self.fig.update_layout(
                plot_bgcolor=self.plot_bgcolor,
                xaxis=dict(gridcolor='white'),
                yaxis=dict(gridcolor='white')
            )

    def print_button_clicked(self, button):

        self.widg_print_out.clear_output()
        text = "A download link will appear soon."
        with self.widg_print_out:
            display(Markdown(text))
        path = "./"
        try:
            os.mkdir(path)
        except:
            pass
        file_name = self.widg_plot_name.value + '.' + self.widg_plot_format.value
        self.fig.write_image(path + file_name, scale=self.widg_scale.value)
        self.widg_print_out.clear_output()
        with self.widg_print_out:
            local_file = FileLink(path + file_name, result_html_prefix="Click here to download: ")
            display(local_file)

    def reset_button_clicked(self, button):

        self.symbols_cls0 = [self.marker_symbol_cls0] * self.npoints_cls0
        self.symbols_cls1 = [self.marker_symbol_cls1] * self.npoints_cls1
        self.set_markers_size(self.widg_featmarker.value)
        self.update_markers()

    def bgcolor_update_button_clicked(self, button):
        if (self.widg_bgcolor.value=='Default'):
                self.fig.update_layout(
                    plot_bgcolor=self.bg_color_default,
                    xaxis=dict(gridcolor='white'),
                    yaxis=dict(gridcolor='white')
                     )
                self.plot_bgcolor = self.bg_color_default
                self.bg_toggle = True
        else:
            try:
                self.fig.update_layout(
                        plot_bgcolor=self.widg_bgcolor.value,
                        xaxis=dict(gridcolor='white'),
                        yaxis=dict(gridcolor='white')
                )
                self.plot_bgcolor = self.widg_bgcolor.value
                self.bg_toggle = True
            except:
                pass

    def plotappearance_button_clicked(self, button):
        if self.widg_box_utils.layout.visibility == 'visible':
            self.widg_box_utils.layout.visibility = 'hidden'
            for i in range(490, -1, -1):
                self.widg_box_viewers.layout.top = str(i) + 'px'
            self.widg_box_utils.layout.bottom = '0px'
        else:
            for i in range(491):
                self.widg_box_viewers.layout.top = str(i) + 'px'
            self.widg_box_utils.layout.bottom = '400px'
            self.widg_box_utils.layout.visibility = 'visible'

    def handle_checkbox_l(self, change):
        if change.new:
            self.widg_checkbox_r.value = False
        else:
            self.widg_checkbox_r.value = True

    def handle_checkbox_r(self, change):
        if change.new:
            self.widg_checkbox_l.value = False
        else:
            self.widg_checkbox_l.value = True

    def handle_point_clicked(self, trace, points, selector):
        # changes the points labeled with a cross on the map.
        if not points.point_inds:
            return

        trace = points.trace_index
        formula = self.fig.data[trace].text[points.point_inds[0]]

        if self.widg_checkbox_l.value:
            self.trace_l = [trace, formula]
        if self.widg_checkbox_r.value:
            self.trace_r = [trace, formula]

        # self.make_dfclusters()
        # self.update_appearance_variables()
        if self.widg_checkbox_l.value:
            self.widg_compound_text_l.value = formula
            view_structure_l(self, formula)
        if self.widg_checkbox_r.value:
            self.widg_compound_text_r.value = formula
            view_structure_r(self, formula)
        update_df_on_map(self)
        update_markers_size(self, feature=self.widg_featmarker.value)
        update_layout_figure(self)

    def display_button_l_clicked(self, button):

        if self.widg_compound_text_l.value in self.path_to_structures.keys():

            # self.replica_l += 1
            formula_l = self.widg_compound_text_l.value
            view_structure_l(self, formula_l)

            # trace_l = self.df_grouped.loc[self.df_grouped.index == formula_l]['Cluster_label'][0]
            # if trace_l == -1:
            #     trace_l = self.n_clusters
            #
            # self.trace_l = [trace_l, formula_l]

            # self.make_dfclusters()
            # self.update_appearance_variables()
            # self.update_layout_figure()
            #
            # if self.widg_colormarkers.value == 'Clustering':
            #     name_trace = self.name_trace[trace_l]
            #     with self.fig.batch_update():
            #         self.fig.update_traces(
            #             selector={'name': name_trace},
            #             visible=True
            #         )

    def display_button_r_clicked(self, button):

        # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
        if self.widg_compound_text_r.value in self.path_to_structures.keys():

            self.replica_r += 1
            formula_r = self.widg_compound_text_r.value
            self.view_structure_r(formula_r)

            # trace_r = self.df_grouped.loc[self.df_grouped.index == formula_r]['Cluster_label'][0]
            # if trace_r == -1:
            #     trace_r = self.n_clusters
            #
            # self.trace_r = [trace_r, formula_r]
            #
            # self.make_dfclusters()
            # self.update_appearance_variables()
            # self.update_layout_figure()
            #
            # if self.widg_colormarkers.value == 'Clustering':
            #     name_trace = self.name_trace[trace_r]
            #     with self.fig.batch_update():
            #         self.fig.update_traces(
            #             selector={'name': name_trace},
            #             visible=True
            #         )

