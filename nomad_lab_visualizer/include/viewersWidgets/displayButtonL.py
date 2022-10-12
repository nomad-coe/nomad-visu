import ipywidgets as widgets

from nomad_lab_visualizer.configWidgets import ConfigWidgets


class DisplayButtonL (ConfigWidgets):

    def __init__ (self):

        self.widget = widgets.Button(
            description="Display", layout=widgets.Layout(width="100px")
        )

    def observe_change (self, visualizerFigure, viewerL, structureNameL, outputL):

        def button_clicked( button ):

            # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
            if structureNameL.widget.value in visualizerFigure.df["Structure"]:

                compound_l = structureNameL.widget.value
                # structure_l = Figure.df["Structure"].at[compound_l]

                viewerL.view_structure(compound_l, visualizerFigure, outputL)
                visualizerFigure.batch_update(self)

            
        self.widget.on_click(button_clicked)