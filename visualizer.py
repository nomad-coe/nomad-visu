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

    def __init__(self, df, sisso, classes, embedding_features, hover_features):
        self.sisso = sisso
        self.df = df
        self.n_classes = df['Classes'].unique().size
        self.classes = df['Classes'].unique()
        self.embedding_features = embedding_features
        self.hover_features = hover_features
        self.total_compounds = df.shape[0]
        self.frac = (1000 / self.total_compounds)
        if self.frac > 1:
            self.frac = 1
        self.frac = int(self.frac*100)/100
        self.marker_size = 7

        # self.marker_symbol_cls0 = 'circle'
        # self.marker_symbol_cls1 = 'square'
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
        # self.color_cls1 = "#EB8273"
        # self.color_cls0 = "rgb(138, 147, 248)"
        # self.color_hull0 = 'Grey'
        # self.color_hull1 = 'Grey'
        # self.color_line = 'Black'
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
        self.n_points = []
        self.global_symbols = []
        self.global_sizes = []
        self.global_symbols = []
        self.name_trace = []
        self.df_classes = []
        self.shuffled_entries = []
        self.df_entries_onmap = []
        self.trace = {}

        self.palette = cycle(getattr(px.colors.qualitative, self.qualitative_colors[0]))
        self.fig = go.FigureWidget()
        self.viewer_l = JsmolView()
        self.viewer_r = JsmolView()
        self.instantiate_widgets()

        # Dataframe should contain the 'Classes' column
        # Traces are addded for each different class the dataframe is composed of 
        for cl in range(self.n_classes):

            self.df_classes.append(self.df.loc[self.df['Classes']==self.classes[cl]])
            self.shuffled_entries.append(self.df_classes[cl].index.to_numpy()[np.random.permutation(self.df_classes[cl].shape[0])])
            self.n_points.append(int(self.frac * self.df_classes[cl].shape[0]))
            self.global_symbols.append(["circle"] * self.n_points[cl])
            self.global_sizes.append([self.marker_size] * self.n_points[cl])
            self.name_trace.append(self.classes[cl])
            self.df_entries_onmap.append(self.df_classes[cl].loc[self.shuffled_entries[cl]].head(self.n_points[cl]))

            self.fig.add_trace(
                (
                    go.Scatter(
                        name=self.name_trace[cl],
                        mode='markers',
                        x=self.df[df['Classes']==df['Classes'].unique()[cl]][str(self.embedding_features[0])],
                        y=self.df[df['Classes']==df['Classes'].unique()[cl]][str(self.embedding_features[1])],
                        marker=dict(symbol=self.symbols[cl], color=next(self.palette), size=self.global_sizes[cl])
                    )))
            self.trace[self.name_trace[cl]] = self.fig['data'][cl]

        # self.fig.update_layout(
        #     plot_bgcolor=self.bg_color,
        #     font=dict(
        #         size=int(self.font_size),
        #         family=self.font_families[0]
        #     ),
        #     xaxis_title=self.features[0],
        #     yaxis_title=self.features[1],
        #     # xaxis_range=[x_min - x_delta, x_max + x_delta],
        #     # yaxis_range=[y_min - y_delta, y_max + y_delta],
        #     hoverlabel=dict(
        #         bgcolor="white",
        #         font_size=16,
        #         font_family="Rockwell"
        #     ),
        #     width=800,
        #     height=400,
        #     margin=dict(
        #         l=50,
        #         r=50,
        #         b=70,
        #         t=20,
        #         pad=4
        #     ),
        # )
        self.fig.update_xaxes(ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor='black')
        self.fig.update_yaxes(ticks="outside", tickwidth=1, ticklen=10, linewidth=1, linecolor='black')
        
        self.update_appearance_variables ()
        self.update_layout_figure ()

    def update_layout_figure(self):

        with self.fig.batch_update():

            # if self.widg_colormarkers.value == 'Default':
                # self.palette = cycle(getattr(px.colors.qualitative, self.widg_colorpalette.value))
                self.fig.update_layout(showlegend=True)
                for cl in np.arange(self.n_classes):
                    color = next(self.palette)
                    self.trace[self.name_trace[cl]].marker.symbol = self.global_symbols[cl]
                    self.trace[self.name_trace[cl]].marker.size = self.global_sizes[cl]
                    # self.trace[self.name_trace[cl]].marker.line.color = self.global_markerlinecolor[cl]
                    # self.trace[self.name_trace[cl]].marker.line.width = self.global_markerlinewidth[cl]
                    # self.trace[self.name_trace[cl]]['x'] = self.df_entries_onmap[cl]['x_emb']
                    # self.trace[self.name_trace[cl]]['y'] = self.df_entries_onmap[cl]['y_emb']
                    self.fig.update_traces(
                        selector={'name': self.name_trace[cl]},
                        text=self.hover_text[cl],
                        customdata=self.hover_custom[cl],
                        hovertemplate=self.hover_template[cl],
                        marker_color=color,
                        visible=True
                    )
                # self.trace[self.name_trace[-1]].marker.symbol = []
                # self.trace[self.name_trace[-1]].marker.size = []
                # self.trace[self.name_trace[-1]].marker.line.color = []
                # self.trace[self.name_trace[-1]].marker.line.width = []
                # self.trace[self.name_trace[-1]]['x'] = []
                # self.trace[self.name_trace[-1]]['y'] = []
                # self.fig.update_traces(
                #     selector={'name': self.name_trace[-1]},
                #     text=self.hover_text[-1],
                #     customdata=self.hover_custom[-1],
                #     hovertemplate=self.hover_template[-1],
                #     visible=False
                # )
            # else:
            #     self.fig.update_layout(showlegend=False)
            #     for cl in np.arange(self.n_clusters+1):
            #         self.trace[self.name_trace[cl]].marker.symbol = []
            #         self.trace[self.name_trace[cl]].marker.size = []
            #         self.trace[self.name_trace[cl]].marker.line.color = []
            #         self.trace[self.name_trace[cl]].marker.line.width = []
            #         self.trace[self.name_trace[cl]]['x'] = []
            #         self.trace[self.name_trace[cl]]['y'] = []
            #         self.fig.update_traces(
            #             selector={'name': self.name_trace[cl]},
            #             text=self.hover_text[cl],
            #             customdata=self.hover_custom[cl],
            #             hovertemplate=self.hover_template[cl],
            #             visible=False
            #         )
            #     self.trace[self.name_trace[-1]].marker.symbol = self.global_symbols[-1]
            #     self.trace[self.name_trace[-1]].marker.size = self.global_sizes[-1]
            #     self.trace[self.name_trace[-1]].marker.line.color = self.global_markerlinecolor[-1]
            #     self.trace[self.name_trace[-1]].marker.line.width = self.global_markerlinewidth[-1]
            #     self.trace[self.name_trace[-1]]['x'] = self.df_entries_onmap[-1]['x_emb']
            #     self.trace[self.name_trace[-1]]['y'] = self.df_entries_onmap[-1]['y_emb']
            #     color = self.df_entries_onmap[-1][self.widg_colormarkers.value]
            #     self.fig.update_traces(
            #         selector={'name': self.name_trace[-1]},
            #         marker=dict(color=color, colorscale=self.widg_continuouscolors.value),
            #         text=self.hover_text[-1],
            #         customdata=self.hover_custom[-1],
            #         hovertemplate=self.hover_template[-1],
            #         visible=True,
            #     )

    def update_appearance_variables(self):

        self.hover_text = []
        self.hover_custom = []
        self.hover_template = []

        for cl in range(self.n_classes):
            self.hover_text.append(self.df_entries_onmap[cl].index)
            hover_template = r"<b>%{text}</b><br><br>"
            if self.hover_features:
                hover_custom = np.dstack([self.df_entries_onmap[cl][str(self.hover_features[0])].to_numpy()])
                hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
                for i in range(1, len(self.hover_features), 1):
                    hover_custom = np.dstack([hover_custom, self.df_entries_onmap[cl][str(self.hover_features[i])].to_numpy()])
                    hover_template += str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
                self.hover_custom.append(hover_custom[0])
                self.hover_template.append(hover_template)
            else:
                self.hover_custom.append([''])
                self.hover_template.append([''])
        self.hover_text.append(self.df_entries_onmap[-1].index)
        hover_template = r"<b>%{text}</b><br><br>"
        if self.hover_features:
            hover_custom = np.dstack([self.df_entries_onmap[-1][str(self.hover_features[0])].to_numpy()])
            hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
            for i in range(1, len(self.hover_features), 1):
                hover_custom = np.dstack([hover_custom, self.df_entries_onmap[-1][str(self.hover_features[i])].to_numpy()])
                hover_template += str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
            self.hover_custom.append(hover_custom[0])
            self.hover_template.append(hover_template)
        else:
            self.hover_custom.append([''])
            self.hover_template.append([''])

        for cl in np.arange(self.n_classes):
            markerlinewidth = [1] * self.n_points[cl]
            markerlinecolor = ['white'] * self.n_points[cl]
            sizes = [self.marker_size] * self.n_points[cl]
            symbols = self.global_symbols[cl]
            try:
                point = symbols.index('x')
                sizes[point] = self.cross_size
                markerlinewidth[point] = 2
                markerlinecolor[point] = 'black'
            except:
                pass
            try:
                point = symbols.index('cross')
                sizes[point] = self.cross_size
                markerlinewidth[point] = 2
                markerlinecolor[point] = 'black'
            except:
                pass
            self.global_sizes[cl] = sizes
            # self.global_markerlinecolor[cl] = markerlinecolor
            # self.global_markerlinewidth[cl] = markerlinewidth
        self.global_sizes[-1] = [symb for sub in self.global_sizes[:-1] for symb in sub]
        # self.global_markerlinecolor[-1] = [symb for sub in self.global_markerlinecolor[:-1] for symb in sub]
        # self.global_markerlinewidth[-1] = [symb for sub in self.global_markerlinewidth[:-1] for symb in sub]

    def handle_yfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordingly
        feat_x = change.new
        feat_y = self.widg_featy.value

        for cl in range(self.n_classes):
            self.trace[self.name_trace[cl]]['x'] = self.df_classes[cl][str(feat_x)]
        
    def handle_xfeat_change(self, change):
        # changes the feature plotted on the x-axis
        # separating line is modified accordingly
        feat_x = self.widg_featx.value
        feat_y = change.new

        for cl in range(self.n_classes):
            self.trace[self.name_trace[cl]]['y'] = self.df_classes[cl][str(feat_y)]


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


    def show(self):
        
        self.widg_featx.observe(self.handle_xfeat_change, names='value')
        self.widg_featy.observe(self.handle_yfeat_change, names='value')      
        self.widg_plotutils_button.on_click(self.plotappearance_button_clicked)

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


    def print(self):
        print (self.symbols)

    def instantiate_widgets(self):

        self.widg_featx = widgets.Dropdown(
            description='x-axis',
            options=self.embedding_features,
            value=self.embedding_features[0]
        )
        self.widg_featy = widgets.Dropdown(
            description='y-axis',
            options=self.embedding_features,
            value=self.embedding_features[1]
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
        # self.widg_gradient = widgets.Dropdown(
        #     description='-gradient',
        #     options=self.gradient_list,
        #     value='Grey scale',
        #     layout=widgets.Layout(width='150px', right='20px')
        # )
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
            layout = widgets.Layout(left='30px', width='200px')
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
            layout=widgets.Layout(left='50px',width='200px')
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
            layout = widgets.Layout(left='50px', width='640px')
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
                                            widgets.HBox([self.widg_bgtoggle_button,self.widg_updatecolor_button,
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

        self.box_feat = widgets.HBox([widgets.VBox([self.widg_featx, self.widg_featy]),
                                 widgets.VBox([self.widg_featmarker,
                                            #    widgets.HBox([self.widg_featcolor, self.widg_gradient])
                                               ])
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
