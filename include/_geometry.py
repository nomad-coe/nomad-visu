from scipy.spatial import ConvexHull
import numpy as np

def make_hull(self, feat_x, feat_y):

    xhull_classes = {}
    yhull_classes = {}

    for name_trace in self.trace_name:

        points = self.df_trace[name_trace][[feat_x, feat_y]].to_numpy()

        delta_0 = max(points[:, 0]) - min(points[:, 0])
        delta_1 = max(points[:, 1]) - min(points[:, 1])
        exp_1 = int(np.log10(delta_0 / delta_1))
        exp_0 = int(np.log10(delta_1 / delta_0))
        if exp_1 > 6:
            points[:, 1] = points[:, 1] * 10 ** exp_1
        if exp_0 > 6:
            points[:, 0] = points[:, 0] * 10 ** exp_0
        hull = ConvexHull(points)
        vertexes = self.df_trace[name_trace][[feat_x, feat_y]].to_numpy()[hull.vertices]

        x_hullvx = vertexes[:, 0]
        y_hullvx = vertexes[:, 1]
        n_intervals = 100

        xhull = np.array([x_hullvx[0]])
        yhull = np.array([y_hullvx[0]])
        for xy in zip(x_hullvx, y_hullvx):
            xhull = np.concatenate([xhull, np.linspace(xhull[-1], xy[0], n_intervals)])
            yhull = np.concatenate([yhull, np.linspace(yhull[-1], xy[1], n_intervals)])

        xhull_classes [name_trace] = np.concatenate([xhull, np.linspace(xhull[-1], x_hullvx[0], n_intervals)])
        yhull_classes [name_trace] = np.concatenate([yhull, np.linspace(yhull[-1], y_hullvx[0], n_intervals)])


    return xhull_classes, yhull_classes

def regr_line(self, feat_x, feat_y):

        idx_x = self.embedding_features.index(feat_x)
        idx_y = self.embedding_features.index(feat_y)
        line_x = np.linspace(self.df[feat_x].min(), self.df[feat_x].max(), 1000)

        # Gives the classifications line
        if self.widg_featx.value == self.widg_featy.value:
            return line_x, line_x
        else:
            line_y = -line_x * self.regr_line_coefs[0][idx_x] / self.regr_line_coefs[0][idx_y] - self.regr_line_coefs[1] / self.regr_line_coefs[0]  [idx_y]
            return line_x, line_y


