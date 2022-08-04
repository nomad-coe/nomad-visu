import numpy as np
import pandas as pd
from include._sisso import make_hull, regr_line

def update_symbols (self):
 
    for cl in range(self.n_classes):
        self.symbols['Class ' + str(self.classes[cl])] = [self.class_symbol['Class ' + str(self.classes[cl])]] * self.n_points['Class ' + str(self.classes[cl])]
        formula_l = self.widg_compound_text_l.value 
        formula_r = self.widg_compound_text_r.value 
        try:
            point = np.where(self.df_classes_on_map[cl].index.to_numpy() == formula_l)[0][0]
            self.symbols['Class ' + str(self.classes[cl])][point] = 'x'
        except:
            pass
        try:
            point = np.where(self.df_classes_on_map[cl].index.to_numpy() == formula_r)[0][0]
            self.symbols['Class ' + str(self.classes[cl])][point] = 'cross'
        except:
            pass
            

def update_markers_size(self ):
    # Defines the size of the markers based on the input feature.
    # In case of default feature all markers have the same size.
    # Points marked with x/cross are set with a specific size
    feature = self.widg_featmarker.value

    if feature == 'default size':

        for cl in range(self.n_classes):

            name_trace = 'Class ' + str(self.classes[cl])

            sizes = [self.marker_size] * self.n_points[name_trace]
            symbols = self.symbols[name_trace]

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
            self.sizes[name_trace] = sizes
    else:
        min_value = min(self.df[feature])
        max_value = max(self.df[feature])
        coeff = 2 * self.marker_size / (max_value - min_value)

        for cl in range(self.n_classes):
            name_trace = 'Class ' + str(self.classes[cl])
            sizes = self.marker_size / 2 + coeff * self.df_classes_on_map[cl][feature].to_numpy()
            self.sizes[name_trace] = sizes


def update_layout_figure(self):
    # All batch_update related changes are handled by this function

    x_min = []
    x_max = []
    y_min = []
    y_max = []
    for cl in np.arange(self.n_classes):
        x_min.append(min(self.df_classes_on_map[cl][self.feat_x]))
        x_max.append(max(self.df_classes_on_map[cl][self.feat_x]))
        y_min.append(min(self.df_classes_on_map[cl][self.feat_y]))
        y_max.append(max(self.df_classes_on_map[cl][self.feat_y]))
    x_min = min(x_min)
    y_min = min(y_min)
    x_max = max(x_max)
    y_max = max(y_max)
    x_delta = 0.05 * abs(x_max - x_min)
    y_delta = 0.05 * abs(y_max - y_min)
    xaxis_range =[x_min - x_delta, x_max + x_delta]
    yaxis_range=[y_min - y_delta, y_max + y_delta]

    update_symbols(self)
    update_markers_size(self)

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
            xaxis_range = xaxis_range,
            yaxis_range = yaxis_range,
        )
        for  cl in np.arange(self.n_classes):
            # All elements on the map and their properties are reinitialized at each change
            self.trace['Class ' + str(self.classes[cl])]['x'] = self.df_classes_on_map[cl][self.feat_x]
            self.trace['Class ' + str(self.classes[cl])]['y'] = self.df_classes_on_map[cl][self.feat_y]
            self.trace['Class ' + str(self.classes[cl])].marker.size = self.sizes['Class ' + str(self.classes[cl])]
            self.trace['Class ' + str(self.classes[cl])].marker.symbol = self.symbols['Class ' + str(self.classes[cl])]
        
            # self.trace[self.name_trace[cl]].marker.line.color = self.colors[cl]
            # self.trace[self.name_trace[cl]].marker.line.width = self.global_markerlinewidth[cl]
            self.fig.update_traces(
                selector={'name': 'Class ' + str(self.classes[cl]) },
                text=self.hover_text[cl],
                customdata=self.hover_custom[cl],
                hovertemplate=self.hover_template[cl],
                marker_color=self.colors['Class ' + str(self.classes[cl])],
                visible=True
            )
        if ( self.convex_hull == True ) :

            if ( self.feat_x == self.feat_y ):
                for cl in np.arange(self.n_classes):
                    self.fig.update_traces(
                        selector={'name': 'Hull '+str(self.classes[cl])},
                        visible=False
                    )            
            else:
                hullx, hully = make_hull(self, self.feat_x, self.feat_y)
                for cl in np.arange(self.n_classes):
                    self.trace['Hull '+str(self.classes[cl])]['x'] = hullx[cl]
                    self.trace['Hull '+str(self.classes[cl])]['y'] = hully[cl]
                    self.trace['Hull '+str(self.classes[cl])].line = dict (color=self.widg_color_hull.value, width=self.widg_width_hull.value, dash=self.widg_style_hull    .value )
                    self.fig.update_traces(
                        selector={'name': 'Hull '+str(self.classes[cl])},
                        visible=True
                    )
        if ( self.regr_line_coefs ) :

            line_x, line_y = regr_line(self, self.feat_x, self.feat_y)
            self.trace['Regression line'].line = dict (color=self.widg_color_line.value, width=self.widg_width_line.value, dash=self.widg_style_line.value )
            self.trace['Regression line']['x'] = line_x
            self.trace['Regression line']['y'] = line_y




def update_df_on_map(self):

    for cl in range(self.n_classes):

        name_trace = 'Class ' + str(self.classes[cl])

        self.df_classes_on_map[cl] = self.df_classes[cl].loc[self.index_classes_shuffled[cl]].head(
            int(self.frac * self.df_classes[cl].shape[0]))

        if self.widg_compound_text_l.value in self.df_classes[cl].index:
            self.df_classes_on_map[cl] = self.df_classes_on_map[cl].append(self.df.loc[self.widg_compound_text_l.value])

        if self.widg_compound_text_r.value in self.df_classes[cl].index:
            self.df_classes_on_map[cl] = self.df_classes_on_map[cl].append(self.df.loc[self.widg_compound_text_r.value])
            
        self.n_points['Class ' + str(self.classes[cl])]= self.df_classes_on_map[cl].shape[0]


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
    #     markerlinecolor = ['white']. * self.n_points[cl]
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


