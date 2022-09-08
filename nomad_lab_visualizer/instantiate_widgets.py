import ipywidgets as widgets


def instantiate_widgets(self):
    """
    instantiate all widgets that are used to construct the visualizer
    """


    self.widg_featx = widgets.Dropdown(
        description="x-axis",
        options=self.embedding_features,
        value=self.feat_x,
        layout=widgets.Layout(width="250px"),
    )
    self.widg_featy = widgets.Dropdown(
        description="y-axis",
        options=self.embedding_features,
        value=self.feat_y,
        layout=widgets.Layout(width="250px"),
    )
    self.widg_fract_slider = widgets.BoundedFloatText(
        min=0,
        max=1,
        step=0.01,
        value=self.fract,
        layout=widgets.Layout(left="98px", width="60px"),
    )
    self.widg_label_fract = widgets.Label(
        value="Fraction: ", layout=widgets.Layout(left="95px")
    )
    self.widg_featcolor = widgets.Dropdown(
        description="Color",
        options=["Default color"] + self.hover_features,
        value="Default color",
        layout=widgets.Layout(width="250px"),
    )
    self.widg_featcolor_type = widgets.RadioButtons(
        options=["Gradient", "Discrete"],
        value="Gradient",
        layout=widgets.Layout(width="140px", left="90px"),
        disabled=True,
    )
    self.widg_featcolor_list = widgets.Dropdown(
        disabled=True,
        options=self.continuous_gradient_colors,
        value="viridis",
        layout=widgets.Layout(width="65px", height="35px", left="40px"),
    )
    self.widg_featmarker = widgets.Dropdown(
        description="Marker",
        options=["Default size"] + self.hover_features,
        value="Default size",
        layout=widgets.Layout(width="250px"),
    )
    self.widg_featmarker_minvalue = widgets.BoundedFloatText(
        min=0,
        max=self.max_value_markerfeat,
        step=1,
        value=self.min_value_markerfeat,
        disabled=True,
        layout=widgets.Layout(left="91px", width="60px", height="10px"),
    )
    self.widg_featmarker_minvalue_label = widgets.Label(
        value="Min value: ", layout=widgets.Layout(left="94px", width="70px")
    )
    self.widg_featmarker_maxvalue = widgets.BoundedFloatText(
        min=self.min_value_markerfeat,
        step=1,
        value=self.max_value_markerfeat,
        layout=widgets.Layout(left="91px", width="60px"),
        disabled=True,
    )
    self.widg_featmarker_maxvalue_label = widgets.Label(
        value="Max value: ", layout=widgets.Layout(left="94px", width="70px")
    )
    self.widg_utils_button = widgets.Button(
        description="For a high-quality print of the plot, click to access the plot appearance utils",
        layout=widgets.Layout(width="600px"),
    )
    self.widg_description = widgets.Label(
        value="Tick the box next to the cross symbols in order to choose which windows visualizes the next "
        "structure selected in the map above."
    )
    self.widg_structure_text_l = widgets.Combobox(
        placeholder="...",
        description="Structure:",
        options=self.structures_list,
        layout=widgets.Layout(width="200px"),
    )
    self.widg_display_button_l = widgets.Button(
        description="Display", layout=widgets.Layout(width="100px")
    )
    self.widg_checkbox_l = widgets.Checkbox(
        value=True, indent=False, layout=widgets.Layout(width="50px")
    )
    self.widg_structure_text_r = widgets.Combobox(
        placeholder="...",
        description="Structure:",
        options=self.structures_list,
        layout=widgets.Layout(width="200px"),
    )
    self.widg_display_button_r = widgets.Button(
        description="Display", layout=widgets.Layout(width="100px")
    )
    self.widg_checkbox_r = widgets.Checkbox(
        value=False,
        indent=False,
        layout=widgets.Layout(width="50px"),
    )

    self.widg_markers_size = widgets.BoundedIntText(
        placeholder=str(self.marker_size),
        description="Marker size",
        value=str(self.marker_size),
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_cross_size = widgets.BoundedIntText(
        placeholder=str(self.cross_size),
        description="Cross size",
        value=str(self.cross_size),
        layout=widgets.Layout(left="30px", width="200px"),
    )

    self.widg_color_palette = widgets.Dropdown(
        options=self.discrete_palette_colors,
        description="Color palette",
        value=self.discrete_palette_colors[0],
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_font_size = widgets.BoundedIntText(
        placeholder=str(self.font_size),
        description="Font size",
        value=str(self.font_size),
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_font_family = widgets.Dropdown(
        options=self.font_families,
        description="Font family",
        value=self.font_families[0],
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_font_color = widgets.Dropdown(
        options=self.font_color,
        description="Font color",
        value="Black",
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_trace_symbol = widgets.Dropdown(
        options=self.trace_name,
        description="Classes",
        value=self.trace_name[0],
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_markers_symbol = widgets.Dropdown(
        options=self.symbols_list,
        description="--- symbol",
        value=self.trace_symbol[self.trace_name[0]],
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_reset_button = widgets.Button(
        description="Reset symbols", layout=widgets.Layout(left="50px", width="200px")
    )

    self.widg_color_hull = widgets.Dropdown(
        options=self.color_hull,
        description="Hull color",
        value=self.hull_color,
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_width_hull = widgets.BoundedIntText(
        description="Hull width",
        value=str(self.hull_width),
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_dash_hull = widgets.Dropdown(
        options=self.hull_dashs,
        description="Hull dash",
        value=self.hull_dash,
        layout=widgets.Layout(left="30px", width="200px"),
    )

    self.widg_color_line = widgets.Dropdown(
        options=self.color_line,
        description="Line color",
        value=self.line_color,
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_width_line = widgets.BoundedIntText(
        description="Line width",
        value=self.line_width,
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_dash_line = widgets.Dropdown(
        options=self.line_dashs,
        description="Line dash",
        value=self.line_dash,
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_bgcolor = widgets.Text(
        placeholder=str("Default"),
        description="Color",
        value=str("Default"),
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_bgtoggle_button = widgets.Button(
        description="Toggle on/off background",
        layout=widgets.Layout(left="50px", width="200px"),
    )
    self.widg_bgcolor_update_button = widgets.Button(
        description="Update background color",
        layout=widgets.Layout(left="50px", width="200px"),
    )
    self.widg_print_description = widgets.Label(
        value="Click 'Print' to export the plot in the desired format and resolution.",
        layout=widgets.Layout(left="50px", width="640px"),
    )
    self.widg_plot_name = widgets.Text(
        placeholder="plot",
        value="plot",
        description="Name",
        layout=widgets.Layout(width="300px"),
    )
    self.widg_plot_format = widgets.Text(
        placeholder="png",
        value="png",
        description="Format",
        layout=widgets.Layout(width="150px"),
    )
    self.widg_resolution = widgets.Text(
        placeholder="1",
        value="1",
        description="Resolution",
        layout=widgets.Layout(width="150px"),
    )
    self.widg_print_button = widgets.Button(
        description="Print", layout=widgets.Layout(left="50px", width="600px")
    )
    self.widg_print_out = widgets.Output(
        layout=widgets.Layout(left="150px", width="400px")
    )

    self.widg_box_utils = widgets.VBox(
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

    import os
    import nomad_lab_visualizer

    file1 = open(
        os.path.join(nomad_lab_visualizer.__path__[0], "assets/cross1.png"), "rb"
    )
    image1 = file1.read()
    self.widg_img1 = widgets.Image(
        value=image1,
        format="png",
        width=30,
        height=30,
    )
    file2 = open(
        os.path.join(nomad_lab_visualizer.__path__[0], "assets/cross2.png"), "rb"
    )
    image2 = file2.read()
    self.widg_img2 = widgets.Image(
        value=image2,
        format="png",
        width=30,
        height=30,
    )
    self.output_l = widgets.Output()
    self.output_r = widgets.Output()

    self.box_feat = widgets.VBox(
        [
            widgets.HBox(
                [
                    widgets.VBox(
                        [
                            self.widg_featx,
                            self.widg_featy,
                            widgets.HBox(
                                [self.widg_label_fract, self.widg_fract_slider]
                            ),
                        ]
                    ),
                    widgets.VBox(
                        [
                            self.widg_featcolor,
                            widgets.HBox(
                                [self.widg_featcolor_type, self.widg_featcolor_list],
                                layout=widgets.Layout(top="10px"),
                            ),
                        ]
                    ),
                    widgets.VBox(
                        [
                            self.widg_featmarker,
                            widgets.VBox(
                                [
                                    widgets.HBox(
                                        [
                                            self.widg_featmarker_minvalue_label,
                                            self.widg_featmarker_minvalue,
                                        ],
                                    ),
                                    widgets.HBox(
                                        [
                                            self.widg_featmarker_maxvalue_label,
                                            self.widg_featmarker_maxvalue,
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )

    self.widg_box_viewers = widgets.VBox(
        [
            self.widg_description,
            widgets.HBox(
                [
                    widgets.VBox(
                        [
                            widgets.HBox(
                                [
                                    self.widg_structure_text_l,
                                    self.widg_display_button_l,
                                    self.widg_img1,
                                    self.widg_checkbox_l,
                                ]
                            ),
                            self.output_l,
                        ]
                    ),
                    widgets.VBox(
                        [
                            widgets.HBox(
                                [
                                    self.widg_structure_text_r,
                                    self.widg_display_button_r,
                                    self.widg_img2,
                                    self.widg_checkbox_r,
                                ]
                            ),
                            self.output_r,
                        ]
                    ),
                ]
            ),
        ]
    )
