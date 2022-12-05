import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from itertools import cycle
from scipy.spatial import ConvexHull
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors


class FigureWidget(go.FigureWidget):
    def __init__(self, x, y, labels, layout=None, **kwargs):

        self._x = x
        self._y = y
        self._labels = labels

        self._regression_trace = None
        self._convex_hull_traces = None

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

        self._regression_trace = go.Scatter(
            x=[p1[0], p2[0]], y=[p1[1], p2[1]], name="Line", mode="lines"
        )
        self.add_trace(self._regression_trace)

    def add_convex_hull(self):

        for (x, y, label) in zip(self._x, self._y, self._labels):
            if len(x) < 3:
                continue

            points = np.column_stack((x, y))
            hull = ConvexHull(points)

            inds = np.append(hull.vertices, hull.vertices[0])
            # TODO: use the same color as the datapoints
            self.add_trace(
                go.Scatter(x=x[inds], y=y[inds], name=f"{label} (hull)", mode="lines")
            )

            # for simplex in hull.simplices:
            #     self.add_trace(go.Scatter(x=points[simplex, 0], y=points[simplex, 1]))

