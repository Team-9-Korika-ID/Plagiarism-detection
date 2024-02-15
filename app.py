import streamlit as st
from PyPDF2 import PdfReader
import zipfile
import io

# Layout
st.set_page_config(layout="wide")

# Just add it after st.sidebar:
# a = st.sidebar.radio('Choose:',[1,2])

st.title("Dolos")
st.caption("Aplikasi untuk membaca teks dari file PDF atau ZIP")


# Membagi layar menjadi dua kolom
left_column, right_column = st.columns(2)

# Input di kolom kiri
with left_column:
    st.header("Input")
    st.caption("Upload file PDF atau ZIP")
    st.info('Datasets and reports older than 30 days may be deleted from our server to save space. You can always delete the data yourself.')
    uploaded_file = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"])
    st.text_input('Text input')
    st.multiselect('Multiselect', ['a', 'b', 'c'])
    st.write('When you upload a dataset, it will be analyzed on our server. Only you and the people you share the report with will be able to view the analysis results.')
    st.checkbox('I accept the terms and conditions')

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
# Sidebar
with st.sidebar:
    st.header("Sidebar")
    # Tombol berukuran besar
    if st.button("Pengumpulan tugas", key="button1"):
        st.write("Pengumpulan tugas")
    if st.button("Pengumpulan ujian", key="button2"):
        st.write("Pengumpulan ujian")
    if st.button("Rekomendasi matkul", key="button3"):
        st.write("Rekomendasi matkul")
