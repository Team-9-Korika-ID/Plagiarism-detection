from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a teacher correcting a student's document. You will be reading
the answer text to a question and summarizing the key points within 250 words.
Please provide a summary of the text given below:"""

# Set Layout
st.set_page_config(layout="wide")
left_column, right_column = st.columns(2)

# Input
with left_column:
    st.header("Input")
    st.info('Datasets and reports older than 30 days may be deleted from our server to save space. You can always delete the data yourself.')
    uploaded_files = st.file_uploader("Upload file (zip/PDF)", type=["zip", "pdf"], accept_multiple_files=True)
    judul_database = st.text_input('Masukkan Judul Database (* Wajib)')
    
'''
if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
        '''
