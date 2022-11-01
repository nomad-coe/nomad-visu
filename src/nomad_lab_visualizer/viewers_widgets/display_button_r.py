import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class DisplayButtonR(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Button(
            description="Display", layout=widgets.Layout(width="100px")
        )

    def observe_change(self, visualizer_figure, viewer_r, structure_name_r, output_r):
        def button_clicked(button):

            # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
            if structure_name_r.widget.value in visualizer_figure.df["Structure"]:

                compound_r = structure_name_r.widget.value
                # structure_r = Figure.df["Structure"].at[compound_r]

                viewer_r.view_structure(compound_r, visualizer_figure, output_r)
                visualizer_figure.batch_update(self)

        self.widget.on_click(button_clicked)
