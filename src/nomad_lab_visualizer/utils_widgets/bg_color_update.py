import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class BgColorUpdate(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Button(
            description="Update background color",
            layout=widgets.Layout(left="50px", width="200px"),
        )

    def observe_change(self, visualizer_figure, bg_color):
        def button_clicked(button):
            """
            update color of the background
            """
            if bg_color.widget.value == "Default" or bg_color.widget.value == "default":
                self.bg_color = self.bg_color_default
                self.bg_toggle = True
            else:
                try:
                    visualizer_figure.FigureWidget.update_layout(
                        plot_bgcolor=bg_color.widget.value,
                        xaxis=dict(gridcolor="white"),
                        yaxis=dict(gridcolor="white"),
                    )
                    self.bg_color = bg_color.widget.value
                    self.bg_toggle = True
                except:
                    pass
            visualizer_figure.batch_update(self)

        self.widget.on_click(button_clicked)
