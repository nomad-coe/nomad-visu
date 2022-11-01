import ipywidgets as widgets

from nomad_lab_visualizer.config_widgets import ConfigWidgets


class ResetButton(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Button(
            description="Reset symbols",
            layout=widgets.Layout(left="50px", width="200px"),
        )

    def observe_change(self, visualizer_figure):
        def button_clicked(button):
            """
            reset all marker sizes
            """

            self.widg_markers_symbol.value = "circle"
            for name_trace in visualizer_figure.name_traces:
                n_points = int(
                    ConfigWidgets.fract
                    * visualizer_figure.df.loc[
                        visualizer_figure.df[visualizer_figure.target] == name_trace
                    ].shape[0]
                )
                name_trace = str(name_trace)
                visualizer_figure.trace_symbol[name_trace] = "circle"
                visualizer_figure.symbols[name_trace] = ["circle"] * n_points
                visualizer_figure.sizes[name_trace] = [self.marker_size] * n_points

            visualizer_figure.batch_update(self)

        self.widget.on_click(button_clicked)
