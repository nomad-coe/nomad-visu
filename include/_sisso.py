from scipy.spatial import ConvexHull
import numpy as np

def make_hull(self, feat_x, feat_y):

    xhull_classes = []
    yhull_classes = []

    for cl in range (self.n_classes):

        points = self.df_classes[cl][[feat_x, feat_y]].to_numpy()

        delta_0 = max(points[:, 0]) - min(points[:, 0])
        delta_1 = max(points[:, 1]) - min(points[:, 1])
        exp_1 = int(np.log10(delta_0 / delta_1))
        exp_0 = int(np.log10(delta_1 / delta_0))
        if exp_1 > 6:
            points[:, 1] = points[:, 1] * 10 ** exp_1
        if exp_0 > 6:
            points[:, 0] = points[:, 0] * 10 ** exp_0
        hull = ConvexHull(points)
        vertexes = self.df_classes[cl][[feat_x, feat_y]].to_numpy()[hull.vertices]

        x_hullvx = vertexes[:, 0]
        y_hullvx = vertexes[:, 1]
        n_intervals = 100

        xhull = np.array([x_hullvx[0]])
        yhull = np.array([y_hullvx[0]])
        for xy in zip(x_hullvx, y_hullvx):
            xhull = np.concatenate([xhull, np.linspace(xhull[-1], xy[0], n_intervals)])
            yhull = np.concatenate([yhull, np.linspace(yhull[-1], xy[1], n_intervals)])

        xhull_classes.append (np.concatenate([xhull, np.linspace(xhull[-1], x_hullvx[0], n_intervals)]))
        yhull_classes.append (np.concatenate([yhull, np.linspace(yhull[-1], y_hullvx[0], n_intervals)]))


    return xhull_classes, yhull_classes
