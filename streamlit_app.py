import streamlit as st
import os
import tempfile
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="wide"
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def find_skills(text):
    skills = [
        "Python",
        "Java",
        "MySQL",
        "SQL",
        "Scikit Learn",
        "Machine Learning",
        "Data Analysis",
        "Excel",
        "Hubspot",
        "AWS"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


def extract_job_skills(job_description):

    response = client.responses.create(
        model="gpt-5-nano",
        input=f"""
        Extract the technical skills from this job description.

        Return only a comma separated list.

        Job Description:

        {job_description}
        """
    )

    skills_text = response.output_text

    return [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

def extract_resume_skills(resume_text):

    response = client.responses.create(
        model="gpt-5-nano",
        input=f"""
        Extract the technical skills from this resume.

        Return only a comma separated list.

        Resume:

        {resume_text}
        """
    )

    skills_text = response.output_text

    return [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

def compare_to_job(candidate_skills, required_skills):
    matched = []
    missing = []

    for skill in required_skills:
        if skill in candidate_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(required_skills) == 0:
        return matched, missing, 0

    score = (
        len(matched) / len(required_skills)
    ) * 100

    return matched, missing, score


def analyze_candidate(
    resume_text,
    job_description
):

    response = client.responses.create(
        model="gpt-5-nano",
        input=f"""
        Resume:

        {resume_text}

        Job Description:

        {job_description}

        Give a short analysis of:

        1. Candidate strengths
        2. Candidate weaknesses
        3. Overall recommendation
        """
    )

    return response.output_text


st.title("🤖 AI Resume Screener")

job_description = st.text_area(
    "Paste Job Description"
)

uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Analyze"):

    with st.spinner(
        "Analyzing resumes..."
    ):

        if not job_description.strip():
            st.error(
                "Please enter a job description."
            )
            st.stop()

        if not uploaded_files:
            st.error(
                "Please upload at least one PDF."
            )
            st.stop()

        results = []

        job_skills = extract_job_skills(
            job_description
        )

        st.subheader(
            "Skills Extracted From Job Description"
        )

        st.write(job_skills)

        for uploaded_file in uploaded_files:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_path = temp_file.name

            resume_text = extract_text(
                temp_path
            )

            candidate_skills = extract_resume_skills(
        resume_text
    )

            matched_skills, missing_skills, score = compare_to_job(
                candidate_skills,
                job_skills
            )

            results.append(
                {
                    "name": uploaded_file.name,
                    "score": score,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "resume_text": resume_text
                }
            )

        results.sort(
            key=lambda candidate:
            candidate["score"],
            reverse=True
        )

        st.header("🏆 Resume Rankings")

        for candidate in results:

            st.subheader(
                candidate["name"]
            )

            st.progress(
                candidate["score"] / 100
            )

            st.write(
                f"Match Score: "
                f"{candidate['score']:.1f}%"
            )

        top_candidate = results[0]

        analysis = analyze_candidate(
            top_candidate["resume_text"],
            job_description
        )
        st.success(
    "Analysis Complete!"
)
        st.balloons()
        st.header("Top Candidate")

        st.write(
            f"{top_candidate['name']} "
            f"({top_candidate['score']:.1f}%)"
        )

        st.subheader(
            "Matched Skills"
        )

        if top_candidate[
            "matched_skills"
        ]:

            for skill in top_candidate[
                "matched_skills"
            ]:

                st.write(
                    f"✅ {skill}"
                )

        else:

            st.write(
                "No matched skills."
            )

        st.subheader(
            "Missing Skills"
        )

        if top_candidate[
            "missing_skills"
        ]:

            for skill in top_candidate[
                "missing_skills"
            ]:

                st.write(
                    f"❌ {skill}"
                )

        else:

            st.write(
                "None, candidate matches all listed skills."
            )

        st.header(
            "AI Analysis"
        )

        st.write(
            analysis
        )