from itertools import cycle
import plotly.express as px

def make_colors(self, feature, gradient):
    if feature == 'Default color':
        self.palette = cycle(getattr(px.colors.qualitative, self.qualitative_colors[0]))

        for cl in range(self.n_classes):
            self.colors[cl] = [next(self.palette)] * self.n_points[cl]

    else:
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