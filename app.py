import pdfplumber
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


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

#skills = find_skills(resume_text)

def compare_to_job(candidate_skills, required_skills):
    matched = []
    missing = []

    for skill in required_skills:
        if skill in candidate_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    score = (len(matched) / len(required_skills)) * 100

    return matched, missing, score

def analyze_candidate(resume_text, job_description):

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

'''
print("Skills Found:")
print(skills)
'''

resume_files = os.listdir("resumes")
results = []

print(resume_files)

job_description = input("Paste Job Description:\n")

job_skills = find_skills(job_description)

for resume_file in resume_files:

    resume_text = extract_text(
        f"resumes/{resume_file}"
    )

    analysis = analyze_candidate(
        resume_text,
        job_description
    )

    candidate_skills = find_skills(resume_text)

    matched_skills, missing_skills, score = compare_to_job(
        candidate_skills,
        job_skills
    )

    results.append(
        {
            "name": resume_file,
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "analysis": analysis
        }
    )
    
results.sort(
    key=lambda candidate: candidate["score"],
    reverse=True
)

print("\n===== RANKINGS =====")

for candidate in results:
    print(
        f"{candidate['name']}: "
        f"{candidate['score']:.1f}%"
    )
report = "===== CANDIDATE REPORTS =====\n\n"

for candidate in results:

    report += f"Candidate: {candidate['name']}\n"
    report += f"Score: {candidate['score']:.1f}%\n\n"

    report += "Matched Skills:\n"

    for skill in candidate["matched_skills"]:
        report += f"- {skill}\n"

    report += "\nMissing Skills:\n"

    if candidate["missing_skills"]:
        for skill in candidate["missing_skills"]:
            report += f"- {skill}\n"
    else:
        report += "None\n"

    report += "\n===== AI ANALYSIS =====\n"
    report += candidate["analysis"]

    report += "\n\n--------------------------------\n\n"

with open("candidate_report.txt", "w") as file:
    file.write(report)

with open("candidate_report.json", "w") as file:
    json.dump(results, file, indent=4)

top_candidate = results[0]

print("\n===== TOP CANDIDATE =====")

print(
    f"{top_candidate['name']} "
    f"({top_candidate['score']:.1f}%)"
)

print("\nMatched Skills:")

for skill in top_candidate["matched_skills"]:
    print(f"- {skill}")

print("\nMissing Skills:")

if top_candidate["missing_skills"]:
    for skill in top_candidate["missing_skills"]:
        print(f"- {skill}")
else:
    print("None")
    
print("\n===== AI ANALYSIS =====")
print(top_candidate["analysis"])

print("\nReport saved to candidate_report.txt")