import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(resume_text, job_description):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, Java development, Android development, and big data engineering. Your task is to evaluate the resume based on the given job description.

    You must consider that the job market is very competitive, and you should provide the best assistance for improving the resumes. Assign the percentage matching based on the JD and the missing keywords with high accuracy.

    resume: {resume_text}
    description: {job_description}

    I want the response in one single string having the structure
    {{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
    """
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Streamlit app
st.title("🚀 Smart ATS")
st.write("Improve Your Resume with Smart ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload your resume in PDF format")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(resume_text, jd)
        response_dict = json.loads(response)

        st.subheader("AI Evaluation Results:")
        st.markdown(f"**JD Match:** {response_dict['JD Match']}%")
        st.markdown(f"**Missing Keywords:** {' '.join(response_dict['MissingKeywords'])}")
        st.markdown(f"**Profile Summary:** {response_dict['Profile Summary']}")





