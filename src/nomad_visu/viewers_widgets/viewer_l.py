import py3Dmol

from ..config_widgets import ConfigWidgets


class ViewerL(ConfigWidgets):
    def __init__(self):

        self.viewer = py3Dmol.view(width="auto", height=400)

    def view_structure(self, formula, visualizer_figure, output):

        ConfigWidgets.structure_text_l = formula

        if ConfigWidgets.replica_l >= visualizer_figure.df["Replicas"].at[formula]:
            ConfigWidgets.replica_l = 0

        filename = (
            visualizer_figure.df["Structure"].at[formula]
            + "/"
            + visualizer_figure.df["File"].at[formula][ConfigWidgets.replica_l]
        )
        ConfigWidgets.replica_l = ConfigWidgets.replica_l + 1

        with open(filename, "r") as file:
            xyz = file.read()

        output.widget.clear_output()
        with output.widget:

            self.viewer.removeAllModels()
            self.viewer.addModel(xyz, "xyz")
            self.viewer.zoomTo()
            self.viewer.setStyle(
                {
                    "stick": {"colorscheme": "Jmol"},
                    "sphere": {"radius": 0.5, "colorscheme": "Jmol"},
                }
            )
            self.viewer.setBackgroundColor("white")
            self.viewer.setProjection("orthographic")
            self.viewer.show()
