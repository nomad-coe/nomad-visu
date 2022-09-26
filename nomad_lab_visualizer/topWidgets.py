from .configWidgets import ConfigWidgets
from .include._batch_update import batch_update
from .include._updates import marker_style_updates, fract_change_updates
import ipywidgets as widgets

class TopWidgets(ConfigWidgets):
    def __init__(self, Figure):

        self.widg_featx = widgets.Dropdown(
            description="x-axis",
            options=ConfigWidgets.embedding_features,
            value=ConfigWidgets.feat_x,
            layout=widgets.Layout(width="250px"),
        )
        self.widg_featy = widgets.Dropdown(
            description="y-axis",
            options=ConfigWidgets.embedding_features,
            value=ConfigWidgets.feat_y,
            layout=widgets.Layout(width="250px"),
        )
        self.widg_fract_slider = widgets.BoundedFloatText(
            min=0,
            max=1,
            step=0.01,
            value=ConfigWidgets.fract,
            layout=widgets.Layout(left="98px", width="60px"),
        )
        self.widg_label_fract = widgets.Label(
            value="Fraction: ", 
            layout=widgets.Layout(left="95px")
        )
        self.widg_featcolor = widgets.Dropdown(
            description="Color",
            options=["Default color"] + ConfigWidgets.hover_features,
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
            options=ConfigWidgets.continuous_gradient_colors,
            value="viridis",
            layout=widgets.Layout(width="65px", height="35px", left="40px"),
        )
        self.widg_featmarker = widgets.Dropdown(
            description="Marker",
            options=["Default size"] + ConfigWidgets.hover_features,
            value="Default size",
            layout=widgets.Layout(width="250px"),
        )
        self.widg_featmarker_minvalue = widgets.BoundedFloatText(
            min=0,
            max=ConfigWidgets.max_value_markerfeat,
            step=1,
            value=ConfigWidgets.min_value_markerfeat,
            disabled=True,
            layout=widgets.Layout(left="91px", width="60px", height="10px"),
        )
        self.widg_featmarker_minvalue_label = widgets.Label(
            value="Min value: ", 
            layout=widgets.Layout(left="94px", width="70px")
        )
        self.widg_featmarker_maxvalue = widgets.BoundedFloatText(
            min=ConfigWidgets.min_value_markerfeat,
            step=1,
            value=ConfigWidgets.max_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px"),
            disabled=True,
        )
        self.widg_featmarker_maxvalue_label = widgets.Label(
            value="Max value: ", 
            layout=widgets.Layout(left="94px", width="70px")
        )

        def handle_xfeat_change(change):
            """
            changes the feature plotted on the x-axis
            """

            ConfigWidgets.feat_x = change.new
            if ConfigWidgets.feat_x != ConfigWidgets.feat_y and Figure.smart_fract:
                ConfigWidgets.fract = Figure.fract_thres[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)]
                self.widg_fract_slider.value = self.fract

            batch_update(Figure, self)

        def handle_yfeat_change(change):
            """
            changes the feature plotted on the y-axis
            """

            ConfigWidgets.feat_y = change.new
            if ConfigWidgets.feat_x != ConfigWidgets.feat_y and Figure.smart_fract:
                ConfigWidgets.fract = Figure.fract_thres[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)]
                self.widg_fract_slider.value = ConfigWidgets.fract

            batch_update(Figure, self)

        def handle_fract_change(change):
            """
            changes the fraction visualized
            """

            ConfigWidgets.fract = change.new
            batch_update(Figure, self)

        def handle_colorfeat_change(change):
            """
            changes markers color according to a specific feature
            """

            ConfigWidgets.featcolor = change.new

            if change.new == "Default color":
                self.widg_featcolor_type.disabled = True
                self.widg_featcolor_list.disabled = True
                # self.widg_color_palette.disabled = False
            else:
                self.widg_featcolor_type.disabled = False
                self.widg_featcolor_list.disabled = False
                # self.widg_color_palette.disabled = True
            batch_update(Figure, self)

        def handle_featcolor_list_change(change):
            """
            changes the color that is used for markers
            """
            
            ConfigWidgets.featcolor_list = change.new
            batch_update(Figure, ConfigWidgets)

        def handle_featcolor_type_change(change):
            """
            changes the type of markers coloring
            """

            ConfigWidgets.featcolor_type = change.new

            if change.new == "Gradient":
                self.widg_featcolor_list.options = ConfigWidgets.continuous_gradient_colors
                ConfigWidgets.featcolor_list = "viridis"
                self.widg_featcolor_list.value = "viridis"
            if change.new == "Discrete":
                self.widg_featcolor_list.options = ConfigWidgets.discrete_palette_colors
                ConfigWidgets.featcolor_list = "Plotly"
                self.widg_featcolor_list.value = "Plotly"

            batch_update(Figure, ConfigWidgets)

        def handle_markerfeat_change(change):
            """
            change markers size according to a specific feature
            """

            if change.new == "Default size":
                self.widg_featmarker_maxvalue.disabled = True
                self.widg_featmarker_minvalue.disabled = True
                # self.widg_markers_size.disabled = False
                # self.widg_cross_size.disabled = False
            else:
                self.widg_featmarker_maxvalue.disabled = False
                self.widg_featmarker_minvalue.disabled = False
                # self.widg_markers_size.disabled = True
                # self.widg_cross_size.disabled = True

            ConfigWidgets.featmarker = change.new
            batch_update(Figure, self)

        def handle_featmarker_maxvalue_change(change):
            """
            changes the max value of the markers size
            """

            ConfigWidgets.max_value_markerfeat = change.new
            self.widg_featmarker_minvalue.max = change.new
            batch_update(Figure, self)

        def handle_featmarker_minvalue_change(change):
            """
            changes the min value of the markers size
            """

            ConfigWidgets.min_value_markerfeat = change.new
            self.widg_featmarker_maxvalue.min = change.new
            batch_update(Figure, self)


        def observe_widgets(self): 

            self.widg_featx.observe(handle_xfeat_change, names="value")
            self.widg_featy.observe(handle_yfeat_change, names="value")
            self.widg_fract_slider.observe(handle_fract_change, names='value')
            self.widg_featmarker.observe(handle_markerfeat_change, names="value")
            self.widg_featcolor.observe(handle_colorfeat_change, names="value")
            self.widg_featcolor_list.observe(
                handle_featcolor_list_change, names="value"
            )
            self.widg_featcolor_type.observe(
                handle_featcolor_type_change, names="value"
            )
            self.widg_featmarker_maxvalue.observe(
                handle_featmarker_maxvalue_change, names="value"
            )
            self.widg_featmarker_minvalue.observe(
                handle_featmarker_minvalue_change, names="value"
            )

        observe_widgets(self)

    def container(self):
        return widgets.VBox(
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