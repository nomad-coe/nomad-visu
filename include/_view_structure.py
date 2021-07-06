def view_structure_l(self, formula):
    replicas = len(self.path_to_structures[formula])
    if self.replica_l >= replicas:
        self.replica_l = 0
    self.viewer_l.script("load " + self.path_to_structures[formula][self.replica_l])


def view_structure_r(self, formula):
    replicas = len(self.path_to_structures[formula])
    if self.replica_r >= replicas:
        self.replica_r = 0
    self.viewer_r.script("load " + self.path_to_structures[formula][self.replica_r])
