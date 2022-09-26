from importlib.resources import path
from turtle import update
from xml.etree.ElementInclude import include
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
from .figure import Figure
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

    def __init__(
        self,
        df,
        embedding_features,
        hover_features, 
        target,
        smart_fract=False,
        regr_line_coefs=None,
        path_to_structures=None,
    ):

        self.df = df
        self.target = target
        self.smart_fract = smart_fract
        # each unique value of the 'target' feature gives the name of a different trace
        self.embedding_features = embedding_features

        self.hover_features = hover_features
        self.path_to_structures = path_to_structures
        self.regr_line_coefs = regr_line_coefs

        if path_to_structures:
            # each row in the dataframe is expected to be identified with a different structure
            # List of all files found in the directory pointed by 'Structure'
            self.df["File"] = self.df["Structure"].apply(lambda x: os.listdir(x))
            # Number of files found in the directory pointed by 'Structure'
            self.df["Replicas"] = self.df["Structure"].apply(
                lambda x: len(os.listdir(x))
            )

        ConfigWidgets.hover_features = hover_features
        ConfigWidgets.embedding_features = embedding_features
        ConfigWidgets.feat_x = ConfigWidgets.embedding_features[0]
        ConfigWidgets.feat_y = ConfigWidgets.embedding_features[1]

        self.visualizerConfigWidgets = ConfigWidgets()
        self.visualizerFigure = Figure(df, embedding_features, hover_features, target, smart_fract, regr_line_coefs, path_to_structures )
        self.visualizerFigure.batch_update(self.visualizerConfigWidgets)
       
        self.viewer_l = py3Dmol.view(width='auto',height=400)
        self.viewer_r = py3Dmol.view(width='auto',height=400)

        self.visualizerTopWidgets = TopWidgets(self.visualizerFigure)
        self.visualizerUtilsWidgets = UtilsWidgets(self.visualizerFigure)
        self.visualizerViewersWiedgets = ViewersWidgets(self.visualizerFigure)
        self.visualizerUtilsButton = UtilsButton(self.visualizerFigure, self.visualizerUtilsWidgets, self.visualizerViewersWiedgets)

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
        figure_widget = self.visualizerFigure.FigureWidget        
        utils_box = self.visualizerUtilsWidgets.container()
        utils_button = self.visualizerUtilsButton.container()
        viewer_box = self.visualizerViewersWiedgets.container()
        

        top_box.layout.height = "140px"
        top_box.layout.top = "30px"
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
                    figure_widget,
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

        display(container)

    def add_convex_hull (self):
        
        ConfigWidgets.convex_hull = True

        self.visualizerUtilsWidgets.widg_color_hull.disabled = False
        self.visualizerUtilsWidgets.widg_width_hull.disabled = False
        self.visualizerUtilsWidgets.widg_dash_hull.disabled = False

        self.visualizerFigure.batch_update(self.visualizerConfigWidgets)

    def remove_convex_hull (self):
        
        ConfigWidgets.convex_hull = False

        self.visualizerUtilsWidgets.widg_color_hull.disabled = True
        self.visualizerUtilsWidgets.widg_width_hull.disabled = True
        self.visualizerUtilsWidgets.widg_dash_hull.disabled = True

        self.visualizerFigure.batch_update(self.visualizerConfigWidgets)