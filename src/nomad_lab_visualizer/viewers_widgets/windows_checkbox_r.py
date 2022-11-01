import ipywidgets as widgets


class WindowsCheckboxR(object):
    def __init__(self):

        self.widget = widgets.Checkbox(
            value=False,
            indent=False,
            layout=widgets.Layout(width="50px"),
        )

    def observe_change(self, windows_checkbox_l):
        def handle_change(change):
            """
            select right viewer
            """

            if change.new:
                windows_checkbox_l.widget.value = False
            else:
                windows_checkbox_l.widget.value = True

        self.widget.observe(handle_change, names="value")
