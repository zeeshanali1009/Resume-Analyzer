import docx2txt
import PyPDF2
import re

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces/newlines
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # remove special characters
    return text

# Simple matching score: percentage of job keywords found in resume
def calculate_match_score(job_text, resume_text):
    job_words = set(job_text.split())
    resume_words = set(resume_text.split())
    matched_words = job_words.intersection(resume_words)
    if len(job_words) == 0:
        return 0
    score = (len(matched_words) / len(job_words)) * 100
    return round(score, 2)
