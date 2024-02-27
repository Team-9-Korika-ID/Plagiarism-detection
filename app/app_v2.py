import streamlit as st
from PyPDF2 import PdfReader
import zipfile
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

st.set_page_config(layout="wide")
left_column, right_column = st.columns(2)

# Input kiri
with left_column:
    st.header("Input")
    st.info('Datasets and reports older than 30 days may be deleted from our server to save space. You can always delete the data yourself.')
    uploaded_files = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"], accept_multiple_files=True)
    judul_database = st.text_input('Masukkan Judul Database (* Wajib)')
    # st.multiselect('Multiselect', ['a', 'b', 'c'])
    st.write('When you upload a dataset, it will be analyzed on our server. Only you and the people you share the report with will be able to view the analysis results.')
    st.checkbox('I accept the terms and conditions')

# Output kanan
with right_column:
    st.header("Output")
    # Tampilkan informasi file jika file telah diunggah
    pdf_data = {"Text": {}, "Images": {}}

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            try:
                if uploaded_file.type == "application/pdf":
                    pdf_reader = PdfReader(uploaded_file)
                    text = ""
                    images = []
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()
                        images += page.get_images(full=True)
                    # Simpan informasi file PDF dalam dictionary dengan nama file sebagai kunci
                    pdf_data["Text"][uploaded_file.name] = text
                    pdf_data["Images"][uploaded_file.name] = images
                elif uploaded_file.type == "application/zip":
                    zip_file = zipfile.ZipFile(uploaded_file)
                    for file_name in zip_file.namelist():
                        if file_name.endswith('.txt'):
                            with zip_file.open(file_name) as file:
                                text = file.read().decode("utf-8")
                                # Simpan informasi file dalam dictionary dengan nama file sebagai kunci
                                pdf_data["Text"][file_name] = text
            except Exception as e:
                st.error(f"An error occurred: {e}")

# DataFrame untuk teks dari PDF
pdf_text_df = pd.DataFrame.from_dict(pdf_data["Text"], orient='index', columns=['Text'])
if not pdf_text_df.empty:
    st.header("Text from PDFs:")
    st.dataframe(pdf_text_df)

# DataFrame untuk gambar dari PDF
pdf_image_df = pd.DataFrame(columns=['File Name', 'Page Number', 'Image'])
for file_name, images in pdf_data["Images"].items():
    for i, img in enumerate(images):
        pdf_image_df = pdf_image_df.append({'File Name': file_name, 'Page Number': i+1, 'Image': img[0]}, ignore_index=True)
if not pdf_image_df.empty:
    st.header("Images from PDFs:")
    st.dataframe(pdf_image_df)

# PERHITUNGAN GATAU

# load environment variables
load_dotenv()

# configure generativeai
genai.configure(api_key="AIzaSyCYyr1lSjWLIck3sHkfnZiV3RLZd_e7qFc")

# define function to generate content
def generate_gemini_content(tulisan, prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+tulisan)
    return response.text

# Prompt
prompt1="""You are a teacher correcting a student's document. You will be reading
        the answer text to a question and summarizing the key points within 250 words.
        Please provide a summary of the text given below:"""
prompt2='''You are a teacher correcting a student's document. You will read the text of an
answer to a question and summarise the key points in 250 words. Provide corrections
if there are words that are not correct, and provide criticism and suggestions.'''

# KODINGAN UNTUK BAGIAN BAWAH
pdf_data = {}  # Dictionary untuk menyimpan informasi dari setiap file PDF

try:
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                pdf_reader = PdfReader(uploaded_file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                # Simpan informasi file PDF dalam dictionary dengan nama file sebagai kunci
                pdf_data[uploaded_file.name] = text
            elif uploaded_file.type == "application/zip":
                zip_file = zipfile.ZipFile(uploaded_file)
                for file_name in zip_file.namelist():
                    if file_name.endswith('.txt'):
                        with zip_file.open(file_name) as file:
                            text = file.read().decode("utf-8")
                            # Simpan informasi file dalam dictionary dengan nama file sebagai kunci
                            pdf_data[file_name] = text
except Exception as e:
    st.error(f"An error occurred: {e}")

pdf_df = pd.DataFrame.from_dict(pdf_data, orient='index', columns=['Text'])
if not pdf_df.empty:
    st.header("Text from PDFs:")
    st.dataframe(pdf_df)
