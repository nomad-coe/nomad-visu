import ipywidgets as widgets


def instantiate_widgets(self):

    self.widg_update_frac_button = widgets.Button(
        description='Click to update',
        layout=widgets.Layout(width='150px', left='130px')
    )
    self.widg_frac_slider = widgets.BoundedFloatText(
        min=0,
        max=1,
        step=0.01,
        value=self.frac,
        layout=widgets.Layout(left='130px', width='60px')
    )
    self.widg_label_frac = widgets.Label(
        value='Fraction of compounds visualized in the map: ',
        layout=widgets.Layout(left='130px')
    )
    self.widg_featx = widgets.Dropdown(
        description='x-axis',
        options=self.embedding_features,
        value=self.feat_x
    )
    self.widg_featy = widgets.Dropdown(
        description='y-axis',
        options=self.embedding_features,
        value=self.feat_y
    )
    self.widg_featmarker = widgets.Dropdown(
        description="Marker",
        options=['default size'] + self.hover_features,
        value='default size',
    )
    self.widg_featcolor = widgets.Dropdown(
        description='Color',
        options=['default color'] + self.hover_features,
        value='default color'
    )
    self.widg_gradient = widgets.Dropdown(
        disabled=True,
        description='-gradient',
        options=self.gradient_list,
        value='Grey scale',
        layout=widgets.Layout(width='150px', right='20px')
    )
    self.widg_compound_text_l = widgets.Combobox(
        placeholder='...',
        description='Compound:',
        options=self.compounds_list,
        # disabled=False,
        layout=widgets.Layout(width='200px')
    )
    self.widg_compound_text_r = widgets.Combobox(
        placeholder='...',
        description='Compound:',
        options=self.compounds_list,
        # disabled=False,
        layout=widgets.Layout(width='200px')
    )
    self.widg_display_button_l = widgets.Button(
        description="Display",
        layout=widgets.Layout(width='100px')
    )
    self.widg_display_button_r = widgets.Button(
        description="Display",
        layout=widgets.Layout(width='100px')
    )
    self.widg_checkbox_l = widgets.Checkbox(
        value=True,
        indent=False,
        layout=widgets.Layout(width='50px')
    )
    self.widg_checkbox_r = widgets.Checkbox(
        value=False,
        indent=False,
        layout=widgets.Layout(width='50px'),
    )
    self.widg_markersize = widgets.BoundedIntText(
        placeholder=str(self.marker_size),
        description='Marker size',
        value=str(self.marker_size),
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_crosssize = widgets.BoundedIntText(
        placeholder=str(self.cross_size),
        description='Cross size',
        value=str(self.cross_size),
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_fontsize = widgets.BoundedIntText(
        placeholder=str(self.font_size),
        description='Font size',
        value=str(self.font_size),
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_fontcolor = widgets.Dropdown(
        options=self.font_color,
        description='Font color',
        value='Black',
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_fontfamily = widgets.Dropdown(
        options=self.font_families,
        description='Font family',
        value=self.font_families[0],
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_width_line = widgets.BoundedIntText(
        placeholder=str(self.width_line),
        description='Line width',
        value=str(self.width_line),
        layout = widgets.Layout(left='30px', width='200px')
    )
    self.widg_style_line = widgets.Dropdown(
        options=self.line_styles,
        description='Line style',
        value='solid',
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_color_line = widgets.Dropdown(
        options=self.color_line,
        description='Line color',
        value='Grey',
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_width_hull = widgets.BoundedIntText(
        placeholder=str(self.width_hull),
        description='Hull width',
        value=str(self.width_hull),
        layout = widgets.Layout(left='30px', width='200px')
    )
    self.widg_style_hull = widgets.Dropdown(
        options=self.line_styles,
        description='Hull style',
        value='dash',
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_color_hull = widgets.Dropdown(
        options=self.color_hull,
        description='Hull color',
        value='Black',
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_colorpalette = widgets.Dropdown(
        options=self.qualitative_colors,
        description='Color palette',
        value=self.qualitative_colors[0],
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_classes_symbol = widgets.Dropdown(
        options=self.classes,
        description='Classes',
        value=self.classes[0],
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_symbols = widgets.Dropdown(
        options=self.symbols_list,
        description='-- symbol',
        value=self.class_symbol['Class ' + str(self.classes[0])],
        layout=widgets.Layout(left='30px', width='200px')
    )
    self.widg_bgcolor = widgets.Text(
        placeholder=str('Default'),
        description='Color',
        value=str('Default'),
        layout=widgets.Layout(left='30px', width='200px'),
    )
    self.widg_bgtoggle_button = widgets.Button(
        description='Toggle on/off background',
        layout=widgets.Layout(left='50px', width='200px'),
    )
    self.widg_bgcolor_update_button = widgets.Button(
        description='Update background color',
        layout=widgets.Layout(left='50px', width='200px')
    )    
    self.widg_reset_button = widgets.Button(
        description='Reset symbols',
        layout=widgets.Layout(left='50px', width='200px')
    )
    self.widg_plot_name = widgets.Text(
        placeholder='plot',
        value='plot',
        description='Name',
        layout=widgets.Layout(width='300px')
    )
    self.widg_plot_format = widgets.Text(
        placeholder='png',
        value='png',
        description='Format',
        layout=widgets.Layout(width='150px')
    )
    self.widg_scale = widgets.Text(
        placeholder='1',
        value='1',
        description="Scale",
        layout=widgets.Layout(width='150px')
    )
    self.widg_print_button = widgets.Button(
        description='Print',
        layout=widgets.Layout(left='50px', width='600px')
    )
    self.widg_print_out = widgets.Output(
        layout=widgets.Layout(left='150px', width='400px')
    )
    self.widg_printdescription = widgets.Label(
        value="Click 'Print' to export the plot in the desired format.",
        layout=widgets.Layout(left='50px', width='640px')
    )
    self.widg_printdescription2 = widgets.Label(
        value="The resolution of the image can be increased by increasing the 'Scale' value.",
        layout=widgets.Layout(left='50px', width='640px')
    )
    self.widg_featuredescription = widgets.Label(
        value="The dropdown menus select the features to visualize."
    )
    self.widg_description = widgets.Label(
        value='Tick the box next to the cross symbols in order to choose which windows visualizes the next '
              'structure selected in the map above.'
    )
    self.widg_colordescription = widgets.Label(
        value='Colors in the boxes below can be written as a text string, i.e. red, '
              'green,...,  or in a rgb/a, hex format. ',
        layout=widgets.Layout(left='50px', width='640px')

    )
    self.widg_colordescription2 = widgets.Label(
        value="After modifying a specific field, click on the 'Update colors' button to display the changes in "
              "the plot.",
        layout=widgets.Layout(left='50px', width='640px')
    )
    self.widg_plotutils_button = widgets.Button(
        description='For a high-quality print of the plot, click to access the plot appearance utils',
        layout=widgets.Layout(width='600px')
    )
    self.widg_box_utils = widgets.VBox([widgets.HBox([self.widg_markersize, self.widg_crosssize, self.widg_colorpalette]),

                                        widgets.HBox([self.widg_fontsize, self.widg_fontfamily, self.widg_fontcolor]),
                                        widgets.HBox([self.widg_classes_symbol, self.widg_symbols, self.widg_reset_button]),

                                        self.widg_colordescription, self.widg_colordescription2,
                                        widgets.HBox([self.widg_color_hull, self.widg_width_hull, self.widg_style_hull ]),
                                        widgets.HBox([self.widg_color_line, self.widg_width_line, self.widg_style_line ]),
                                        widgets.HBox([self.widg_bgtoggle_button, self.widg_bgcolor,
                                                      self.widg_bgcolor_update_button]),
                                        self.widg_printdescription, self.widg_printdescription2,
                                        widgets.HBox([self.widg_plot_name, self.widg_plot_format, self.widg_scale]),
                                        self.widg_print_button, self.widg_print_out,
                                        ])

    file1 = open("./assets/cross.png", "rb")
    image1 = file1.read()
    self.widg_img1 = widgets.Image(
        value=image1,
        format='png',
        width=30,
        height=30,
    )
    file2 = open("./assets/cross2.png", "rb")
    image2 = file2.read()
    self.widg_img2 = widgets.Image(
        value=image2,
        format='png',
        width=30,
        height=30,
    )
    self.output_l = widgets.Output()
    self.output_r = widgets.Output()

    self.box_feat = widgets.VBox([
        widgets.HBox([
            widgets.VBox([self.widg_featx, self.widg_featy]),
            widgets.VBox([self.widg_featmarker,
                          widgets.HBox([self.widg_featcolor, self.widg_gradient])
                          ]),
        ]),
        widgets.HBox([self.widg_label_frac, self.widg_frac_slider, self.widg_update_frac_button]),

    ])

    self.widg_box_viewers = widgets.VBox([self.widg_description, widgets.HBox([
        widgets.VBox([
            widgets.HBox([self.widg_compound_text_l, self.widg_display_button_l,
                          self.widg_img1, self.widg_checkbox_l]),
            self.output_l]),
        widgets.VBox(
            [widgets.HBox([self.widg_compound_text_r, self.widg_display_button_r,
                           self.widg_img2, self.widg_checkbox_r]),
             self.output_r])
    ])])
