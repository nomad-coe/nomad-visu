import ipywidgets as widgets

from nomad_lab_visualizer.config_widgets import ConfigWidgets


class MarkersSymbol(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Dropdown(
            options=self.symbols_list,
            description="--- symbol",
            value=self.symbols_list[0],
            layout=widgets.Layout(left="30px", width="200px"),
        )

    def observe_change(self, visualizer_figure, trace_symbol):

        self.widget.value = visualizer_figure.trace_symbol[
            visualizer_figure.name_traces[0]
        ]

        def handle_change(change):
            """
            change marker symbol for trace
            """
            name_trace = str(trace_symbol.widget.value)
            visualizer_figure.trace_symbol[name_trace] = change.new
            visualizer_figure.symbols[name_trace] = [str(change.new)] * len(
                visualizer_figure.df_trace_on_map[name_trace]
            )
            visualizer_figure.batch_update(self)

        self.widget.observe(handle_change, names="value")
