🤖 AI Resume Screener

## IMPORTANT!!!: An OpenAI API key is required to run the application locally. Create a .env file and set OPENAI_API_KEY before launching the application

An AI powered resume screening web application built with Python, Streamlit, and the OpenAI API.

The application allows users to upload multiple PDF resumes, paste a job description, and automatically rank candidates based on skill alignment. It also generates AI-powered candidate evaluations including strengths, weaknesses, and hiring recommendations.

---

Features:

Upload multiple PDF resumes
Extract technical skills from job descriptions using AI
Extract technical skills from resumes using AI
Rank candidates based on skill alignment
Display matched and missing skills
Generate recruiter style candidate evaluations
Interactive web interface built with Streamlit
Support for any technology stack (Python, React, TypeScript, AWS, Docker, etc.)

---

Tech Stack

Python
Streamlit
OpenAI API
PDFPlumber
Python Dotenv

---

Installation

Clone the repository:

```bash
git clone https://github.com/jjama415/ai-resume-screener.git
cd ai-resume-screener
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```
^^make sure to follow the above format exactly, no spaces before or after the equal sign

Run the application:

```bash
streamlit run streamlit_app.py
```

---

Usage

1. Upload one or more PDF resumes.
2. Paste a job description.
3. Click *Analyze*.
4. Review candidate rankings.
5. View matched and missing skills.
6. Read ai generated candidate recommendations.

---

Example Workflow

```text
Upload Resumes
        ↓
Paste Job Description
        ↓
AI Extracts Skills
        ↓
Candidate Ranking
        ↓
AI Candidate Evaluation
```

---

Future improvements for a v2

* CSV export functionality
* Downloadable candidate reports
* Candidate comparison dashboard
* Database integration
* User authentication
* Resume history tracking
* Advanced analytics and visualizations

--

Author:

Said Djama

Indiana University Indianapolis

Artificial Intelligence Major
