import streamlit as st
from PIL import Image
import numpy as np
from model import GetTopSimilar
from getData import GetMatrixCompare, GetInputArray
import os
import time
from io import BytesIO

def imgProcessing(image):
        # Get input array using GetInputArray
        num_of_ingredient = 24  # Assuming number of ingredients
        input_array = GetInputArray(image, num_of_ingredient).numpy_input_array

        # Assuming your JSON file path
        json_file_path = 'data.json'

        # Get compare matrix using GetMatrixCompare
        gmc = GetMatrixCompare(json_file_path)
        compare_matrix = gmc.matrix
        materials = {material["id"]: material["name"] for material in gmc.materials}
        recycled_items = {item["id"]: item for item in gmc.recycled}

        # Display identified materials

        st.write("Identified Materials")
        for material_id, material_quantity in enumerate(input_array):
            if material_quantity != 0:
                material_name = materials.get(material_id + 1, "Unknown Material")
                st.write(f"- You have {material_quantity} {material_name}")

        
        for i in range(len(materials)):
            col1, col2 = st.sidebar.columns(2)
            col1.write(f"ID: {i+1}")
            col2.write(f"{materials.get(i + 1, 'Unknown Material')}")
        
        adjust = st.text_input("Confirm the quantities.")
        st.write(" Type 'ok' to confirm. Or adjust specific value use ~ EX: 1:3, 2:4")
        if adjust:
            if adjust == "ok":
                pass
            else:
                pairs = adjust.split(", ")
                for pair in pairs:
                    index, value = pair.split(":")
                    index = int(index)
                    value = int(value)
                    input_array[index - 1] = value

            for material_id, material_quantity in enumerate(input_array):
                if material_quantity != 0:
                    material_name = materials.get(material_id + 1, "Unknown Material")
                    st.write(f"- You have {material_quantity} {material_name}")
            

            # Get top similar using GetTopSimilar
            top_similar = GetTopSimilar(input_array, compare_matrix)

            # Display top similar recycled items
            for recycled_id, euclidean_distance in zip(top_similar.recycled_id, top_similar.euclidean_distances):
                if recycled_id == 15 or recycled_id == 16:
                    continue
                    
                col1, col2 = st.columns(2)
                with col1:
                    recycled_image_path = f'recycled_images/{recycled_id+1}.png'
                    if os.path.exists(recycled_image_path):
                        recycled_image = Image.open(recycled_image_path)
                        st.image(recycled_image, caption=f'Recycled ID: {recycled_id+1}', use_column_width=True)
                    else:
                        st.write(f'Image not found for Recycled ID: {recycled_id+1}')
                with col2:
                    recycled_item = recycled_items[recycled_id+1]
                    st.write(f'Recycled ID: {recycled_id+1}')
                    st.write(f'Error rate: {euclidean_distance}')
                    st.write(f"Name: {recycled_item['name']}")
                    st.write(f"URL: {recycled_item['url']}")
                    st.write(f"Difficulty Level: {recycled_item['difficult_level']}")
                    st.write(f"Danger Level: {recycled_item['danger_level']}")
                    compare_materials = input_array - compare_matrix[recycled_id]
                    for i, _ in enumerate(compare_materials):
                        if _ == 0:
                            pass
                        elif _ > 0:
                            st.write(f"You are redundant  {int(_)} material: {materials.get(i+1)}")
                        else:
                            st.write(f"You are missing {int(-_)} material: {materials.get(i+1)}")
                    st.write('--------------------------------')





st.title('Recycled stuffs from materials recommendation')
# Add a radio button to select the input method
input_method = st.radio("Select Input Method:", ("Upload Image", "Take Photo"))

start = time.time()  # Start time

if input_method == "Upload Image":
    # File uploader for image
    image_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'webp'])
    if image_file is not None:
        # Display the uploaded image
        image = Image.open(image_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        imgProcessing(image)

elif input_method == "Take Photo":
    # Camera input to take a photo
    picture = st.camera_input("Take a picture")
    if picture is not None:
        # Convert the captured image to bytes
        image_bytes = picture.read()
        # Convert the bytes to a PIL Image
        image = Image.open(BytesIO(image_bytes))
        imgProcessing(image)


# Calculate time taken
end = time.time()
st.write(f"Processing Time: {end - start} seconds")



