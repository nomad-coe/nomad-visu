import re
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler

def smart_fract_make (self):

    n_neighbors = 10

    fractions_dict = {}
    fractions_thres = {}

    for i,feat_x in enumerate(self.embedding_features):
        for j in np.arange(i+1,len(self.embedding_features)):

            feat_y = self.embedding_features[j]
            
            fractions_dict [(feat_x,feat_y)]={}
            fractions_dict [(feat_y,feat_x)]={}
            
            fractions_thres_cl = []

            for name_trace in self.trace_name:

                feat_x_norm = MinMaxScaler().fit_transform(self.df_trace[name_trace][feat_x].values.reshape(-1,1))
                feat_y_norm = MinMaxScaler().fit_transform(self.df_trace[name_trace][feat_y].values.reshape(-1,1))            

                distances = pairwise_distances ( 
                    np.concatenate((feat_x_norm, feat_y_norm), 
                    axis=1)
                )
                n_values = len(self.df_trace[name_trace])

                remaininig_indexes = np.arange(n_values)
                new_index = np.array([
                    remaininig_indexes[np.argmin(np.sum(distances, axis=1))]
                    ])
                selected_indexes = np.array([new_index]).reshape(1)
                remaininig_indexes = np.delete(remaininig_indexes,selected_indexes)

                last_cost = 1
                bool_cost = True

                while (len(remaininig_indexes)>0):

                    n_neighbors = int(len(remaininig_indexes)/10)
                    if (n_neighbors<10):
                        n_neighbors = 10                
                    # prob = np.sum(np.exp(distances[remaininig_indexes,:][:,selected_indexes]), axis=1)
                    # prob /= np.sum(prob)
                    # new_index = np.array([np.random.choice(remaininig_indexes, p=prob)])

                    num=np.sum(np.sort(distances[remaininig_indexes,:][:,remaininig_indexes])[:,:n_neighbors], axis=1)
                    den=np.sum(np.sort(distances[remaininig_indexes,:][:,selected_indexes])[:,:n_neighbors], axis=1)
                    cost = num/den
                    arg = np.argmin(cost)

                    if (bool_cost) :
                        new_cost = cost[arg]
                        if (new_cost>1 and last_cost<1):
                            fractions_thres_cl.append(len(selected_indexes)/len(distances))
                            # fractions_thres [(feat_x, feat_y)] = len(selected_indexes)/len(distances)
                            # fractions_thres [(feat_y, feat_x)] = len(selected_indexes)/len(distances)
                            bool_cost = False
                        last_cost = new_cost

                    new_index = np.array([remaininig_indexes[arg]])
                    remaininig_indexes = np.delete(remaininig_indexes,np.where(remaininig_indexes==new_index))
                    selected_indexes = np.concatenate((selected_indexes, new_index))
                    
                    if (len(remaininig_indexes>0) and len(remaininig_indexes)%10==0):
                        new_index = np.array([remaininig_indexes[np.argmax(
                            np.sum(np.sort(distances[remaininig_indexes,:][:,selected_indexes])[:,:n_neighbors], axis=1)
                        )]])
                        remaininig_indexes = np.delete(remaininig_indexes,np.where(remaininig_indexes==new_index))
                        selected_indexes = np.concatenate((selected_indexes, new_index))

                fractions_dict[(feat_x,feat_y)][name_trace] = self.df_trace[name_trace].index.to_numpy()[selected_indexes]
                fractions_dict[(feat_y,feat_x)][name_trace] = self.df_trace[name_trace].index.to_numpy()[selected_indexes]

        fractions_thres[(feat_x,feat_y)] = min(fractions_thres_cl)
        fractions_thres[(feat_y,feat_x)] = min(fractions_thres_cl)

    return fractions_dict, fractions_thres

 