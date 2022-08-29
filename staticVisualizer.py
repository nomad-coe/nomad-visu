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
        # embedding_features - list of features used for embedding
        # hover features - list of features shown while hovering
        # target - feature used to create traces (same target value - same trace) 
        # smart_frac - fraction of points is selected to maximize visualization of data distribution
        # convex_hull - convex hull is drawn around each trace
        # regr_line_coefs - coeffs of a regression line
        # path_to_structures - path to a directory that contains all 'xyz' structures to be visualized

        self.df = df
        self.target = target
        self.smart_fract = smart_fract
        # each unique value of the 'target' feature gives the name of a different trace
        self.trace_name = df[target].unique().astype(str) 
        self.embedding_features = embedding_features
        # x-axis is taken as the first value in the 'embedding_features' list
        self.feat_x = embedding_features[0]
        # y-axis is taken as the second value in the 'embedding_features' list
        self.feat_y = embedding_features[1]
        self.hover_features = hover_features
        self.path_to_structures = path_to_structures
        self.convex_hull = convex_hull
        self.regr_line_coefs = regr_line_coefs
        self.bg_color_default = 'rgba(229,236,246, 0.5)' # default value of the background color


        # fraction to be initially visualized is set to be 1
        # this value is eventually modified later if 'smart_frac' is true 
        self.fract = 1

        # all values below are initialized to a specific value that can be modified using widgets
        self.marker_size = 7 # size of all markers
        self.cross_size = 15 # size of the crosses
        self.min_value_markerfeat = 4 # min value of markers size if sizes represent a certain feature value
        self.max_value_markerfeat = 20 # max value of markers size if sizes represent a certain feature value
        self.font_size = 12 # size of fonts
        self.hull_width = 1 # width of the  the convex hull
        self.line_width = 1 # width of the regression line
        self.hull_dash = 'solid' # dash of the convex hull
        self.line_dash = 'dash' # dash of the regression line
        self.hull_color = 'Grey' # color of the convex hull
        self.line_color = 'Black' # color of the regression line
        self.bg_color = self.bg_color_default # background color initially set to its default value
        self.bg_toggle = True # background color is shown

        if self.path_to_structures:
            # each row in the dataframe is expected to be identified with a different structure 
            self.structures_list = df.index.tolist()
            # List of all files found in the directory pointed by 'Structure'
            self.df['File'] = self.df['Structure'].apply( lambda x :  os.listdir(x))
            # Number of files found in the directory pointed by 'Structure'
            self.df['Replicas'] = self.df['Structure'].apply( lambda x :  len(os.listdir(x)) )
            # which file in the list is shown in the left visualizer
            self.replica_l = 0
            # which file in the list is shown in the right visualizer
            self.replica_r = 0

        # list of possible marker symbols
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
        # list of possible colors of the hulls
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
        # list of possible colors of the regression line
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
        # list of possible dash types for the regression line
        self.line_dashs = [
            "dash",
            "solid",
            "dot",
            "longdash",
            "dashdot",
            "longdashdot"
            ]
        # list of possible dash types for the hulls
        self.hull_dashs = [
            "dash",
            "solid",
            "dot",
            "longdash",
            "dashdot",
            "longdashdot"
            ]
        # list of possible font families
        self.font_families = [
            'Arial',
            'Courier New',
            'Helvetica',
            "Open Sans", 
            'Times New Roman',
            'Verdana'                              
            ]
        # list of possible font colors
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
        # list of possible discrete palette colors
        self.discrete_palette_colors = [
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
        # list of possible continuous gradient colors
        self.continuous_gradient_colors = px.colors.named_colorscales() 

        

        # The 'target' feature is used to divide data into different traces 
        # Each item in the following dictionaries will be related to a different trace in the dataframe
        # For each different 'target' value a new trace is created

        self.trace = {} 
        self.df_trace = {}  # section of the pandas dataframe containing elements of a specific trace
        self.index_df_trace_shuffled = {}  # index of the dataframe trace shuffled for fraction visualization
        self.n_points = {}  # total points of the class which are visualized - can be less than the total number of data depending on the fraction visualized
        self.df_trace_on_map = {}  # dataframe which contains only the elements that are visualized on the map
        self.symbols = {}  # symbols used for markers of each trace
        self.sizes = {}  # sizes used for markers of each trace
        self.colors = {}  # colors used for markers of each trace
        self.trace_symbol = {} # symbol used for the trace


        self.fig = go.FigureWidget()
        self.viewer_l = JsmolView()
        self.viewer_r = JsmolView()

        # palette used for the initial values
        palette = cycle(getattr(px.colors.qualitative, self.discrete_palette_colors[0]))

        # dictionaries initialized above are compiled for all different trace names
        for cl  in range (len(self.trace_name)):

            name_trace = self.trace_name[cl]

            self.df_trace[name_trace] = (self.df.loc[self.df[self.target] == self.df[target].unique()[cl]])

            # a trace with a specific name taken from the 'target' values is constructed and assigned to the 'trace' dictionary
            self.fig.add_trace(
                    go.Scatter(
                        name=name_trace,
                        mode='markers',
                    ))                    
            self.trace[name_trace] = self.fig['data'][-1]

            # add a convex hull for each different 'target' value 
            if ( self.convex_hull ) :
                name_trace = 'Hull ' + name_trace
                self.fig.add_trace(
                        go.Scatter(
                            name=name_trace,
                    ))
                self.trace[name_trace] = self.fig['data'][-1]

        # add a trace that contains the regression line
        if self.regr_line_coefs :
            name_trace = 'Line'
            self.fig.add_trace(
                go.Scatter(
                    name=name_trace
                ))
            self.trace[name_trace] = self.fig['data'][-1]
        
        # the shuffled values for fraction visualization are given using a max covering algorithm
        if (self.smart_fract):
            fract_dict, fract_thres = smart_fract_make(self)
            # each pair of features has a different list of shuffled values accessbile in the dictionary 'fract_dict'
            self.fract_dict = fract_dict
            # each pair of features has a different initial fraction value accessbile in the dictionary 'fract_thres'
            self.fract_thres = fract_thres
            self.fract = self.fract_thres[(self.feat_x,self.feat_y)]

        for name_trace in self.trace_name:
            
            # shuffled values are taken randomly if not 'smart_fract'
            if ( self.smart_fract == False):
                self.index_df_trace_shuffled[name_trace] = self.df_trace[name_trace].index.to_numpy()[np.random.permutation(self.df_trace[name_trace].shape[0])]
            else:
                self.index_df_trace_shuffled[name_trace] = self.fract_dict[(self.feat_x,self.feat_y)][name_trace]

            # number of points visualized given by a certain fraction
            self.n_points[name_trace] = int(self.fract * self.df_trace[name_trace].shape[0])
            # fraction of the dataframe that is visualized on the map 
            self.df_trace_on_map[name_trace] = self.df_trace[name_trace].loc[self.index_df_trace_shuffled[name_trace]].head(self.n_points[name_trace])
            # symbol used for the trace
            self.trace_symbol[name_trace] = 'circle'
            # attributes of the markers
            self.symbols[name_trace] = [self.trace_symbol[name_trace]] * self.n_points[name_trace]
            self.sizes[name_trace] = ([self.marker_size] * self.n_points[name_trace])
            self.colors[name_trace] = ([next(palette)] * self.n_points[name_trace])

        # All permanent layout settings are defined here
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

        # widgets are instantiated
        instantiate_widgets(self)
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
            self.widg_dash_hull.disabled = True

        if self.regr_line_coefs == None:
            self.widg_color_line.disabled = True
            self.widg_width_line.disabled = True
            self.widg_dash_line.disabled = True


    
    def show(self):
        # displays the map and all widgets

        with self.output_l:
            display(self.viewer_l)
        with self.output_r:
            display(self.viewer_r)

        # jsmol visualizer is displayed only if there is a path to structes
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


        update_hover_variables(self)
        batch_update(self)

        display(container)
