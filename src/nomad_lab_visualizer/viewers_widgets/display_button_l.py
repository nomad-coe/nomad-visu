import ipywidgets as widgets

from nomad_lab_visualizer.config_widgets import ConfigWidgets


class DisplayButtonL(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Button(
            description="Display", layout=widgets.Layout(width="100px")
        )

    def observe_change(self, visualizer_figure, viewer_l, structure_name_l, output_l):
        def button_clicked(button):

            # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
            if structure_name_l.widget.value in visualizer_figure.df["Structure"]:

                compound_l = structure_name_l.widget.value
                # structure_l = Figure.df["Structure"].at[compound_l]

                viewer_l.view_structure(compound_l, visualizer_figure, output_l)
                visualizer_figure.batch_update(self)

        self.widget.on_click(button_clicked)
