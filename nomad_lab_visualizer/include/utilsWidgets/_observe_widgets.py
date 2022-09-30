from ...configWidgets import ConfigWidgets

def observe_widgets(self, Figure): 

    def handle_font_family_change( change):
        """
        changes font family
        """
        ConfigWidgets.font_family = change.new
        Figure.batch_update(self)


    def handle_font_size_change( change):
        """
        changes font size
        """
        ConfigWidgets.font_size = change.new
        Figure.batch_update(self)


    def handle_font_color_change( change):
        """
        changes font color
        """
        ConfigWidgets.font_color = change.new
        Figure.batch_update(self)


    def handle_colorpalette_change(change):
        """
        change color palette used to distinguish different traces
        """

        ConfigWidgets.color_palette = change.new
        Figure.batch_update(self)


    def handle_markers_size_change(change):
        """
        change markers size
        """

        ConfigWidgets.marker_size = int(change.new)
        Figure.batch_update(self)


    def handle_cross_size_change(change):
        """
        change cross size
        """

        ConfigWidgets.cross_size = int(change.new)
        Figure.batch_update(self)


    def handle_trace_symbol_change(change):
        """
        change selected trace for marker symbol change
        """
        ConfigWidgets.widg_markers_symbol.value = Figure.trace_symbol[str(change.new)]


    def handle_markers_symbol_change( change ) :
        """
        change marker symbol for trace
        """
        name_trace = str(self.widg_trace_symbol.value)
        Figure.trace_symbol[name_trace] = change.new
        Figure.symbols[name_trace] = [str(change.new)] * len(
            Figure.df_trace_on_map[name_trace]
        )
        Figure.batch_update(self)

    def reset_button_clicked( button ):
        """
        reset all marker sizes
        """

        self.widg_markers_symbol.value = "circle"
        for name_trace in Figure.name_traces:
            n_points = int(
                ConfigWidgets.fract * \
                Figure.df.loc[Figure.df[Figure.target] == name_trace].shape[0]
                )
            name_trace = str(name_trace)
            Figure.trace_symbol[name_trace] = "circle"
            Figure.symbols[name_trace] = ["circle"] * n_points
            Figure.sizes[name_trace] = [self.marker_size] * n_points

        Figure.batch_update(self)


    def handle_width_hull_change( change ):
        """
        change width hull
        """
        ConfigWidgets.hull_width = change.new
        Figure.batch_update(self)


    def handle_color_hull_change( change ):
        """
        change hull color
        """
        ConfigWidgets.hull_color = change.new
        Figure.batch_update(self)


    def handle_dash_hull_change( change ):
        """
        cange hull dash
        """
        ConfigWidgets.hull_dash = change.new
        Figure.batch_update(self)


    def handle_width_line_change( change ):
        """
        change line width
        """
        ConfigWidgets.line_width = change.new
        Figure.batch_update(self)


    def handle_color_line_change( change ):
        """
        change line color
        """
        ConfigWidgets.line_color = change.new
        Figure.batch_update(self)


    def handle_dash_line_change( change):
        """
        change line dash
        """
        ConfigWidgets.line_dash = change.new
        Figure.batch_update(self)


    def bgtoggle_button_clicked( button):
        """
        switch color of the background
        """
        if self.bg_toggle:
            self.bg_toggle = False
        else:
            self.bg_toggle = True
        Figure.batch_update(self)


    def bgcolor_update_button_clicked(button):
        """
        update color of the background
        """
        if self.widg_bgcolor.value == "Default" or self.widg_bgcolor.value == "default":
            self.bg_color = self.bg_color_default
            self.bg_toggle = True
        else:
            try:
                Figure.FigureWidget.update_layout(
                    plot_bgcolor=self.widg_bgcolor.value,
                    xaxis=dict(gridcolor="white"),
                    yaxis=dict(gridcolor="white"),
                )
                self.bg_color = self.widg_bgcolor.value
                self.bg_toggle = True
            except:
                pass
        Figure.batch_update(self)


    def print_button_clicked( button):
        """
        print map
        """

        self.widg_print_out.clear_output()
        text = "A download link will appear soon."
        with self.widg_print_out:
            display(Markdown(text))
        path = "./"
        try:
            os.mkdir(path)
        except:
            pass
        file_name = self.widg_plot_name.value + "." + self.widg_plot_format.value
        Figure.FigureWidget.write_image(path + file_name, scale=self.widg_resolution.value)
        self.widg_print_out.clear_output()
        with self.widg_print_out:
            local_file = FileLink(
                path + file_name, result_html_prefix="Click here to download: "
            )
            display(local_file)




    self.widg_reset_button.on_click(reset_button_clicked)
    self.widg_bgcolor_update_button.on_click(bgcolor_update_button_clicked)
    self.widg_print_button.on_click(print_button_clicked)
    self.widg_bgtoggle_button.on_click(bgtoggle_button_clicked)
    self.widg_color_palette.observe(handle_colorpalette_change, names="value")

    self.widg_width_hull.observe(handle_width_hull_change, names="value")
    self.widg_dash_hull.observe(handle_dash_hull_change, names="value")
    self.widg_color_hull.observe(handle_color_hull_change, names="value")
    self.widg_width_line.observe(handle_width_line_change, names="value")
    self.widg_dash_line.observe(handle_dash_line_change, names="value")
    self.widg_color_line.observe(handle_color_line_change, names="value")
    self.widg_trace_symbol.observe(handle_trace_symbol_change, names="value")
    self.widg_markers_symbol.observe(
        handle_markers_symbol_change, names="value"
    )
    self.widg_markers_size.observe(handle_markers_size_change, names="value")
    self.widg_cross_size.observe(handle_cross_size_change, names="value")
    self.widg_font_family.observe(handle_font_family_change, names="value")
    self.widg_font_size.observe(handle_font_size_change, names="value")
    self.widg_font_color.observe(handle_font_color_change, names="value")
