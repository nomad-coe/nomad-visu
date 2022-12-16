import os
import ipywidgets as widgets
import nomad_visu


class CrossImageR(object):
    def __init__(self):

        file2 = open(
            os.path.join(nomad_visu.__path__[0], "assets/cross2.png"), "rb"
        )
        image2 = file2.read()
        self.widget = widgets.Image(
            value=image2,
            format="png",
            width=30,
            height=30,
        )
