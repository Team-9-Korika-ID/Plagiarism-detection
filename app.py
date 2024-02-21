import streamlit as st
from PyPDF2 import PdfReader
import zipfile
import pandas as pd

# Set Layout
st.set_page_config(layout="wide")
left_column, right_column = st.columns(2)

# Input
with left_column:
    st.header("Input")
    uploaded_file = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"])

# Output
with right_column:
    st.header("Output")
    # Tampilkan informasi file jika file telah diunggah
    if uploaded_file is not None:
        # Informasi file
        file_info = {"Nama siswa": uploaded_file.name, 
                     "Tipe file": uploaded_file.type, 
                     "Ukuran file (bytes)": len(uploaded_file.read())}
        df_file_info = pd.DataFrame(file_info, index=[0])
        st.write("Informasi file yang diinput:")
        st.dataframe(df_file_info)

        # Memisahkan nomor dan teks dari nama dokumen
        nama_dokumen = uploaded_file.name
        nomor, teks = nama_dokumen.split('_', 1)

        # Membuat dataframe untuk nomor dan teks
        data = {'Nomor': [nomor], 'Teks': [teks]}
        df_nomor_teks = pd.DataFrame(data)

        st.write("DataFrame dengan Nomor dan Teks:")
        st.dataframe(df_nomor_teks)
        
st.write("")

# Meng-handle error jika file tidak dapat dibaca atau diproses
try:
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Jika file yang diunggah adalah PDF, ekstrak teks dari setiap halaman
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            st.header("Text from PDF:")
            st.write(text)
        elif uploaded_file.type == "application/zip":
            # Jika file yang diunggah adalah ZIP, ekstrak teks dari semua file teks dalam arsip ZIP
            zip_file = zipfile.ZipFile(uploaded_file)
            text = ""
            for file_name in zip_file.namelist():
                if file_name.endswith('.txt'):  # Hanya membaca file teks
                    with zip_file.open(file_name) as file:
                        text += file.read().decode("utf-8")
            st.header("Text from files in ZIP:")
            st.write(text)
except Exception as e:
    st.error(f"An error occurred: {e}")
