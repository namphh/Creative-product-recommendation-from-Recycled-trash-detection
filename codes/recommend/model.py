import json
import numpy as np
import time

# class GetTopSimilar():
#     def __init__(self, input_array, compare_matrix):
#         print(input_array)
#         print(compare_matrix)
#         distances = np.linalg.norm(compare_matrix - input_array, axis=1)
#         print(distances.shape)
#         self.recycled_id = np.argsort(distances)
#         self.euclidean_distances = distances[self.recycled_id]


import numpy as np
import torch
import torch.nn.functional as F

class GetTopSimilar():
    def __init__(self, input_array, compare_matrix):
        distances = self.compute_error(input_array, compare_matrix)
        self.recycled_id = np.argsort(distances)
        self.euclidean_distances = distances[self.recycled_id]



    def compute_error(self, input_array, compare_matrix):
        
        errors = []
        for arr in compare_matrix:
            
            err = np.sum(np.where(arr != 0, 1/arr, 1) * (-0.01 *(input_array - arr))) + 0.1

            print(err)
            errors.append(err)  

        return np.array(errors)

if __name__ == "__main__":
    input_array = np.array([0, 3, 10, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)


    compare_matrix = np.array(data["annotation"][0]["annotation_matrix"])
    print(GetTopSimilar(input_array, compare_matrix).euclidean_distances)

 

        


