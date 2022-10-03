import ipywidgets as widgets

from ...configWidgets import ConfigWidgets

class Featx (ConfigWidgets):

    def __init__(self):

        self.widget = widgets.Dropdown(
            description="x-axis",
            options=self.embedding_features,
            value=self.feat_x,
            layout=widgets.Layout(width="250px"),
        )

    def observe_change(self, visualizerFigure, fractSliderWidget):

        def handle_change(change):
            """
            changes the feature plotted on the x-axis
            """      
                
            ConfigWidgets.feat_x = change.new

            if (self.feat_x,self.feat_y) in  visualizerFigure.regr_line_trace:
                name_trace = "Regr line" + str(self.feat_x) + ' ' + str(self.feat_y) 
                visualizerFigure.trace[name_trace].line = dict(width=0)

            if self.feat_x != self.feat_y:
                if (self.feat_x, self.feat_y) in visualizerFigure.optimized_init_fract:
                
                    init_fract = visualizerFigure.optimized_init_fract[
                        (self.feat_x, self.feat_y)] 
                    ConfigWidgets.fract = init_fract
                    fractSliderWidget.value = init_fract
                else:
                    init_fract = visualizerFigure.init_fract
                    ConfigWidgets.fract = init_fract
                    fractSliderWidget.value = init_fract
            
            visualizerFigure.batch_update(self)

        self.widget.observe(handle_change, names="value")
