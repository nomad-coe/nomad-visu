import numpy as np


def update_layout_figure(self):
    # All batch_update related changes are handled by this function
    with self.fig.batch_update():
        self.fig.update_layout(
            showlegend=True,
            plot_bgcolor=self.bg_color,
            font=dict(
                size=int(self.font_size),
                family=self.font_families[0],
            ),
            xaxis_title=self.widg_featx.value,
            yaxis_title=self.widg_featy.value,
            # xaxis_range =[x_min - x_delta, x_max + x_delta],
            # yaxis_range=[y_min - y_delta, y_max + y_delta],
        )
        for cl in np.arange(self.n_classes):
            # All elements on the map and their properties are reinitialized at each change
            self.trace[self.name_trace[cl]]['x'] = self.df_classes_on_map[cl][self.feat_x]
            self.trace[self.name_trace[cl]]['y'] = self.df_classes_on_map[cl][self.feat_y]
            self.trace[self.name_trace[cl]].marker.symbol = self.symbols[cl]
            self.trace[self.name_trace[cl]].marker.size = self.sizes[cl]
            # self.trace[self.name_trace[cl]].marker.line.color = self.colors[cl]
            # self.trace[self.name_trace[cl]].marker.line.width = self.global_markerlinewidth[cl]
            self.fig.update_traces(
                selector={'name': str(self.name_trace[cl])},
                text=self.hover_text[cl],
                customdata=self.hover_custom[cl],
                hovertemplate=self.hover_template[cl],
                marker_color=self.colors[cl],
                visible=True
            )


def update_df_on_map(self):
    # if self.trace_l:
    #     trace_l, formula_l = self.trace_l
    # else:
    #     trace_l = -2
    # if self.trace_r:
    #     trace_r, formula_r = self.trace_r
    # else:
    #     trace_r = -2

    for cl in range(self.n_classes):
        self.df_classes_on_map[cl] = self.df_classes[cl].loc[self.index_classes_shuffled[cl]].head(
            int(self.frac * self.df_classes[cl].shape[0]))
        # if cl == trace_l:
        #     self.df_entries_onmap[cl] = pd.concat([
        #         self.df_entries_onmap[cl],
        #         self.df_clusters[trace_l].loc[[formula_l]]
        #     ], axis=0)
        # if cl == trace_r:
        #     self.df_entries_onmap[cl] = pd.concat([
        #         self.df_entries_onmap[cl],
        #         self.df_clusters[trace_r].loc[[formula_r]],
        #     ], axis=0)
        self.n_points[cl] = self.df_classes_on_map[cl].shape[0]


    for cl in range(self.n_classes):
        self.symbols[cl]=['circle']*self.n_points[cl]
        formula_l = self.widg_compound_text_l.value 
        formula_r = self.widg_compound_text_r.value 
        try:
            point = np.where(self.df_classes_on_map[cl].index.to_numpy() == formula_l)[0][0]
            self.symbols[cl][point] = 'x'
        except:
            pass
        try:
            point = np.where(self.df_classes_on_map[cl].index.to_numpy() == formula_r)[0][0]
            self.symbols[cl][point] = 'cross'
        except:
            pass

    # if self.widg_outliersbox.value:
    #     self.df_entries_onmap[-1] = pd.concat(self.df_entries_onmap[:self.n_clusters + 1], axis=0, sort=False)
    #     self.n_points[-1] = int(self.df_entries_onmap[-1].shape[0])
    #     self.global_symbols[-1] = [symb for sub in self.global_symbols[:-1] for symb in sub]
    # else:
    #     self.df_entries_onmap[-1] = pd.concat(self.df_entries_onmap[:self.n_clusters], axis=0, sort=False)
    #     self.n_points[-1] = int(self.df_entries_onmap[-1].shape[0])
    #     self.global_symbols[-1] = [symb for sub in self.global_symbols[:-2] for symb in sub]


