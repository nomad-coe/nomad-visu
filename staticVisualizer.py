from turtle import update
from xml.etree.ElementInclude import include
import plotly.graph_objects as go
import ipywidgets as widgets
from jupyter_jsmol import JsmolView
import numpy as np
from IPython.display import display
from itertools import cycle
import plotly.express as px
import os

from include._smart_fract import smart_fract_make
from include._instantiate_widgets import instantiate_widgets
from include._updates import update_hover_variables
from include._batch_update import batch_update

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



class StaticVisualizer:

    def __init__(
        self, 
        df, 
        embedding_features, 
        hover_features, 
        target,
        smart_fract=False, 
        convex_hull=False, 
        regr_line_coefs=None, 
        path_to_structures=None
        ):

        # df - pandas dataframe containing all data to be visualized
        # sisso - sisso objects 
        # embedding_features - list of features used for embedding
        # hover features - list of features shown while hovering

        self.df = df
        self.target = target
        self.smart_fract = smart_fract
        self.trace_name = df[target].unique().astype(str)
        self.structures_list = df.index.tolist()
        self.embedding_features = embedding_features
        self.feat_x = embedding_features[0]
        self.feat_y = embedding_features[1]
        self.hover_features = hover_features
        self.path_to_structures = path_to_structures
        self.convex_hull = convex_hull
        self.regr_line_coefs = regr_line_coefs

        self.replica_l = 0
        self.replica_r = 0
        self.fract = 1

        self.marker_size = 7
        self.cross_size = 15
        self.min_value_markerfeat = 4
        self.max_value_markerfeat = 20
        self.font_size = 12
        self.width_hull = 1
        self.width_line = 1
        self.style_line = 'solid'
        self.hullsline_width = 1
        self.bg_color_default = 'rgba(229,236,246, 0.5)'
        self.bg_color = self.bg_color_default
        self.bg_toggle = True

        if self.path_to_structures:
            self.df['File'] = self.df['Structure'].apply( lambda x :  os.listdir( x))
            self.df['Replicas'] = self.df['Structure'].apply( lambda x :  len(os.listdir(x)) )


        self.symbols_list = [
            'circle',
            'circle-open',
            'circle-dot',
            'circle-open-dot',
            'circle-cross',
            'circle-x',
            'square',
            'square-open',
            'square-dot',
            'square-open-dot',
            'square-cross',
            'square-x',
            'diamond',
            'diamond-open',
            'diamond-dot',
            'diamond-open-dot',
            'diamond-cross',
            'diamond-x',
            'triangle-up',
            'triangle-up-open',
            'triangle-up-dot',
            'triangle-up-open-dot',
            'triangle-down',
            'triangle-down-open',
            'triangle-down-dot',
            'triangle-down-open-dot',
        ]
        self.color_hull = [
            'Black',
            'Blue',
            "Cyan",
            'Green',
            'Grey',
            "Orange",
            'Red',
            "Yellow",
        ]
        self.color_line = [
            'Black',
            'Blue',
            "Cyan",
            'Green',
            'Grey',
            "Orange",
            'Red',
            "Yellow",
        ]
        self.font_families = [
            'Arial',
            'Courier New',
            'Helvetica',
            "Open Sans", 
            'Times New Roman',
            'Verdana'                              
            ]
        self.font_color = [
            'Black',
            'Blue',
            "Cyan",
            'Green',
            'Grey',
            "Orange",
            'Red',
            "Yellow",
        ]
        self.line_styles = [
            "dash",
            "solid",
            "dot",
            "longdash",
            "dashdot",
            "longdashdot"
            ]
        self.hull_styles = [
            "dash",
            "solid",
            "dot",
            "longdash",
            "dashdot",
            "longdashdot"
            ]
        self.qualitative_colors = [
            'Plotly',
            'D3',
            'G10',
            'T10',
            'Alphabet',
            'Dark24',
            'Light24',
            'Set1',
            'Pastel1',
            'Dark2',
            'Set2',
            'Pastel2',
            'Set3',
            'Antique',
            'Bold',
            'Pastel',
            'Prism',
            'Safe',
            'Vivid'
        ]
        self.gradient_list = px.colors.named_colorscales() 
        
        

        # The 'target' feature is used to divide data into different classes 
        # Each item in the following lists will be related to a different class in the dataframe
        # For each different class a new trace is created

        self.trace = {}  # trace related to the class
        self.df_trace = {}  # section of the pandas dataframe containing elements of only a specific class
        self.index_classes_shuffled = {}  # index of the dataframe class shuffled - used to avoid bias visualization when only a fraction is visualized
        self.n_points = {}  # total points of the class which are visualized - can be less than the total number of data depending on the fraction visualized
        self.df_trace_on_map = {}  # dataframe which contains only the elements that are visualized on the map
        self.symbols = {}  # each item is a list of symbols
        self.sizes = {}  # each item is a list of sizes
        self.colors = {}  # each item is a list of colors
        self.trace_symbol = {}

        self.palette = cycle(getattr(px.colors.qualitative, self.qualitative_colors[0]))  # each class has by default a different color

        self.fig = go.FigureWidget()
        self.viewer_l = JsmolView()
        self.viewer_r = JsmolView()


        # All different classes are iterated and a class-specific item is added to the list defined above 
        for cl  in range (len(self.trace_name)):

            name_trace = self.trace_name[cl]

            self.df_trace[name_trace] = (self.df.loc[self.df[self.target] == self.df[target].unique()[cl]])

            self.fig.add_trace(
                    go.Scatter(
                        name=name_trace,
                        mode='markers',
                    ))                    
            self.trace[name_trace] = self.fig['data'][-1]

            if ( self.convex_hull == True ) :
                name_trace = 'Hull ' + name_trace
                self.fig.add_trace(
                        go.Scatter(
                            name=name_trace,
                    ))
                self.trace[name_trace] = self.fig['data'][-1]

        if self.regr_line_coefs :
            name_trace = 'Line'
            self.fig.add_trace(
                go.Scatter(
                    name=name_trace
                ))
            self.trace[name_trace] = self.fig['data'][-1]
        
        if (self.smart_fract):
            fract_dict, fract_thres = smart_fract_make(self)
            self.fract_dict = fract_dict
            self.fract_thres = fract_thres
            self.fract = self.fract_thres[(self.feat_x,self.feat_y)]

        for name_trace in self.trace_name:

            if ( self.smart_fract == False):
                self.index_classes_shuffled[name_trace] = self.df_trace[name_trace].index.to_numpy()[np.random.permutation(self.df_trace[name_trace].shape[0])]
            else:
                self.index_classes_shuffled[name_trace] = self.fract_dict[(self.feat_x,self.feat_y)][name_trace]

            self.n_points[name_trace] = int(self.fract * self.df_trace[name_trace].shape[0])
            self.df_trace_on_map[name_trace] = self.df_trace[name_trace].loc[self.index_classes_shuffled[name_trace]].head(self.n_points[name_trace])

            self.trace_symbol[name_trace] = 'circle'
            self.symbols[name_trace] = [self.trace_symbol[name_trace]] * self.n_points[name_trace]
            self.sizes[name_trace] = ([self.marker_size] * self.n_points[name_trace])
            self.colors[name_trace] = ([next(self.palette)] * self.n_points[name_trace])

        # All permanent layout settings are defined here - functions below do not change these fields
        self.fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            width=800,
            height=400,
            margin=dict(
                l=50,
                r=50,
                b=70,
                t=20,
                pad=4
            ),
        )
        self.fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor='black')
        self.fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor='black')


        instantiate_widgets(self)
        update_hover_variables(self)
        batch_update(self)


    
    def show(self):
        with self.output_l:
            display(self.viewer_l)
        with self.output_r:
            display(self.viewer_r)


        self.box_feat.layout.height = '140px'
        self.box_feat.layout.top = '30px'
        self.widg_utils_button.layout.left = '50px'
        self.widg_box_utils.layout.border = 'dashed 1px'
        self.widg_box_utils.right = '100px'
        self.widg_box_utils.layout.max_width = '700px'
        self.widg_box_utils.layout.visibility = 'hidden'


        if self.convex_hull == False:
            self.widg_color_hull.disabled = True
            self.widg_width_hull.disabled = True
            self.widg_style_hull.disabled = True

        if self.regr_line_coefs == None:
            self.widg_color_line.disabled = True
            self.widg_width_line.disabled = True
            self.widg_style_line.disabled = True

        if self.path_to_structures:
            container = widgets.VBox([
                self.box_feat,
                self.fig,
                self.widg_utils_button,
                self.widg_box_viewers,
                self.widg_box_utils
            ])
        else :
            self.widg_box_utils.layout.top = '10px'
            container = widgets.VBox([
                self.box_feat,
                self.fig,
                self.widg_utils_button,
                self.widg_box_utils
            ])

        display(container)
