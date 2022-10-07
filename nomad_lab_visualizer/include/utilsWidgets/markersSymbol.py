import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets

class MarkersSymbol (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.symbols_list,
            description="--- symbol",
            value=self.symbols_list[0],
            layout=widgets.Layout(left="30px", width="200px"),
        )


    def observe_change (self, visualizerFigure, TraceSymbol):

        self.widget.value = visualizerFigure.trace_symbol[visualizerFigure.name_traces[0]]
        
        def handle_change ( change ) :
            """
            change marker symbol for trace
            """
            name_trace = str(TraceSymbol.widget.value)
            visualizerFigure.trace_symbol[name_trace] = change.new
            visualizerFigure.symbols[name_trace] = [str(change.new)] * len(
                visualizerFigure.df_trace_on_map[name_trace]
            )
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")