import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
import os
from PIL import Image

st.set_page_config(
    page_title="Processing Page",
    page_icon="👋",
)

st.write("# Lets get started! 👋")

uploaded_file = st.file_uploader("Choose a file")

st.markdown('<a href="/ouput_page" target="_self">Click on this line to get your output!</a>', unsafe_allow_html=True)



def get_image_path(img):
    # Create a directory and save the uploaded image.
    file_path = f"data/uploadedImages/{img.name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as img_file:
        img_file.write(img.getbuffer())
    return file_path

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # Store "Image file" into actual image
    bytes_data = get_image_path(uploaded_file)
    #Resizing image
    image = Image.open(bytes_data)
    width = image.width 
    height = image.height 
    if width > height :
        x = 512
        ratio = 512/width
        y = int(height * ratio)
        while y%64 != 0:
            y = y + 1
    else :
        y = 512
        ratio = 512/height
        x = int(width * ratio)
        while y%64 != 0:
            y = y + 1     
    new_bytes_data = image.resize((x,y))
    #display image
    st.image(new_bytes_data)

