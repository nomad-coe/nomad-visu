import re
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

def make_optimized_frac (self, feat_x, feat_y):

    n_neighbors = 10
    fraction_thres = 1
    optimized_sequence = {}

    for name_trace in self.trace_name:

        feat_x_norm = MinMaxScaler().fit_transform(self.df_trace[name_trace][feat_x].values.reshape(-1,1))
        feat_y_norm = MinMaxScaler().fit_transform(self.df_trace[name_trace][feat_y].values.reshape(-1,1))            

        X = np.concatenate((feat_x_norm, feat_y_norm), axis=1)

        nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree').fit(X)
        nbrs_distances, nbrs_indices = nbrs.kneighbors(X)

        n_values = len(self.df_trace[name_trace])

        remaining_indices= np.arange(n_values)

        new_index = np.array([
            remaining_indices[np.argmin(np.sum(nbrs_distances, axis=1))]
            ])
        selected_indices = np.array([new_index]).reshape(1)
        remaining_indices = np.delete(remaining_indices,selected_indices)
        mask = np.where(nbrs_indices==new_index, 1, 0)

        last_cost = 0
        bool_cost = True

        while (len(remaining_indices)>0):
    
            # prob = np.sum(np.exp(distances[remaininig_indexes,:][:,selected_indexes]), axis=1)
            # prob /= np.sum(prob)
            # new_index = np.array([np.random.choice(remaininig_indexes, p=prob)])

            # the numerator gives the sum of the distances over the indexes that do not appear on the map
            # the closer the points that do not appear on the map are, the more likely the point is selected
            num=np.sum((mask*nbrs_distances)[remaining_indices],axis=1)
            # the denominater gives the sum of the distances over the indexes that appear on the map
            # the closer the points that appear on the map are, the less likely the point is selected
            den=np.sum(((1-mask)*nbrs_distances)[remaining_indices],axis=1)
            if (np.min(num)==0):
                arg=np.argmax(den[np.where(num==0)])
                new_index = np.array([remaining_indices[np.where(num==0)][arg]])
                new_cost = 0
            elif (np.min(den)==0):
                arg=np.argmin(num[np.where(den==0)])
                new_index = np.array([remaining_indices[np.where(den==0)][arg]])
                new_cost = float('inf')
            else:
                arg=np.argmin(num/den)
                new_index = np.array([remaining_indices[arg]])
                new_cost = (num/den)[arg]

            if (bool_cost) :
                if (new_cost>1 and last_cost<1):
                    fraction_thres = len(selected_indices)/n_values
                    # fractions_thres [(feat_x, feat_y)] = len(selected_indexes)/len(distances)
                    # fractions_thres [(feat_y, feat_x)] = len(selected_indexes)/len(distances)
                    bool_cost = False
                last_cost = new_cost

            remaining_indices = np.delete(remaining_indices,np.where(remaining_indices==new_index))
            selected_indices = np.concatenate((selected_indices, new_index))
            mask = mask+np.where(nbrs_indices==new_index, 1, 0)
            
            if (len(remaining_indices>0) and len(remaining_indices)%10==0):
                arg=np.argmax(np.sum((mask*nbrs_distances)[remaining_indices],axis=1))
                new_index = np.array([remaining_indices[arg]])
                remaining_indices = np.delete(remaining_indices,np.where(remaining_indices==new_index))
                selected_indices = np.concatenate((selected_indices, new_index))
                mask = mask+np.where(nbrs_indices==new_index, 1, 0)
        
        optimized_sequence[name_trace] =  selected_indices

    return optimized_sequence, fraction_thres

 