import plotly.graph_objects as go
import ipywidgets as widgets
from jupyter_jsmol import JsmolView
import numpy as np
from IPython.display import display, Markdown, FileLink
import os
from scipy.spatial import ConvexHull
import copy
import pandas as pd

class Visualizer:
    def __init__(self, df, sisso, classes):
        self.sisso = sisso
        self.df = df
        self.class0 = str(classes[0])
        self.class1 = str(classes[1])
        self.marker_size = 7
        self.marker_symbol_cls0 = 'circle'
        self.marker_symbol_cls1 = 'square'
        self.symbols = [
            'circle',
            'square',
            'triangle-up',
            'triangle-down',
            'circle-cross',
            'circle-x'
        ]
        self.font_size = 12
        self.cross_size = 15
        self.hullsline_width = 1
        self.clsline_width = 1
        self.font_families = ['Source Sans Pro',
                              'Helvetica',
                              'Open Sans',
                              'Times New Roman',
                              'Arial',
                              'Verdana',
                              'Courier New',
                              'Comic Sans MS',
                              ]
        self.line_styles = ["dash",
                            "solid",
                            "dot",
                            "longdash",
                            "dashdot",
                            "longdashdot"]
        self.gradient_list = ['Blue to red',
                              'Blue to green',
                              'Green to red',
                              'Grey scale',
                              'Purple scale',
                              'Turquoise scale']
        self.bg_color = 'rgba(229,236,246, 0.5)'
        self.color_cls1 = "#EB8273"
        self.color_cls0 = "rgb(138, 147, 248)"
        self.color_hull0 = 'Grey'
        self.color_hull1 = 'Grey'
        self.color_line = 'Black'

    def print(self):
        print (self.symbols)