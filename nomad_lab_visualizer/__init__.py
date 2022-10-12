import ipywidgets as widgets
from IPython.display import display
import os
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

from .topWidgets import TopWidgets
from .configWidgets import ConfigWidgets
from .utilsWidgets import UtilsWidgets
from .viewersWidgets import ViewersWidgets
from .utilsButton import UtilsButton
from .figure import Figure


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
        path_to_structures=None,
    ):

        self.df = df
        self.target = target

        # each unique value of the 'target' feature gives the name of a different trace
        self.embedding_features = embedding_features

        self.hover_features = hover_features
        self.path_to_structures = path_to_structures

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
        self.visualizerFigure = Figure(df, embedding_features, hover_features, target, path_to_structures )
       
        total_points = self.df.shape[0]
        if (total_points>1000):
            init_fract = 1000/total_points
            self.visualizerFigure.init_fract = init_fract
            ConfigWidgets.fract = init_fract
        
        self.visualizerFigure.batch_update(self.visualizerConfigWidgets)

        self.visualizerTopWidgets = TopWidgets(self.visualizerFigure)
        self.visualizerUtilsWidgets = UtilsWidgets(self.visualizerFigure)
        self.visualizerViewersWiedgets = ViewersWidgets(self.visualizerFigure)
        self.visualizerUtilsButton = UtilsButton(self.visualizerFigure, self.visualizerUtilsWidgets, self.visualizerViewersWiedgets)

        self.visualizerUtilsWidgets.ColorHull.widget.disabled = True
        self.visualizerUtilsWidgets.WidthHull.widget.disabled = True
        self.visualizerUtilsWidgets.DashHull.widget.disabled = True

        # self.visualizerUtilsWidgets.widg_color_line.disabled = True
        # self.visualizerUtilsWidgets.widg_width_line.disabled = True
        # self.visualizerUtilsWidgets.widg_dash_line.disabled = True
        

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
                    figure_widget,
                    utils_button,
                    utils_box,
                ]
            )
        display(container)

        with self.visualizerViewersWiedgets.windowsOutputL.widget:
            self.visualizerViewersWiedgets.viewerL.viewer.show()
        with self.visualizerViewersWiedgets.windowsOutputR.widget:
            self.visualizerViewersWiedgets.viewerR.viewer.show()

    def add_convex_hull (self):
        
        self.visualizerFigure.convex_hull = True

        self.visualizerUtilsWidgets.ColorHull.widget.disabled = False
        self.visualizerUtilsWidgets.WidthHull.widget.disabled = False
        self.visualizerUtilsWidgets.DashHull.widget.disabled = False

        self.visualizerFigure.batch_update(self.visualizerConfigWidgets)

    def remove_convex_hull (self):
        
        self.visualizerFigure.convex_hull = False
        self.visualizerUtilsWidgets.ColorHull.widget.disabled = True
        self.visualizerUtilsWidgets.WidthHull.widget.disabled = True
        self.visualizerUtilsWidgets.DashHull.widget.disabled = True

        self.visualizerFigure.batch_update(self.visualizerConfigWidgets)

    def add_regr_line (self, coefs, feat_x, feat_y):

        self.visualizerFigure.add_regr_line(coefs, feat_x, feat_y, self.visualizerConfigWidgets)

    def remove_regr_line (self, feat_x, feat_y):

        self.visualizerFigure.remove_regr_line( feat_x, feat_y, self.visualizerConfigWidgets)

    def optimize_fract (self):

        self.visualizerFigure.optimize_fract(self.visualizerTopWidgets, self.visualizerConfigWidgets)