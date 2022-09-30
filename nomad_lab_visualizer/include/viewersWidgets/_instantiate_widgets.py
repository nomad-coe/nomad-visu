import ipywidgets as widgets
import os
import nomad_lab_visualizer
import py3Dmol

from ...configWidgets import ConfigWidgets


def instantiate_widgets(self, Figure):   
    
    file1 = open(
        os.path.join(nomad_lab_visualizer.__path__[0], "assets/cross1.png"), "rb"
        )
    image1 = file1.read()
    self.widg_img1 = widgets.Image(
        value=image1,
        format="png",
        width=30,
        height=30,
    )
    file2 = open(
        os.path.join(nomad_lab_visualizer.__path__[0], "assets/cross2.png"), "rb"
    )
    image2 = file2.read()
    self.widg_img2 = widgets.Image(
        value=image2,
        format="png",
        width=30,
        height=30,
    )
    self.output_l = widgets.Output()
    self.output_r = widgets.Output()
    self.widg_description = widgets.Label(
        value="Tick the box next to the cross symbols in order to choose which windows visualizes the next "
        "structure selected in the map above."
    )
    self.widg_structure_text_l = widgets.Combobox(
        placeholder="...",
        description="Structure:",
        options=ConfigWidgets.structures_list,
        layout=widgets.Layout(width="200px"),
    )
    self.widg_display_button_l = widgets.Button(
        description="Display", layout=widgets.Layout(width="100px")
    )
    self.widg_checkbox_l = widgets.Checkbox(
        value=True, indent=False, layout=widgets.Layout(width="50px")
    )
    self.widg_structure_text_r = widgets.Combobox(
        placeholder="...",
        description="Structure:",
        options=ConfigWidgets.structures_list,
        layout=widgets.Layout(width="200px"),
    )
    self.widg_display_button_r = widgets.Button(
        description="Display", layout=widgets.Layout(width="100px")
    )
    self.widg_checkbox_r = widgets.Checkbox(
        value=False,
        indent=False,
        layout=widgets.Layout(width="50px"),
    )
    self.viewer_l = py3Dmol.view(width='auto',height=400)
    self.viewer_r = py3Dmol.view(width='auto',height=400)
