from PyPDF2 import PdfReader

def convert_pdf_to_text(pdf_file_path):
    pdf_reader = PdfReader(pdf_file_path)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Example usage
pdf_file_path = "D:/Jupyter lab/Plagiarism-detection/datasets/3323600054_Manusia berbatang.pdf"  # Replace with the path to your PDF file
text = convert_pdf_to_text(pdf_file_path)

###
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# load environment variables
load_dotenv()

# configure generativeai
genai.configure(api_key="AIzaSyDiEvJyv_j5ZLMDt6E6lSM3ytQTqvWEpUE")

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
# streamlit app
def main():
    st.title("Fine Tuningnya belum kelar")
    text = st.text_area("Enter your text here")
    if st.button("Summarize"):
        prompt1="""You are a teacher correcting a student's document. You will be reading
        the answer text to a question and summarizing the key points within 250 words.
        Please provide a summary of the text given below:"""
        summary = generate_gemini_content(text, prompt1)
        st.markdown(f"**Summary:** {summary}")
        
    if st.button("Correct and Suggest"):
        prompt2='''You are a teacher correcting a student's document. You will read the text of an
        answer to a question and summarise the key points in 250 words. Provide corrections
        if there are words that are not correct, and provide criticism and suggestions.'''
        corrections = generate_gemini_content(text, prompt2)
        st.markdown(f"**Corrections and Suggestions:**")
        st.markdown(f"{corrections}")
if __name__ == "__main__":
    main()
