import ipywidgets as widgets

from ...configWidgets import ConfigWidgets

class BgColorUpdate (ConfigWidgets):

    def __init__(self):
    
        self.widget = widgets.Button(
            description="Update background color",
            layout=widgets.Layout(left="50px", width="200px"),
        )

    def observe_change(self, visualizerFigure, BgColor):

        def button_clicked(button):
            """
            update color of the background
            """
            if BgColor.widget.value == "Default" or BgColor.widget.value == "default":
                self.bg_color = self.bg_color_default
                self.bg_toggle = True
            else:
                try:
                    visualizerFigure.FigureWidget.update_layout(
                        plot_bgcolor=BgColor.widget.value,
                        xaxis=dict(gridcolor="white"),
                        yaxis=dict(gridcolor="white"),
                    )
                    self.bg_color = BgColor.widget.value
                    self.bg_toggle = True
                except:
                    pass
            visualizerFigure.batch_update(self)

        self.widget.on_click(button_clicked)