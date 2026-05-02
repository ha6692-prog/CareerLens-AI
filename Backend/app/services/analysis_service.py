# ============================================================
# analysis_service.py — AI Analysis Logic
# ============================================================
# This is the core feature of CareerLens AI.
# Steps:
# 1. Check user hasn't exceeded their free limit
# 2. Fetch the resume text from the database
# 3. Send resume + job description to Groq AI
# 4. Parse the AI response (score, keywords, suggestions)
# 5. Save results to the database
# 6. Increment user's usage counter
# ============================================================

import json
from groq import Groq
from sqlalchemy.orm import Session
from app.models.analysis import Analysis
from app.models.user import User
from app.models.resume import Resume
from app.core.config import settings
from app.core.exceptions import UsageLimitException, NotFoundException

# Initialize the Groq client with your API key
groq_client = Groq(api_key=settings.GROQ_API_KEY)


def run_analysis(resume_id: int, job_description: str, user: User, db: Session) -> Analysis:

    # Step 1 — Enforce free plan limit
    if user.analyses_used >= user.free_limit:
        raise UsageLimitException()

    # Step 2 — Get the resume (and verify it belongs to this user)
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == user.id
    ).first()
    if not resume:
        raise NotFoundException(detail="Resume not found")

    # Step 3 — Build the prompt and call Groq AI
    ai_response = call_groq_ai(resume.extracted_text, job_description)

    # Step 4 — Parse the structured JSON response from AI
    parsed = parse_ai_response(ai_response)

    # Step 5 — Save analysis results to the database
    # missing_keywords and suggestions are stored as JSON strings
    analysis = Analysis(
        user_id=user.id,
        resume_id=resume_id,
        job_description=job_description,
        match_score=parsed.get("match_score"),
        missing_keywords=json.dumps(parsed.get("missing_keywords", [])),
        suggestions=json.dumps(parsed.get("suggestions", [])),
        ai_feedback=ai_response,
    )
    db.add(analysis)

    # Step 6 — Increment the user's usage counter
    user.analyses_used += 1
    db.commit()
    db.refresh(analysis)

    return analysis


def call_groq_ai(resume_text: str, job_description: str) -> str:
    # This is the prompt we send to the AI model
    # We ask it to respond in strict JSON so we can parse it reliably
    prompt = f"""
You are an expert ATS (Applicant Tracking System) and career coach.

Analyze this resume against the job description and respond ONLY with a JSON object.
No extra text. No explanation outside the JSON.

Resume:
{resume_text}

Job Description:
{job_description}

Respond with exactly this JSON structure:
{{
  "match_score": <number between 0 and 100>,
  "missing_keywords": [<list of important keywords missing from resume>],
  "suggestions": [<list of specific improvement suggestions>]
}}
"""
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",   # fast and free Groq model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,          # lower = more consistent/predictable output
    )

    # Extract the text content from the response
    return response.choices[0].message.content


def parse_ai_response(response_text: str) -> dict:
    try:
        # AI should return pure JSON — parse it directly
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Sometimes the AI wraps JSON in ```json ... ``` — strip those
        cleaned = response_text.strip().strip("```json").strip("```").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # If all else fails return safe defaults — don't crash the request
            return {
                "match_score": 0,
                "missing_keywords": [],
                "suggestions": ["Could not parse AI response. Please try again."]
            }


def get_user_analyses(user_id: int, db: Session) -> list:
    # Returns all analyses for this user, newest first
    return (
        db.query(Analysis)
        .filter(Analysis.user_id == user_id)
        .order_by(Analysis.created_at.desc())
        .all()
    )