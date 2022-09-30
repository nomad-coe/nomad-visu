from .configWidgets import ConfigWidgets
import ipywidgets as widgets

class TopWidgets(ConfigWidgets):

    from .include.topWidgets._instantiate_widgets import instantiate_widgets
    from .include.topWidgets._observe_widgets import observe_widgets

    def __init__(self, Figure):

        self.instantiate_widgets()        
        self.observe_widgets(Figure)
        self.widg_box = widgets.VBox(
            [
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                self.widg_featx,
                                self.widg_featy,
                                widgets.HBox(
                                    [self.widg_label_fract, self.widg_fract_slider]
                                ),
                            ]
                        ),
                        widgets.VBox(
                            [
                                self.widg_featcolor,
                                widgets.HBox(
                                    [self.widg_featcolor_type, self.widg_featcolor_list],
                                    layout=widgets.Layout(top="10px"),
                                ),
                            ]
                        ),
                        widgets.VBox(
                            [
                                self.widg_featmarker,
                                widgets.VBox(
                                    [
                                        widgets.HBox(
                                            [
                                                self.widg_featmarker_minvalue_label,
                                                self.widg_featmarker_minvalue,
                                            ],
                                        ),
                                        widgets.HBox(
                                            [
                                                self.widg_featmarker_maxvalue_label,
                                                self.widg_featmarker_maxvalue,
                                            ],
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    
    def container(self):

        return self.widg_box