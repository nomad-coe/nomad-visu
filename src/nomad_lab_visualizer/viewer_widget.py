import py3Dmol
import ipywidgets as widgets


class py3DmolWidget(widgets.Output):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = widgets.Layout(width="400px", height="350px")
        # self._viewer = py3Dmol.view()
        self._viewer = py3Dmol.view(width="auto", height=400)
        # with self:
            # self._viewer.show()
            # self._viewer.resize()

    def load_structure(self, xyz: str):
        self._viewer.clear()
        # self._viewer.removeAllModels()
        self._viewer.addModel(xyz, "xyz")
        self._viewer.zoomTo()
        self._viewer.setStyle(
            {
                "stick": {"colorscheme": "Jmol"},
                "sphere": {"radius": 0.5, "colorscheme": "Jmol"},
            }
        )
        self._viewer.setBackgroundColor("white")
        self._viewer.setProjection("orthographic")

        with self:
            self._viewer.update()

class AtomisticViewerWidget(widgets.HBox):
    pass


#
# structures_list = ["h2o", "co2"]
#
#
# widget_structure = widgets.Combobox(
#     placeholder="",
#     description="Structure:",
#     options=structures_list,
#     # layout=widgets.Layout(width="200px"),
# )
#
# widget_perv_button = widgets.Button(
#     description="<", layout=widgets.Layout(width="50px")
# )
# widget_next_button = widgets.Button(
#     description=">", layout=widgets.Layout(width="50px")
# )
#
# widget_label = widgets.Label('1/6', layout=widgets.Layout(width="50px", display="flex", justify_content="center"))
#
# output = widgets.Output(layout = widgets.Layout(width="400px", height="350px"))
#
#
# widgets.VBox(
#     [
#         widgets.HBox(
#             [
#                 widget_structure,
#                 widget_perv_button,
#                 widget_label,
#                 widget_next_button
#             ]
#         ),
#         output,
#     ]
# )
