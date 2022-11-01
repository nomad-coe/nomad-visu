import ipywidgets as widgets
from IPython.display import display, Markdown, FileLink
import os

from ..config_widgets import ConfigWidgets


class Print(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Button(
            description="Print", layout=widgets.Layout(left="50px", width="600px")
        )

    def observe_change(
        self, visualizer_figure, print_out, plot_name, plot_format, plot_resolution
    ):
        def button_clicked(button):
            """
            print map
            """

            print_out.widget.clear_output()
            text = "A download link will appear soon."
            with print_out.widget:
                display(Markdown(text))
            path = "./"
            try:
                os.mkdir(path)
            except:
                pass
            file_name = plot_name.widget.value + "." + plot_format.widget.value
            visualizer_figure.FigureWidget.write_image(
                path + file_name, scale=plot_resolution.widget.value
            )
            print_out.widget.clear_output()
            with print_out.widget:
                local_file = FileLink(
                    path + file_name, result_html_prefix="Click here to download: "
                )
                display(local_file)

        self.widget.on_click(button_clicked)
