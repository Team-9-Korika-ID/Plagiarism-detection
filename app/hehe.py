import streamlit as st
from PyPDF2 import PdfReader
import zipfile
import pandas as pd
from dotenv import load_dotenv
import os
import google.generativeai as genai

# load environment variables
load_dotenv()

# configure generativeai
genai.configure(api_key="your_api_key_here")

# define function to generate content
def generate_gemini_content(tulisan, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + tulisan)
    return response.text

st.set_page_config(layout="wide")
left_column, right_column = st.columns(2)

# Input kiri
with left_column:
    st.header("Input")
    st.info('Datasets and reports older than 30 days may be deleted from our server to save space. You can always delete the data yourself.')
    uploaded_files = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"], accept_multiple_files=True)
    judul_database = st.text_input('Masukkan Judul Database (* Wajib)')
    st.write('When you upload a dataset, it will be analyzed on our server. Only you and the people you share the report with will be able to view the analysis results.')
    st.checkbox('I accept the terms and conditions')

# Output kanan
with right_column:
    st.header("Output")
    # Tampilkan informasi file jika file telah diunggah
    if uploaded_files is not None:
        df_files_info = pd.DataFrame(columns=["NRP", "Nama siswa", "Tipe file", "File size (bytes)"])
        for uploaded_file in uploaded_files:
            # Informasi file
            nama_dokumen = uploaded_file.name
            nomor, teks = nama_dokumen.split('_', 1)

            file_info = {"NRP": nomor,
                         "Nama siswa": teks,
                         "Tipe file": uploaded_file.type,
                         "File size (bytes)": len(uploaded_file.read()),
                         "Info": "✅"}
            df_files_info = pd.concat([df_files_info, pd.DataFrame(file_info, index=[0])], ignore_index=True)

        if not df_files_info.empty:
            st.write("Informasi file yang diinput:")
            st.dataframe(df_files_info)
            st.write("Judul Database:")
            st.write(judul_database)

            st.write("")

            # Loop through uploaded PDF files
            for uploaded_file in uploaded_files:
                st.write(f"Koreksi dan Saran untuk {uploaded_file.name}:")
                pdf_data = process_pdf(uploaded_file)
                corrections, suggestions = generate_corrections_and_suggestions(pdf_data)
                st.write("**Koreksi:**")
                st.write(corrections)
                st.write("**Saran:**")
                st.write(suggestions)

# Fungsi untuk memproses file PDF
def process_pdf(uploaded_file):
    pdf_data = {"Text": "", "Summary": ""}
    # Baca file PDF
    with open(uploaded_file.name, "rb") as file:
        pdf_reader = PdfReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_data["Text"] += page.extractText()
    return pdf_data

# Fungsi untuk menghasilkan koreksi dan saran dari teks
def generate_corrections_and_suggestions(pdf_data):
    # Lakukan pemrosesan atau panggil model AI untuk mendapatkan koreksi dan saran
    corrections = "Koreksi belum diimplementasikan untuk contoh ini."
    suggestions = "Saran belum diimplementasikan untuk contoh ini."
    return corrections, suggestions
