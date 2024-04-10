import streamlit as st
import os
from PIL import Image

st.set_page_config(layout="wide")
left_column, right_column = st.columns(2)

with left_column:
    st.title("Aplikasi edukasi berbasis Artificial Intelligence")
    st.markdown('''Lorem ipsum dolor sit amet. Ea placeat rerum ut autem beatae id vero odit est harum
                voluptatem At maxime quia cum perferendis quos. Ea voluptatibus labore aut dolor
                enim sed officiis reiciendis aut veritatis dicta sit alias magni et animi consequatur.''')
    with st.expander("Petunjuk"):
        st.markdown("Ini adalah deskripsi sederhana tentang aplikasi ini.")
with right_column:
    img = Image.open('D:/Jupyter lab/Plagiarism-detection/app/img/contoh saja bang.jpg')
    st.image(img)

st.info("FAQ 1")
st.info("FAQ 2")
st.info("FAQ 3")