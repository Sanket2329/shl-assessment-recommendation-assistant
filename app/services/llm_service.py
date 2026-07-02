import json
import logging
import os
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)


def _parse_json(text: str) -> dict:
    text = text.strip()

    # Strip markdown code fences
    text = re.sub(r"^```(?:json)?", "", text, flags=re.MULTILINE).strip()
    text = re.sub(r"```$", "", text, flags=re.MULTILINE).strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract the first {...} block and try again
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from Gemini response: {text[:300]}")


class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)

    def recommend(self, conversation: str,
    user_query: str,
    assessments: list,):
        context = ""

        for assessment in assessments:
            context += f"""
Assessment Name: {assessment.get("name", "")}

Retrieval Score:
{assessment.get("retrieval_score", 0)}

Description:
{assessment.get("description", "")}

Categories:
{", ".join(assessment.get("keys", []))}

Job Levels:
{", ".join(assessment.get("job_levels", []))}

Languages:
{", ".join(assessment.get("languages", []))}

Duration:
{assessment.get("duration", "Not specified")}

Remote Testing:
{assessment.get("remote", "Unknown")}

Adaptive:
{assessment.get("adaptive", "Unknown")}

URL:
{assessment.get("url", "")}

"""

        prompt = f"""
You are an SHL Assessment Recommendation Expert.

You will receive:
1. A hiring requirement.
2. Retrieved SHL assessments.

Rules:

- Use ONLY the provided assessments.
- Never invent or rename assessment names.
- Never generate URLs, durations, remote testing, or adaptive support.
- Rank assessments from best to least suitable.

Ranking Guidelines:

- For software engineering or technical roles, prioritize technical and coding assessments.
- Prioritize assessments that directly evaluate the requested technologies and skills.
- Only recommend behavioral or personality assessments if the user's request explicitly mentions leadership, communication, teamwork, personality, culture fit, or behavioral traits.
- Avoid recommending remote work assessments unless the user specifically asks for remote work readiness.
- Explain clearly why each assessment matches the hiring requirement.

Return ONLY valid JSON.

Conversation History:
{conversation}

Latest User Request:
{user_query}

Retrieved Assessments
(sorted by semantic relevance):

{context}

IMPORTANT:

- The assessments are already sorted from most relevant to least relevant.
- Each assessment includes a retrieval_score.
- Higher retrieval_score means the assessment is a stronger semantic match.
- Prefer assessments with higher retrieval_score unless another assessment is clearly a better fit.
- Do NOT change the assessment names.
- Explain WHY each assessment matches the user's requirement.

Return ONLY valid JSON.

Format:

{{
  "summary": "One paragraph summarizing the recommendation.",
  "recommendations": [
    {{
      "assessment_name": "exact assessment name",
      "reason": "Why this assessment fits"
    }}
  ]
}}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                },
            )

            text = response.text.strip()
            return _parse_json(text)

        except Exception as e:
            logger.error("Gemini recommendation error: %s", e)

            return {
                "summary": "Unable to generate recommendations at the moment.",
                "recommendations": [],
                "error": str(e),
            }

    def compare(self, assessment1: dict, assessment2: dict):
        prompt = f"""
You are an SHL Assessment Expert.

Compare ONLY these two SHL assessments.

Assessment 1:
Name: {assessment1["name"]}
Description: {assessment1.get("description", "")}
Duration: {assessment1.get("duration", "")}
Remote Testing: {assessment1.get("remote", "")}
Adaptive: {assessment1.get("adaptive", "")}
Categories: {", ".join(assessment1.get("keys", []))}

Assessment 2:
Name: {assessment2["name"]}
Description: {assessment2.get("description", "")}
Duration: {assessment2.get("duration", "")}
Remote Testing: {assessment2.get("remote", "")}
Adaptive: {assessment2.get("adaptive", "")}
Categories: {", ".join(assessment2.get("keys", []))}

Write a concise comparison.

Include:

- Purpose
- Key differences
- Best use case for each
- Which one should a recruiter choose and why

Keep it under 250 words.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text