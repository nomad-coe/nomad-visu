import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets


class DisplayButtonR (ConfigWidgets):

    def __init__ (self):

        self.widget = widgets.Button(
            description="Display", layout=widgets.Layout(width="100px")
        )

    def observe_change (self, visualizerFigure, viewerR, structureNameR, outputR):

        def button_clicked( button ):

            # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
            if structureNameR.widget.value in visualizerFigure.df["Structure"]:

                compound_r = structureNameR.widget.value
                # structure_r = Figure.df["Structure"].at[compound_r]

                viewerR.view_structure(compound_r, visualizerFigure, outputR)
                visualizerFigure.batch_update(self)

        self.widget.on_click(button_clicked)