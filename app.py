import streamlit as st
import pdfplumber
import re
# -------------------------------
# Function to extract text from PDF
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# -------------------------------
# Clean text
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# -------------------------------
# Extract keywords
# -------------------------------
def extract_keywords(text):
    stopwords = {"and", "or", "the", "a", "an", "of", "to", "in", "on", "for", "with", "by", "is", "are"}
    words = clean_text(text).split()
    keywords = {w for w in words if w not in stopwords and len(w) > 2}
    return keywords

# -------------------------------
# Calculate match and ATS scores
# -------------------------------
def calculate_scores(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    if not resume_keywords or not jd_keywords:
        return 0, 0

    match_count = len(resume_keywords & jd_keywords)
    match_score = (match_count / len(jd_keywords)) * 100
    ats_score = (len(resume_keywords & jd_keywords) / len(resume_keywords)) * 100

    return round(match_score, 2), round(ats_score, 2)

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Resume Analyzer")
st.write("Upload your **Job Description (JD)** and **Resume** to see the Match Score & ATS Score instantly!")

jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if jd_file and resume_file:
    jd_text = extract_text_from_pdf(jd_file)
    resume_text = extract_text_from_pdf(resume_file)

    match_score, ats_score = calculate_scores(resume_text, jd_text)

    st.subheader("📊 Results")
    st.write(f"**Match Score:** {match_score}%")
    st.write(f"**ATS Score:** {ats_score}%")

    if match_score > 70:
        st.success("✅ Great! Your resume matches the job description well.")
    elif match_score > 40:
        st.warning("⚠️ Partial Match — You might need to adjust some keywords.")
    else:
        st.error("❌ Low Match — Your resume doesn’t align with the job description.")
