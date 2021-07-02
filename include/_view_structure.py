
def view_structure_l(self, formula):
    # replicas = self.df.loc[self.df['Formula'] == formula].index.shape[0]
    # if self.replica_l >= replicas:
    #     self.replica_l = 0
    # i_structure = self.df.loc[self.df['Formula'] == formula]['File-id'].values[self.replica_l]
    # self.viewer_l.script("load data/query_nomad_archive/structures/" + str(int(i_structure)) + ".xyz")
    self.viewer_l.script("load " + self.path_to_structures + formula + ".xyz")


def view_structure_r(self, formula):
    # replicas = self.df[self.df['Formula'] == formula].index.shape[0]
    # if self.replica_r >= replicas:
    #     self.replica_r = 0
    # i_structure = self.df.loc[self.df['Formula'] == formula]['File-id'].values[self.replica_r]
    # self.viewer_r.script("load data/query_nomad_archive/structures/" + str(int(i_structure)) + ".xyz")
    self.viewer_r.script("load " + self.path_to_structures + formula + ".xyz")

