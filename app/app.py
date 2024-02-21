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
    st.info('Datasets and reports older than 30 days may be deleted from our server to save space. You can always delete the data yourself.')
    uploaded_files = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"], accept_multiple_files=True)
    judul_database = st.text_input('Masukkan Judul Database (* Wajib)')
    st.multiselect('Multiselect', ['a', 'b', 'c'])
    st.write('When you upload a dataset, it will be analyzed on our server. Only you and the people you share the report with will be able to view the analysis results.')
    st.checkbox('I accept the terms and conditions')

# Output
with right_column:
    st.header("Output")
    # Tampilkan informasi file jika file telah diunggah
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # Informasi file
            nama_dokumen = uploaded_file.name
            nomor, teks = nama_dokumen.split('_', 1)
            
            file_info = {"NRP": [nomor],
                         "Nama siswa": [teks],
                         "Tipe file": uploaded_file.type, 
                         "File size (bytes)": len(uploaded_file.read())}
            df_file_info = pd.DataFrame(file_info, index=[1])
            st.write("Informasi file yang diinput:")
            st.dataframe(df_file_info)
            st.write("Judul Database:")
            st.write(judul_database)

st.write("")

# PDF to Text
try:
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                pdf_reader = PdfReader(uploaded_file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                st.header("Text from PDF:")
                st.write(text)
            elif uploaded_file.type == "application/zip":
                zip_file = zipfile.ZipFile(uploaded_file)
                text = ""
                for file_name in zip_file.namelist():
                    if file_name.endswith('.txt'):
                        with zip_file.open(file_name) as file:
                            text += file.read().decode("utf-8")
                st.header("Text from files in ZIP:")
                st.write(text)
except Exception as e:
    st.error(f"An error occurred: {e}")

# Contents of ~/my_app/main_page.py
import streamlit as st

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

# Contents of ~/my_app/pages/page_2.py
import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

# Contents of ~/my_app/pages/page_3.py
import streamlit as st

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")

'''
# Sidebar
with st.sidebar:
    st.header("Sidebar")
    if st.button("Pengumpulan tugas [SISWA]", key="button0"):
        st.write("Pengumpulan tugas [SISWA]")
    if st.button("Pengumpulan tugas [GURU]", key="button1"):
        st.write("Pengumpulan tugas [GURU]")
    if st.button("Pengumpulan ujian", key="button2"):
        st.write("Pengumpulan ujian")
    if st.button("Rekomendasi matkul", key="button3"):
        st.write("Rekomendasi matkul")
'''
