from turtle import update
from xml.etree.ElementInclude import include
import plotly.graph_objects as go
import ipywidgets as widgets
import py3Dmol
import numpy as np
from IPython.display import display
from itertools import cycle
import os
from .topWidgets import TopWidgets
from .configWidgets import ConfigWidgets
from .utilsWidgets import UtilsWidgets
from .viewersWidgets import ViewersWidgets
from .utilsButton import UtilsButton

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


class Visualizer:
    """
    Visualizer

    Attributes:
        df: pandas dataframe containing all data to be visualized
        embedding_features: list of features used for embedding
        hover features: list of features shown while hovering
        target: feature used to create traces (same target value - same trace)
        smart_frac: fraction of points is selected to maximize visualization of data distribution
        convex_hull: convex hull is drawn around each trace
        regr_line_coefs: coeffs of a regression line
        path_to_structures: path to a directory that contains all 'xyz' structures to be visualized

    """
    from .include._smart_fract import smart_fract_make
    from .include._instantiate_widgets import instantiate_widgets
    from .include._updates import fract_change_updates
    from .include._batch_update import batch_update

    def __init__(
        self,
        df,
        embedding_features,
        hover_features, 
        target,
        smart_fract=False,
        convex_hull=False,
        regr_line_coefs=None,
        path_to_structures=None,
    ):

        self.df = df
        self.target = target
        self.smart_fract = smart_fract
        # each unique value of the 'target' feature gives the name of a different trace
        self.trace_name = df[target].unique().astype(str)
        self.embedding_features = embedding_features

        self.hover_features = hover_features
        self.path_to_structures = path_to_structures
        self.convex_hull = convex_hull
        self.regr_line_coefs = regr_line_coefs

        if path_to_structures:
            # each row in the dataframe is expected to be identified with a different structure
            # List of all files found in the directory pointed by 'Structure'
            self.df["File"] = self.df["Structure"].apply(lambda x: os.listdir(x))
            # Number of files found in the directory pointed by 'Structure'
            self.df["Replicas"] = self.df["Structure"].apply(
                lambda x: len(os.listdir(x))
            )

        # The 'target' feature is used to divide data into different traces
        # Each item in the following dictionaries will be related to a different trace in the dataframe
        # For each different 'target' value a new trace is created
        
        self.fig = go.FigureWidget()
        # All permanent layout settings are defined here
        self.fig.update_layout(
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
            width=800,
            height=400,
            margin=dict(l=50, r=50, b=70, t=20, pad=4),
        )
        self.fig.update_xaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )
        self.fig.update_yaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )


        self.trace = {}
        self.df_trace = (
            {}
        )  # section of the pandas dataframe containing elements of a specific trace
        self.index_df_trace_shuffled = (
            {}
        )  # index of the dataframe trace shuffled for fraction visualization
        self.n_points = (
            {}
        )  # total points of the class which are visualized - can be less than the total number of data depending on the fraction visualized
        self.df_trace_on_map = (
            {}
        )  # dataframe which contains only the elements that are visualized on the map
        self.symbols = {}  # symbols used for markers of each trace
        self.sizes = {}  # sizes used for markers of each trace
        self.colors = {}  # colors used for markers of each trace
        self.trace_symbol = {}  # symbol used for the trace

    
        # dictionaries initialized above are compiled for all different trace names
        for cl in range(len(self.trace_name)):

            name_trace = self.trace_name[cl]

            self.df_trace[name_trace] = self.df.loc[
                self.df[self.target] == self.df[target].unique()[cl]
            ]

            # a trace with a specific name taken from the 'target' values is constructed and assigned to the 'trace' dictionary
            self.fig.add_trace(
                go.Scatter(
                    name=name_trace,
                    mode="markers",
                )
            )
            self.trace[name_trace] = self.fig["data"][-1]

            # add a convex hull for each different 'target' value
            if self.convex_hull:
                name_trace = "Hull " + name_trace
                self.fig.add_trace(
                    go.Scatter(
                        name=name_trace,
                    )
                )
                self.trace[name_trace] = self.fig["data"][-1]

        # add a trace that contains the regression line
        if self.regr_line_coefs:
            name_trace = "Line"
            self.fig.add_trace(go.Scatter(name=name_trace))
            self.trace[name_trace] = self.fig["data"][-1]

        # the shuffled values for fraction visualization are given using a max covering algorithm
        if self.smart_fract:
            fract_dict, fract_thres = self.smart_fract_make()
            # each pair of features has a different list of shuffled values accessbile in the dictionary 'fract_dict'
            self.fract_dict = fract_dict
            # each pair of features has a different initial fraction value accessbile in the dictionary 'fract_thres'
            self.fract_thres = fract_thres
            ConfigWidgets.fract = self.fract_thres[(self.embedding_features[0], self.embedding_features[1])]

        for name_trace in self.trace_name:

            # shuffled values are taken randomly if not 'smart_fract'
            if self.smart_fract == False:
                self.index_df_trace_shuffled[name_trace] = self.df_trace[
                    name_trace
                ].index.to_numpy()[
                    np.random.permutation(self.df_trace[name_trace].shape[0])
                ]
            else:
                self.index_df_trace_shuffled[name_trace] = self.fract_dict[
                    (self.embedding_features[0], self.embedding_features[1])
                ][name_trace]

            # number of points visualized given by a certain fraction
            self.n_points[name_trace] = int(
                TopWidgets.fract * self.df_trace[name_trace].shape[0]
            )
            # fraction of the dataframe that is visualized on the map
            self.df_trace_on_map[name_trace] = (
                self.df_trace[name_trace]
                .loc[self.index_df_trace_shuffled[name_trace]]
                .head(self.n_points[name_trace])
            )
            # symbol used for the trace
            self.trace_symbol[name_trace] = "circle"
            # attributes of the markers
            self.symbols[name_trace] = [self.trace_symbol[name_trace]] * self.n_points[
                name_trace
            ]
            self.sizes[name_trace] = [ConfigWidgets.marker_size] * self.n_points[name_trace]
            self.colors[name_trace] = [next(ConfigWidgets.palette)] * self.n_points[name_trace]




        self.viewer_l = py3Dmol.view(width='auto',height=400)
        self.viewer_r = py3Dmol.view(width='auto',height=400)
        self.visualizerConfigWidgets = ConfigWidgets(embedding_features, hover_features)
        self.visualizerTopWidgets = TopWidgets(self)
        self.visualizerUtilsWidgets = UtilsWidgets(self)
        self.visualizerViewersWiedgets = ViewersWidgets(self)
        self.visualizerUtilsButton = UtilsButton(self, self.visualizerUtilsWidgets, self.visualizerViewersWiedgets)
   
        if self.convex_hull == False:
            self.visualizerUtilsWidgets.widg_color_hull.disabled = True
            self.visualizerUtilsWidgets.widg_width_hull.disabled = True
            self.visualizerUtilsWidgets.widg_dash_hull.disabled = True

        if self.regr_line_coefs == None:
            self.visualizerUtilsWidgets.widg_color_line.disabled = True
            self.visualizerUtilsWidgets.widg_width_line.disabled = True
            self.visualizerUtilsWidgets.widg_dash_line.disabled = True
        


    def show(self):
        # displays the map and all widgets

        top_box = self.visualizerTopWidgets.container()
        top_box.layout.height = "140px"
        top_box.layout.top = "30px"
        
        utils_box = self.visualizerUtilsWidgets.container()
        utils_button = self.visualizerUtilsButton.container()
        viewer_box = self.visualizerViewersWiedgets.container()

        utils_button.layout.left = "50px"
        utils_box.layout.border = "dashed 1px"
        utils_box.right = "100px"
        utils_box.layout.max_width = "700px"
        utils_box.layout.visibility = "hidden"

        # jsmol visualizer is displayed only if there is a path to structures
        if self.path_to_structures:
            container = widgets.VBox(
                [
                    top_box,
                    self.fig,
                    utils_button,
                    viewer_box,
                    utils_box,
                ]
            )

        else:
            utils_box.layout.top = "10px"
            container = widgets.VBox(
                                [
                    top_box,
                    self.fig,
                    utils_button,
                    utils_box,
                ]
            )

        self.fract_change_updates()
        self.batch_update()

        display(container)
