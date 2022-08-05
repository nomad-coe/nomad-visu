import re
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler

def max_covering_shuffle (self, df):


    fractions_dict = {}
    for i,feat_x in enumerate(self.embedding_features):
        for j in np.arange(i+1,len(self.embedding_features)):

            feat_y = self.embedding_features[j]

            # print([MinMaxScaler().fit_transform(df[[feat_x]].values.reshape(-1,1)), MinMaxScaler().fit_transform(df[[feat_y]].values.reshape(-1,1))])

            feat_x_norm = MinMaxScaler().fit_transform(df[feat_x].values.reshape(-1,1))
            feat_y_norm = MinMaxScaler().fit_transform(df[feat_y].values.reshape(-1,1))            
            distances = pairwise_distances ( 
                np.concatenate((feat_x_norm, feat_y_norm), 
                axis=1)
            )
            # distances = np.exp(2*distances)
            n_values = len(df)

            remaininig_indexes = np.arange(n_values)
            selected_indexes = np.array([np.random.randint(n_values)])
            remaininig_indexes = np.delete(remaininig_indexes,selected_indexes)
            
            while (len(remaininig_indexes)>0):
                # prob = np.sum(np.exp(distances[remaininig_indexes,:][:,selected_indexes]), axis=1)
                # prob /= np.sum(prob)
                # new_index = np.array([np.random.choice(remaininig_indexes, p=prob)])

                new_index = np.array([
                    remaininig_indexes[np.argmax(np.sum(distances[remaininig_indexes,:][:,selected_indexes], axis=1))]
                    ])
                selected_indexes = np.concatenate((selected_indexes, new_index))
                remaininig_indexes = np.delete(remaininig_indexes,np.where(remaininig_indexes==new_index))

                if (len(remaininig_indexes)>0):
                    new_index = np.array([
                        remaininig_indexes[np.argmin(np.sum(distances[remaininig_indexes,:][:,remaininig_indexes], axis=1))]
                        ])
                    selected_indexes = np.concatenate((selected_indexes, new_index))
                    remaininig_indexes = np.delete(remaininig_indexes,np.where(remaininig_indexes==new_index))

            fractions_dict [(feat_x,feat_y)] = df.index.to_numpy()[selected_indexes]
            fractions_dict [(feat_y,feat_x)] = df.index.to_numpy()[selected_indexes]

    return fractions_dict

 