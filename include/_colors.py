from itertools import cycle
import numpy as np
import plotly.express as px
from colour import Color
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def make_colors(self):

        feature=self.widg_featcolor.value
        if feature == 'Default color':

                self.palette = cycle(getattr(px.colors.qualitative, self.widg_colorpalette.value))
                with self.fig.batch_update():

                        for cl in range(self.n_classes):

                                name_trace = 'Class ' + str(self.classes[cl])
                                self.colors[name_trace] = [next(self.palette)] * len(self.df_classes_on_map[name_trace])

                                self.fig.update_traces(
                                        selector={'name': 'Class ' + str(self.classes[cl]) },                                       
                                        marker=dict(showscale=False, color=self.colors[name_trace]) 
                                        )

        elif (self.widg_featcolor_type.value == 'Discrete'):

                colors_dict = {}
                self.palette = cycle(getattr(px.colors.qualitative, self.widg_featcolor_list.value))
                for value in self.df[feature].unique():
                        colors_dict[value]=next(self.palette)

                for cl in range(self.n_classes):

                        name_trace = 'Class ' + str(self.classes[cl])
                        self.colors[name_trace] = [' '] * len(self.df_classes_on_map[name_trace])

                        for i,value in enumerate(self.df_classes_on_map[name_trace][feature]):
                                self.colors[name_trace][i] = colors_dict[value]

                        with self.fig.batch_update():                       
                                self.fig.update_traces(
                                        selector={'name': 'Class ' + str(self.classes[cl]) },
                                        marker=dict(showscale=False, color=self.colors[name_trace]) 
                                )

        elif (self.widg_featcolor_type.value == 'Gradient'):

                feature=self.widg_featcolor.value
                gradient = self.widg_featcolor_list.value
                min_value = self.df[feature].min()
                max_value = self.df[feature].max()

                for cl in range(self.n_classes):
                        name_trace = 'Class ' + str(self.classes[cl])

                        with self.fig.batch_update():
                                
                                self.fig.update_traces(
                                        selector={'name': 'Class ' + str(self.classes[cl]) },
                                        text=self.hover_text[cl],
                                        customdata=self.hover_custom[cl],
                                        hovertemplate=self.hover_template[cl],
                                        # marker_color=self.colors['Class ' + str(self.classes[cl])],
                                        # marker=dict(color=self.colors['Class ' + str(self.classes[cl])],colorbar=dict(thickness=20))
                                        marker = dict (colorscale=gradient, showscale=True, color=self.df_classes_on_map[name_trace][feature], cmin=min_value, cmax=max_value, 
                                        colorbar = dict(thickness=10, orientation='v', len=0.5, y=0.25, title= dict(text=feature, side='right', font={"size":10})) 
                                        )    
                                )