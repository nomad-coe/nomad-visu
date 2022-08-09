from turtle import update
from xml.etree.ElementInclude import include
import plotly.graph_objects as go
import ipywidgets as widgets
from jupyter_jsmol import JsmolView
import numpy as np
from IPython.display import display
from itertools import cycle
import plotly.express as px
from include._sisso  import regr_line
from include._max_covering import max_covering_shuffle
import os

class StaticVisualizer:

    def __init__(
        self, 
        df, 
        embedding_features, 
        hover_features, 
        target,
        max_covering=False, 
        convex_hull=False, 
        regr_line_coefs=None, 
        path_to_structures=None
        ):

        # df - pandas dataframe containing all data to be visualized
        # sisso - sisso objects 
        # embedding_features - list of features used for embedding
        # hover features - list of features shown while hovering

        from include._instantiate_widgets import instantiate_widgets
        from include._updates import update_hover_variables, update_layout_figure, update_markers_size

        self.convex_hull = convex_hull
        self.df = df
        self.target = target
        self.max_covering = max_covering

        self.n_classes = df[target].unique().size
        self.classes = df[target].unique()
        self.embedding_features = embedding_features
        self.feat_x = embedding_features[0]
        self.feat_y = embedding_features[1]
        self.hover_features = hover_features
        self.total_compounds = df.shape[0]
        self.path_to_structures = path_to_structures

        self.replica_l = 0
        self.replica_r = 0

        self.frac_init = []
        self.frac = 1
        # self.frac = (1000 / self.total_compounds)
        # if self.frac > 1:
        #     self.frac = 1
        # self.frac = int(self.frac * 100) / 100
        self.marker_size = 7
        self.cross_size = 15

        self.compounds_list = df.index.tolist()
        self.symbols_list = [
            'circle',
            'square',
            'triangle-up',
            'triangle-down',
            'circle-cross',
            'circle-x'
        ]
        self.class_symbol = {}
        self.font_size = 12
        self.width_hull = 1
        self.style_hull = 'dash'
        self.color_hull = [
            'black',
            'grey',
            'green',
            'blue',
            'red',
            "yellow",
            "cyan",
            "orange",
            "purple",
        ]
        self.width_line = 1
        self.style_line = 'solid'
        self.color_line = [
            'black',
            'grey',
            'green',
            'blue',
            'red',
            "yellow",
            "cyan",
            "orange",
            "purple",
        ]
        self.hullsline_width = 1
        self.clsline_width = 1
        self.font_families = ['Source Sans Pro',
                              'Helvetica',
                              'Open Sans',
                              'Times New Roman',
                              'Arial',
                              'Verdana',
                              'Courier New',
                              'Comic Sans MS']
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
        self.bg_color_default = 'rgba(229,236,246, 0.5)'
        self.bg_color = self.bg_color_default
        self.bg_toggle = True
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
        self.regr_line_coefs = regr_line_coefs
            


        # The 'target' feature is used to divide data into different classes 
        # Each item in the following lists will be related to a different class in the dataframe
        # For each different class a new trace is created
        self.name_trace = []  # name of the trace that is given by the specific 'target' feature
        self.trace = {}  # trace related to the class
        self.df_classes = []  # section of the pandas dataframe containing elements of only a specific class
        self.index_classes_shuffled = []  # index of the dataframe class shuffled - used to avoid bias visualization when only a fraction is visualized
        self.n_points = {}  # total points of the class which are visualized - can be less than the total number of data depending on the fraction visualized
        self.df_classes_on_map = []  # dataframe which contains only the elements that are visualized on the map
        self.symbols = {}  # each item is a list of symbols
        self.sizes = {}  # each item is a list of sizes
        self.colors = {}  # each item is a list of colors
        self.palette = cycle(
            getattr(px.colors.qualitative, self.qualitative_colors[0]))  # each class has by default a different color

        self.fig = go.FigureWidget()
        self.viewer_l = JsmolView()
        self.viewer_r = JsmolView()

        # All different classes are iterated and a class-specific item is added to the list defined above 
        for cl in range(self.n_classes):

            name_trace = 'Class ' + str(self.classes[cl])

            self.df_classes.append(self.df.loc[self.df[self.target] == self.classes[cl]])


            self.fig.add_trace(
                    go.Scatter(
                        name=name_trace,
                        mode='markers',
                    ))                    
            self.trace[name_trace] = self.fig['data'][-1]
 
            if ( self.convex_hull == True ) :
                name_trace = 'Hull ' + str(self.classes[cl])
                self.fig.add_trace(
                        go.Scatter(
                            name=name_trace,
                    ))
                self.trace[name_trace] = self.fig['data'][-1]

        if self.regr_line_coefs :
            name_trace = 'Regression line'
            self.fig.add_trace(
                go.Scatter(
                    name=name_trace
                ))
            self.trace[name_trace] = self.fig['data'][-1]
        
        frac_dict, frac_thres = max_covering_shuffle(self)
        self.frac_dict = frac_dict
        self.frac_thres = frac_thres
        self.frac = self.frac_thres[(self.feat_x,self.feat_y)]

        for cl in range(self.n_classes):

            name_trace = 'Class ' + str(self.classes[cl])

            if ( self.max_covering == False):
                self.index_classes_shuffled.append(
                    self.df_classes[cl].index.to_numpy()[np.random.permutation(self.df_classes[cl].shape[0])])
            else:
                self.index_classes_shuffled.append(
                    self.frac_dict[(self.feat_x,self.feat_y)][cl]
                    )

            self.class_symbol[name_trace] = 'circle'
            self.n_points[name_trace] = int(self.frac * self.df_classes[cl].shape[0])
            self.symbols[name_trace] = ["circle"] * self.n_points[name_trace]
            self.sizes[name_trace] = ([self.marker_size] * self.n_points[name_trace])
            self.colors[name_trace] = ([next(self.palette)] * self.n_points[name_trace])
            self.df_classes_on_map.append(
                self.df_classes[cl].loc[self.index_classes_shuffled[cl]].head(self.n_points[name_trace]))

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
        # self.frac = self.frac_init[(self.feat_x,self.feat_y)]
        self.df['File'] = self.df['Structure'].apply( lambda x :  os.listdir( x))
        self.df['Replicas'] = self.df['Structure'].apply( lambda x :  len(os.listdir(x)) )

        instantiate_widgets(self)
        update_hover_variables(self)
        update_layout_figure(self)

    
    def show(self):
        with self.output_l:
            display(self.viewer_l)
        with self.output_r:
            display(self.viewer_r)

        self.widg_box_utils.layout.visibility = 'hidden'
        # self.widg_gradient.layout.visibility = 'hidden'

        self.widg_plotutils_button.layout.left = '50px'
        self.widg_box_utils.layout.border = 'dashed 1px'
        self.widg_box_utils.right = '100px'
        self.widg_box_utils.layout.max_width = '700px'

        self.box_feat.layout.height = '150px'
        self.box_feat.layout.top = '30px'
        self.widg_plotutils_button.layout.left = '50px'

        self.widg_box_utils.layout.border = 'dashed 1px'
        self.widg_box_utils.right = '100px'
        self.widg_box_utils.layout.max_width = '700px'

        if self.convex_hull == False:
            self.widg_color_hull.disabled = True
            self.widg_width_hull.disabled = True
            self.widg_style_hull.disabled = True

        if self.regr_line_coefs == None:
            self.widg_color_line.disabled = True
            self.widg_width_line.disabled = True
            self.widg_style_line.disabled = True

        container = widgets.VBox([
            self.box_feat,
            self.fig,
            self.widg_plotutils_button,
            self.widg_box_viewers,
            self.widg_box_utils
        ])

        display(container)
