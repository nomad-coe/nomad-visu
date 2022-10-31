import ipywidgets as widgets

class WindowsCheckboxL (object):

    def __init__ (self):

        self.widget = widgets.Checkbox(
            value=True, 
            indent=False, 
            layout=widgets.Layout(width="50px")
        )

    def observe_change (self, windowsCheckboxR ):

        def handle_change( change ):
            """
            select left viewer
            """

            if change.new:
                windowsCheckboxR.widget.value = False
            else:
                windowsCheckboxR.widget.value = True

        self.widget.observe(handle_change, names="value")