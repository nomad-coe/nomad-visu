from IPython.display import display, Markdown, FileLink
from include._updates import update_hover_variables, update_df_on_map, update_layout_figure
from include._colors import make_colors
from include._view_structure import view_structure_r, view_structure_l
import numpy as np

class WidgetsInteractionsMixin:

    def handle_xfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordinglysI
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
        update_layout_figure(self)

    def handle_frac_change(self, change):
        self.frac = change.new
        update_df_on_map(self)
        update_hover_variables(self)
        update_layout_figure(self)

    def handle_colorfeat_change(self, change):
        if change.new == 'default color':
            self.widg_gradient.disabled = True
        else:
            self.widg_gradient.disabled = False
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
        update_layout_figure(self)

    def handle_crossize_change(self, change):
        self.cross_size = int(change.new)
        update_layout_figure(self)

    def handle_classes_symbol_change(self, change):
        self.widg_symbols.value = self.class_symbol['Class ' + str(change.new)]

    def handle_symbols_change(self, change):
        self.class_symbol['Class ' + str(self.widg_classes_symbol.value) ] = change.new
        self.symbols['Class ' + str(self.widg_classes_symbol.value)] = [str(change.new)] * self.n_points['Class ' + str(self.widg_classes_symbol.value)]
        update_layout_figure(self)

    def handle_hullslinewidth_change(self, change):
        update_layout_figure(self)
        
    def handle_hullslinecolor_change(self, change):
        update_layout_figure(self)
        
    def handle_hullslinestyle_change(self, change):
        update_layout_figure(self)

    def handle_linelinewidth_change(self, change):
        update_layout_figure(self)
        
    def handle_linelinecolor_change(self, change):
        update_layout_figure(self)
        
    def handle_linelinestyle_change(self, change):
        update_layout_figure(self)


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
                plot_bgcolor=self.bg_color,
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
                self.bg_color = self.widg_bgcolor.value
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
        structure = self.df.iloc[points.point_inds[0]]['Structure']

        if self.widg_checkbox_l.value:
            self.widg_compound_text_l.value = formula
            view_structure_l(self, structure)
        if self.widg_checkbox_r.value:
            self.widg_compound_text_r.value = formula
            view_structure_r(self, structure)

        update_df_on_map(self)
        update_layout_figure(self)


    def display_button_l_clicked(self, button):

        if self.widg_compound_text_r.value in self.df['Structure']:

            # self.replica_l += 1
            compound_l = self.widg_compound_text_l.value
            structure_l = self.df['Structure'].at[compound_l]

            view_structure_l(self, structure_l)

            update_df_on_map(self)
            update_layout_figure(self)
            
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
        if self.widg_compound_text_r.value in self.df['Structure']:

            # self.replica_r += 1
            compound_r = self.widg_compound_text_r.value
            structure_r = self.df['Structure'].at[compound_r]

            view_structure_r(self, structure_r)

            update_df_on_map(self)
            update_layout_figure(self)

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

