import ipywidgets as widgets
import os
import nomad_lab_visualizer

class CrossImageR (object):

    def __init__ (self):

        file2 = open(
            os.path.join(nomad_lab_visualizer.__path__[0], "assets/cross2.png"), "rb"
        )
        image2 = file2.read()
        self.widget = widgets.Image(
            value=image2,
            format="png",
            width=30,
            height=30,
        )