import numpy as np
import pandas as pd
import plotly.express as px

def fract_change_updates(self, ConfigWidgets):
    """
    All updates caused by a change in the fraction value.
    """

    self.update_df_on_map(ConfigWidgets)
    self.update_hover_variables()


    
def update_df_on_map(self, ConfigWidgets):
    """
    Updates the number of points based on the fraction value, 
    then 'df_trace_on_map' which is the fraction of the dataframe that is visualized
    """

    for name_trace in self.name_traces:


        n_points = int(
            ConfigWidgets.fract * \
            self.df.loc[self.df[self.target] == name_trace].shape[0]
            )

        if n_points < 1:
            n_points = 1


        if (ConfigWidgets.feat_x, ConfigWidgets.feat_y) in self.optimized_sequence_indexes:
            sequence_indexes = self.optimized_sequence_indexes[
                (ConfigWidgets.feat_x, ConfigWidgets.feat_y)][name_trace] 
        else:
            sequence_indexes = self.random_permutation_indexes[name_trace]

        self.df_trace_on_map[name_trace] = (
            self.df.loc[self.df[self.target] == name_trace]
            .loc[sequence_indexes]
            .head(n_points)
            )

        # if a structure is visualized, its dataframe entry is added to the visualized dataframe 'df_trace_on_map'
        # this to avoid that the entry relative to a visualized structure is not available on the map
        if ConfigWidgets.structure_text_l in self.df.loc[self.df[self.target] == name_trace].index:
            self.df_trace_on_map[name_trace] = pd.concat(
                [
                    self.df_trace_on_map[name_trace],
                    self.df.loc[[ConfigWidgets.structure_text_l]],
                ]
            )

        if ConfigWidgets.structure_text_r in self.df.loc[self.df[self.target] == name_trace].index:
            self.df_trace_on_map[name_trace] = pd.concat(
                [
                    self.df_trace_on_map[name_trace],
                    self.df.loc[[ConfigWidgets.structure_text_r]],
                ]
            )


def update_hover_variables(self):
    """
    Updates the hover data based on the points that are visualized on the map.
    """

    self.hover_text = {}
    self.hover_custom = {}
    self.hover_template = {}

    for name_trace in self.name_traces:

        self.hover_text[name_trace] = self.df_trace_on_map[name_trace].index
        hover_template = r"<b>%{text}</b><br><br>"
        if self.hover_features:
            hover_custom = np.dstack(
                [
                    self.df_trace_on_map[name_trace][
                        str(self.hover_features[0])
                    ].to_numpy()
                ]
            )
            hover_template += str(self.hover_features[0]) + ": %{customdata[0]}<br>"
            for i in range(1, len(self.hover_features), 1):
                hover_custom = np.dstack(
                    [
                        hover_custom,
                        self.df_trace_on_map[name_trace][
                            str(self.hover_features[i])
                        ].to_numpy(),
                    ]
                )
                hover_template += (
                    str(self.hover_features[i]) + ": %{customdata[" + str(i) + "]}<br>"
                )
            self.hover_custom[name_trace] = hover_custom[0]
            self.hover_template[name_trace] = hover_template
        else:
            self.hover_customp[name_trace]=['']
            self.hover_template[name_trace]=['']


