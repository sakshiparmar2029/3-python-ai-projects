import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
}

/* Headings */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1e293b;
}

/* Cards */
.card {
    background: #020617;
    padding: 24px;
    border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

/* Inputs */
input, textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #6366f1, #818cf8);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 12px;
    border: none;
}

.stButton button:hover {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #020617;
    border-radius: 12px;
    padding: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 14px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown("<h2> Overview</h2>", unsafe_allow_html=True)
    st.markdown("""
    **AI-Powered Resume Review Tool**
    - Resume clarity & impact  
    - Skills optimization  
    - Job-role alignment  
    """)
    st.markdown("---")
    st.markdown(" **Python AI Internship Project**")

# ---------------- HEADER ---------------- #
st.markdown("""
<h1 style='text-align:center;'>AI Resume Analyzer</h1>
<p style='text-align:center; font-size:18px; color:#9ca3af;'>
Upload your resume and receive detailed, actionable feedback instantly 🚀
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUT SECTION ---------------- #
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "📤 Upload Resume",
        type=["pdf", "txt"],
        help="Supported formats: PDF, TXT"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    job_role = st.text_input(
        "Target Job Role (optional)",
        placeholder="e.g. Data Analyst, Software Engineer"
    )
    st.markdown("</div>", unsafe_allow_html=True)

analyze = st.button("Analyze Resume", use_container_width=True)

# ---------------- FUNCTIONS ---------------- #
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(file.read()))
    return file.read().decode("utf-8")

# ---------------- ANALYSIS ---------------- #
if analyze:
    if not uploaded_file:
        st.warning(" Please upload a resume first.")
        st.stop()

    with st.spinner("Analyzing resume... "):
        try:
            resume_text = extract_text_from_file(uploaded_file)

            if not resume_text.strip():
                st.error("The uploaded file is empty or unreadable.")
                st.stop()

            prompt = f"""
            Analyze the following resume and provide professional feedback.

            Focus on:
            1. Overall clarity & impact
            2. Skills presentation
            3. Experience descriptions
            4. Improvements for {job_role if job_role else 'general job applications'}

            Resume Content:
            {resume_text}

            Provide structured bullet-point feedback.
            """

            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert HR professional and resume reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            st.success("Analysis Completed")

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("## Resume Feedback")
            st.markdown(response.choices[0].message.content)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

# ---------------- FOOTER ---------------- #
st.markdown("""
<div class='footer'>
Built using Streamlit & OpenAI • Internship Project
</div>
""", unsafe_allow_html=True)