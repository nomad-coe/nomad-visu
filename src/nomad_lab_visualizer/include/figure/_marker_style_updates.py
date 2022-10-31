import numpy as np
import pandas as pd
from itertools import cycle
import plotly.express as px

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

