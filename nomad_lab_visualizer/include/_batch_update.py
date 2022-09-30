def batch_update(self, ConfigWidgets):
    """
    updates the layout of the map with all values stored in the staticVisualizer
    """

    self.marker_style_updates(ConfigWidgets)
    self.fract_change_updates(ConfigWidgets)

    x_min = []
    x_max = []
    y_min = []
    y_max = []

    for name_trace in self.name_traces:


        x_min.append(min(self.df_trace_on_map[name_trace][ConfigWidgets.feat_x]))
        x_max.append(max(self.df_trace_on_map[name_trace][ConfigWidgets.feat_x]))
        y_min.append(min(self.df_trace_on_map[name_trace][ConfigWidgets.feat_y]))
        y_max.append(max(self.df_trace_on_map[name_trace][ConfigWidgets.feat_y]))

    x_min = min(x_min)
    y_min = min(y_min)
    x_max = max(x_max)
    y_max = max(y_max)
    x_delta = 0.05 * abs(x_max - x_min)
    y_delta = 0.05 * abs(y_max - y_min)

    # range of the x-,y- values that are visualized on the map
    xaxis_range = [x_min - x_delta, x_max + x_delta]
    yaxis_range = [y_min - y_delta, y_max + y_delta]

    if ConfigWidgets.bg_toggle:
        bg_color = ConfigWidgets.bg_color
        gridcolor = 'white'
    else:
        bg_color = 'white'
        gridcolor = 'rgb(229,236,246)'

    with self.FigureWidget.batch_update():

        self.FigureWidget.update_layout(
            showlegend=True,
            plot_bgcolor=bg_color,
            xaxis=dict(gridcolor=gridcolor, showgrid=True, zeroline=False),
            yaxis=dict(gridcolor=gridcolor, showgrid=True, zeroline=False),
            font=dict(
                size=int(ConfigWidgets.font_size),
                family=ConfigWidgets.font_family,
                color=ConfigWidgets.font_color,
            ),
            xaxis_title=ConfigWidgets.feat_x,
            yaxis_title=ConfigWidgets.feat_y,
            xaxis_range=xaxis_range,
            yaxis_range=yaxis_range,
        )
        

        for name_trace in self.name_traces:
            # all elements on the map and their properties are reinitialized at each change


            self.FigureWidget.update_traces(
                selector={"name": str(name_trace)},
                text=self.hover_text[name_trace],
                customdata=self.hover_custom[name_trace],
                hovertemplate=self.hover_template[name_trace],
                x=self.df_trace_on_map[name_trace][ConfigWidgets.feat_x],
                y=self.df_trace_on_map[name_trace][ConfigWidgets.feat_y],
                marker=dict(
                    size=self.sizes[name_trace], symbol=self.symbols[name_trace]
                ),
            )
            if (
                ConfigWidgets.featcolor != "Default color"
                and ConfigWidgets.featcolor_type == "Gradient"
            ):

                feature = ConfigWidgets.featcolor
                gradient = ConfigWidgets.featcolor_list
                min_value = self.df[feature].min()
                max_value = self.df[feature].max()

                self.FigureWidget.update_traces(
                    selector={"name": str(name_trace)},
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

                self.FigureWidget.update_traces(
                    selector={"name": str(name_trace)},
                    marker=dict(showscale=False, color=self.colors[name_trace]),
                )
        if (ConfigWidgets.feat_x,ConfigWidgets.feat_y) in self.regr_line_trace:
            name_trace = "Regr line" + str(ConfigWidgets.feat_x) + ' ' + (ConfigWidgets.feat_y) 
            if self.regr_line_trace[(ConfigWidgets.feat_x,ConfigWidgets.feat_y)]:
                self.trace[name_trace].line = dict(
                        color=ConfigWidgets.line_color, 
                        width=ConfigWidgets.line_width, 
                        dash=ConfigWidgets.line_dash
                    )
            else:
                self.trace[name_trace].line = dict(width=0)


        if self.convex_hull == True:

            if ConfigWidgets.feat_x == ConfigWidgets.feat_y:

                for name_trace in self.name_traces:

                    self.trace["Hull " + str(name_trace)].line = dict(width=0)
                    self.FigureWidget.update_traces(
                        selector={"name": "Hull " + name_trace},
                    )
            else:
                hullx, hully = self.make_hull(ConfigWidgets.feat_x, ConfigWidgets.feat_y)
                for name_trace in self.name_traces:
    
                    self.trace["Hull " + str(name_trace)]["x"] = hullx[name_trace]
                    self.trace["Hull " + str(name_trace)]["y"] = hully[name_trace]
                    self.trace["Hull " + str(name_trace)].line = dict(
                        color=ConfigWidgets.hull_color,
                        width=ConfigWidgets.hull_width,
                        dash=ConfigWidgets.hull_dash,
                    )
                    self.FigureWidget.update_traces(
                        selector={"name": "Hull " + name_trace}, showlegend=False
                    )
        else:
            for name_trace in self.name_traces:

                self.trace["Hull " + str(name_trace)].line = dict(width=0)
                self.FigureWidget.update_traces(
                    selector={"name": "Hull " + str(name_trace)},
                )
  