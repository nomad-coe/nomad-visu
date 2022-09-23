from .configWidgets import ConfigWidgets
from .include._batch_update import batch_update
from .include._updates import marker_style_updates, fract_change_updates
import ipywidgets as widgets
import os
import nomad_lab_visualizer
import py3Dmol

class ViewersWidgets( ConfigWidgets ):
    def __init__( self, Visualizer ):
        
        ConfigWidgets.structures_list = Visualizer.df.index.tolist()

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

        self.widg_box_viewers = widgets.VBox(
            [
                self.widg_description,
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                widgets.HBox(
                                    [
                                        self.widg_structure_text_l,
                                        self.widg_display_button_l,
                                        self.widg_img1,
                                        self.widg_checkbox_l,
                                    ]
                                ),
                                self.output_l,
                            ]
                        ),
                        widgets.VBox(
                            [
                                widgets.HBox(
                                    [
                                        self.widg_structure_text_r,
                                        self.widg_display_button_r,
                                        self.widg_img2,
                                        self.widg_checkbox_r,
                                    ]
                                ),
                                self.output_r,
                            ]
                        ),
                    ]
                ),
            ]
        )

        

        def handle_checkbox_l( change ):
            """
            select left viewer
            """

            if change.new:
                self.widg_checkbox_r.value = False
            else:
                self.widg_checkbox_r.value = True

        def handle_checkbox_r( change ):
            """
            select right viewer
            """

            if change.new:
                self.widg_checkbox_l.value = False
            else:
                self.widg_checkbox_l.value = True

        def handle_point_clicked( trace, points, selector ):
            """
            visualizes structure of clicked point and changes its marker symbol to a cross
            """

            if not points.point_inds:
                return

            trace = points.trace_index
            formula = Visualizer.fig.data[trace].text[points.point_inds[0]]
            structure = Visualizer.df.iloc[points.point_inds[0]]["Structure"]

            if self.widg_checkbox_l.value:
                self.widg_structure_text_l.value = formula
                view_structure_l(self, formula)
            if self.widg_checkbox_r.value:
                self.widg_structure_text_r.value = formula
                view_structure_r(self, formula)

            fract_change_updates(Visualizer)
            marker_style_updates(Visualizer)
            batch_update(Visualizer)

        def display_button_l_clicked( button ):

            # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
            if self.widg_structure_text_l.value in Visualizer.df["Structure"]:

                compound_l = self.widg_structure_text_l.value
                # structure_l = Visualizer.df["Structure"].at[compound_l]

                view_structure_l(self, compound_l)

                fract_change_updates(Visualizer)
                marker_style_updates(Visualizer)
                batch_update(Visualizer)

        def display_button_r_clicked( button ):

            # Actions are performed only if the string inserted in the text widget corresponds to an existing compound
            if self.widg_structure_text_r.value in Visualizer.df["Structure"]:

                compound_r = self.widg_structure_text_r.value
                # structure_r = Visualizer.df["Structure"].at[compound_r]

                view_structure_r(self, compound_r)

                fract_change_updates(Visualizer)
                marker_style_updates(Visualizer)
                batch_update(Visualizer)

        def view_structure_l(self, formula):

            ConfigWidgets.structure_text_l = formula

            if ConfigWidgets.replica_l >= Visualizer.df["Replicas"].at[formula]:
                ConfigWidgets.replica_l = 0

            filename = (
                Visualizer.df["Structure"].at[formula]
                + "/"
                + Visualizer.df["File"].at[formula][ConfigWidgets.replica_l]
            )
            ConfigWidgets.replica_l = ConfigWidgets.replica_l + 1
            
            with open(filename, 'r') as file:
                xyz = file.read()

            self.output_l.clear_output()
            with self.output_l:

                self.viewer_l.removeAllModels()
                self.viewer_l.addModel(xyz, 'xyz')
                self.viewer_l.zoomTo()
                self.viewer_l.setStyle({'stick':{'colorscheme':'Jmol'}, 'sphere':{'radius': .5, 'colorscheme':'Jmol'}})
                self.viewer_l.setBackgroundColor('white')
                self.viewer_l.setProjection('orthographic')
                self.viewer_l.show()

        def view_structure_r(self, formula):
            
            ConfigWidgets.structure_text_r = formula

            if ConfigWidgets.replica_r >= Visualizer.df["Replicas"].at[formula]:
                ConfigWidgets.replica_r = 0

            filename = (
                Visualizer.df["Structure"].at[formula]
                + "/"
                + Visualizer.df["File"].at[formula][ConfigWidgets.replica_r]
            )
            ConfigWidgets.replica_r += 1

            with open(filename, 'r') as file:
                xyz = file.read()

            self.output_r.clear_output()
            with self.output_r:

                self.viewer_r.removeAllModels()
                self.viewer_r.addModel(xyz, 'xyz')
                self.viewer_r.zoomTo()
                self.viewer_r.setStyle({'stick':{'colorscheme':'Jmol'}, 'sphere':{'radius': .5, 'colorscheme':'Jmol'}})
                self.viewer_r.setBackgroundColor('white')
                self.viewer_r.setProjection('orthographic')
                self.viewer_r.show()


        # if Visualizer.path_to_structures:
        for name_trace in Visualizer.trace_name:
            Visualizer.trace[name_trace].on_click(
                handle_point_clicked
            )  # actions performed after clicking points on the map

        self.widg_checkbox_l.observe(handle_checkbox_l, names="value")
        self.widg_checkbox_r.observe(handle_checkbox_r, names="value")

        self.widg_display_button_l.on_click(display_button_l_clicked)
        self.widg_display_button_r.on_click(display_button_r_clicked)

        self.output_l.layout = widgets.Layout(width="400px", height="350px")
        self.output_r.layout = widgets.Layout(width="400px", height="350px")

    def container (self):
        return self.widg_box_viewers
