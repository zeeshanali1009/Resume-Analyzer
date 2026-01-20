import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def calculate_ats_score(resume_text, job_text):
    # Clean and vectorize both texts
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)
    
    vectorizer = CountVectorizer().fit_transform([resume_text, job_text])
    similarity = cosine_similarity(vectorizer)[0][1]
    
    score = round(similarity * 100, 2)
    return score
