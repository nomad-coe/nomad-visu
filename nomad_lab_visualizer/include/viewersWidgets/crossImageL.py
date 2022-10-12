import ipywidgets as widgets
import os

from nomad_lab_visualizer.configWidgets import ConfigWidgets 
import nomad_lab_visualizer

class CrossImageL (ConfigWidgets):

    def __init__ (self):
    
        file1 = open(
            os.path.join(nomad_lab_visualizer.__path__[0], "assets/cross1.png"), "rb"
            )
        image1 = file1.read()
        self.widget = widgets.Image(
            value=image1,
            format="png",
            width=30,
            height=30,
        )