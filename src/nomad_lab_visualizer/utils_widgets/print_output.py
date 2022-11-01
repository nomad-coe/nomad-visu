import ipywidgets as widgets


class PrintOutput(object):
    def __init__(self):

        self.widget = widgets.Output(layout=widgets.Layout(left="150px", width="400px"))
