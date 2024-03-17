import json
import numpy as np

matrix = np.zeros((16, 24))

with open('Matrix.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
for line in data:
    matrix[int(line['Product_ID']),int(line['\ufeffIngredient_ID'])] = int(line['Num_Ingre'])
print(matrix)