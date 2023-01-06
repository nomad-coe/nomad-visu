import ipywidgets as widgets
from .config import config, ColormapContinuousEnum, ColormapDiscreteEnum


class SettingsWidget(widgets.HBox):
    def __init__(self, feature_cols: list[str], target_cols: list[str], fracture=0.75):

        self._widget_feature_x = widgets.Dropdown(
            description="x-axis",
            options=feature_cols,
            value=feature_cols[0],
            layout=widgets.Layout(width="250px"),
            style={"description_width": "70px"},
        )

        self._widget_feature_y = widgets.Dropdown(
            description="y-axis",
            options=feature_cols,
            value=feature_cols[1],
            layout=widgets.Layout(width="250px"),
            style={"description_width": "70px"},
        )

        self._widget_fracture = widgets.BoundedFloatText(
            min=0,
            max=1.0,
            step=0.01,
            value=fracture,
            description="fraction",
            layout=widgets.Layout(width="250px"),
            style={"description_width": "70px"},
        )

        self._widget_feature_color = widgets.Dropdown(
            description="color",
            options=target_cols,
            layout=widgets.Layout(width="250px"),
            style={"description_width": "70px"},
        )

        self._widget_feature_colormap = widgets.Dropdown(
            description="colormap",
            options=[member.value for member in ColormapContinuousEnum],
            value=config.colormap,
            layout=widgets.Layout(width="250px"),
            style={"description_width": "70px"},
        )

        self._widget_feature_colormap_discrete = widgets.Dropdown(
            description="colormap",
            options=[member.value for member in ColormapDiscreteEnum],
            value=config.colormap_discrete,
            layout=widgets.Layout(width="250px"),
            # layout=widgets.Layout(width="250px", visibility="hidden"),
            style={"description_width": "70px"},
        )

        self._widget_feature_size = widgets.Dropdown(
            description="size",
            options=["fixed size"] + target_cols,
            layout=widgets.Layout(width="250px"),
            style={"description_width": "70px"},
        )

        self._widget_feature_size_minmax_label = widgets.Label(
            value="min/max",
            layout=widgets.Layout(
                width="70px",
                display="flex",
                justify_content="flex-end",
                margin="0px 4px 0px 4px",
            ),
        )

        self._widget_feature_min_size_value = widgets.BoundedFloatText(
            min=0,
            step=1,
            value=config.min_size,
            layout=widgets.Layout(width="84px"),
        )
        self._widget_feature_max_size_value = widgets.BoundedFloatText(
            min=0,
            step=1,
            value=config.max_size,
            layout=widgets.Layout(width="84px"),
        )

        super().__init__(
            children=[
                widgets.VBox(
                    [
                        self._widget_feature_x,
                        self._widget_feature_y,
                        self._widget_fracture,
                    ]
                ),
                widgets.VBox(
                    [
                        self._widget_feature_color,
                        self._widget_feature_colormap,
                        self._widget_feature_colormap_discrete,
                    ]
                ),
                widgets.VBox(
                    [
                        self._widget_feature_size,
                        widgets.HBox(
                            [
                                self._widget_feature_size_minmax_label,
                                self._widget_feature_min_size_value,
                                self._widget_feature_max_size_value,
                            ]
                        ),
                    ]
                ),
            ],
            layout=widgets.Layout(
                # display="flex",
                # flex_flow="column",
                # border="solid 2px",
                # align_items="stretch",
                # width="50%",
            ),
        )
        # self.layout.height = "140px"
        # self.layout.top = "30px"

    def switch_colormap(self, is_discrete):
        if is_discrete:
            self._widget_feature_colormap.layout.visibility = "hidden"
            self._widget_feature_colormap_discrete.layout.visibility = "visible"
        else:
            self._widget_feature_colormap.layout.visibility = "visible"
            self._widget_feature_colormap_discrete.layout.visibility = "hidden"
