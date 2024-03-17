from ultralytics import YOLO
import cv2
import numpy as np
import json

class GetInputArray():
    def __init__(self, image_path, num_of_ingredient):
        self.image_path = image_path
        self.model_path = "best.pt"
        self.model = YOLO(self.model_path)


        results = self.model.predict(show=False, source=image_path)
        for result in results:
            detects = [int(self.model.names[int(box.cls)]) for box in result.boxes if box is not None]
        self.input_array = [0] * num_of_ingredient

        for _ in detects:
            self.input_array[_ - 1] += 1

            
        self.numpy_input_array = np.array(self.input_array)

class GetMatrixCompare():
    def __init__(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.matrix = np.array(data["annotation"][0]["annotation_matrix"])
        self.info = data["info"]
        self.recycled = data["recycled"]
        self.materials = data["materials"]
        

if __name__ == "__main__":
    print(GetInputArray("1.jpg", 24).input_array)   





