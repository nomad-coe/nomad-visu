import plotly.graph_objects as go
import ipywidgets as widgets
from jupyter_jsmol import JsmolView
import numpy as np
from IPython.display import display
from itertools import cycle
import plotly.express as px


class StaticVisualizer:

    def __init__(self, df, embedding_features, hover_features, target, sisso=None, path_to_structures=None):

        # df - pandas dataframe containing all data to be visualized
        # sisso - sisso objects 
        # embedding_features - list of features used for embedding
        # hover features - list of features shown while hovering

        from include._instantiate_widgets import instantiate_widgets
        from include._updates import update_hover_variables, update_df_on_map, update_layout_figure, update_markers_size

        self.sisso = sisso
        self.df = df
        self.target = target

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
        self.trace_l = []
        self.trace_r = []

        self.frac = (1000 / self.total_compounds)
        if self.frac > 1:
            self.frac = 1
        self.frac = int(self.frac * 100) / 100
        self.marker_size = 7
        self.compounds_list = df.index.tolist()
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
        self.bg_color = 'rgba(229,236,246, 0.5)'
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

        # The 'target' feature is used to divide data into different classes 
        # Each item in the following lists will be related to a different class in the dataframe
        # For each different class a new trace is created
        self.df_classes = []  # section of the pandas dataframe containing elements of only a specific class
        self.index_classes_shuffled = []  # index of the dataframe class shuffled - used to avoid bias visualization when only a fraction is visualized
        self.n_points = []  # total points of the class which are visualized - can be less than the total number of data depending on the fraction visualized
        self.df_classes_on_map = []  # dataframe which contains only the elements that are visualized on the map
        self.symbols = []  # each item is a list of symbols
        self.sizes = []  # each item is a list of sizes
        self.colors = []  # each iteindex_classes_shuffled
        self.name_trace = []  # name of the trace that is given by the specific 'target' feature
        self.trace = {}  # trace related to the class
        self.palette = cycle(
            getattr(px.colors.qualitative, self.qualitative_colors[0]))  # each class has by default a different color

        self.fig = go.FigureWidget()
        self.viewer_l = JsmolView()
        self.viewer_r = JsmolView()
        instantiate_widgets(self)

        # All different classes are iterated and a class-specific item is added to the list defined above 
        for cl in range(self.n_classes):
            self.df_classes.append(self.df.loc[self.df[self.target] == self.classes[cl]])
            self.index_classes_shuffled.append(
                self.df_classes[cl].index.to_numpy()[np.random.permutation(self.df_classes[cl].shape[0])])
            self.name_trace.append(self.classes[cl])
            self.fig.add_trace(
                (
                    go.Scatter(
                        name=self.name_trace[cl],
                        mode='markers',
                    )))
            self.trace[self.name_trace[cl]] = self.fig['data'][cl]

            self.n_points.append(int(self.frac * self.df_classes[cl].shape[0]))
            self.symbols.append(["circle"] * self.n_points[cl])
            self.sizes.append([self.marker_size] * self.n_points[cl])
            self.colors.append([next(self.palette)] * self.n_points[cl])
            self.df_classes_on_map.append(
                self.df_classes[cl].loc[self.index_classes_shuffled[cl]].head(self.n_points[cl]))

        # All permanent layout settings are here defined - functions below do not change these fields
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

        container = widgets.VBox([
            self.box_feat,
            self.fig,
            self.widg_plotutils_button,
            self.widg_box_viewers,
            self.widg_box_utils
        ])

        display(container)
