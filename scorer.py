import anthropic
import json
import os

api_key = os.environ.get("ANTHROPIC_API_KEY") or open(".streamlit/secrets.toml").read().split('"')[1]
client = anthropic.Anthropic(api_key=api_key)

def score_cv(cv_text: str, jd_text: str) -> dict:
    prompt = f"""You are an expert recruiter. Analyse the fit between this CV and job description.

CV:
{cv_text}

JOB DESCRIPTION:
{jd_text}

Return ONLY a JSON object in this exact format, no other text:
{{
    "score": <integer 0-100>,
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "gaps": ["gap 1", "gap 2", "gap 3"],
    "recommendation": "<one sentence hiring recommendation>"
}}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)