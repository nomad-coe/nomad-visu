import ipywidgets as widgets

def instantiate_widgets(self, Figure):

    self.widg_description = widgets.Label(
        value="Tick the box next to the cross symbols in order to choose which windows visualizes the next "
        "structure selected in the map above."
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
        options=self.font_colors,
        description="Font color",
        value="Black",
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_trace_symbol = widgets.Dropdown(
        options=Figure.name_traces,
        description="Classes",
        value=Figure.name_traces[0],
        layout=widgets.Layout(left="30px", width="200px"),
    )
    self.widg_markers_symbol = widgets.Dropdown(
        options=self.symbols_list,
        description="--- symbol",
        value=Figure.trace_symbol[Figure.name_traces[0]],
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