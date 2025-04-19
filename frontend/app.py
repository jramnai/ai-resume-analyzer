import streamlit as st
import requests
import base64

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🎯 AI Resume Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])
include_ats = st.checkbox("Include ATS Score")

if st.button("Analyze") and resume_file and jd_file:
    with st.spinner("Analyzing..."):
        response = requests.post(
            "http://localhost:8000/analyze/",
            files={
                "resume": (resume_file.name, resume_file, resume_file.type),
                "job_description": (jd_file.name, jd_file, jd_file.type),
            },
            data={"include_ats_score": str(include_ats)}
        )
        result = response.json()
        st.subheader("Match Percentage")
        st.write(f"{result['match_percent']}%")
        st.subheader("Suggestions")
        st.write("Changes applied as per job description.")
        st.subheader("Updated Resume")
        st.text_area("Editable Updated Resume", result["updated_resume"], height=300)
        b64 = base64.b64encode(result["updated_resume"].encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="updated_resume.txt">Download Updated Resume</a>'
        st.markdown(href, unsafe_allow_html=True)
        if include_ats:
            st.subheader("ATS Score")
            st.write(f"Before: {result['ats_before']}, After: {result['ats_after']}")
