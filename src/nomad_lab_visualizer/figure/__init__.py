import plotly.graph_objects as go
import numpy as np
import os
import numpy as np
import pandas as pd
import plotly.express as px

from scipy.spatial import ConvexHull
import numpy as np

import numpy as np
import pandas as pd
from itertools import cycle
import plotly.express as px

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors



class Figure (object):


    def __init__ (self, df, embedding_features, hover_features, target, path_to_structures):

        self.df = df.copy()
        self.embedding_features = embedding_features
        self.hover_features = hover_features
        self.path_to_structures = path_to_structures
        self.target = target

        self.FigureWidget = go.FigureWidget()
        # Permanent layout settings are defined here
        self.FigureWidget.update_layout(
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
            width=800,
            height=400,
            margin=dict(l=50, r=50, b=70, t=20, pad=4),
        )
        self.FigureWidget.update_xaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )
        self.FigureWidget.update_yaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )

        # The 'target' feature is used to divide data into different traces.
        # Each item in the following dictionaries will be related to a different trace in the dataframe.
        self.name_traces = self.df[target].unique()
        self.trace = {} # a pair of features (feat_0, feat_1) returns 'True' if a regression line was added for those features
        self.regr_line_trace = {} # a pair of features (feat_0, feat_1) returns the values of the regression line for those features
        self.df_trace_on_map = {} # dataframe containing only the elements that are visualized on the map
        self.symbols = {}  # list of symbols used for every marker in each trace
        self.sizes = {}  # list of sizes used for every marker in each trace
        self.colors = {}  # list of colors used for every marker in each trace
        self.trace_symbol = {}  # default symbol used for the trace

        self.optimized_sequence_indexes = {} # optimized sequence of entries that is visualized varying the fraction for each pair of features.
        self.optimized_init_fract = {} # optimized initial fraction that is visualized for each pair of features.

        self.random_permutation_indexes = {} # random sequence of entries that is visualized varying the fraction.

        self.init_fract = 1
        total_points = self.df.shape[0]
        if (total_points>1000):
            # The initial fraction of visualized points is by default 1, unless there are more than 1000 points.
            self.init_fract = 1000/total_points

        self.convex_hull = False

        if path_to_structures:
            # List of all files found in the directory pointed by 'Structure'.
            self.df["File"] = self.df["Structure"].apply(lambda x: os.listdir(x))
            # Number of files found in the directory pointed by 'Structure'.
            self.df["Replicas"] = self.df["Structure"].apply(
                lambda x: len(os.listdir(x))
            )

        # Dictionaries initialized above are compiled for all different trace names.
        for cl in range(len(self.name_traces)):

            name_trace = str(self.name_traces[cl])

            # A 'Plotly go trace' is constructed and assigned to the 'trace' dictionary.
            self.FigureWidget.add_trace(
                go.Scatter(
                    name=name_trace,
                    mode="markers",
                )
            )
            self.trace[name_trace] = self.FigureWidget["data"][-1]

            # Add convex hull trace.
            name_trace = "Hull " + name_trace
            self.FigureWidget.add_trace(
                go.Scatter(
                    name=name_trace,
                )
            )
            self.trace[name_trace] = self.FigureWidget["data"][-1]

        for name_trace in self.name_traces:

            self.random_permutation_indexes[name_trace] = self.df.loc[
                self.df[target] == name_trace
            ].index.to_numpy()[np.random.permutation(self.df.loc[self.df[self.target] == name_trace].shape[0])]

            n_points = self.df.loc[
                self.df[target] == name_trace
            ].shape[0]

            self.df_trace_on_map[name_trace] = (
                self.df.loc[self.df[target] == name_trace]
                .loc[self.random_permutation_indexes[name_trace]]
                .head(n_points)
            )

            self.trace_symbol[name_trace] = "circle" # Circle is the init symbol used for each trace


    def add_regr_line (self, coefs, feat_x, feat_y, ConfigWidgets, ColorLineWidget, WidthLineWidget, DashLineWidget):

        if not (feat_x,feat_y) in self.regr_line_trace:

            self.regr_line_trace[(feat_x,feat_y)]=True
            line_x, line_y = self.make_line( feat_x, feat_y, coefs)

            name_trace = "Regr line" + str(feat_x) + ' ' + str(feat_y)
            self.FigureWidget.add_trace(go.Scatter(
                name=name_trace,
                x=line_x,
                y=line_y,
                ))
            self.trace[name_trace] = self.FigureWidget["data"][-1]
            self.FigureWidget.update_traces(selector={"name": name_trace}, showlegend=False)

        else:

            self.regr_line_trace[(feat_x,feat_y)]=True
            line_x, line_y = self.make_line(feat_x, feat_y, coefs)

            name_trace = "Regr line" + str(feat_x) + ' ' + str(feat_y)
            self.trace[name_trace].x=line_x
            self.trace[name_trace].y=line_y
            self.FigureWidget.update_traces(selector={"name": name_trace}, showlegend=False)

        if feat_x == ConfigWidgets.feat_x and feat_y == ConfigWidgets.feat_y:
            ColorLineWidget.disabled = False
            WidthLineWidget.disabled = False
            DashLineWidget.disabled = False

        self.batch_update(ConfigWidgets)


    def remove_regr_line (self, feat_x, feat_y, ConfigWidgets, ColorLineWidget, WidthLineWidget, DashLineWidget):

        self.regr_line_trace[(feat_x,feat_y)]=False

        if feat_x == ConfigWidgets.feat_x and feat_y == ConfigWidgets.feat_y:
            ColorLineWidget.disabled = True
            WidthLineWidget.disabled = True
            DashLineWidget.disabled = True

        self.batch_update(ConfigWidgets)


    def optimize_fract(self, visualizerTopWidgets, ConfigWidgets):

        if not (ConfigWidgets.feat_x, ConfigWidgets.feat_y) in self.optimized_sequence_indexes :
            sequence_indexes, init_fract = self.optimize_sequence(ConfigWidgets.feat_x, ConfigWidgets.feat_y)

            self.optimized_sequence_indexes[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)] = sequence_indexes
            self.optimized_sequence_indexes[(ConfigWidgets.feat_y, ConfigWidgets.feat_x)] = sequence_indexes
            self.optimized_init_fract[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)] = init_fract
            self.optimized_init_fract[(ConfigWidgets.feat_y, ConfigWidgets.feat_x)] = init_fract

            ConfigWidgets.fract = init_fract
            visualizerTopWidgets.FractSlider.widget.value = init_fract
            self.batch_update(ConfigWidgets)

    def batch_update(self, ConfigWidgets):
        """
        Updates the layout of the map according to values stored in "ConfigWidgets".
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
    def fract_change_updates(self, ConfigWidgets):
        """
        All updates caused by a change in the fraction value.
        """

        self.update_df_on_map(ConfigWidgets)
        self.update_hover_variables()



    def update_df_on_map(self, ConfigWidgets):
        """
        Updates the number of points based on the fraction value,
        then 'df_trace_on_map' which is the fraction of the dataframe that is visualized
        """

        for name_trace in self.name_traces:


            n_points = int(
                ConfigWidgets.fract * \
                self.df.loc[self.df[self.target] == name_trace].shape[0]
                )

            if n_points < 1:
                n_points = 1


            if (ConfigWidgets.feat_x, ConfigWidgets.feat_y) in self.optimized_sequence_indexes:
                sequence_indexes = self.optimized_sequence_indexes[
                    (ConfigWidgets.feat_x, ConfigWidgets.feat_y)][name_trace]
            else:
                sequence_indexes = self.random_permutation_indexes[name_trace]

            self.df_trace_on_map[name_trace] = (
                self.df.loc[self.df[self.target] == name_trace]
                .loc[sequence_indexes]
                .head(n_points)
                )

            # if a structure is visualized, its dataframe entry is added to the visualized dataframe 'df_trace_on_map'
            # this to avoid that the entry relative to a visualized structure is not available on the map
            if ConfigWidgets.structure_text_l in self.df.loc[self.df[self.target] == name_trace].index:
                self.df_trace_on_map[name_trace] = pd.concat(
                    [
                        self.df_trace_on_map[name_trace],
                        self.df.loc[[ConfigWidgets.structure_text_l]],
                    ]
                )

            if ConfigWidgets.structure_text_r in self.df.loc[self.df[self.target] == name_trace].index:
                self.df_trace_on_map[name_trace] = pd.concat(
                    [
                        self.df_trace_on_map[name_trace],
                        self.df.loc[[ConfigWidgets.structure_text_r]],
                    ]
                )


    def update_hover_variables(self):
        """
        Updates the hover data based on the points that are visualized on the map.
        """

        self.hover_text = {}
        self.hover_custom = {}
        self.hover_template = {}

        for name_trace in self.name_traces:

            self.hover_text[name_trace] = self.df_trace_on_map[name_trace].index
            hover_template = r"<b>%{text}</b><br><br>"
            if self.hover_features:
                hover_custom = np.dstack(
                    [
                        self.df_trace_on_map[name_trace][
                            str(self.hover_features[0])
                        ].to_numpy()
                    ]
                )
                hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
                for i in range(1, len(self.hover_features), 1):
                    hover_custom = np.dstack(
                        [
                            hover_custom,
                            self.df_trace_on_map[name_trace][
                                str(self.hover_features[i])
                            ].to_numpy(),
                        ]
                    )
                    hover_template += (
                        str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
                    )
                self.hover_custom[name_trace] = hover_custom[0]
                self.hover_template[name_trace] = hover_template
            else:
                self.hover_customp[name_trace]=['']
                self.hover_template[name_trace]=['']




    def make_hull(self, feat_x, feat_y):

        xhull_classes = {}
        yhull_classes = {}

        for name_trace in self.name_traces:

            name_trace = str(name_trace)
            points = self.df.loc[
                    self.df[self.target] == name_trace
                ][[feat_x, feat_y]].to_numpy()

            delta_0 = max(points[:, 0]) - min(points[:, 0])
            delta_1 = max(points[:, 1]) - min(points[:, 1])
            exp_1 = int(np.log10(delta_0 / delta_1))
            exp_0 = int(np.log10(delta_1 / delta_0))
            if exp_1 > 6:
                points[:, 1] = points[:, 1] * 10**exp_1
            if exp_0 > 6:
                points[:, 0] = points[:, 0] * 10**exp_0
            hull = ConvexHull(points)
            vertexes = self.df.loc[
                    self.df[self.target] == name_trace
                ][[feat_x, feat_y]].to_numpy()[hull.vertices]

            x_hullvx = vertexes[:, 0]
            y_hullvx = vertexes[:, 1]
            n_intervals = 100

            xhull = np.array([x_hullvx[0]])
            yhull = np.array([y_hullvx[0]])
            for xy in zip(x_hullvx, y_hullvx):
                xhull = np.concatenate([xhull, np.linspace(xhull[-1], xy[0], n_intervals)])
                yhull = np.concatenate([yhull, np.linspace(yhull[-1], xy[1], n_intervals)])

            xhull_classes[name_trace] = np.concatenate(
                [xhull, np.linspace(xhull[-1], x_hullvx[0], n_intervals)]
            )
            yhull_classes[name_trace] = np.concatenate(
                [yhull, np.linspace(yhull[-1], y_hullvx[0], n_intervals)]
            )

        return xhull_classes, yhull_classes


    def make_line(self, feat_x, feat_y, regr_line_coefs):

        idx_x = self.embedding_features.index(feat_x)
        idx_y = self.embedding_features.index(feat_y)
        line_x = np.linspace(self.df[feat_x].min(), self.df[feat_x].max(), 1000)

        # Gives the classifications line
        if feat_x == feat_y:
            return line_x, line_x
        else:
            line_y = (
                -line_x * regr_line_coefs[0][idx_x] / regr_line_coefs[0][idx_y]
                - regr_line_coefs[1] / regr_line_coefs[0][idx_y]
            )
            return line_x, line_y

    def marker_style_updates(self, ConfigWidgets):
        """
        All updates caused by a change in the markers properties.
        """

        self.update_marker_color( ConfigWidgets)
        self.update_marker_symbol( ConfigWidgets)
        self.update_marker_size( ConfigWidgets)


    def update_marker_symbol(self, ConfigWidgets):
        """
        Updates the list of marker symbols for each trace.
        All markers are initally set to have the symbol specific of the trace "trace_symbol".
        Points whose structure is visualized have a cross as marker.
        """

        for name_trace in self.name_traces:

            self.symbols[name_trace] = [self.trace_symbol[name_trace]] * len(
                self.df_trace_on_map[name_trace]
            )
            formula_l = ConfigWidgets.structure_text_l
            formula_r = ConfigWidgets.structure_text_r

            for i in range(2):
                # entries whose structure is visualized appear twice on 'df_trace_on_map'
                try:
                    point = np.where(
                        self.df_trace_on_map[name_trace].index.to_numpy() == formula_l
                    )[0][i]
                    self.symbols[name_trace][point] = "x"
                except:
                    pass
                try:
                    point = np.where(
                        self.df_trace_on_map[name_trace].index.to_numpy() == formula_r
                    )[0][i]
                    self.symbols[name_trace][point] = "cross"
                except:
                    pass

            if formula_l == formula_r and formula_l:
                try:
                    point = np.where(
                        self.df_trace_on_map[name_trace].index.to_numpy() == formula_l
                    )[0][1]
                    self.symbols[name_trace][point] = "x"
                    point = np.where(
                        self.df_trace_on_map[name_trace].index.to_numpy() == formula_l
                    )[0][2]
                    self.symbols[name_trace][point] = "cross"
                except:
                    pass


    def update_marker_size(self, ConfigWidgets):
        """
        Updates the size of the markers:
        in case of 'Default size' all markers have the same size, and points marked with x/cross are set with a specific cross size;
        in case 'Marker' has a feature value, marker sizes are selected according to that specific feature.
        """

        feature = ConfigWidgets.featmarker

        if feature == "Default size":

            for name_trace in self.name_traces:

                sizes = [ConfigWidgets.marker_size] * len(self.df_trace_on_map[name_trace])
                symbols = self.symbols[name_trace]

                indices_x = [i for i, symbol in enumerate(symbols) if symbol == "x"]
                indices_cross = [i for i, symbol in enumerate(symbols) if symbol == "cross"]

                if indices_x:
                    sizes[indices_x[0]] = ConfigWidgets.cross_size

                if len(indices_x) == 2:
                    # entries whose structure is visualized appear twice on 'df_trace_on_map'

                    sizes[indices_x[0]] = 0
                    sizes[indices_x[1]] = ConfigWidgets.cross_size

                if indices_cross:
                    sizes[indices_cross[0]] = ConfigWidgets.cross_size

                if len(indices_cross) == 2:
                    sizes[indices_cross[0]] = 0
                    sizes[indices_cross[1]] = ConfigWidgets.cross_size

                self.sizes[name_trace] = sizes
        else:

            min_value = ConfigWidgets.min_value_markerfeat
            max_value = ConfigWidgets.max_value_markerfeat
            min_feat = min(
                [
                    min(self.df_trace_on_map[name_trace][feature].to_numpy())
                    for name_trace in self.df_trace_on_map
                ]
            )
            max_feat = max(
                [
                    max(self.df_trace_on_map[name_trace][feature].to_numpy())
                    for name_trace in self.df_trace_on_map
                ]
            )

            coeff = (max_value - min_value) / (max_feat - min_feat)

            for name_trace in self.name_traces:

                sizes = min_value + coeff * (
                    self.df_trace_on_map[name_trace][feature].to_numpy() - min_feat
                )
                self.sizes[name_trace] = sizes


    def update_marker_color(self, ConfigWidgets):
        """
        Updates the color of markers:
        in case of "Default color" each trace has a different color;
        in case of a feature, each different feature value has a different color.
        """

        feature = ConfigWidgets.featcolor

        if feature == "Default color":

            palette = cycle(
                getattr(px.colors.qualitative, ConfigWidgets.color_palette)
            )
            for name_trace in self.name_traces:
                self.colors[name_trace] = [next(palette)] * len(
                    self.df_trace_on_map[name_trace]
                )

        elif ConfigWidgets.featcolor_type == "Discrete":
            # each color represents a different discrete feature value

            colors_dict = {}
            palette = cycle(getattr(px.colors.qualitative, ConfigWidgets.featcolor_list))
            for value in np.sort(self.df[feature].unique()):
                colors_dict[value] = next(palette)

            for name_trace in self.name_traces:

                self.colors[name_trace] = [" "] * len(self.df_trace_on_map[name_trace])
                for i, value in enumerate(self.df_trace_on_map[name_trace][feature]):

                    self.colors[name_trace][i] = colors_dict[value]

        elif ConfigWidgets.featcolor_type == "Gradient":
            # colors are interpolated in a gradient, according to the feature value

            feature = ConfigWidgets.featcolor

            for name_trace in self.name_traces:
                self.colors[name_trace] = self.df_trace_on_map[name_trace][feature]

    def optimize_sequence (self, feat_x, feat_y):

        n_neighbors = 10
        fraction_thres = 1
        optimized_sequence_indexes = {}

        for name_trace in self.name_traces:

            name_trace = str(name_trace)
            feat_x_norm = MinMaxScaler().fit_transform(self.df.loc[
                    self.df[self.target] == name_trace
                ][feat_x].values.reshape(-1,1))
            feat_y_norm = MinMaxScaler().fit_transform(self.df.loc[
                    self.df[self.target] == name_trace
                ][feat_y].values.reshape(-1,1))

            X = np.concatenate((feat_x_norm, feat_y_norm), axis=1)

            nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree').fit(X)
            nbrs_distances, nbrs_indices = nbrs.kneighbors(X)

            n_values = len(self.df.loc[
                    self.df[self.target] == name_trace
                ])

            remaining_indices= np.arange(n_values)

            new_index = np.array([
                remaining_indices[np.argmin(np.sum(nbrs_distances, axis=1))]
                ])
            selected_indices = np.array([new_index]).reshape(1)
            remaining_indices = np.delete(remaining_indices,selected_indices)
            mask = np.where(nbrs_indices==new_index, 1, 0)

            last_cost = 0
            bool_cost = True

            while (len(remaining_indices)>0):

                # prob = np.sum(np.exp(distances[remaininig_indexes,:][:,selected_indexes]), axis=1)
                # prob /= np.sum(prob)
                # new_index = np.array([np.random.choice(remaininig_indexes, p=prob)])

                # the numerator gives the sum of the distances over the indexes that do not appear on the map
                # the closer the points that do not appear on the map are, the more likely the point is selected
                num=np.sum((mask*nbrs_distances)[remaining_indices],axis=1)
                # the denominater gives the sum of the distances over the indexes that appear on the map
                # the closer the points that appear on the map are, the less likely the point is selected
                den=np.sum(((1-mask)*nbrs_distances)[remaining_indices],axis=1)
                if (np.min(num)==0):
                    arg=np.argmax(den[np.where(num==0)])
                    new_index = np.array([remaining_indices[np.where(num==0)][arg]])
                    new_cost = 0
                elif (np.min(den)==0):
                    arg=np.argmin(num[np.where(den==0)])
                    new_index = np.array([remaining_indices[np.where(den==0)][arg]])
                    new_cost = float('inf')
                else:
                    arg=np.argmin(num/den)
                    new_index = np.array([remaining_indices[arg]])
                    new_cost = (num/den)[arg]

                if (bool_cost) :
                    if (new_cost>1 and last_cost<1):
                        fraction_thres = len(selected_indices)/n_values
                        # fractions_thres [(feat_x, feat_y)] = len(selected_indexes)/len(distances)
                        # fractions_thres [(feat_y, feat_x)] = len(selected_indexes)/len(distances)
                        bool_cost = False
                    last_cost = new_cost

                remaining_indices = np.delete(remaining_indices,np.where(remaining_indices==new_index))
                selected_indices = np.concatenate((selected_indices, new_index))
                mask = mask+np.where(nbrs_indices==new_index, 1, 0)

                if (len(remaining_indices>0) and len(remaining_indices)%10==0):
                    arg=np.argmax(np.sum((mask*nbrs_distances)[remaining_indices],axis=1))
                    new_index = np.array([remaining_indices[arg]])
                    remaining_indices = np.delete(remaining_indices,np.where(remaining_indices==new_index))
                    selected_indices = np.concatenate((selected_indices, new_index))
                    mask = mask+np.where(nbrs_indices==new_index, 1, 0)

            optimized_sequence_indexes[name_trace] = self.df[self.df[self.target] == name_trace].index.to_numpy()[selected_indices]

        return optimized_sequence_indexes, fraction_thres

