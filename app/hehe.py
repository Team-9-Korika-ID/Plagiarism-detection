import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
import os

# load environment variables
load_dotenv()

# configure generativeai
genai.configure(api_key="AIzaSyCYyr1lSjWLIck3sHkfnZiV3RLZd_e7qFc")

# define function to generate content
def generate_gemini_content(tulisan, prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+tulisan)
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

    # Convert dictionary to DataFrame and display
    # Assuming pdf_data is the dictionary you want to convert to DataFrame
    # pdf_df = pd.DataFrame.from_dict(pdf_data, orient='index', columns=['Text', 'Summary'])
    # if not pdf_df.empty:
    #     st.header("Text from PDFs:")
    #     st.dataframe(pdf_df)

    # Text summarization and corrections
    text = st.text_area("Enter your text here")
    prompt1="""You are a teacher correcting a student's document. You will be reading
    the answer text to a question and summarizing the key points within 250 words.
    Please provide a summary of the text given below:"""
    summary = generate_gemini_content(text, prompt1)  # Fixed function call
    st.markdown(f"**Summary:** {summary}")

    prompt2='''You are a teacher correcting a student's document. You will read the text of an
    answer to a question and summarise the key points in 250 words. Provide corrections
    if there are words that are not correct, and provide criticism and suggestions.'''
    corrections = generate_gemini_content(text, prompt2)  # Fixed function call
    st.markdown(f"**Corrections and Suggestions:**")
    st.markdown(f"{corrections}")
