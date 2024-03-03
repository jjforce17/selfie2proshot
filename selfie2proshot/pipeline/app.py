import streamlit as st
import image_background_lib as glib

import pandas as pd
from io import StringIO, BytesIO
import os
from PIL import Image

def generate_download_button(generated_image):
        with generated_image as file: 
            btn = st.download_button(
                label = "Download",
                data = file,
                file_name = "Selfie2Pro.png",
                mime="image/png"
                )


st.set_page_config(layout="wide", page_title="Image Background")

st.title("Selfie2Pro")

col1, col2, col3 = st.columns(3)


with col1:
    st.subheader("Upload")
    uploaded_file = st.file_uploader("Select an image", type=['png', 'jpg'])
    
    if uploaded_file:
        uploaded_image_preview = glib.get_bytesio_from_bytes(uploaded_file.getvalue())
        st.image(uploaded_image_preview)
    else:
        st.image("images/example.jpg")

with col2:
    
    # mask_prompt = st.text_input("Object to keep:", value="Car", help="The mask text")
    
    # prompt_text = st.text_area("Description including the object to keep and background to add:", value="Car at the beach", height=100, help="The prompt text")
    
    # negative_prompt = st.text_input("What should not be in the background:", help="The negative prompt")

    # outpainting_mode = st.radio("Outpainting mode:", ["DEFAULT", "PRECISE"], horizontal=True)
    
    generate_button = st.button("Generate", type="primary")


with col3:
    st.subheader("Result")
    
    if generate_button:
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
        else:
            image_bytes = glib.get_bytes_from_file("images/example.jpg")
        
        with st.spinner("Drawing..."):
            generated_image = glib.get_image_from_model(
                prompt_content=None, 
                image_bytes=image_bytes,
                mask_prompt=None,
                negative_prompt=None,
                outpainting_mode=None,
            )
        st.image(generated_image)
        generate_download_button(generated_image)
    
