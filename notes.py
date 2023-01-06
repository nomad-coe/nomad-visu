import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import ipywidgets as widgets
import plotly.graph_objects as go
import plotly.express as px

from IPython.display import display, Markdown, FileLink

from itertools import cycle

from nomad_lab_visualizer.updates import (
    marker_style_updates,
    fract_change_updates,
    update_hover_variables,
)

from nomad_lab_visualizer.view_structure import view_structure_r, view_structure_l
from nomad_lab_visualizer.smart_fract import smart_fract_make
from nomad_lab_visualizer.instantiate_widgets import instantiate_widgets
from nomad_lab_visualizer.batch_update import batch_update


# TODO:
# - [ ] gui optino for target
# - [ ] switch on and off the convex hull
# - [ ] smart_fract as an preprocess
# - [ ] moving options out
#
# python api is same as: http://3dmol.csb.pitt.edu/doc/$3Dmol.GLViewer.html#toc0



# Generate data

N = 100

df = pd.DataFrame(np.random.randn(N, 4), columns=list("ABCD"))
df["E"] = pd.Series(np.random.randint(0, 10, size=N), dtype="category")
df["F"] = pd.Series(np.random.randint(-1, 2, size=N), dtype="category")
df
# df.dtypes

def resample(data):
    return data


def Visualize(
    data: pd.DataFrame,
    embedding_features: list[str],
    hover_features: list[str],
    target: list[str],
    smart_frac: float,
    convex_hull: bool,
    regr_line_,
    path_to_structures: list[str],
):
    """
    df: pandas dataframe containing all data to be visualized
    embedding_features: list of features used for embedding
    hover_features: list of features shown while hovering
    target: feature used to create traces (same target value - same trace)
    smart_frac: fraction of points is selected to maximize visualization of data distribution
    path_to_structures: path to a directory that contains all 'xyz' structures to be visualized
    """
    pass

    def add_comvex_hull(self):
        """
        convex hull is drawn around each trace
        """
        pass

    def add_regression_line(self, coefs: list[float]):
        """
        coefs: coeffs of a regression line
        """
        pass


# ????df = resample(df, fraction, target)

# visualiser = Visualize(df)
# visualiser.add_comvex_hull()
# visualiser.add_regression_line()

class FigureWidget:
    pass


class AtomisticViewer:
    pass


class SettingsWidget:
    pass


class Visualizer:
    def __init__(self, *args, **kwargs):

        self.figure = FigureWidget()
        self.viewer = AtomisticViewer()
        self.settings = SettingsWidget()

        # TODO: link events together between different widgets

def make(
    data: pd.DataFrame,
    embedding_features: list[str],
    hover_features: list[str],
    target: list[str],
    smart_frac: float,
    convex_hull: bool,
    regr_line_coefs: list[float],
    path_to_structures: list[str],
):
    """
    df: pandas dataframe containing all data to be visualized
    embedding_features: list of features used for embedding
    hover_features: list of features shown while hovering
    target: feature used to create traces (same target value - same trace)
    smart_frac: fraction of points is selected to maximize visualization of data distribution
    convex_hull: convex hull is drawn around each trace
    regr_line_coefs: coeffs of a regression line
    path_to_structures: path to a directory that contains all 'xyz' structures to be visualized
    """
    pass



# constants

# list of possible marker symbols
symbols_list = [
    "circle",
    "circle-open",
    "circle-dot",
    "circle-open-dot",
    "circle-cross",
    "circle-x",
    "square",
    "square-open",
    "square-dot",
    "square-open-dot",
    "square-cross",
    "square-x",
    "diamond",
    "diamond-open",
    "diamond-dot",
    "diamond-open-dot",
    "diamond-cross",
    "diamond-x",
    "triangle-up",
    "triangle-up-open",
    "triangle-up-dot",
    "triangle-up-open-dot",
    "triangle-down",
    "triangle-down-open",
    "triangle-down-dot",
    "triangle-down-open-dot",
]
# list of possible colors of the hulls
color_hull = [
    "Black",
    "Blue",
    "Cyan",
    "Green",
    "Grey",
    "Orange",
    "Red",
    "Yellow",
]
# list of possible colors of the regression line
color_line = [
    "Black",
    "Blue",
    "Cyan",
    "Green",
    "Grey",
    "Orange",
    "Red",
    "Yellow",
]
# list of possible dash types for the regression line
line_dashs = ["dash", "solid", "dot", "longdash", "dashdot", "longdashdot"]
# list of possible dash types for the hulls
hull_dashs = ["dash", "solid", "dot", "longdash", "dashdot", "longdashdot"]
# list of possible font families
font_families = [
    "Arial",
    "Courier New",
    "Helvetica",
    "Open Sans",
    "Times New Roman",
    "Verdana",
]
# list of possible font colors
font_color = [
    "Black",
    "Blue",
    "Cyan",
    "Green",
    "Grey",
    "Orange",
    "Red",
    "Yellow",
]
# list of possible discrete palette colors
discrete_palette_colors = [
    "Plotly",
    "D3",
    "G10",
    "T10",
    "Alphabet",
    "Dark24",
    "Light24",
    "Set1",
    "Pastel1",
    "Dark2",
    "Set2",
    "Pastel2",
    "Set3",
    "Antique",
    "Bold",
    "Pastel",
    "Prism",
    "Safe",
    "Vivid",
]
# list of possible continuous gradient colors
continuous_gradient_colors = px.colors.named_colorscales()




