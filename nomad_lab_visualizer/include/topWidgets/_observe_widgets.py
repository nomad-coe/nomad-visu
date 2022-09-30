from ...configWidgets import ConfigWidgets

def observe_widgets(self, Figure): 

    def handle_xfeat_change(change):
        """
        changes the feature plotted on the x-axis
        """
        
        ConfigWidgets.feat_x = change.new

        if (self.feat_x,self.feat_y) in  Figure.regr_line_trace:
            name_trace = "Regr line" + str(self.feat_x) + ' ' + str(self.feat_y) 
            Figure.trace[name_trace].line = dict(width=0)

        if self.feat_x != self.feat_y:
            if (self.feat_x, self.feat_y) in Figure.optimized_init_fract:
            
                init_fract = Figure.optimized_init_fract[
                    (self.feat_x, self.feat_y)] 
                ConfigWidgets.fract = init_fract
                self.widg_fract_slider.value = init_fract
            else:
                init_fract = Figure.init_fract
                ConfigWidgets.fract = init_fract
                self.widg_fract_slider.value = init_fract
        
        Figure.batch_update(self)

    def handle_yfeat_change(change):
        """
        changes the feature plotted on the y-axis
        """
        ConfigWidgets.feat_y = change.new

        if (self.feat_x,self.feat_y) in  Figure.regr_line_trace:
            name_trace = "Regr line" + str(self.feat_x) + ' ' + str(self.feat_y) 
            Figure.trace[name_trace].line = dict(width=0)

        if self.feat_x != self.feat_y:
            if (self.feat_x, self.feat_y) in Figure.optimized_init_fract:
        
                init_fract = Figure.optimized_init_fract[
                    (self.feat_x, self.feat_y)] 
                ConfigWidgets.fract = init_fract
                self.widg_fract_slider.value = init_fract
            else:
                init_fract = Figure.init_fract
                ConfigWidgets.fract = init_fract
                self.widg_fract_slider.value = init_fract

        Figure.batch_update(self)

    def handle_fract_change(change):
        """
        changes the fraction visualized
        """

        ConfigWidgets.fract = change.new
        Figure.batch_update(self)

    def handle_colorfeat_change(change):
        """
        changes markers color according to a specific feature
        """

        ConfigWidgets.featcolor = change.new

        if change.new == "Default color":
            self.widg_featcolor_type.disabled = True
            self.widg_featcolor_list.disabled = True
            # self.widg_color_palette.disabled = False
        else:
            self.widg_featcolor_type.disabled = False
            self.widg_featcolor_list.disabled = False
            # self.widg_color_palette.disabled = True
        Figure.batch_update(self)

    def handle_featcolor_list_change(change):
        """
        changes the color that is used for markers
        """
        
        ConfigWidgets.featcolor_list = change.new
        Figure.batch_update(self)

    def handle_featcolor_type_change(change):
        """
        changes the type of markers coloring
        """

        ConfigWidgets.featcolor_type = change.new

        if change.new == "Gradient":
            self.widg_featcolor_list.options = self.continuous_gradient_colors
            ConfigWidgets.featcolor_list = "viridis"
            self.widg_featcolor_list.value = "viridis"
        if change.new == "Discrete":
            self.widg_featcolor_list.options = self.discrete_palette_colors
            ConfigWidgets.featcolor_list = "Plotly"
            self.widg_featcolor_list.value = "Plotly"

        Figure.batch_update(self)

    def handle_markerfeat_change(change):
        """
        change markers size according to a specific feature
        """

        if change.new == "Default size":
            self.widg_featmarker_maxvalue.disabled = True
            self.widg_featmarker_minvalue.disabled = True
            # self.widg_markers_size.disabled = False
            # self.widg_cross_size.disabled = False
        else:
            self.widg_featmarker_maxvalue.disabled = False
            self.widg_featmarker_minvalue.disabled = False
            # self.widg_markers_size.disabled = True
            # self.widg_cross_size.disabled = True

        ConfigWidgets.featmarker = change.new
        Figure.batch_update(self)

    def handle_featmarker_maxvalue_change(change):
        """
        changes the max value of the markers size
        """

        ConfigWidgets.max_value_markerfeat = change.new
        self.widg_featmarker_minvalue.max = change.new
        Figure.batch_update(self)

    def handle_featmarker_minvalue_change(change):
        """
        changes the min value of the markers size
        """

        ConfigWidgets.min_value_markerfeat = change.new
        self.widg_featmarker_maxvalue.min = change.new
        Figure.batch_update(self)


    self.widg_featx.observe(handle_xfeat_change, names="value")
    self.widg_featy.observe(handle_yfeat_change, names="value")
    self.widg_fract_slider.observe(handle_fract_change, names='value')
    self.widg_featmarker.observe(handle_markerfeat_change, names="value")
    self.widg_featcolor.observe(handle_colorfeat_change, names="value")
    self.widg_featcolor_list.observe(
        handle_featcolor_list_change, names="value"
    )
    self.widg_featcolor_type.observe(
        handle_featcolor_type_change, names="value"
    )
    self.widg_featmarker_maxvalue.observe(
        handle_featmarker_maxvalue_change, names="value"
    )
    self.widg_featmarker_minvalue.observe(
        handle_featmarker_minvalue_change, names="value"
    )