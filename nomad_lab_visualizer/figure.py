import plotly.graph_objects as go
import numpy as np
import os

class Figure(object):

    from .include.figure._fract_change_updates import fract_change_updates, update_df_on_map,update_hover_variables
    from .include.figure._marker_style_updates import marker_style_updates, update_marker_size, update_marker_color, update_marker_symbol
    from .include.figure._batch_update import batch_update
    from .include.figure._geometry import make_hull, make_line
    from .include.figure._optimize_sequence import optimize_sequence

    def __init__( self, df, embedding_features, hover_features, target, path_to_structures ):

        
        self.df = df.copy()
        self.embedding_features = embedding_features
        self.hover_features = hover_features
        self.path_to_structures = path_to_structures
        self.target = target

        self.FigureWidget = go.FigureWidget()
        # Permanent layout settings are defined here
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

        # The 'target' feature is used to divide data into different traces.
        # Each item in the following dictionaries will be related to a different trace in the dataframe.
        self.name_traces = self.df[target].unique()
        self.trace = {}
        self.regr_line_trace = {}
        self.df_trace_on_map = (
            {}
        )  # dataframe containing only the elements that are visualized on the map        
        self.symbols = {}  # list of symbols used for every marker in each trace
        self.sizes = {}  # list of sizes used for every marker in each trace
        self.colors = {}  # list of colors used for every marker in each trace
        self.trace_symbol = {}  # default symbol used for the trace

        self.optimized_sequence_indexes = {} # optimized sequence of entries that is visualized varying the fraction for each pair of features.
        self.optimized_init_fract = {} # optimized initial fraction that is visualized for each pair of features.

        self.random_permutation_indexes = {} # random sequence of entries that is visualized varying the fraction.

        self.init_fract = 1
        total_points = self.df.shape[0]
        if (total_points>1000):
            # The initial fraction of visualized points is by default 1, unless there are more than 1000 points.
            self.init_fract = 1000/total_points

        self.convex_hull = False

        if path_to_structures:
            # List of all files found in the directory pointed by 'Structure'.
            self.df["File"] = self.df["Structure"].apply(lambda x: os.listdir(x))
            # Number of files found in the directory pointed by 'Structure'.
            self.df["Replicas"] = self.df["Structure"].apply(
                lambda x: len(os.listdir(x))
            )

        # Dictionaries initialized above are compiled for all different trace names.
        for cl in range(len(self.name_traces)):

            name_trace = str(self.name_traces[cl])

            # A 'Plotly go trace' is constructed and assigned to the 'trace' dictionary.
            self.FigureWidget.add_trace(
                go.Scatter(
                    name=name_trace,
                    mode="markers",
                )
            )
            self.trace[name_trace] = self.FigureWidget["data"][-1]

            # Add convex hull trace.
            name_trace = "Hull " + name_trace
            self.FigureWidget.add_trace(
                go.Scatter(
                    name=name_trace,
                )
            )
            self.trace[name_trace] = self.FigureWidget["data"][-1]


        for name_trace in self.name_traces:
            
            self.random_permutation_indexes[name_trace] = self.df.loc[
                self.df[target] == name_trace
            ].index.to_numpy()[np.random.permutation(self.df.loc[self.df[self.target] == name_trace].shape[0])]

            n_points = self.df.loc[
                self.df[target] == name_trace
            ].shape[0]

            self.df_trace_on_map[name_trace] = (
                self.df.loc[self.df[target] == name_trace]
                .loc[self.random_permutation_indexes[name_trace]]
                .head(n_points)
            )
                    
            # Circle is the init symbol used for each trace
            self.trace_symbol[name_trace] = "circle"
    
    def add_regr_line (self, coefs, feat_x, feat_y, ConfigWidgets):

        if not (feat_x,feat_y) in self.regr_line_trace:
            
            self.regr_line_trace[(feat_x,feat_y)]=True
            line_x, line_y = self.make_line( feat_x, feat_y, coefs)

            name_trace = "Regr line" + str(feat_x) + ' ' + str(feat_y) 
            self.FigureWidget.add_trace(go.Scatter(
                name=name_trace,
                x=line_x,
                y=line_y,
                )
                )
            self.trace[name_trace] = self.FigureWidget["data"][-1]
            self.FigureWidget.update_traces(selector={"name": name_trace}, showlegend=False)

        else: 

            self.regr_line_trace[(feat_x,feat_y)]=True           
            line_x, line_y = self.make_line(feat_x, feat_y, coefs)

            name_trace = "Regr line" + str(feat_x) + ' ' + str(feat_y) 
            self.trace[name_trace].x=line_x
            self.trace[name_trace].y=line_y

            self.FigureWidget.update_traces(selector={"name": name_trace}, showlegend=False)

        self.batch_update(ConfigWidgets)
        
    def remove_regr_line (self, feat_x, feat_y,ConfigWidgets):

        self.regr_line_trace[(feat_x,feat_y)]=False

        self.batch_update(ConfigWidgets)

    def optimize_fract(self, visualizerTopWidgets, ConfigWidgets):

        if not (ConfigWidgets.feat_x, ConfigWidgets.feat_y) in self.optimized_sequence_indexes :      
            sequence_indexes, init_fract = self.optimize_sequence(ConfigWidgets.feat_x, ConfigWidgets.feat_y)

            self.optimized_sequence_indexes[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)] = sequence_indexes
            self.optimized_sequence_indexes[(ConfigWidgets.feat_y, ConfigWidgets.feat_x)] = sequence_indexes
            self.optimized_init_fract[(ConfigWidgets.feat_x, ConfigWidgets.feat_y)] = init_fract
            self.optimized_init_fract[(ConfigWidgets.feat_y, ConfigWidgets.feat_x)] = init_fract
            
            ConfigWidgets.fract = init_fract
            visualizerTopWidgets.FractSlider.widget.value = init_fract
            self.batch_update(ConfigWidgets)