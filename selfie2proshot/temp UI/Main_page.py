import streamlit as st

#Task Bar
st.set_page_config(page_title = "Welcome Home", page_icon = "😮") #layout = "wide"

#Title page
st.title("Selfie to Headshot generator")
st.subheader("Need a professional photo but don't have the resources? We're here to help!")
st.markdown('<a href="/input_page" target="_self">Click on this line to get started!</a>', unsafe_allow_html=True)