def update_hover_variables(self):
    self.hover_text = []
    self.hover_custom = []
    self.hover_template = []

    for cl in range(self.n_classes):
        self.hover_text.append(self.df_classes_on_map[cl].index)
        hover_template = r"<b>%{text}</b><br><br>"
        if self.hover_features:
            hover_custom = np.dstack([self.df_classes_on_map[cl][str(self.hover_features[0])].to_numpy()])
            hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
            for i in range(1, len(self.hover_features), 1):
                hover_custom = np.dstack(
                    [hover_custom, self.df_classes_on_map[cl][str(self.hover_features[i])].to_numpy()])
                hover_template += str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
            self.hover_custom.append(hover_custom[0])
            self.hover_template.append(hover_template)
        else:
            self.hover_custom.append([''])
            self.hover_template.append([''])
    self.hover_text.append(self.df_classes_on_map[-1].index)
    hover_template = r"<b>%{text}</b><br><br>"
    if self.hover_features:
        hover_custom = np.dstack([self.df_classes_on_map[-1][str(self.hover_features[0])].to_numpy()])
        hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
        for i in range(1, len(self.hover_features), 1):
            hover_custom = np.dstack(
                [hover_custom, self.df_classes_on_map[-1][str(self.hover_features[i])].to_numpy()])
            hover_template += str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
        self.hover_custom.append(hover_custom[0])
        self.hover_template.append(hover_template)
    else:
        self.hover_custom.append([''])
        self.hover_template.append([''])

    # for cl in np.arange(self.n_classes):
    #     markerlinewidth = [1] * self.n_points[cl]
    #     markerlinecolor = ['white'] * self.n_points[cl]
    #     sizes = [self.marker_size] * self.n_points[cl]
    #     symbols = self.symbols[cl]
    #     try:
    #         point = symbols.index('x')
    #         sizes[point] = self.cross_size
    #         markerlinewidth[point] = 2
    #         markerlinecolor[point] = 'black'
    #     except:
    #         pass
    #     try:
    #         point = symbols.index('cross')
    #         sizes[point] = self.cross_size
    #         markerlinewidth[point] = 2
    #         markerlinecolor[point] = 'black'
    #     except:
    #         pass
    #     self.sizes[cl] = sizes
    #     # self.global_markerlinecolor[cl] = markerlinecolor
    #     # self.global_markerlinewidth[cl] = markerlinewidth
    # self.sizes[-1] = [symb for sub in self.sizes[:-1] for symb in sub]
    # self.global_markerlinecolor[-1] = [symb for sub in self.global_markerlinecolor[:-1] for symb in sub]
    # self.global_markerlinewidth[-1] = [symb for sub in self.global_markerlinewidth[:-1] for symb in sub]


def update_markers_size(self, feature='Default size'):
    # Defines the size of the markers based on the input feature.
    # In case of default feature all markers have the same size.
    # Points marked with x/cross are set with a specific size
    if feature == 'Default size':

        for cl in range(self.n_classes):

            sizes = [self.marker_size] * self.n_points[cl]
            symbols = [self.symbols[cl]] * self.n_points[cl]

            try:
                point = symbols.index('x')
                sizes[point] = self.cross_size
            except:
                try:
                    point = symbols.index('x')
                    sizes[point] = self.cross_size
                except:
                    pass
            try:
                point = symbols.index('cross')
                sizes[point] = self.cross_size
            except:
                try:
                    point = symbols.index('cross')
                    sizes[point] = self.cross_size
                except:
                    pass
            self.sizes = sizes
    else:
        min_value = min(self.df[feature])
        max_value = max(self.df[feature])
        coeff = 2 * self.marker_size / (max_value - min_value)

        for cl in range(self.n_classes):
            sizes = self.marker_size / 2 + coeff * self.df_classes_on_map[cl][feature].to_numpy()
            self.sizes[cl] = sizes
