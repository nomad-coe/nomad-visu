import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class Featx(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            description="x-axis",
            options=self.embedding_features,
            value=self.feat_x,
            layout=widgets.Layout(width="250px"),
        )

    def observe_change(
        self,
        visualizer_figure,
        fract_slider_widget,
        color_line_widget,
        width_line_widget,
        dash_line_widget,
    ):
        def handle_change(change):
            """
            changes the feature plotted on the x-axis
            """

            if (self.feat_x, self.feat_y) in visualizer_figure.regr_line_trace:
                name_trace = "Regr line" + str(self.feat_x) + " " + str(self.feat_y)
                visualizer_figure.trace[name_trace].line = dict(width=0)

            ConfigWidgets.feat_x = change.new

            if (self.feat_x, self.feat_y) in visualizer_figure.regr_line_trace:
                name_trace = "Regr line" + str(self.feat_x) + " " + str(self.feat_y)
                visualizer_figure.trace[name_trace].line = dict(width=0)

            color_line_widget.disabled = True
            width_line_widget.disabled = True
            dash_line_widget.disabled = True

            if self.feat_x != self.feat_y:
                if (self.feat_x, self.feat_y) in visualizer_figure.optimized_init_fract:

                    init_fract = visualizer_figure.optimized_init_fract[
                        (self.feat_x, self.feat_y)
                    ]
                    ConfigWidgets.fract = init_fract
                    fract_slider_widget.value = init_fract
                    color_line_widget.disabled = False
                    width_line_widget.disabled = False
                    dash_line_widget.disabled = False
                else:
                    init_fract = visualizer_figure.init_fract
                    ConfigWidgets.fract = init_fract
                    fract_slider_widget.value = init_fract

            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
