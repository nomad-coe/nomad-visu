from .configWidgets import ConfigWidgets
from .include._batch_update import batch_update
from .include._updates import marker_style_updates, fract_change_updates
import ipywidgets as widgets
from IPython.display import display, Markdown, FileLink
import os

class UtilsWidgets(ConfigWidgets):
    def __init__(self, Figure):

        self.widg_description = widgets.Label(
            value="Tick the box next to the cross symbols in order to choose which windows visualizes the next "
            "structure selected in the map above."
        )
        self.widg_markers_size = widgets.BoundedIntText(
            placeholder=str(ConfigWidgets.marker_size),
            description="Marker size",
            value=str(ConfigWidgets.marker_size),
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_cross_size = widgets.BoundedIntText(
            placeholder=str(ConfigWidgets.cross_size),
            description="Cross size",
            value=str(ConfigWidgets.cross_size),
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_color_palette = widgets.Dropdown(
            options=ConfigWidgets.discrete_palette_colors,
            description="Color palette",
            value=ConfigWidgets.discrete_palette_colors[0],
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_font_size = widgets.BoundedIntText(
            placeholder=str(ConfigWidgets.font_size),
            description="Font size",
            value=str(ConfigWidgets.font_size),
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_font_family = widgets.Dropdown(
            options=ConfigWidgets.font_families,
            description="Font family",
            value=ConfigWidgets.font_families[0],
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_font_color = widgets.Dropdown(
            options=ConfigWidgets.font_colors,
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
            options=ConfigWidgets.symbols_list,
            description="--- symbol",
            value=Figure.trace_symbol[Figure.name_traces[0]],
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_reset_button = widgets.Button(
            description="Reset symbols", layout=widgets.Layout(left="50px", width="200px")
        )
        self.widg_color_hull = widgets.Dropdown(
            options=ConfigWidgets.color_hull,
            description="Hull color",
            value=ConfigWidgets.hull_color,
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_width_hull = widgets.BoundedIntText(
            description="Hull width",
            value=str(ConfigWidgets.hull_width),
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_dash_hull = widgets.Dropdown(
            options=ConfigWidgets.hull_dashs,
            description="Hull dash",
            value=ConfigWidgets.hull_dash,
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_color_line = widgets.Dropdown(
            options=ConfigWidgets.color_line,
            description="Line color",
            value=ConfigWidgets.line_color,
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_width_line = widgets.BoundedIntText(
            description="Line width",
            value=ConfigWidgets.line_width,
            layout=widgets.Layout(left="30px", width="200px"),
        )
        self.widg_dash_line = widgets.Dropdown(
            options=ConfigWidgets.line_dashs,
            description="Line dash",
            value=ConfigWidgets.line_dash,
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
        def handle_font_family_change( change):
            """
            changes font family
            """
            ConfigWidgets.font_family = change.new
            batch_update(Figure, self)


        def handle_font_size_change( change):
            """
            changes font size
            """
            ConfigWidgets.font_size = change.new
            batch_update(Figure, self)


        def handle_font_color_change( change):
            """
            changes font color
            """
            ConfigWidgets.font_color = change.new
            batch_update(Figure, self)


        def handle_colorpalette_change(change):
            """
            change color palette used to distinguish different traces
            """

            ConfigWidgets.color_palette = change.new
            marker_style_updates(Figure)
            batch_update(Figure, self)


        def handle_markers_size_change(change):
            """
            change markers size
            """

            ConfigWidgets.marker_size = int(change.new)
            batch_update(Figure, self)


        def handle_cross_size_change(change):
            """
            change cross size
            """

            ConfigWidgets.cross_size = int(change.new)
            batch_update(Figure, self)


        def handle_trace_symbol_change(change):
            """
            change selected trace for marker symbol change
            """
            self.widg_markers_symbol.value = Figure.trace_symbol[str(change.new)]


        def handle_markers_symbol_change( change ) :
            """
            change marker symbol for trace
            """
            name_trace = str(self.widg_trace_symbol.value)
            Figure.trace_symbol[name_trace] = change.new
            Figure.symbols[name_trace] = [str(change.new)] * len(
                Figure.df_trace_on_map[name_trace]
            )
            batch_update(Figure, self)

        def reset_button_clicked( button ):
            """
            reset all marker sizes
            """

            self.widg_markers_symbol.value = "circle"
            for name_trace in Figure.name_traces:
                name_trace = str(name_trace)
                Figure.trace_symbol[name_trace] = "circle"
                Figure.symbols[name_trace] = ["circle"] * Figure.n_points[name_trace]
                Figure.sizes[name_trace] = [ConfigWidgets.marker_size] * Figure.n_points[name_trace]

            batch_update(Figure, self)


        def handle_width_hull_change( change ):
            """
            change width hull
            """
            ConfigWidgets.hull_width = change.new
            batch_update(Figure, self)


        def handle_color_hull_change( change ):
            """
            change hull color
            """
            ConfigWidgets.hull_color = change.new
            batch_update(Figure, self)


        def handle_dash_hull_change( change ):
            """
            cange hull dash
            """
            ConfigWidgets.hull_dash = change.new
            batch_update(Figure, self)


        def handle_width_line_change( change ):
            """
            change line width
            """
            ConfigWidgets.line_width = change.new
            batch_update(Figure, self)


        def handle_color_line_change( change ):
            """
            change line color
            """
            ConfigWidgets.line_color = change.new
            batch_update(Figure, self)


        def handle_dash_line_change( change):
            """
            change line dash
            """
            ConfigWidgets.line_dash = change.new
            batch_update(Figure, self)


        def bgtoggle_button_clicked( button):
            """
            switch color of the background
            """
            if ConfigWidgets.bg_toggle:
                ConfigWidgets.bg_toggle = False
            else:
                ConfigWidgets.bg_toggle = True
            batch_update(Figure, self)


        def bgcolor_update_button_clicked(button):
            """
            update color of the background
            """
            if self.widg_bgcolor.value == "Default" or self.widg_bgcolor.value == "default":
                ConfigWidgets.bg_color = ConfigWidgets.bg_color_default
                ConfigWidgets.bg_toggle = True
            else:
                try:
                    Figure.FigureWidget.update_layout(
                        plot_bgcolor=self.widg_bgcolor.value,
                        xaxis=dict(gridcolor="white"),
                        yaxis=dict(gridcolor="white"),
                    )
                    ConfigWidgets.bg_color = self.widg_bgcolor.value
                    ConfigWidgets.bg_toggle = True
                except:
                    pass
            batch_update(Figure, self)


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


        def observe_widgets(self):


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

        observe_widgets(self)




    def container(self):
        return self.widg_box_utils