class Config:
    """ all values below are initialized to a specific value that can be modified using widgets
    """
    bg_color = "rgba(229,236,246, 0.5)"  # default value of the background color
    marker_size = 7  # size of all markers
    cross_size = 15  # size of the crosses
    min_value_markerfeat =  4  # min value of markers size if sizes represent a certain feature value
    max_value_markerfeat = 20  # max value of markers size if sizes represent a certain feature value
    font_size = 12  # size of fonts
    hull_width = 1  # width of the  the convex hull
    line_width = 1  # width of the regression line
    hull_dash = "solid"  # dash of the convex hull
    line_dash = "dash"  # dash of the regression line
    hull_color = "Grey"  # color of the convex hull
    line_color = "Black"  # color of the regression line


import ipywidgets as widgets
from ipywidgets import GridspecLayout
import ipywidgets as widgets
import plotly.graph_objects as go
import plotly.express as px

class Settings(GridspecLayout):
    def __init__(
        self,
        embedding_features,
        hover_features,
        feature_x,
        feature_y,
        fracture,
        **kwargs
    ):
        super().__init__(3, 3)

        widget_feature_x = widgets.Dropdown(
            description="x-axis",
            options=embedding_features,
            value=feature_x,
            layout=widgets.Layout(width="250px"),
        )

        widget_feature_y = widgets.Dropdown(
            description="y-axis",
            options=embedding_features,
            value=feature_y,
            layout=widgets.Layout(width="250px"),
        )

        widget_fracture = widgets.BoundedFloatText(
            min=0,
            max=1.0,
            # step=0.01,
            value=fracture,
            layout=widgets.Layout(left="98px", width="60px"),
        )

        widget_facture_label = widgets.Label(
            value="Fraction: ", layout=widgets.Layout(left="95px")
        )

        widget_feature_color = widgets.Dropdown(
            description="Color",
            options=["Default color"] + hover_features,
            value="Default color",
            layout=widgets.Layout(width="250px"),
        )

        widget_feature_color_type = widgets.RadioButtons(
            options=["Gradient", "Discrete"],
            value="Gradient",
            layout=widgets.Layout(width="140px", left="90px"),
        )

        widget_feature_color_list = widgets.Dropdown(
            options=px.colors.named_colorscales(),
            value="viridis",
            layout=widgets.Layout(width="65px", height="35px", left="40px"),
        )

        widget_feature_marker = widgets.Dropdown(
            description="Marker",
            options=["Default size"] + hover_features,
            value="Default size",
            layout=widgets.Layout(width="250px"),
        )
        widget_feature_marker_minvalue = widgets.BoundedFloatText(
            min=0,
            # max=self.max_value_markerfeat,
            step=1,
            # value=self.min_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px", height="10px"),
        )
        widget_feature_marker_minvalue_label = widgets.Label(
            value="Min value: ", layout=widgets.Layout(left="94px", width="70px")
        )
        widget_feature_marker_maxvalue = widgets.BoundedFloatText(
            # min=self.min_value_markerfeat,
            step=1,
            # value=self.max_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px"),
        )
        widget_feature_marker_maxvalue_label = widgets.Label(
            value="Max value: ", layout=widgets.Layout(left="94px", width="70px")
        )

        self[0, 0] = widget_feature_x
        self[1, 0] = widget_feature_y
        self[2, 0] = widgets.Box([widget_facture_label, widget_fracture])

        self[0, 1] = widget_feature_color
        self[1:, 1] = widgets.HBox(
            [widget_feature_color_type, widget_feature_color_list],
            layout=widgets.Layout(top="10px"),
        )

        self[0, 2] = widget_feature_marker
        self[1, 2] = widgets.Box(
            [
                widget_feature_marker_minvalue_label,
                widget_feature_marker_minvalue,
            ]
        )

        self[2, 2] = widgets.Box(
            [
                widget_feature_marker_maxvalue_label,
                widget_feature_marker_maxvalue,
            ]
        )

        self.layout.height = "140px"
        # self.layout.top = "30px"



embedding_features = ["A", "B", "C"]
hover_features = ["AA", "BB", "CC"]
feature_x = "A"
feature_y = "B"
fracture = 1.0

settings = Settings(
    embedding_features, hover_features, feature_x, feature_y, fracture
)
settings




