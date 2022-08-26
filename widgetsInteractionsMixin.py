from IPython.display import display, Markdown, FileLink
from include._updates import update_hover_variables, update_df_on_map, update_marker_color, update_marker_size, update_marker_symbol, marker_style_updates, fract_change_updates
from include._batch_update import batch_update
from include._view_structure import view_structure_r, view_structure_l


class WidgetsInteractionsMixin:

    def handle_xfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordinglysI
        self.feat_x = change.new
        if (self.feat_x != self.feat_y and self.max_covering):
            self.fract = self.fract_thres[(self.feat_x,self.feat_y)]
            self.widg_fract_slider.value = self.fract

        marker_style_updates(self)        
        batch_update(self)

    def handle_yfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordingly
        self.feat_y = change.new
        if (self.feat_x != self.feat_y and self.max_covering):
            self.fract = self.fract_thres[(self.feat_x,self.feat_y)]
            self.widg_fract_slider.value = self.fract

        marker_style_updates(self)        
        batch_update(self)

    def handle_fract_change(self, change):
        self.fract = change.new
        fract_change_updates(self)
        marker_style_updates(self)        
        batch_update(self)

    def handle_colorfeat_change(self, change):
        if change.new == 'Default color':
            self.widg_featcolor_type.disabled = True
            self.widg_featcolor_list.disabled = True
        else:
            self.widg_featcolor_type.disabled = False
            self.widg_featcolor_list.disabled = False
        marker_style_updates(self)        
        batch_update(self)

    def handle_markerfeat_change(self, change):
        if change.new == 'Default size':
            self.widg_featmarker_maxvalue.disabled = True
            self.widg_featmarker_minvalue.disabled = True
        else:
            self.widg_featmarker_maxvalue.disabled = False
            self.widg_featmarker_minvalue.disabled = False

        marker_style_updates(self)        
        batch_update(self)

    def handle_colorpalette_change(self, change):
        marker_style_updates(self)        
        batch_update(self)

    def handle_featcolor_list_change(self, change):
        marker_style_updates(self)        
        batch_update(self)
        batch_update(self)

    def handle_gradient_change(self, change):
        marker_style_updates(self)        
        batch_update(self)

    def handle_featcolor_type_change(self, change):
        if change.new == 'Gradient':
            self.widg_featcolor_list.options = self.gradient_list
            self.widg_featcolor_list.value = 'viridis'
        if change.new == 'Discrete':
            self.widg_featcolor_list.options = self.qualitative_colors
            self.widg_featcolor_list.value = 'Plotly'
        marker_style_updates(self)        
        batch_update(self)

 
    def handle_featmarker_maxvalue_change(self, change):
        self.max_value_markerfeat = change.new
        self.widg_featmarker_minvalue.max = change.new
        marker_style_updates(self)        
        batch_update(self)

    def handle_featmarker_minvalue_change(self, change):
        self.min_value_markerfeat = change.new
        self.widg_featmarker_maxvalue.min = change.new
        marker_style_updates(self)        

    def handle_point_clicked(self, trace, points, selector):
        # changes the points labeled with a cross on the map.
 
        if not points.point_inds:
            return

        trace = points.trace_index
        formula = self.fig.data[trace].text[points.point_inds[0]]
        structure = self.df.iloc[points.point_inds[0]]['Structure']

        if self.widg_checkbox_l.value:
            self.widg_compound_text_l.value = formula
            view_structure_l(self, formula)
        if self.widg_checkbox_r.value:
            self.widg_compound_text_r.value = formula
            view_structure_r(self, formula)

        fract_change_updates(self)
        marker_style_updates(self)        
        batch_update(self)      


    def handle_font_family_change(self, change):
        self.fig.update_layout(
            font=dict(family=change.new)
        )

    def handle_font_size_change(self, change):
        self.fig.update_layout(
            font=dict(size=change.new)
        )
    def handle_font_color_change(self, change):
        self.fig.update_layout(
            font=dict(color=change.new)
        )

    def utils_button_clicked(self, button):
        if self.path_to_structures:
            if self.widg_box_utils.layout.visibility == 'visible':
                self.widg_box_utils.layout.visibility = 'hidden'
                for i in range(340, -1, -1):
                    self.widg_box_viewers.layout.top = str(i) + 'px'
                self.widg_box_utils.layout.bottom = '0px'
            else:
                for i in range(341):
                    self.widg_box_viewers.layout.top = str(i) + 'px'
                self.widg_box_utils.layout.bottom = '400px'
                self.widg_box_utils.layout.visibility = 'visible'
        else:
            if self.widg_box_utils.layout.visibility == 'visible':
                self.widg_box_utils.layout.visibility = 'hidden'
            else:
                self.widg_box_utils.layout.visibility = 'visible'

    def handle_markers_size_change(self, change):
        self.marker_size = int(change.new)
        marker_style_updates(self)        
        batch_update(self)


    def handle_cross_size_change(self, change):
        self.cross_size = int(change.new)
        marker_style_updates(self)        
        batch_update(self)


    def handle_trace_symbol_change(self, change):
        self.widg_markers_symbol.value = self.trace_symbol[str(change.new)]


    def handle_markers_symbol_change(self, change):
        name_trace = str(self.widg_trace_symbol.value)
        self.trace_symbol[name_trace] = change.new
        self.symbols[name_trace] = [str(change.new)] * len(self.df_trace_on_map[name_trace])
        marker_style_updates(self)        
        batch_update(self)


    def reset_button_clicked(self, button):

        self.widg_trace_symbol.value = 'circle'

        with self.fig.batch_update():
 
            for name_trace in self.trace_name:

                self.trace_symbol[name_trace] = 'circle'
                self.symbols[name_trace] = ['circle'] * self.n_points[name_trace]
                self.sizes[name_trace] = [self.marker_size] * self.n_points[name_trace]
                self.trace[name_trace].marker.symbol = self.symbols[name_trace]
                self.trace[name_trace].marker.size = self.sizes[name_trace]


    def handle_width_hull_change(self, change):
        batch_update(self)
        
    def handle_color_hull_change(self, change):
        batch_update(self)
        
    def handle_style_hull_change(self, change):
        batch_update(self)

    def handle_width_line_change(self, change):
        batch_update(self)
        
    def handle_color_line_change(self, change):
        batch_update(self)
        
    def handle_style_line_change(self, change):
        batch_update(self)


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


    def bgcolor_update_button_clicked(self, button):
        if (self.widg_bgcolor.value=='Default' or self.widg_bgcolor.value=='default' ):
                self.fig.update_layout(
                    plot_bgcolor=self.bg_color_default,
                    xaxis=dict(gridcolor='white'),
                    yaxis=dict(gridcolor='white')
                     )
                self.bg_color = self.bg_color_default
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


    def display_button_l_clicked(self, button):

        # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
        if self.widg_compound_text_r.value in self.df['Structure']:

            compound_l = self.widg_compound_text_l.value
            structure_l = self.df['Structure'].at[compound_l]

            view_structure_l(self, compound_l)

            fract_change_updates(self)
            marker_style_updates(self)        
            batch_update(self)            

    def display_button_r_clicked(self, button):

        # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
        if self.widg_compound_text_r.value in self.df['Structure']:

            compound_r = self.widg_compound_text_r.value
            structure_r = self.df['Structure'].at[compound_r]

            view_structure_r(self, compound_r)

            update_df_on_map(self)
            fract_change_updates(self)
            marker_style_updates(self)        
            batch_update(self)            
