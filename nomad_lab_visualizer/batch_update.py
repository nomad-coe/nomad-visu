from .geometry import make_hull, make_line


def batch_update(self):
    """
    updates the layout of the map with all values stored in the staticVisualizer
    """

    x_min = []
    x_max = []
    y_min = []
    y_max = []

    for name_trace in self.trace_name:

        x_min.append(min(self.df_trace_on_map[name_trace][self.feat_x]))
        x_max.append(max(self.df_trace_on_map[name_trace][self.feat_x]))
        y_min.append(min(self.df_trace_on_map[name_trace][self.feat_y]))
        y_max.append(max(self.df_trace_on_map[name_trace][self.feat_y]))

    x_min = min(x_min)
    y_min = min(y_min)
    x_max = max(x_max)
    y_max = max(y_max)
    x_delta = 0.05 * abs(x_max - x_min)
    y_delta = 0.05 * abs(y_max - y_min)

    # range of the x-,y- values that are visualized on the map
    xaxis_range = [x_min - x_delta, x_max + x_delta]
    yaxis_range = [y_min - y_delta, y_max + y_delta]

    with self.fig.batch_update():
        self.fig.update_layout(
            showlegend=True,
            plot_bgcolor=self.bg_color,
            font=dict(
                size=int(self.font_size),
                family=self.widg_font_family.value,
                color=self.widg_font_color.value,
            ),
            xaxis_title=self.widg_featx.value,
            yaxis_title=self.widg_featy.value,
            xaxis_range=xaxis_range,
            yaxis_range=yaxis_range,
        )

        for name_trace in self.trace_name:
            # all elements on the map and their properties are reinitialized at each change

            self.fig.update_traces(
                selector={"name": name_trace},
                text=self.hover_text[name_trace],
                customdata=self.hover_custom[name_trace],
                hovertemplate=self.hover_template[name_trace],
                x=self.df_trace_on_map[name_trace][self.feat_x],
                y=self.df_trace_on_map[name_trace][self.feat_y],
                marker=dict(
                    size=self.sizes[name_trace], symbol=self.symbols[name_trace]
                ),
            )
            if (
                self.widg_featcolor.value != "Default color"
                and self.widg_featcolor_type.value == "Gradient"
            ):

                feature = self.widg_featcolor.value
                gradient = self.widg_featcolor_list.value
                min_value = self.df[feature].min()
                max_value = self.df[feature].max()

                self.fig.update_traces(
                    selector={"name": name_trace},
                    marker=dict(
                        colorscale=gradient,
                        showscale=True,
                        color=self.colors[name_trace],
                        cmin=min_value,
                        cmax=max_value,
                        colorbar=dict(
                            thickness=10,
                            orientation="v",
                            len=0.5,
                            y=0.25,
                            title=dict(text=feature, side="right", font={"size": 10}),
                        ),
                    ),
                )
            else:

                self.fig.update_traces(
                    selector={"name": name_trace},
                    marker=dict(showscale=False, color=self.colors[name_trace]),
                )

        if self.convex_hull == True:

            if self.feat_x == self.feat_y:

                for name_trace in self.trace_name:
                    self.trace["Hull " + name_trace].line = dict(width=0)
                    self.fig.update_traces(
                        selector={"name": "Hull " + name_trace},
                    )
            else:
                hullx, hully = make_hull(self, self.feat_x, self.feat_y)
                for name_trace in self.trace_name:

                    self.trace["Hull " + name_trace]["x"] = hullx[name_trace]
                    self.trace["Hull " + name_trace]["y"] = hully[name_trace]
                    self.trace["Hull " + name_trace].line = dict(
                        color=self.hull_color,
                        width=self.hull_width,
                        dash=self.hull_dash,
                    )
                    self.fig.update_traces(
                        selector={"name": "Hull " + name_trace}, showlegend=False
                    )
        if self.regr_line_coefs:

            line_x, line_y = make_line(self, self.feat_x, self.feat_y)
            self.trace["Line"].line = dict(
                color=self.line_color, width=self.line_width, dash=self.line_dash
            )
            self.trace["Line"]["x"] = line_x
            self.trace["Line"]["y"] = line_y
            self.fig.update_traces(selector={"name": "Line"}, showlegend=False)
