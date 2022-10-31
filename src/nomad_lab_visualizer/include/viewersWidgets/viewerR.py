

import py3Dmol

from nomad_lab_visualizer.configWidgets import ConfigWidgets


class ViewerR (ConfigWidgets):
    
    def __init__ (self):

        self.viewer = py3Dmol.view(width='auto',height=400)

    def view_structure(self, formula, visualizerFigure, output) :
        
        ConfigWidgets.structure_text_r = formula

        if ConfigWidgets.replica_r >= visualizerFigure.df["Replicas"].at[formula]:
            ConfigWidgets.replica_r = 0

        filename = (
            visualizerFigure.df["Structure"].at[formula]
            + "/"
            + visualizerFigure.df["File"].at[formula][ConfigWidgets.replica_r]
        )
        ConfigWidgets.replica_r += 1

        with open(filename, 'r') as file:
            xyz = file.read()

        output.widget.clear_output()
        with output.widget:

            self.viewer.removeAllModels()
            self.viewer.addModel(xyz, 'xyz')
            self.viewer.zoomTo()
            self.viewer.setStyle({'stick':{'colorscheme':'Jmol'}, 'sphere':{'radius': .5, 'colorscheme':'Jmol'}})
            self.viewer.setBackgroundColor('white')
            self.viewer.setProjection('orthographic')
            self.viewer.show()
