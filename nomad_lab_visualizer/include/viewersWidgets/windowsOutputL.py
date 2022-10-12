import ipywidgets as widgets
from IPython.display import display

class WindowsOutputL (object):

    def __init__ (self, viewer):

        self.widget = widgets.Output()

        # with self.widget:
        #     viewer.viewer.show()


        # self.widget.clear_output()
