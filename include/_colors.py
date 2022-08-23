from itertools import cycle
import numpy as np
import plotly.express as px
from colour import Color

def make_colors(self):

    feature=self.widg_featcolor.value
    if feature == 'Default color':

        self.palette = cycle(getattr(px.colors.qualitative, self.widg_colorpalette.value))
        for cl in range(self.n_classes):
            name_trace = 'Class ' + str(self.classes[cl])
            self.colors[name_trace] = [next(self.palette)] * len(self.df_classes_on_map[name_trace])

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


    elif (self.widg_featcolor_type.value == 'Gradient'):

        gradient = self.widg_featcolor_list.value
        min_value = self.df[feature].min()
        max_value = self.df[feature].max()

        intervals = 100        

        for cl in range(self.n_classes):

            name_trace = 'Class ' + str(self.classes[cl])
            self.colors[name_trace] = [' '] * len(self.df_classes_on_map[name_trace])


            if gradient == 'Grey scale':
                shade_cl = 0.85 * (self.df_classes_on_map[name_trace][feature].to_numpy() - min_value) / \
                        (max_value - min_value)

                for i, e in enumerate(shade_cl):
                    value = 255 * (0.85 - e)
                    string = 'rgb(' + str(value) + "," + str(value) + "," + str(value) + ')'
                    self.colors[name_trace][i] = string

            if gradient == 'Blue to green':
                    colors = list(Color('blue').range_to(Color('green'), intervals+1))
                    shade_cl = np.trunc(intervals * ((self.df_classes_on_map[name_trace][feature].to_numpy() - min_value) / (max_value - min_value))).astype(int)
                    self.colors[name_trace]=[ str(color) for color in np.array(colors)[shade_cl]]

            if gradient == 'Blue to red':
                    colors = list(Color('blue').range_to(Color('red'), intervals+1))
                    shade_cl = np.trunc(intervals * ((self.df_classes_on_map[name_trace][feature].to_numpy() - min_value) / (max_value - min_value))).astype(int)
                    self.colors[name_trace]=[ str(color) for color in np.array(colors)[shade_cl]]

            if gradient == 'Green to purple':
                    colors = list(Color('green').range_to(Color('purple'), intervals+1))
                    shade_cl = np.trunc(intervals * ((self.df_classes_on_map[name_trace][feature].to_numpy() - min_value) / (max_value - min_value))).astype(int)
                    self.colors[name_trace]=[ str(color) for color in np.array(colors)[shade_cl]]

            if gradient == 'Green to red':
                    colors = list(Color('green').range_to(Color('red'), intervals+1))
                    shade_cl = np.trunc(intervals * ((self.df_classes_on_map[name_trace][feature].to_numpy() - min_value) / (max_value - min_value))).astype(int)
                    self.colors[name_trace]=[ str(color) for color in np.array(colors)[shade_cl]]

            if gradient == 'Yellow to red':
                    colors = list(Color('yellow').range_to(Color('red'), intervals+1))
                    shade_cl = np.trunc(intervals * ((self.df_classes_on_map[name_trace][feature].to_numpy() - min_value) / (max_value - min_value))).astype(int)
                    self.colors[name_trace]=[ str(color) for color in np.array(colors)[shade_cl]]
