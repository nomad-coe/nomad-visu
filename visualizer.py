import plotly.graph_objects as go
import ipywidgets as widgets
from jupyter_jsmol import JsmolView
import numpy as np
from IPython.display import display, Markdown, FileLink
import os
from scipy.spatial import ConvexHull
import copy
import pandas as pd
from itertools import cycle
import plotly.express as px


class Visualizer:

    def __init__(self, df, embedding_features, hover_features, target, sisso=None, path_to_structures=None):

        # df - pandas dataframe containing all data to be visualized
        # sisso - sisso objects 
        # embedding_features - list of features used for embedding
        # hover features - list of features shown while hovering

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
        self.path_to_structures=path_to_structures

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
        self.df_classes_on_map = []  # dataframe which contains only the elements that are to be visualized on the map
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
        self.instantiate_widgets()

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

        self.update_hover_variables()
        self.update_layout_figure()

    def update_layout_figure(self):

        # All batch_update related changes are handled by this function
        with self.fig.batch_update():
            self.fig.update_layout(
                showlegend=True,
                plot_bgcolor=self.bg_color,
                font=dict(
                    size=int(self.font_size),
                    family=self.font_families[0],
                ),
                xaxis_title=self.widg_featx.value,
                yaxis_title=self.widg_featy.value,
                # xaxis_range=[x_min - x_delta, x_max + x_delta],
                # yaxis_range=[y_min - y_delta, y_max + y_delta],
            )
            for cl in np.arange(self.n_classes):
                # All elements on the map and their properties are reinitialized at each change
                self.trace[self.name_trace[cl]]['x'] = self.df_classes_on_map[cl][self.feat_x]
                self.trace[self.name_trace[cl]]['y'] = self.df_classes_on_map[cl][self.feat_y]
                self.trace[self.name_trace[cl]].marker.symbol = self.symbols[cl]
                self.trace[self.name_trace[cl]].marker.size = self.sizes[cl]
                # self.trace[self.name_trace[cl]].marker.line.color = self.colors[cl]
                # self.trace[self.name_trace[cl]].marker.line.width = self.global_markerlinewidth[cl]
                self.fig.update_traces(
                    selector={'name': str(self.name_trace[cl])},
                    text=self.hover_text[cl],
                    customdata=self.hover_custom[cl],
                    hovertemplate=self.hover_template[cl],
                    marker_color=self.colors[cl],
                    visible=True
                )


    def update_df_on_map(self):

        # if self.trace_l:
        #     trace_l, formula_l = self.trace_l
        # else:
        #     trace_l = -2
        # if self.trace_r:
        #     trace_r, formula_r = self.trace_r
        # else:
        #     trace_r = -2

        for cl in range(self.n_classes):
            self.df_classes_on_map[cl] = self.df_classes[cl].loc[self.index_classes_shuffled[cl]].head(
                int(self.frac * self.df_classes[cl].shape[0]))
            # if cl == trace_l:
            #     self.df_entries_onmap[cl] = pd.concat([
            #         self.df_entries_onmap[cl],
            #         self.df_clusters[trace_l].loc[[formula_l]]
            #     ], axis=0)
            # if cl == trace_r:
            #     self.df_entries_onmap[cl] = pd.concat([
            #         self.df_entries_onmap[cl],
            #         self.df_clusters[trace_r].loc[[formula_r]],
            #     ], axis=0)
            self.n_points[cl] = self.df_classes_on_map[cl].shape[0]

        # self.reset_markers()
        # for cl in range(self.n_clusters+1):
        #     try:
        #         try:
        #             point = np.where(self.df_entries_onmap[cl].index.to_numpy() == formula_l)[0][1]
        #             self.global_symbols[cl][point] = 'x'
        #         except:
        #             point = np.where(self.df_entries_onmap[cl].index.to_numpy() == formula_l)[0][0]
        #             self.global_symbols[cl][point] = 'x'
        #     except:
        #         pass
        #     try:
        #         try:
        #             point = np.where(self.df_entries_onmap[cl].index.to_numpy() == formula_r)[0][1]
        #             self.global_symbols[cl][point] = 'cross'
        #         except:
        #             point = np.where(self.df_entries_onmap[cl].index.to_numpy() == formula_r)[0][0]
        #             self.global_symbols[cl][point] = 'cross'
        #     except:
        #         pass

        # if self.widg_outliersbox.value:
        #     self.df_entries_onmap[-1] = pd.concat(self.df_entries_onmap[:self.n_clusters + 1], axis=0, sort=False)
        #     self.n_points[-1] = int(self.df_entries_onmap[-1].shape[0])
        #     self.global_symbols[-1] = [symb for sub in self.global_symbols[:-1] for symb in sub]
        # else:
        #     self.df_entries_onmap[-1] = pd.concat(self.df_entries_onmap[:self.n_clusters], axis=0, sort=False)
        #     self.n_points[-1] = int(self.df_entries_onmap[-1].shape[0])
        #     self.global_symbols[-1] = [symb for sub in self.global_symbols[:-2] for symb in sub]

    def update_hover_variables(self):

        self.hover_text = []
        self.hover_custom = []
        self.hover_template = []

        for cl in range(self.n_classes):
            self.hover_text.append(self.df_classes_on_map[cl].index)
            hover_template = r"<b>%{text}</b><br><br>"
            if self.hover_features:
                hover_custom = np.dstack([self.df_classes_on_map[cl][str(self.hover_features[0])].to_numpy()])
                hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
                for i in range(1, len(self.hover_features), 1):
                    hover_custom = np.dstack(
                        [hover_custom, self.df_classes_on_map[cl][str(self.hover_features[i])].to_numpy()])
                    hover_template += str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
                self.hover_custom.append(hover_custom[0])
                self.hover_template.append(hover_template)
            else:
                self.hover_custom.append([''])
                self.hover_template.append([''])
        self.hover_text.append(self.df_classes_on_map[-1].index)
        hover_template = r"<b>%{text}</b><br><br>"
        if self.hover_features:
            hover_custom = np.dstack([self.df_classes_on_map[-1][str(self.hover_features[0])].to_numpy()])
            hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
            for i in range(1, len(self.hover_features), 1):
                hover_custom = np.dstack(
                    [hover_custom, self.df_classes_on_map[-1][str(self.hover_features[i])].to_numpy()])
                hover_template += str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
            self.hover_custom.append(hover_custom[0])
            self.hover_template.append(hover_template)
        else:
            self.hover_custom.append([''])
            self.hover_template.append([''])

        # for cl in np.arange(self.n_classes):
        #     markerlinewidth = [1] * self.n_points[cl]
        #     markerlinecolor = ['white'] * self.n_points[cl]
        #     sizes = [self.marker_size] * self.n_points[cl]
        #     symbols = self.symbols[cl]
        #     try:
        #         point = symbols.index('x')
        #         sizes[point] = self.cross_size
        #         markerlinewidth[point] = 2
        #         markerlinecolor[point] = 'black'
        #     except:
        #         pass
        #     try:
        #         point = symbols.index('cross')
        #         sizes[point] = self.cross_size
        #         markerlinewidth[point] = 2
        #         markerlinecolor[point] = 'black'
        #     except:
        #         pass
        #     self.sizes[cl] = sizes
        #     # self.global_markerlinecolor[cl] = markerlinecolor
        #     # self.global_markerlinewidth[cl] = markerlinewidth
        # self.sizes[-1] = [symb for sub in self.sizes[:-1] for symb in sub]
        # self.global_markerlinecolor[-1] = [symb for sub in self.global_markerlinecolor[:-1] for symb in sub]
        # self.global_markerlinewidth[-1] = [symb for sub in self.global_markerlinewidth[:-1] for symb in sub]

    def update_markers_size(self, feature='Default size'):
        # Defines the size of the markers based on the input feature.
        # In case of default feature all markers have the same size.
        # Points marked with x/cross are set with a specific size

        if feature == 'Default size':

            for cl in range(self.n_classes):

                sizes = [self.marker_size] * self.n_points[cl]
                symbols = [self.symbols[cl]] * self.n_points[cl]

                try:
                    point = symbols.index('x')
                    sizes[point] = self.cross_size
                except:
                    try:
                        point = symbols.index('x')
                        sizes[point] = self.cross_size
                    except:
                        pass
                try:
                    point = symbols.index('cross')
                    sizes[point] = self.cross_size
                except:
                    try:
                        point = symbols.index('cross')
                        sizes[point] = self.cross_size
                    except:
                        pass
                self.sizes = sizes
        else:

            min_value = min(self.df[feature])
            max_value = max(self.df[feature])
            coeff = 2 * self.marker_size / (max_value - min_value)

            for cl in range(self.n_classes):
                sizes = self.marker_size / 2 + coeff * self.df_classes[cl][feature].to_numpy()
                self.sizes[cl] = sizes

    def handle_xfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordingly
        self.feat_x = change.new
        self.update_layout_figure()

    def handle_yfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordingly
        self.feat_y = change.new
        self.update_layout_figure()

    def plotappearance_button_clicked(self, button):
        if self.widg_box_utils.layout.visibility == 'visible':
            self.widg_box_utils.layout.visibility = 'hidden'
            for i in range(290, -1, -1):
                self.widg_box_viewers.layout.top = str(i) + 'px'
            self.widg_box_utils.layout.bottom = '0px'
        else:
            for i in range(291):
                self.widg_box_viewers.layout.top = str(i) + 'px'
            self.widg_box_utils.layout.bottom = '400px'
            self.widg_box_utils.layout.visibility = 'visible'

    def handle_markerfeat_change(self, change):
        self.update_markers_size(feature=change.new)
        self.update_layout_figure()

    def handle_frac_change(self, change):
        self.frac = change.new
        self.update_df_on_map()
        self.update_hover_variables()
        self.update_layout_figure()

    def handle_colorfeat_change(self, change):
        self.make_colors(feature=change.new, gradient=self.widg_gradient.value)
        self.update_layout_figure()

    def handle_gradient_change(self, change):
        self.make_colors(feature=self.widg_featcolor.value, gradient=change.new)
        self.update_layout_figure()

    def updatefrac_button_clicked(self, button):
        self.frac = self.widg_frac_slider.value
        self.make_dfclusters()
        self.update_hover_variables()
        self.update_layout_figure()

    def update_point(self, trace, points, selector):
        # changes the points labeled with a cross on the map.

        if not points.point_inds:
            return

        trace = points.trace_index
        formula = self.fig.data[trace].text[points.point_inds[0]]

        if self.widg_checkbox_l.value:
            self.trace_l = [trace, formula]
            # self.replica_l = 0
        if self.widg_checkbox_r.value:
            self.trace_r = [trace, formula]
              # self.replica_r = 0

        # self.make_dfclusters()
        # self.update_appearance_variables()
        self.update_layout_figure()

        if self.widg_checkbox_l.value:
            self.widg_compound_text_l.value = formula
            self.view_structure_l(formula)
        if self.widg_checkbox_r.value:
            self.widg_compound_text_r.value = formula
            self.view_structure_r(formula)

    def view_structure_l(self, formula):
        # replicas = self.df.loc[self.df['Formula'] == formula].index.shape[0]
        # if self.replica_l >= replicas:
        #     self.replica_l = 0
        # i_structure = self.df.loc[self.df['Formula'] == formula]['File-id'].values[self.replica_l]
        # self.viewer_l.script("load data/query_nomad_archive/structures/" + str(int(i_structure)) + ".xyz")
        self.viewer_l.script("load " + self.path_to_structures + formula + ".xyz")

    def view_structure_r(self, formula):
        # replicas = self.df[self.df['Formula'] == formula].index.shape[0]
        # if self.replica_r >= replicas:
        #     self.replica_r = 0
        # i_structure = self.df.loc[self.df['Formula'] == formula]['File-id'].values[self.replica_r]
        # self.viewer_r.script("load data/query_nomad_archive/structures/" + str(int(i_structure)) + ".xyz")
        self.viewer_r.script("load " + self.path_to_structures + formula + ".xyz")

    def show(self):

        for name in self.name_trace:
            self.trace[name].on_click(self.update_point)  # actions are performed after clicking points on the map

        self.widg_featx.observe(self.handle_xfeat_change, names='value')
        self.widg_featy.observe(self.handle_yfeat_change, names='value')
        self.widg_featmarker.observe(self.handle_markerfeat_change, names='value')
        self.widg_featcolor.observe(self.handle_colorfeat_change, names='value')
        self.widg_gradient.observe(self.handle_gradient_change, names='value')
        self.widg_plotutils_button.on_click(self.plotappearance_button_clicked)
        self.widg_frac_slider.observe(self.handle_frac_change, names='value')
        self.output_l.layout = widgets.Layout(width="400px", height='350px')
        self.output_r.layout = widgets.Layout(width="400px", height='350px')

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

    def instantiate_widgets(self):

        self.widg_update_frac_button = widgets.Button(
            description='Click to update',
            layout=widgets.Layout(width='150px', left='130px')
        )
        self.widg_frac_slider = widgets.BoundedFloatText(
            min=0,
            max=1,
            step=0.01,
            value=self.frac,
            layout=widgets.Layout(left='130px', width='60px')
        )
        self.widg_label_frac = widgets.Label(
            value='Fraction of compounds visualized in the map: ',
            layout=widgets.Layout(left='130px')
        )
        self.widg_featx = widgets.Dropdown(
            description='x-axis',
            options=self.embedding_features,
            value=self.feat_x
        )
        self.widg_featy = widgets.Dropdown(
            description='y-axis',
            options=self.embedding_features,
            value=self.feat_y
        )
        self.widg_featmarker = widgets.Dropdown(
            description="Marker",
            options=['Default size'] + self.hover_features,
            value='Default size',
        )
        self.widg_featcolor = widgets.Dropdown(
            description='Color',
            options=['Default color'] + self.hover_features,
            value='Default color'
        )
        self.widg_gradient = widgets.Dropdown(
            description='-gradient',
            options=self.gradient_list,
            value='Grey scale',
            layout=widgets.Layout(width='150px', right='20px')
        )
        self.widg_compound_text_l = widgets.Combobox(
            placeholder='...',
            description='Compound:',
            options=self.compounds_list,
            # disabled=False,
            layout=widgets.Layout(width='200px')
        )
        self.widg_compound_text_r = widgets.Combobox(
            placeholder='...',
            description='Compound:',
            options=self.compounds_list,
            # disabled=False,
            layout=widgets.Layout(width='200px')
        )
        self.widg_display_button_l = widgets.Button(
            description="Display",
            layout=widgets.Layout(width='100px')
        )
        self.widg_display_button_r = widgets.Button(
            description="Display",
            layout=widgets.Layout(width='100px')
        )
        self.widg_checkbox_l = widgets.Checkbox(
            value=True,
            indent=False,
            layout=widgets.Layout(width='50px')
        )
        self.widg_checkbox_r = widgets.Checkbox(
            value=False,
            indent=False,
            layout=widgets.Layout(width='50px'),
        )
        self.widg_markersize = widgets.BoundedIntText(
            placeholder=str(self.marker_size),
            description='Marker size',
            value=str(self.marker_size),
            layout=widgets.Layout(left='30px', width='200px')
        )
        self.widg_crosssize = widgets.BoundedIntText(
            placeholder=str(self.cross_size),
            description='Cross size',
            value=str(self.cross_size),
            layout=widgets.Layout(left='30px', width='200px')
        )
        self.widg_fontsize = widgets.BoundedIntText(
            placeholder=str(self.font_size),
            description='Font size',
            value=str(self.font_size),
            layout=widgets.Layout(left='30px', width='200px')
        )
        # self.widg_linewidth = widgets.BoundedIntText(
        #     placeholder=str(self.line_width),
        #     description='Line width',
        #     value=str(self.line_width),
        #     layout = widgets.Layout(left='30px', width='200px')
        # )
        # self.widg_linestyle = widgets.Dropdown(
        #     options=self.line_styles,
        #     description='Line style',
        #     value=self.line_styles[0],
        #     layout=widgets.Layout(left='30px', width='200px')
        # )

        self.widg_fontfamily = widgets.Dropdown(
            options=self.font_families,
            description='Font family',
            value=self.font_families[0],
            layout=widgets.Layout(left='30px', width='200px')
        )
        self.widg_bgcolor = widgets.Text(
            placeholder=str(self.bg_color),
            description='Background',
            value=str(self.bg_color),
            layout=widgets.Layout(left='30px', width='200px'),
        )
        # self.widg_rscolor = widgets.Text(
        #     placeholder=str(self.rs_color),
        #     description='RS color',
        #     value=str(self.rs_color),
        #     layout=widgets.Layout(left='30px', width='200px'),
        # )
        # self.widg_zbcolor = widgets.Text(
        #     placeholder=str(self.zb_color),
        #     description='ZB color',
        #     value=str(self.zb_color),
        #     layout=widgets.Layout(left='30px', width='200px'),
        # )
        # self.widg_rsmarkersymbol = widgets.Dropdown(
        #     description='RS symbol',
        #     options=self.symbols,
        #     value=self.marker_symbol_RS,
        #     layout=widgets.Layout(left='30px', width='200px')
        # )
        # self.widg_zbmarkersymbol = widgets.Dropdown(
        #     description='ZB symbol',
        #     options=self.symbols,
        #     value=self.marker_symbol_ZB,
        #     layout=widgets.Layout(left='30px', width='200px')
        # )
        self.widg_bgtoggle_button = widgets.Button(
            description='Toggle on/off background',
            layout=widgets.Layout(left='50px', width='200px'),
        )
        self.widg_updatecolor_button = widgets.Button(
            description='Update colors',
            layout=widgets.Layout(left='50px', width='200px')
        )
        self.widg_reset_button = widgets.Button(
            description='Reset symbols',
            layout=widgets.Layout(left='50px', width='200px')
        )
        self.widg_plot_name = widgets.Text(
            placeholder='plot',
            value='plot',
            description='Name',
            layout=widgets.Layout(width='300px')
        )
        self.widg_plot_format = widgets.Text(
            placeholder='png',
            value='png',
            description='Format',
            layout=widgets.Layout(width='150px')
        )
        self.widg_scale = widgets.Text(
            placeholder='1',
            value='1',
            description="Scale",
            layout=widgets.Layout(width='150px')
        )
        self.widg_print_button = widgets.Button(
            description='Print',
            layout=widgets.Layout(left='50px', width='600px')
        )
        self.widg_print_out = widgets.Output(
            layout=widgets.Layout(left='150px', width='400px')
        )
        self.widg_printdescription = widgets.Label(
            value="Click 'Print' to export the plot in the desired format.",
            layout=widgets.Layout(left='50px', width='640px')
        )
        self.widg_printdescription2 = widgets.Label(
            value="The resolution of the image can be increased by increasing the 'Scale' value.",
            layout=widgets.Layout(left='50px', width='640px')
        )
        self.widg_featuredescription = widgets.Label(
            value="The dropdown menus select the features to visualize."
        )
        self.widg_description = widgets.Label(
            value='Tick the box next to the cross symbols in order to choose which windows visualizes the next '
                  'structure selected in the map above.'
        )
        self.widg_colordescription = widgets.Label(
            value='Colors in the boxes below can be written as a text string, i.e. red, '
                  'green,...,  or in a rgb/a, hex format. ',
            layout=widgets.Layout(left='50px', width='640px')

        )
        self.widg_colordescription2 = widgets.Label(
            value="After modifying a specific field, click on the 'Update colors' button to display the changes in "
                  "the plot.",
            layout=widgets.Layout(left='50px', width='640px')
        )
        self.widg_plotutils_button = widgets.Button(
            description='For a high-quality print of the plot, click to access the plot appearance utils',
            layout=widgets.Layout(width='600px')
        )
        self.widg_box_utils = widgets.VBox([widgets.HBox([self.widg_markersize, self.widg_crosssize]),
                                            #   self.widg_rsmarkersymbol]),
                                            # widgets.HBox([self.widg_linewidth, self.widg_linestyle]),
                                            #   self.widg_zbmarkersymbol]),
                                            widgets.HBox([self.widg_fontsize, self.widg_fontfamily]),
                                            self.widg_colordescription, self.widg_colordescription2,
                                            # widgets.HBox([self.widg_rscolor, self.widg_zbcolor, self.widg_bgcolor]),
                                            widgets.HBox([self.widg_bgtoggle_button, self.widg_updatecolor_button,
                                                          self.widg_reset_button]),
                                            self.widg_printdescription, self.widg_printdescription2,
                                            widgets.HBox([self.widg_plot_name, self.widg_plot_format, self.widg_scale]),
                                            self.widg_print_button, self.widg_print_out,
                                            ])

        file1 = open("./assets/cross.png", "rb")
        image1 = file1.read()
        self.widg_img1 = widgets.Image(
            value=image1,
            format='png',
            width=30,
            height=30,
        )
        file2 = open("./assets/cross2.png", "rb")
        image2 = file2.read()
        self.widg_img2 = widgets.Image(
            value=image2,
            format='png',
            width=30,
            height=30,
        )
        self.output_l = widgets.Output()
        self.output_r = widgets.Output()

        self.box_feat = widgets.VBox([
            widgets.HBox([
                widgets.VBox([self.widg_featx, self.widg_featy]),
                widgets.VBox([self.widg_featmarker,
                              widgets.HBox([self.widg_featcolor, self.widg_gradient])
                              ]),
            ]),
            widgets.HBox([self.widg_label_frac, self.widg_frac_slider, self.widg_update_frac_button]),

        ])

        self.widg_box_viewers = widgets.VBox([self.widg_description, widgets.HBox([
            widgets.VBox([
                widgets.HBox([self.widg_compound_text_l, self.widg_display_button_l,
                              self.widg_img1, self.widg_checkbox_l]),
                self.output_l]),
            widgets.VBox(
                [widgets.HBox([self.widg_compound_text_r, self.widg_display_button_r,
                               self.widg_img2, self.widg_checkbox_r]),
                 self.output_r])
        ])])

    def make_colors(self, feature, gradient):

        if feature == 'Default color':
            self.palette = cycle(getattr(px.colors.qualitative, self.qualitative_colors[0]))

            for cl in range(self.n_classes):
                self.colors[cl] = [next(self.palette)] * self.n_points[cl]

        else:
            self.df
            min_value = self.df[feature].min()
            max_value = self.df[feature].max()

            if gradient == 'Grey scale':
                for cl in range(self.n_classes):
                    shade_cl = 0.7 * (self.df_classes[cl][feature].to_numpy() - min_value) / \
                               (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * (0.7 - e)
                        string = 'rgb(' + str(value) + "," + str(value) + "," + str(value) + ')'
                        self.colors[cl][i] = string

            if gradient == 'Purple scale':
                for cl in range(self.n_classes):
                    shade_cl = 0.7 * (self.df_classes[cl][feature].to_numpy() - min_value) / \
                               (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * (0.7 - e)
                        string = 'rgb(' + str(value) + "," + str(0) + "," + str(value) + ')'
                        self.colors[cl][i] = string

            if gradient == 'Turquoise scale':
                for cl in range(self.n_classes):
                    shade_cl = 0.7 * (self.df_classes[cl][feature].to_numpy() - min_value) / \
                               (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * (0.7 - e)
                        string = 'rgb(' + str(0) + "," + str(value) + "," + str(value) + ')'
                        self.colors[cl][i] = string

            if gradient == 'Blue to green':
                for cl in range(self.n_classes):
                    shade_cl = 0.7 * (self.df_classes[cl][feature].to_numpy() - min_value) / \
                               (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * e
                        value2 = 255 - value
                        string = 'rgb(' + str(0) + "," + str(value) + "," + str(value2) + ')'
                        self.colors[cl][i] = string

            if gradient == 'Blue to red':
                for cl in range(self.n_classes):
                    shade_cl = 0.7 * (self.df_classes[cl][feature].to_numpy() - min_value) / \
                               (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * e
                        value2 = 255 - value
                        string = 'rgb(' + str(value) + "," + str(0) + "," + str(value2) + ')'
                        self.colors[cl][i] = string

            if gradient == 'Green to red':
                for cl in range(self.n_classes):
                    shade_cl = 0.7 * (self.df_classes[cl][feature].to_numpy() - min_value) / \
                               (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * e
                        value2 = 255 - value
                        string = 'rgb(' + str(value) + "," + str(value2) + "," + str(0) + ')'
                        self.colors[cl][i] = string
