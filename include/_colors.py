from itertools import cycle
import plotly.express as px

def make_colors(self):

    feature=self.widg_featcolor.value
    if feature == 'default color':

        self.palette = cycle(getattr(px.colors.qualitative, self.widg_colorpalette.value))
        for cl in range(self.n_classes):
            name_trace = 'Class ' + str(self.classes[cl])
            self.colors[name_trace] = [next(self.palette)] * self.n_points[name_trace]

    else:
        gradient = self.widg_gradient.value
        min_value = self.df[feature].min()
        max_value = self.df[feature].max()

        for cl in range(self.n_classes):

            name_trace = 'Class ' + str(self.classes[cl])
            self.colors[name_trace] = [' '] * self.n_points[name_trace]

            if gradient == 'Grey scale':
                shade_cl = 0.7 * (self.df_classes_on_map[cl][feature].to_numpy() - min_value) / \
                        (max_value - min_value)
                for i, e in enumerate(shade_cl):
                    value = 255 * (0.7 - e)
                    string = 'rgb(' + str(value) + "," + str(value) + "," + str(value) + ')'
                    self.colors[name_trace][i] = string

            if gradient == 'Purple scale':
                    shade_cl = 0.7 * (self.df_classes_on_map[cl][feature].to_numpy() - min_value) / \
                            (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * (0.7 - e)
                        string = 'rgb(' + str(value) + "," + str(0) + "," + str(value) + ')'
                        self.colors[name_trace][i] = string

            if gradient == 'Turquoise scale':
                    shade_cl = 0.7 * (self.df_classes_on_map[cl][feature].to_numpy() - min_value) / \
                            (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * (0.7 - e)
                        string = 'rgb(' + str(0) + "," + str(value) + "," + str(value) + ')'
                        self.colors[name_trace][i] = string

            if gradient == 'Blue to green':
                    shade_cl = 0.7 * (self.df_classes_on_map[cl][feature].to_numpy() - min_value) / \
                            (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * e
                        value2 = 255 - value
                        string = 'rgb(' + str(0) + "," + str(value) + "," + str(value2) + ')'
                        self.colors[name_trace][i] = string

            if gradient == 'Blue to red':
                    shade_cl = 0.7 * (self.df_classes_on_map[cl][feature].to_numpy() - min_value) / \
                            (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * e
                        value2 = 255 - value
                        string = 'rgb(' + str(value) + "," + str(0) + "," + str(value2) + ')'
                        self.colors[name_trace][i] = string

            if gradient == 'Green to red':
                    shade_cl = 0.7 * (self.df_classes_on_map[cl][feature].to_numpy() - min_value) / \
                            (max_value - min_value)
                    for i, e in enumerate(shade_cl):
                        value = 255 * e
                        value2 = 255 - value
                        string = 'rgb(' + str(value) + "," + str(value2) + "," + str(0) + ')'
                        self.colors[name_trace][i] = string