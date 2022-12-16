import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class StructureNameR(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Combobox(
            placeholder="...",
            description="Structure:",
            options=self.structures_list,
            layout=widgets.Layout(width="200px"),
        )
