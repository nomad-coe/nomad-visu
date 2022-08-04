def view_structure_l(self, formula):


    if (self.replica_l >= self.df['Replicas'].at[formula]):
        self.replica_l = 0

    path = self.df['Structure'].at[formula] + "/" + self.df['File'].at[formula][self.replica_l]
    string = "load " + path
    self.viewer_l.script(string)
    self.replica_l = self.replica_l + 1


def view_structure_r(self, formula):


    if (self.replica_r >= self.df['Replicas'].at[formula]):
        self.replica_r = 0

    path = self.df['Structure'].at[formula] + "/" + self.df['File'].at[formula][self.replica_r]
    string = "load " + path
    self.viewer_r.script(string)
    self.replica_r += 1

