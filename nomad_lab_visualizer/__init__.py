from .staticVisualizer import StaticVisualizer
import ipywidgets as widgets


class Visualizer(StaticVisualizer):
    """
    in 'Visualizer' all widgets defined in 'staticVisualizer' are given a specific action

    """

    def __init__(
        self,
        df,
        embedding_features,
        hover_features,
        target,
        smart_fract=False,
        convex_hull=False,
        regr_line_coefs=None,
        path_to_structures=None,
    ):
        super().__init__(
            df,
            embedding_features,
            hover_features,
            target,
            smart_fract,
            convex_hull,
            regr_line_coefs,
            path_to_structures,
        )

