from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.utils import compute_ats_score, generate_suggestions_and_match_percent, process_files


app = FastAPI()

# change this for prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze/")
async def analyze(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
    include_ats_score: bool = Form(False)
):
    resume_text, jd_text = await process_files(resume, job_description)
    updated_resume, match_percent = generate_suggestions_and_match_percent(resume_text, jd_text)
    ats_before, ats_after = None, None

    if include_ats_score:
        ats_before, ats_after = compute_ats_score(resume_text, updated_resume)

    return JSONResponse({
        "match_percent": match_percent,
        "updated_resume": updated_resume,
        "ats_before": ats_before,
        "ats_after": ats_after
    })
