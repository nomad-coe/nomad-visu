import ipywidgets as widgets
from IPython.display import display, Markdown, FileLink
import os

from ...configWidgets import ConfigWidgets

class Print (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Button(
            description="Print", layout=widgets.Layout(left="50px", width="600px")
        )

    def observe_change(self, visualizerFigure, PrintOut, PlotName, PlotFormat, PlotResolution):

        def button_clicked(button):
            """
            print map
            """

            PrintOut.widget.clear_output()
            text = "A download link will appear soon."
            with PrintOut.widget:
                display(Markdown(text))
            path = "./"
            try:
                os.mkdir(path)
            except:
                pass
            file_name = PlotName.widget.value + "." + PlotFormat.widget.value
            visualizerFigure.FigureWidget.write_image(path + file_name, scale=PlotResolution.widget.value)
            PrintOut.widget.clear_output()
            with PrintOut.widget:
                local_file = FileLink(
                    path + file_name, result_html_prefix="Click here to download: "
                )
                display(local_file)

        self.widget.on_click(button_clicked)