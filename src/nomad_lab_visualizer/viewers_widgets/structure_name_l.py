import ipywidgets as widgets

from ..config_widgets import ConfigWidgets


class StructureNameL(ConfigWidgets):
    def __init__(self):

        self.widget = widgets.Combobox(
            placeholder="...",
            description="Structure:",
            options=ConfigWidgets.structures_list,
            layout=widgets.Layout(width="200px"),
        )
