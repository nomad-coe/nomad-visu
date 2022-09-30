import plotly.graph_objects as go
import numpy as np

class Figure(object):

    from .include.figure._updates import marker_style_updates, fract_change_updates
    from .include.figure._batch_update import batch_update
    from .include.figure._geometry import make_hull, make_line
    from .include.figure._optimize_sequence import optimize_sequence

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

        self.name_traces = df[target].unique()
        self.trace = {}
        self.df_trace_on_map = (
            {}
        )  # dataframe which contains only the elements that are visualized on the map
        
        self.symbols = {}  # symbols used for markers of each trace
        self.sizes = {}  # sizes used for markers of each trace
        self.colors = {}  # colors used for markers of each trace
        self.trace_symbol = {}  # symbol used for the trace

        self.regr_line_trace = {}

        self.optimized_sequence_indexes = {}
        self.optimized_init_fract = {}

        self.random_permutation_indexes = {}
        self.init_fract = 1

        self.convex_hull = False

        # dictionaries initialized above are compiled for all different trace names
        for cl in range(len(self.name_traces)):

            name_trace = str(self.name_traces[cl])

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


        for name_trace in self.name_traces:
            
            self.random_permutation_indexes[name_trace] = self.df.loc[
                self.df[target] == name_trace
            ].index.to_numpy()[np.random.permutation(self.df.loc[self.df[self.target] == name_trace].shape[0])]

            n_points = self.df.loc[
                self.df[target] == name_trace
            ].shape[0]

            # fraction of the dataframe that is visualized on the map
            self.df_trace_on_map[name_trace] = (
                self.df.loc[self.df[target] == name_trace]
                .loc[self.random_permutation_indexes[name_trace]]
                .head(n_points)
            )
                    
            # symbol used for the trace
            self.trace_symbol[name_trace] = "circle"
            
    def add_regr_line (self, coefs, feat_x, feat_y, ConfigWidgets):


        if not (feat_x,feat_y) in self.regr_line_trace:
            
            self.regr_line_trace[(feat_x,feat_y)]=True

            # add a trace that contains the regression line
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
            visualizerTopWidgets.widg_fract_slider.value = init_fract
            self.batch_update(ConfigWidgets)