class SettingsList(widgets.Box):
    def __init__(
        self,
        embedding_features,
        hover_features,
        feature_x,
        feature_y,
        fracture,
        **kwargs
    ):
        widget_feature_x = widgets.Dropdown(
            description="x-axis",
            options=embedding_features,
            value=feature_x,
            layout=widgets.Layout(width="250px"),
        )

        widget_feature_y = widgets.Dropdown(
            description="y-axis",
            options=embedding_features,
            value=feature_y,
            layout=widgets.Layout(width="250px"),
        )

        widget_fracture = widgets.BoundedFloatText(
            min=0,
            max=1.0,
            # step=0.01,
            value=fracture,
            layout=widgets.Layout(left="98px", width="60px"),
        )

        widget_feature_color = widgets.Dropdown(
            description="Color",
            options=["Default color"] + hover_features,
            value="Default color",
            layout=widgets.Layout(width="250px"),
        )

        widget_feature_color_type = widgets.RadioButtons(
            options=["Gradient", "Discrete"],
            value="Gradient",
            layout=widgets.Layout(width="140px", left="90px"),
        )

        widget_feature_color_list = widgets.Dropdown(
            options=px.colors.named_colorscales(),
            value="viridis",
            layout=widgets.Layout(width="65px", height="35px", left="40px"),
        )

        widget_feature_marker = widgets.Dropdown(
            description="Marker",
            options=["Default size"] + hover_features,
            value="Default size",
            layout=widgets.Layout(width="250px"),
        )
        widget_feature_marker_minvalue = widgets.BoundedFloatText(
            min=0,
            # max=self.max_value_markerfeat,
            step=1,
            # value=self.min_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px", height="10px"),
        )
        widget_feature_marker_minvalue_label = widgets.Label(
            value="Min value: ", layout=widgets.Layout(left="94px", width="70px")
        )
        widget_feature_marker_maxvalue = widgets.BoundedFloatText(
            # min=self.min_value_markerfeat,
            step=1,
            # value=self.max_value_markerfeat,
            layout=widgets.Layout(left="91px", width="60px"),
        )
        widget_feature_marker_maxvalue_label = widgets.Label(
            value="Max value: ", layout=widgets.Layout(left="94px", width="70px")
        )
        super().__init__(
            children=[
                widget_feature_x,
                widget_feature_y,
                widgets.Box(
                    [
                        widgets.Label(
                            value="Fraction: ", layout=widgets.Layout(left="95px")
                        ),
                        widget_fracture,
                    ]
                ),
                widget_feature_color,
                widgets.HBox(
                    [widget_feature_color_type, widget_feature_color_list],
                    layout=widgets.Layout(top="10px"),
                ),
                widget_feature_marker,
                widgets.Box(
                    [
                        widget_feature_marker_minvalue_label,
                        widget_feature_marker_minvalue,
                    ]
                ),
                widgets.Box(
                    [
                        widget_feature_marker_maxvalue_label,
                        widget_feature_marker_maxvalue,
                    ]
                ),
            ],
            layout=widgets.Layout(
                display="flex",
                flex_flow="column",
                border="solid 2px",
                align_items="stretch",
                # width="50%",
            ),
        )
        # self.layout.height = "140px"
        # self.layout.top = "30px"


embedding_features = ["A", "B", "C"]
hover_features = ["AA", "BB", "CC"]
feature_x = "A"
feature_y = "B"
fracture = 1.0

settings = SettingsList(
    embedding_features, hover_features, feature_x, feature_y, fracture
)
settings


# extract features

target = 'F'
feature_x = 'A'
feature_y = 'B'

labels = df[target].unique().tolist()

x = []
y = []
for label in labels:
    mask = df['F']==label
    x.append(df[feature_x][mask].to_numpy())
    y.append(df[feature_y][mask].to_numpy())

# TODO dict for
# TODO: default: points = np.column_stack((x, y))

from scipy.spatial import ConvexHull, convex_hull_plot_2d

class Figure(go.FigureWidget):
    def __init__(self, x, y, labels, layout=None, **kwargs):

        self._x = x
        self._y = y
        self._labels = labels

        self._regression_trace = None
        self._complex_hull_traces = None

        super().__init__(None, layout, **kwargs)

        # All permanent layout settings are defined here
        self.update_layout(
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
            width=800,
            height=400,
            margin=dict(l=50, r=50, b=70, t=20, pad=4),
        )
        self.update_xaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )
        self.update_yaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )

        for (x, y, label) in zip(x, y, labels):
            self.add_trace(go.Scatter(x=x, y=y, name=label, mode="markers"))

    def add_regression_line(self, p1, p2):
        """
        Note: solution of the intersection of the line and the boundary box
        Arguments:
        - p1: point in 2d
        - p2: point in 2d
        """

        self._regression_trace = go.Scatter(x = [p1[0], p2[0]],y = [p1[1], p2[1]], name="Line", mode="lines")
        self.add_trace(self._regression_trace)

    def add_complex_hull(self):

        for (x, y, label) in zip(self._x, self._y, self._labels):
            if len(x) < 3: continue

            points = np.column_stack((x, y))
            hull = ConvexHull(points)

            inds = np.append(hull.vertices, hull.vertices[0])
            # TODO: use the same color as the datapoints
            self.add_trace(go.Scatter(x=x[inds], y=y[inds], name=f'{label} (hull)', mode="lines"))

            # for simplex in hull.simplices:
            #     self.add_trace(go.Scatter(x=points[simplex, 0], y=points[simplex, 1]))


fig = Figure(x, y, labels)
fig.add_complex_hull()

fig.add_regression_line([-2,-2], [2,3])
fig
