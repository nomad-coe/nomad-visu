from .configWidgets import ConfigWidgets
import ipywidgets as widgets


class ViewersWidgets( ConfigWidgets ):
        
    from .include.viewersWidgets._instantiate_widgets import instantiate_widgets
    from .include.viewersWidgets._observe_widgets import observe_widgets

    def __init__(self, Figure):

        ConfigWidgets.structures_list = Figure.df.index.tolist()

        self.instantiate_widgets(Figure)         
        self.observe_widgets(Figure)

        self.widg_box = widgets.VBox(
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
        
    def container (self):

        return self.widg_box
