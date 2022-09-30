import ipywidgets as widgets

def instantiate_widgets(self):

    self.widg_featx = widgets.Dropdown(
        description="x-axis",
        options=self.embedding_features,
        value=self.feat_x,
        layout=widgets.Layout(width="250px"),
    )
    self.widg_featy = widgets.Dropdown(
        description="y-axis",
        options=self.embedding_features,
        value=self.feat_y,
        layout=widgets.Layout(width="250px"),
    )
    self.widg_fract_slider = widgets.BoundedFloatText(
        min=0,
        max=1,
        step=0.01,
        value=self.fract,
        layout=widgets.Layout(left="98px", width="60px"),
    )
    self.widg_label_fract = widgets.Label(
        value="Fraction: ", 
        layout=widgets.Layout(left="95px")
    )
    self.widg_featcolor = widgets.Dropdown(
        description="Color",
        options=["Default color"] + self.hover_features,
        value="Default color",
        layout=widgets.Layout(width="250px"),
    )
    self.widg_featcolor_type = widgets.RadioButtons(
        options=["Gradient", "Discrete"],
        value="Gradient",
        layout=widgets.Layout(width="140px", left="90px"),
        disabled=True,
    )
    self.widg_featcolor_list = widgets.Dropdown(
        disabled=True,
        options=self.continuous_gradient_colors,
        value="viridis",
        layout=widgets.Layout(width="65px", height="35px", left="40px"),
    )
    self.widg_featmarker = widgets.Dropdown(
        description="Marker",
        options=["Default size"] + self.hover_features,
        value="Default size",
        layout=widgets.Layout(width="250px"),
    )
    self.widg_featmarker_minvalue = widgets.BoundedFloatText(
        min=0,
        max=self.max_value_markerfeat,
        step=1,
        value=self.min_value_markerfeat,
        disabled=True,
        layout=widgets.Layout(left="91px", width="60px", height="10px"),
    )
    self.widg_featmarker_minvalue_label = widgets.Label(
        value="Min value: ", 
        layout=widgets.Layout(left="94px", width="70px")
    )
    self.widg_featmarker_maxvalue = widgets.BoundedFloatText(
        min=self.min_value_markerfeat,
        step=1,
        value=self.max_value_markerfeat,
        layout=widgets.Layout(left="91px", width="60px"),
        disabled=True,
    )
    self.widg_featmarker_maxvalue_label = widgets.Label(
        value="Max value: ", 
        layout=widgets.Layout(left="94px", width="70px")
    )
