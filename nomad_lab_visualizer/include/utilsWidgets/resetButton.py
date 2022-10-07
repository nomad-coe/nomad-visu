import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class ResetButton (ConfigWidgets):

    def __init__(self):
    
        self.widget = widgets.Button(
            description="Reset symbols", layout=widgets.Layout(left="50px", width="200px")
        )

    def observe_change(self, visualizerFigure):

        def button_clicked( button ):
            """
            reset all marker sizes
            """

            self.widg_markers_symbol.value = "circle"
            for name_trace in visualizerFigure.name_traces:
                n_points = int(
                    ConfigWidgets.fract * \
                    visualizerFigure.df.loc[visualizerFigure.df[visualizerFigure.target] == name_trace].shape[0]
                    )
                name_trace = str(name_trace)
                visualizerFigure.trace_symbol[name_trace] = "circle"
                visualizerFigure.symbols[name_trace] = ["circle"] * n_points
                visualizerFigure.sizes[name_trace] = [self.marker_size] * n_points

            visualizerFigure.batch_update(self)

        self.widget.on_click(button_clicked)
