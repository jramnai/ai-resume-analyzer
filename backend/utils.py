import os
import tempfile

import docx
from dotenv import load_dotenv
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


load_dotenv()

provider = os.getenv("LLM_PROVIDER", "openai")

if provider == "openai":
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
else:
    import ollama


def generate_suggestions_and_match_percent(resume_text, jd_text):
    prompt = f"""Job Description: {jd_text}

Resume: {resume_text}

Suggest specific improvements to the resume based on the job description and return the updated resume.
"""

    if provider == "openai":
        model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a resume improvement assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        updated_resume = response.choices[0].message.content
    else:
        response = ollama.chat(
            model="gemma3:1b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        updated_resume = response['message']['content']

    match_percent = score_match_percentage(resume_text, jd_text)
    return updated_resume, match_percent


async def read_file(uploaded_file):
    if uploaded_file.filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await uploaded_file.read())
            tmp.flush()
            with pdfplumber.open(tmp.name) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif uploaded_file.filename.endswith(".docx"):
        doc = docx.Document(uploaded_file.file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return (await uploaded_file.read()).decode("utf-8")


async def process_files(resume_file, jd_file):
    resume_text = await read_file(resume_file)
    jd_text = await read_file(jd_file)
    return resume_text, jd_text


def score_match_percentage(resume_text, jd_text):
    vectorizer = TfidfVectorizer().fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return round(float(similarity[0][0]) * 100, 2)


def compute_ats_score(before_text, after_text):
    def score(text):
        return min(100, len(set(text.split())) // 5)
    return score(before_text), score(after_text)
