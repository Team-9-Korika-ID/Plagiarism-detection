import streamlit as st
from PyPDF2 import PdfReader
import zipfile
import io

# Layout
st.set_page_config(layout="wide")

# Membagi layar menjadi dua kolom
left_column, right_column = st.columns(2)

# Input di kolom kiri
with left_column:
    st.header("Input")
    uploaded_file = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"])

# Output di kolom kanan
with right_column:
    st.header("Output")
    # Tampilkan output di sebelah kanan
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                pdf_reader = PdfReader(uploaded_file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                st.write("Text from PDF:")
                st.write(text)
            elif uploaded_file.type == "application/zip":
                zip_file = zipfile.ZipFile(uploaded_file)
                text = ""
                for file_name in zip_file.namelist():
                    if file_name.endswith('.txt'):  # Hanya membaca file teks
                        with zip_file.open(file_name) as file:
                            text += file.read().decode("utf-8")
                st.write("Text from files in ZIP:")
                st.write(text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
