import warnings

import pandas as pd
import ipywidgets as widgets

from IPython.display import display

from .top_widgets import TopWidgets
from .config_widgets import ConfigWidgets
from .utils_widgets import UtilsWidgets
from .viewers_widgets import ViewersWidgets
from .utils_button import UtilsButton
from .figure import Figure

from .config import Config
from .settings_widget import SettingsWidget
from .figure import FigureWidget
from .viewer_widget import AtomisticViewerWidget

warnings.simplefilter(action="ignore", category=FutureWarning)


class Visualizer2(widgets.Box):
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
        df: pd.DataFrame,
        embedding_features: list[str],
        hover_features: list[str],
        target: str,
        show_structures: bool = False,
    ):

        self.df = df
        self.embedding_features = embedding_features
        self.hover_features = hover_features
        self.target = target
        self.show_structures = show_structures

        self.config = Config()

        settings_widget = SettingsWidget(
            embedding_features,
            hover_features,
            embedding_features[0],
            embedding_features[1],
            1,
        )

        labels = df[target].unique().tolist()

        x = []
        y = []
        for label in labels:
            mask = df[target] == label
            x.append(df[embedding_features[0]][mask].to_numpy())
            y.append(df[embedding_features[1]][mask].to_numpy())

        figure = FigureWidget(x, y, labels=labels)

        viewer1 = AtomisticViewerWidget()
        viewer2 = AtomisticViewerWidget()

        children = [settings_widget, figure, widgets.HBox([viewer1, viewer2])]
        layout = widgets.Layout(
            display="flex",
            flex_flow="column",
            # border="solid 2px",
            align_items="stretch",
            # width="50%",
        )

        super().__init__(children, layout=layout)

        # self.visualizer_top_widgets.observe_changes(self.visualizer_figure, self.visualizer_utils_widgets)
        # self.visualizer_utils_widgets.observe_changes(self.visualizer_figure)
        # self.visualizer_viewers_widgets.observe_changes(self.visualizer_figure)
        # self.visualizer_utils_button.observe_changes(self.visualizer_figure, self.visualizer_utils_widgets, self.visualizer_viewers_widgets)


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
        df: pd.DataFrame,
        embedding_features: list[str],
        hover_features: list[str],
        target: str,
        path_to_structures: bool = False,
    ):

        self.path_to_structures = path_to_structures

        self.visualizer_config_widgets = ConfigWidgets()
        self.visualizer_figure = Figure(
            df, embedding_features, hover_features, target, path_to_structures
        )

        ConfigWidgets.hover_features = hover_features
        ConfigWidgets.embedding_features = embedding_features
        ConfigWidgets.feat_x = ConfigWidgets.embedding_features[0]
        ConfigWidgets.feat_y = ConfigWidgets.embedding_features[1]
        ConfigWidgets.fract = self.visualizer_figure.init_fract

        self.visualizer_top_widgets = TopWidgets()
        self.visualizer_utils_widgets = UtilsWidgets()
        self.visualizer_viewers_widgets = ViewersWidgets()
        self.visualizer_utils_button = UtilsButton()

        self.visualizer_top_widgets.observe_changes(
            self.visualizer_figure, self.visualizer_utils_widgets
        )
        self.visualizer_utils_widgets.observe_changes(self.visualizer_figure)
        self.visualizer_viewers_widgets.observe_changes(self.visualizer_figure)
        self.visualizer_utils_button.observe_changes(
            self.visualizer_figure,
            self.visualizer_utils_widgets,
            self.visualizer_viewers_widgets,
        )

    def show(self):
        # Displays the map and all widgets.

        top_box = self.visualizer_top_widgets.widg_box
        figure_widget = self.visualizer_figure.FigureWidget
        utils_box = self.visualizer_utils_widgets.widg_box
        utils_button = self.visualizer_utils_button.widget
        viewer_box = self.visualizer_viewers_widgets.widg_box

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

        self.visualizer_figure.batch_update(self.visualizer_config_widgets)

        display(container)

        if self.path_to_structures:
            with self.visualizer_viewers_widgets.windows_output_l.widget:
                self.visualizer_viewers_widgets.viewer_l.viewer.show()
            with self.visualizer_viewers_widgets.windows_output_r.widget:
                self.visualizer_viewers_widgets.viewer_r.viewer.show()

    def add_convex_hull(self):

        self.visualizer_figure.convex_hull = True
        self.visualizer_utils_widgets.color_hull.widget.disabled = False
        self.visualizer_utils_widgets.width_hull.widget.disabled = False
        self.visualizer_utils_widgets.dash_hull.widget.disabled = False

        self.visualizer_figure.batch_update(self.visualizer_config_widgets)

    def remove_convex_hull(self):

        self.visualizer_figure.convex_hull = False
        self.visualizer_utils_widgets.color_hull.widget.disabled = True
        self.visualizer_utils_widgets.width_hull.widget.disabled = True
        self.visualizer_utils_widgets.dash_hull.widget.disabled = True

        self.visualizer_figure.batch_update(self.visualizer_config_widgets)

    def add_regr_line(self, coefs, feat_x, feat_y):

        self.visualizer_figure.add_regr_line(
            coefs,
            feat_x,
            feat_y,
            self.visualizer_config_widgets,
            self.visualizer_utils_widgets.color_line.widget,
            self.visualizer_utils_widgets.width_line.widget,
            self.visualizer_utils_widgets.dash_line.widget,
        )

    def remove_regr_line(self, feat_x, feat_y):

        self.visualizer_figure.remove_regr_line(
            feat_x,
            feat_y,
            self.visualizer_config_widgets,
            self.visualizer_utils_widgets.color_line.widget,
            self.visualizer_utils_widgets.width_line.widget,
            self.visualizer_utils_widgets.dash_line.widget,
        )

    def optimize_fract(self):

        self.visualizer_figure.optimize_fract(
            self.visualizer_top_widgets, self.visualizer_config_widgets
        )
