import ipywidgets as widgets
import plotly.express as px


class SettingsWidget(widgets.GridspecLayout):
    def __init__(
        self,
        embedding_features,
        hover_features,
        feature_x,
        feature_y,
        fracture,
        **kwargs
    ):
        super().__init__(3, 3)

        widget_feature_x = widgets.Dropdown(
            description="x-axis",
            options=embedding_features,
            value=feature_x,
            layout=widgets.Layout(width="250px"),
        )

        widget_feature_y = widgets.Dropdown(
            description="y-axis",
            options=embedding_features,
            value=feature_y,
            layout=widgets.Layout(width="250px"),
        )

        widget_fracture = widgets.BoundedFloatText(
            min=0,
            max=1.0,
            # step=0.01,
            value=fracture,
            layout=widgets.Layout(left="98px", width="60px"),
        )

        widget_facture_label = widgets.Label(
            value="Fraction: ", layout=widgets.Layout(left="95px")
        )

        widget_feature_color = widgets.Dropdown(
            description="Color",
            options=["Default color"] + hover_features,
            value="Default color",
            layout=widgets.Layout(width="250px"),
        )

        widget_feature_color_type = widgets.RadioButtons(
            options=["Gradient", "Discrete"],
            value="Gradient",
            layout=widgets.Layout(width="140px", left="90px"),
        )

        widget_feature_color_list = widgets.Dropdown(
            options=px.colors.named_colorscales(),
            value="viridis",
            layout=widgets.Layout(width="65px", height="35px", left="40px"),
        )

        widget_feature_marker = widgets.Dropdown(
            description="Marker",
            options=["Default size"] + hover_features,
            value="Default size",
            layout=widgets.Layout(width="250px"),
        )
        widget_feature_marker_minvalue = widgets.BoundedFloatText(
            min=0,
            # max=self.max_value_markerfeat,
            step=1,
            # value=self.min_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px", height="10px"),
        )
        widget_feature_marker_minvalue_label = widgets.Label(
            value="Min value: ", layout=widgets.Layout(left="94px", width="70px")
        )
        widget_feature_marker_maxvalue = widgets.BoundedFloatText(
            # min=self.min_value_markerfeat,
            step=1,
            # value=self.max_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px"),
        )
        widget_feature_marker_maxvalue_label = widgets.Label(
            value="Max value: ", layout=widgets.Layout(left="94px", width="70px")
        )

        self[0, 0] = widget_feature_x
        self[1, 0] = widget_feature_y
        self[2, 0] = widgets.Box([widget_facture_label, widget_fracture])

        self[0, 1] = widget_feature_color
        self[1:, 1] = widgets.HBox(
            [widget_feature_color_type, widget_feature_color_list],
            layout=widgets.Layout(top="10px"),
        )

        self[0, 2] = widget_feature_marker
        self[1, 2] = widgets.Box(
            [
                widget_feature_marker_minvalue_label,
                widget_feature_marker_minvalue,
            ]
        )

        self[2, 2] = widgets.Box(
            [
                widget_feature_marker_maxvalue_label,
                widget_feature_marker_maxvalue,
            ]
        )

        self.layout.height = "140px"
        # self.layout.top = "30px"


# class SettingsListWidget(widgets.Box):
#     def __init__(
#         self,
#         embedding_features,
#         hover_features,
#         feature_x,
#         feature_y,
#         fracture,
#         config,
#         **kwargs
#     ):
#         widget_feature_x = widgets.Dropdown(
#             description="x-axis",
#             options=embedding_features,
#             value=feature_x,
#             layout=widgets.Layout(width="250px"),
#         )
#
#         widget_feature_y = widgets.Dropdown(
#             description="y-axis",
#             options=embedding_features,
#             value=feature_y,
#             layout=widgets.Layout(width="250px"),
#         )
#
#         widget_fracture = widgets.BoundedFloatText(
#             min=0,
#             max=1.0,
#             # step=0.01,
#             value=fracture,
#             layout=widgets.Layout(left="98px", width="60px"),
#         )
#
#         widget_feature_color = widgets.Dropdown(
#             description="Color",
#             options=["Default color"] + hover_features,
#             value="Default color",
#             layout=widgets.Layout(width="250px"),
#         )
#
#         widget_feature_color_type = widgets.RadioButtons(
#             options=["Gradient", "Discrete"],
#             value="Gradient",
#             layout=widgets.Layout(width="140px", left="90px"),
#         )
#
#         widget_feature_color_list = widgets.Dropdown(
#             options=px.colors.named_colorscales(),
#             value="viridis",
#             layout=widgets.Layout(width="65px", height="35px", left="40px"),
#         )
#
#         widget_feature_marker = widgets.Dropdown(
#             description="Marker",
#             options=["Default size"] + hover_features,
#             value="Default size",
#             layout=widgets.Layout(width="250px"),
#         )
#         widget_feature_marker_minvalue = widgets.BoundedFloatText(
#             min=0,
#             # max=self.max_value_markerfeat,
#             step=1,
#             # value=self.min_value_markerfeat,
#             layout=widgets.Layout(left="91px", width="60px", height="10px"),
#         )
#         widget_feature_marker_minvalue_label = widgets.Label(
#             value="Min value: ", layout=widgets.Layout(left="94px", width="70px")
#         )
#         widget_feature_marker_maxvalue = widgets.BoundedFloatText(
#             # min=self.min_value_markerfeat,
#             step=1,
#             # value=self.max_value_markerfeat,
#             layout=widgets.Layout(left="91px", width="60px"),
#         )
#         widget_feature_marker_maxvalue_label = widgets.Label(
#             value="Max value: ", layout=widgets.Layout(left="94px", width="70px")
#         )
#         super().__init__(
#             children=[
#                 widget_feature_x,
#                 widget_feature_y,
#                 widgets.Box(
#                     [
#                         widgets.Label(
#                             value="Fraction: ", layout=widgets.Layout(left="95px")
#                         ),
#                         widget_fracture,
#                     ]
#                 ),
#                 widget_feature_color,
#                 widgets.HBox(
#                     [widget_feature_color_type, widget_feature_color_list],
#                     layout=widgets.Layout(top="10px"),
#                 ),
#                 widget_feature_marker,
#                 widgets.Box(
#                     [
#                         widget_feature_marker_minvalue_label,
#                         widget_feature_marker_minvalue,
#                     ]
#                 ),
#                 widgets.Box(
#                     [
#                         widget_feature_marker_maxvalue_label,
#                         widget_feature_marker_maxvalue,
#                     ]
#                 ),
#             ],
#             layout=widgets.Layout(
#                 display="flex",
#                 flex_flow="column",
#                 border="solid 2px",
#                 align_items="stretch",
#                 # width="50%",
#             ),
#         )
#         # self.layout.height = "140px"
#         # self.layout.top = "30px"
