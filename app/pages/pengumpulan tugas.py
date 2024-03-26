import streamlit as st
from PyPDF2 import PdfReader

st.header("Input")
st.info('Datasets and reports older than 30 days may be deleted from our server to save space. You can always delete the data yourself.')
uploaded_files = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"], accept_multiple_files=True)
judul_database = st.text_input('Masukkan Judul Database (* Wajib)')
# st.multiselect('Multiselect', ['a', 'b', 'c'])
st.write('When you upload a dataset, it will be analyzed on our server. Only you and the people you share the report with will be able to view the analysis results.')
st.checkbox('I accept the terms and conditions')