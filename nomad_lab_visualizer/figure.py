from .configWidgets import ConfigWidgets
from .include._batch_update import batch_update
from .include._updates import marker_style_updates, fract_change_updates
import plotly.graph_objects as go
import numpy as np
from .include._geometry import make_hull, make_line
from .include._smart_fract import make_optimized_frac

class Figure( ):
    
    from .include._batch_update import batch_update

    def __init__( self, df, embedding_features, hover_features, target, path_to_structures ):

        # The 'target' feature is used to divide data into different traces
        # Each item in the following dictionaries will be related to a different trace in the dataframe
        # For each different 'target' value a new trace is created
        
        self.df = df.copy()
        self.FigureWidget = go.FigureWidget()
        # All permanent layout settings are defined here
        self.FigureWidget.update_layout(
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
            width=800,
            height=400,
            margin=dict(l=50, r=50, b=70, t=20, pad=4),
        )
        self.FigureWidget.update_xaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )
        self.FigureWidget.update_yaxes(
            ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor="black"
        )

        self.embedding_features = embedding_features
        self.hover_features = hover_features
        self.path_to_structures = path_to_structures
        self.target = target

        self.name_traces = df[target].unique().astype(str)
        self.trace = {}
        self.index_df_trace_shuffled = (
            {}
        )  # index of the dataframe trace shuffled for fraction visualization
        self.n_points = (
            {}
        )  # total points of the class which are visualized - can be less than the total number of data depending on the fraction visualized
        self.df_trace_on_map = (
            {}
        )  # dataframe which contains only the elements that are visualized on the map
        self.symbols = {}  # symbols used for markers of each trace
        self.sizes = {}  # sizes used for markers of each trace
        self.colors = {}  # colors used for markers of each trace
        self.trace_symbol = {}  # symbol used for the trace
    
        # dictionaries initialized above are compiled for all different trace names
        for cl in range(len(self.name_traces)):

            name_trace = self.name_traces[cl]

            # a trace with a specific name taken from the 'target' values is constructed and assigned to the 'trace' dictionary
            self.FigureWidget.add_trace(
                go.Scatter(
                    name=name_trace,
                    mode="markers",
                )
            )
            self.trace[name_trace] = self.FigureWidget["data"][-1]

            # add a convex hull for each different 'target' value
            name_trace = "Hull " + name_trace
            self.FigureWidget.add_trace(
                go.Scatter(
                    name=name_trace,
                )
            )
            self.trace[name_trace] = self.FigureWidget["data"][-1]

        
        total_points = self.df.shape[0]

        for name_trace in self.name_traces:

        
            self.index_df_trace_shuffled[name_trace] = self.df.loc[
                self.df[target] == name_trace
            ].index.to_numpy()[
                np.random.permutation(self.df.loc[
                self.df[target] == name_trace
            ].shape[0])
            ]

            self.n_points[name_trace] = self.df.loc[
                self.df[target] == name_trace
            ].shape[0]
            # fraction of the dataframe that is visualized on the map
            self.df_trace_on_map[name_trace] = (
                self.df.loc[
                self.df[target] == name_trace
            ]
                .loc[self.index_df_trace_shuffled[name_trace]]
                .head(self.n_points[name_trace])
            )
                    
            # symbol used for the trace
            self.trace_symbol[name_trace] = "circle"
            
    def add_regr_line (self, coefs, feat_x, feat_y):


        if not (feat_x,feat_y) in ConfigWidgets.regr_line_trace:
            
            ConfigWidgets.regr_line_trace[(feat_x,feat_y)]=True

            # add a trace that contains the regression line
            line_x, line_y = make_line(self, feat_x, feat_y, coefs)

            name_trace = "Regr line" + feat_x + ' ' + feat_y 
            self.FigureWidget.add_trace(go.Scatter(
                name=name_trace,
                x=line_x,
                y=line_y,
                )
                )
            self.trace[name_trace] = self.FigureWidget["data"][-1]
            self.FigureWidget.update_traces(selector={"name": name_trace}, showlegend=False)

        else: 

            ConfigWidgets.regr_line_trace[(feat_x,feat_y)]=True           
            line_x, line_y = make_line(self, feat_x, feat_y, coefs)

            name_trace = "Regr line" + feat_x + ' ' + feat_y 
            self.trace[name_trace].x=line_x
            self.trace[name_trace].y=line_y

            self.FigureWidget.update_traces(selector={"name": name_trace}, showlegend=False)

        batch_update(self, ConfigWidgets)
        
    def remove_regr_line (self, feat_x, feat_y):

        ConfigWidgets.regr_line_trace[(feat_x,feat_y)]=False

        batch_update(self, ConfigWidgets)


    def optimize_fract(self, visualizerTopWidgets):

        if not (ConfigWidgets.feat_x, ConfigWidgets.feat_y) in ConfigWidgets.optimized_frac:      
            optimized_sequence, fract_thres = make_optimized_frac(self, ConfigWidgets.feat_x, ConfigWidgets.feat_y)

            ConfigWidgets.optimized_frac[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)] = optimized_sequence, fract_thres
            ConfigWidgets.optimized_frac[(ConfigWidgets.feat_y, ConfigWidgets.feat_x)] = optimized_sequence, fract_thres
            ConfigWidgets.fract = fract_thres
            visualizerTopWidgets.widg_fract_slider.value = fract_thres
            batch_update(self, ConfigWidgets)

  


