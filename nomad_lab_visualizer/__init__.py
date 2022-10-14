import ipywidgets as widgets
from IPython.display import display
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
        df: pandas dataframe containing all data to be visualized.
        embedding_features: list of features used for embedding.
        hover features: list of features shown while hovering.
        target: feature used to create traces (same target value - same trace).
        path_to_structures: true if dataframe contains a 'structure' columns with path to structures.
    """

    def __init__(
        self,
        df,
        embedding_features,
        hover_features, 
        target,
        path_to_structures=None,
    ):

        self.path_to_structures = path_to_structures

        self.visualizerConfigWidgets = ConfigWidgets()
        self.visualizerFigure = Figure(df, embedding_features, hover_features, target, path_to_structures )

        ConfigWidgets.hover_features = hover_features
        ConfigWidgets.embedding_features = embedding_features
        ConfigWidgets.feat_x = ConfigWidgets.embedding_features[0]
        ConfigWidgets.feat_y = ConfigWidgets.embedding_features[1]
        ConfigWidgets.fract = self.visualizerFigure.init_fract
        
        self.visualizerTopWidgets = TopWidgets()
        self.visualizerUtilsWidgets = UtilsWidgets()
        self.visualizerViewersWidgets = ViewersWidgets()
        self.visualizerUtilsButton = UtilsButton()

        self.visualizerTopWidgets.observe_changes(self.visualizerFigure, self.visualizerUtilsWidgets)
        self.visualizerUtilsWidgets.observe_changes(self.visualizerFigure)
        self.visualizerViewersWidgets.observe_changes(self.visualizerFigure)
        self.visualizerUtilsButton.observe_changes(self.visualizerFigure, self.visualizerUtilsWidgets, self.visualizerViewersWidgets)
        

    def show(self):
        # Displays the map and all widgets.

        top_box = self.visualizerTopWidgets.widg_box
        figure_widget = self.visualizerFigure.FigureWidget        
        utils_box = self.visualizerUtilsWidgets.widg_box
        utils_button = self.visualizerUtilsButton.widget
        viewer_box = self.visualizerViewersWidgets.widg_box
        
        top_box.layout.height = "140px"
        top_box.layout.top = "30px"
        utils_button.layout.left = "50px"
        utils_box.layout.border = "dashed 1px"
        utils_box.layout.max_width = "700px"
        utils_box.layout.visibility = "hidden"

        # Structure visualizer is displayed only if there is a path to structures
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

        self.visualizerFigure.batch_update(self.visualizerConfigWidgets)

        display(container)

        if self.path_to_structures:
            with self.visualizerViewersWidgets.windowsOutputL.widget:
                self.visualizerViewersWidgets.viewerL.viewer.show()
            with self.visualizerViewersWidgets.windowsOutputR.widget:
                self.visualizerViewersWidgets.viewerR.viewer.show()



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

        self.visualizerFigure.add_regr_line(
            coefs, 
            feat_x, 
            feat_y, 
            self.visualizerConfigWidgets,
            self.visualizerUtilsWidgets.ColorLine.widget,
            self.visualizerUtilsWidgets.WidthLine.widget,
            self.visualizerUtilsWidgets.DashLine.widget
            )

    def remove_regr_line (self, feat_x, feat_y):

        self.visualizerFigure.remove_regr_line( 
            feat_x, 
            feat_y, 
            self.visualizerConfigWidgets,
            self.visualizerUtilsWidgets.ColorLine.widget,
            self.visualizerUtilsWidgets.WidthLine.widget,
            self.visualizerUtilsWidgets.DashLine.widget
            )

    def optimize_fract (self):

        self.visualizerFigure.optimize_fract(self.visualizerTopWidgets, self.visualizerConfigWidgets)