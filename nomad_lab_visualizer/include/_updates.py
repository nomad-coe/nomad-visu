import numpy as np
import pandas as pd
from itertools import cycle
import plotly.express as px
from ..configWidgets import ConfigWidgets 

def update_df_on_map(self):
    """
    updates the number of points based on the fraction value, then the fraction of the dataframe 'df_trace_on_map' that is visualized
    """

    for name_trace in self.name_traces:

        n_points_trace = int(ConfigWidgets.fract * self.df.loc[self.df[self.target] == name_trace].shape[0])

        if n_points_trace < 1:
            n_points_trace = 1

        self.n_points[name_trace] = n_points_trace

        if (ConfigWidgets.feat_x, ConfigWidgets.feat_y) in ConfigWidgets.optimized_frac:
            optimized_sequence, _ = ConfigWidgets.optimized_frac[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)] 

            self.df_trace_on_map[name_trace] = (
                self.df.loc[self.df[self.target] == name_trace]
                .loc[self.df.loc[self.df[self.target] == name_trace].index.to_numpy()[optimized_sequence[name_trace]]]
                .head(self.n_points[name_trace])
            )
        else:
            self.df_trace_on_map[name_trace] = (
                self.df.loc[self.df[self.target] == name_trace]
                .loc[self.index_df_trace_shuffled[name_trace]]
                .head(self.n_points[name_trace])
            )

        # if a structure is visualized, its dataframe entry is added to the visualized dataframe 'df_trace_on_map'
        # this to avoid that the entry relative to a structure visualized is not available on the map
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
    updates the hover data based on the points that are visualized on the map
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
        # else:
        #     self.hover_custom.append([''])
        #     self.hover_template.append([''])


def update_marker_symbol(self):
    """
    updates the list of marker symbols for each trace
    all markers are initally set to have the symbol specific of the trace
    points whose structure is visualized have a cross as marker
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


def update_marker_size(self):
    """
    updates the size of the markers
    in case 'Default size' is set all markers have the same size, and points marked with x/cross are set with a specific size
    in case 'Marker' has a feature value, marker sizes are selected according to that specific feature
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


def update_marker_color(self):
    """
    updates the color of markers
    """

    feature = ConfigWidgets.featcolor

    if feature == "Default color":
        # each trace has a different color picked from a given palette

        self.palette = cycle(
            getattr(px.colors.qualitative, ConfigWidgets.color_palette)
        )

        for name_trace in self.name_traces:
            self.colors[name_trace] = [next(self.palette)] * len(
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


def fract_change_updates(self):
    """
    updates relative to a change in the fraction value that is visualized
    """

    update_df_on_map(self)
    update_hover_variables(self)


def marker_style_updates(self):
    """
    updates relative to a change in the markers properties
    """

    update_marker_color(self)
    update_marker_symbol(self)
    update_marker_size(self)
