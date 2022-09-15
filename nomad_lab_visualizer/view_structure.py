def view_structure_l(self, formula):

    if self.replica_l >= self.df["Replicas"].at[formula]:
        self.replica_l = 0

    filename = (
        self.df["Structure"].at[formula]
        + "/"
        + self.df["File"].at[formula][self.replica_l]
    )
    self.replica_l = self.replica_l + 1
    
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

    if self.replica_r >= self.df["Replicas"].at[formula]:
        self.replica_r = 0

    filename = (
        self.df["Structure"].at[formula]
        + "/"
        + self.df["File"].at[formula][self.replica_r]
    )
    self.replica_r += 1

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

